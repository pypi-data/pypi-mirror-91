"""
Classes for generating diff coverage reports.
"""
from abc import ABCMeta, abstractmethod

from jinja2 import Environment, PackageLoader
from jinja2_pluralize import pluralize_dj
from diff_cover.snippets import Snippet
import json


class DiffViolations:
    """
    Class to capture violations generated by a particular diff
    """

    def __init__(self, violations, measured_lines, diff_lines):
        self.lines = {violation.line for violation in violations}.intersection(
            diff_lines
        )

        self.violations = {
            violation for violation in violations if violation.line in self.lines
        }

        # By convention, a violation reporter
        # can return `None` to indicate that all lines are "measured"
        # by default.  This is an optimization to avoid counting
        # lines in all the source files.
        if measured_lines is None:
            self.measured_lines = set(diff_lines)
        else:
            self.measured_lines = set(measured_lines).intersection(diff_lines)


class BaseReportGenerator:
    """
    Generate a diff coverage report.
    """

    __metaclass__ = ABCMeta

    def __init__(self, violations_reporter, diff_reporter):
        """
        Configure the report generator to build a report
        from `violations_reporter` (of type BaseViolationReporter)
        and `diff_reporter` (of type BaseDiffReporter)
        """
        self._violations = violations_reporter
        self._diff = diff_reporter
        self._diff_violations_dict = None

        self._cache_violations = None

    @abstractmethod
    def generate_report(self, output_file):
        """
        Write the report to `output_file`, which is a file-like
        object implementing the `write()` method.

        Concrete subclasses should access diff coverage info
        using the base class methods.
        """
        pass

    def coverage_report_name(self):
        """
        Return the name of the coverage report.
        """
        return self._violations.name()

    def diff_report_name(self):
        """
        Return the name of the diff.
        """
        return self._diff.name()

    def src_paths(self):
        """
        Return a list of source files in the diff
        for which we have coverage information.
        """
        return {
            src
            for src, summary in self._diff_violations().items()
            if len(summary.measured_lines) > 0
        }

    def percent_covered(self, src_path):
        """
        Return a float percent of lines covered for the source
        in `src_path`.

        If we have no coverage information for `src_path`, returns None
        """
        diff_violations = self._diff_violations().get(src_path)

        if diff_violations is None:
            return None

        # Protect against a divide by zero
        num_measured = len(diff_violations.measured_lines)
        if num_measured > 0:
            num_uncovered = len(diff_violations.lines)
            return 100 - float(num_uncovered) / num_measured * 100

        else:
            return None

    def violation_lines(self, src_path):
        """
        Return a list of lines in violation (integers)
        in `src_path` that were changed.

        If we have no coverage information for
        `src_path`, returns an empty list.
        """

        diff_violations = self._diff_violations().get(src_path)

        if diff_violations is None:
            return []

        return sorted(diff_violations.lines)

    def total_num_lines(self):
        """
        Return the total number of lines in the diff for
        which we have coverage info.
        """

        return sum(
            [
                len(summary.measured_lines)
                for summary in self._diff_violations().values()
            ]
        )

    def total_num_violations(self):
        """
        Returns the total number of lines in the diff
        that are in violation.
        """

        return sum(len(summary.lines) for summary in self._diff_violations().values())

    def total_percent_covered(self):
        """
        Returns the float percent of lines in the diff that are covered.
        (only counting lines for which we have coverage info).
        """
        total_lines = self.total_num_lines()

        if total_lines > 0:
            num_covered = total_lines - self.total_num_violations()
            return int(float(num_covered) / total_lines * 100)

        else:
            return 100

    def _diff_violations(self):
        """
        Returns a dictionary of the form:

            { SRC_PATH: DiffViolations(SRC_PATH) }

        where `SRC_PATH` is the path to the source file.

        To make this efficient, we cache and reuse the result.
        """
        if not self._diff_violations_dict:
            self._diff_violations_dict = {
                src_path: DiffViolations(
                    self._violations.violations(src_path),
                    self._violations.measured_lines(src_path),
                    self._diff.lines_changed(src_path),
                )
                for src_path in self._diff.src_paths_changed()
            }
        return self._diff_violations_dict

    def report_dict(self):
        src_stats = {src: self._src_path_stats(src) for src in self.src_paths()}

        return {
            "report_name": self.coverage_report_name(),
            "diff_name": self.diff_report_name(),
            "src_stats": src_stats,
            "total_num_lines": self.total_num_lines(),
            "total_num_violations": self.total_num_violations(),
            "total_percent_covered": self.total_percent_covered(),
        }

    def _src_path_stats(self, src_path):
        """
        Return a dict of statistics for the source file at `src_path`.
        """

        # Find violation lines
        violation_lines = self.violation_lines(src_path)
        violations = sorted(self._diff_violations()[src_path].violations)

        return {
            "percent_covered": self.percent_covered(src_path),
            "violation_lines": violation_lines,
            "violations": violations,
        }


# Set up the template environment
TEMPLATE_LOADER = PackageLoader(__package__)
TEMPLATE_ENV = Environment(loader=TEMPLATE_LOADER, trim_blocks=True, lstrip_blocks=True)
TEMPLATE_ENV.filters["pluralize"] = pluralize_dj


class JsonReportGenerator(BaseReportGenerator):
    def generate_report(self, output_file):
        json_report_str = json.dumps(self.report_dict())

        # all report generators are expected to write raw bytes, so we encode
        # the json
        output_file.write(json_report_str.encode("utf-8"))


class TemplateReportGenerator(BaseReportGenerator):
    """
    Reporter that uses a template to generate the report.
    """

    # Subclasses override this to specify the name of the templates
    # If not overridden, the template reporter will raise an exception
    TEMPLATE_NAME = None
    CSS_TEMPLATE_NAME = None

    # Subclasses should set this to True to indicate
    # that they want to include source file snippets.
    INCLUDE_SNIPPETS = False

    def __init__(self, violations_reporter, diff_reporter, css_url=None):
        super().__init__(violations_reporter, diff_reporter)
        self.css_url = css_url

    def generate_report(self, output_file):
        """
        See base class.
        output_file must be a file handler that takes in bytes!
        """

        if self.TEMPLATE_NAME is not None:
            template = TEMPLATE_ENV.get_template(self.TEMPLATE_NAME)
            report = template.render(self._context())

            if isinstance(report, str):
                report = report.encode("utf-8")

            output_file.write(report)

    def generate_css(self, output_file):
        """
        Generate an external style sheet file.

        output_file must be a file handler that takes in bytes!
        """
        if self.CSS_TEMPLATE_NAME is not None:
            template = TEMPLATE_ENV.get_template(self.CSS_TEMPLATE_NAME)
            style = template.render(self._context())

        if isinstance(style, str):
            style = style.encode("utf-8")

        output_file.write(style)

    def _context(self):
        """
        Return the context to pass to the template.

        The context is a dict of the form:

        {
            'css_url': CSS_URL,
            'report_name': REPORT_NAME,
            'diff_name': DIFF_NAME,
            'src_stats': {SRC_PATH: {
                            'percent_covered': PERCENT_COVERED,
                            'violation_lines': [LINE_NUM, ...]
                            }, ... }
            'total_num_lines': TOTAL_NUM_LINES,
            'total_num_violations': TOTAL_NUM_VIOLATIONS,
            'total_percent_covered': TOTAL_PERCENT_COVERED
        }
        """

        # Include snippet style info if we're displaying
        # source code snippets
        if self.INCLUDE_SNIPPETS:
            snippet_style = Snippet.style_defs()
        else:
            snippet_style = None

        context = super().report_dict()
        context.update({"css_url": self.css_url, "snippet_style": snippet_style})

        return context

    @staticmethod
    def combine_adjacent_lines(line_numbers):
        """
        Given a sorted collection of line numbers this will
        turn them to strings and combine adjacent values

        [1, 2, 5, 6, 100] -> ["1-2", "5-6", "100"]
        """
        combine_template = "{0}-{1}"
        combined_list = []

        # Add a terminating value of `None` to list
        line_numbers.append(None)
        start = line_numbers[0]
        end = None

        for line_number in line_numbers[1:]:
            # If the current number is adjacent to the previous number
            if (end if end else start) + 1 == line_number:
                end = line_number
            else:
                if end:
                    combined_list.append(combine_template.format(start, end))
                else:
                    combined_list.append(str(start))
                start = line_number
                end = None
        return combined_list

    def _src_path_stats(self, src_path):

        stats = super()._src_path_stats(src_path)

        # Load source snippets (if the report will display them)
        # If we cannot load the file, then fail gracefully
        formatted_snippets = {"html": [], "markdown": []}
        if self.INCLUDE_SNIPPETS:
            try:
                formatted_snippets = Snippet.load_formatted_snippets(
                    src_path, stats["violation_lines"]
                )
            except OSError:
                pass

        stats.update(
            {
                "snippets_html": formatted_snippets["html"],
                "snippets_markdown": formatted_snippets["markdown"],
                "violation_lines": TemplateReportGenerator.combine_adjacent_lines(
                    stats["violation_lines"]
                ),
            }
        )

        return stats


class StringReportGenerator(TemplateReportGenerator):
    """
    Generate a string diff coverage report.
    """

    TEMPLATE_NAME = "console_coverage_report.txt"


class HtmlReportGenerator(TemplateReportGenerator):
    """
    Generate an HTML formatted diff coverage report.
    """

    TEMPLATE_NAME = "html_coverage_report.html"
    CSS_TEMPLATE_NAME = "external_style.css"
    INCLUDE_SNIPPETS = True


class StringQualityReportGenerator(TemplateReportGenerator):
    """
    Generate a string diff quality report.
    """

    TEMPLATE_NAME = "console_quality_report.txt"


class HtmlQualityReportGenerator(TemplateReportGenerator):
    """
    Generate an HTML formatted diff quality report.
    """

    TEMPLATE_NAME = "html_quality_report.html"
    CSS_TEMPLATE_NAME = "external_style.css"
    INCLUDE_SNIPPETS = True


class MarkdownReportGenerator(TemplateReportGenerator):
    """
    Generate a Markdown formatted diff quality report.
    """

    TEMPLATE_NAME = "markdown_coverage_report.md"
    INCLUDE_SNIPPETS = True


class MarkdownQualityReportGenerator(TemplateReportGenerator):
    """
    Generate a Markdown formatted diff quality report.
    """

    TEMPLATE_NAME = "markdown_quality_report.md"
    INCLUDE_SNIPPETS = True
