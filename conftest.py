# conftest.py
import pytest
import os


def pytest_runtest_logreport(report):
    """Ensure logs are always strings so pytest-html doesn't crash."""
    if hasattr(report, "sections"):
        safe_sections = []
        for sec in report.sections:
            if isinstance(sec, tuple) and len(sec) == 2:
                name, content = sec
                safe_sections.append((str(name), str(content)))
            else:
                safe_sections.append((str(sec), ""))
        report.sections = safe_sections
    return report


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """Hook wrapper to attach suite name and sanitize extras."""
    outcome = yield
    rep = outcome.get_result()

    # derive suite name from module and class
    suite_name = os.path.splitext(os.path.basename(item.location[0]))[0]
    if hasattr(item, "cls") and item.cls is not None:
        suite_name += f".{item.cls.__name__}"

    setattr(rep, "suite_name", suite_name)

    # sanitize extras
    extras = getattr(rep, "extra", [])
    rep.extra = [str(e) if not isinstance(e, str) else e for e in extras]


def pytest_html_results_table_header(cells):
    """Add Suite column to HTML report."""
    cells.insert(1, "<th>Suite</th>")


def pytest_html_results_table_row(report, cells):
    """Fill Suite column with our suite_name."""
    suite = getattr(report, "suite_name", "N/A")
    cells.insert(1, f"<td>{suite}</td>")


def pytest_configure(config):
    """Ensure pytest-html plugin is loaded and metadata is clean."""
    global pytest_html
    pytest_html = config.pluginmanager.getplugin("html")


def pytest_html_report_title(report):
    """Set a custom report title."""
    report.title = "Robotics TDD Simulation Test Report"


def pytest_html_results_summary(prefix, summary, postfix):
    """Inject Author and Email in the report header banner."""
    prefix.extend([
        "<p><strong>Author:</strong> Bang Thien Nguyen</p>",
        "<p><strong>Email:</strong> ontario1998@gmail.com</p>"
    ])
