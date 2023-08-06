import time
import json
import html

from .log import Log

TOP = "<html><body>"

BOTTOM = "</body></html>"


def get_status_colors(status):
    return dict(
        ERROR=("red", "cyan"),
        FAILED=("#FDD", "maroon"),
        PASSED=("#DFD", "green"),
        FIXED=("#DDF", "green"),
        IRRELEVANT=("#BBB", "eee"),
        NA=("grey", "white"),
    )[status]


def get_status_style(status):
    style = "padding: 5; margin: 0 -5px 0 0;"
    bg, fg = get_status_colors(status)
    return f"{style} background-color: {bg}; color: {fg};"


def get_indent_style(depth, status):
    indent = depth * 25
    bg, _ = get_status_colors(status)
    if 0:
        # this does not show correctly in QTextEdit :'(
        style = f"border-left: {indent}px solid {bg};"
    else:
        style = f"color: {bg}; "
    return style


def get_context_style(status):
    return "background-color: #ffb; color: #aa6;"


def get_doc_style(status):
    return "background-color: #eee; color: #aaa;"


def get_default_config():
    return dict(
        filter_statuses=None,
        show_logs=True,
        show_debug_logs=False,
        logs_indent_string="  ",
        show_times=False,
        show_context_edits=False,
        show_contexts=False,
        show_descriptions=False,
    )


def E(s):
    return html.escape(s or "")


def test_to_html_table(
    test,
    root_timestamp,
    indent,
    config,
):
    """
    Returns the html table-tree for the given test json export.
    """
    S = indent * "  "
    lines = []
    test_name = test["test_name"]
    short = E(test["short_description"] or "No description...")
    long = E(test["long_description"] or "")
    result = test["result"]
    status = result["status"]
    summary = E(result["summary"] or "")
    error = E(result["error"])
    trace = E(result["trace"])
    test_filename = E(test["test_filename"])
    status_style = get_status_style(status)

    lines = []
    lines.append(f'{S}<tr style="{status_style}">')

    if test["sub_tests"]:
        icon = "&#x1F52C;"  # microscope
        icon = "&#x2697;"  # alembic
        icon = "&#x1F9EB;"  # petri dish
    else:
        icon = "&#x1F9EA;"  # test tube
    indent_style = get_indent_style(indent, status)
    indent_text = indent * "__"
    source = f'{test["test_type"]}\n{test_filename}\n'
    lines.append(f"{S}  <td>")
    lines.append(
        f'{S}    <span style="{indent_style}">{indent_text}</span>'
        f'<span title="{source}\n{short}\n{long}">{icon} {test_name}</span>'
    )
    lines.append(f"{S}  </td>")
    lines.append(f"{S}  <td>{status}</td>")
    lines.append(f"{S}  <td>{summary}</td>")
    lines.append(f"{S}</tr>")

    if error:
        short = test["short_description"] or "No description..."
        long = test["long_description"] or ""
        lines.append(f"{S}<tr>")
        lines.append(f"{S}<td></td>")
        lines.append(
            f'{S}<td colspan=2 style="{status_style}">'
            f"{error}<br><pre>{trace}</pre>"
            "</td>"
        )
        lines.append(f"{S}</tr>")

    if config.get("show_logs"):
        log_lines = test["log_lines"]
        if log_lines:
            log = Log.pformat_lines(
                test["log_lines"],
                include_debug=config.get("show_debug_logs", False),
                indent_level=0,
                indent_string=config.get("logs_indent_string", "  "),
            )
        else:
            log = "No log found :/"
        log = E(log)
        # style = get_context_style(status)
        lines.append(f"{S}<tr>")
        lines.append(f"{S}<td></td>")
        lines.append(f'{S}<td colspan=2 style="{status_style}"><pre>{log}</pre></td>')
        lines.append(f"{S}</tr>")

    if config.get("show_times", False):
        style = get_context_style(status)
        start_time = test["timestamp"] - root_timestamp
        run_time = test["result"]["timestamp"] - test["timestamp"]
        time_txt = f"started at +{start_time:.02f}, ran for {run_time:.02f}s."
        lines.append(f"{S}<tr>")
        lines.append(f"{S}<td></td>")
        lines.append(
            f'{S}<td style="{style}  vertical-align:top; text-align:right;">'
            "Run time:"
            "</td>"
        )
        lines.append(f'{S}<td style="{style}">{time_txt}</td>')
        lines.append(f"{S}</tr>")

    if config.get("show_context_edits", False):
        style = get_context_style(status)
        adds, overs, dels = test["context_edits"] or ({}, {}, [])
        nb = len(adds) + len(overs) + len(dels)
        if nb:
            adds = "\n".join(["+%s=%r" % (k, v) for k, v in adds.items()])
            overs = "\n".join(["*%s=%r" % (k, v) for k, v in overs.items()])
            dels = "\n".join(["-" + i for i in dels])
            title = "%i Context Edits:" % (nb,)
            context_edits = "\n%s\n%s\n%s" % (
                adds,
                overs,
                dels,
            )
        else:
            title = "Context Edits:"
            context_edits = "/"
        context_edits = E(context_edits.strip())
        lines.append(f"{S}<tr>")
        lines.append(f"{S}<td></td>")
        lines.append(
            f'{S}<td style="{style} vertical-align:top; text-align:right">'
            f"{title}"
            f"</td>"
        )
        lines.append(f'{S}<td style="{style}"><pre>{context_edits}</pre></td>')
        lines.append(f"{S}</tr>")

    if config.get("show_contexts", False):
        style = get_context_style(status)
        context = test["context"]
        title = "Context Values:"
        if context:
            context = "\n".join(["    %s=%r" % (k, v) for k, v in context.items()])
            context = E(context.strip())
        else:
            context = "/!\\ Empty Context /!\\"
        lines.append(f"{S}<tr>")
        lines.append(f"{S}<td></td>")
        lines.append(
            f'{S}<td style="{style} vertical-align:top; text-align:right;">'
            f"{title}"
            "</td>"
        )
        lines.append(f'{S}<td style="{style}"><pre>{context}</pre></td>')
        lines.append(f"{S}</tr>")

    if config.get("show_descriptions", False):
        style = get_doc_style(status)
        lines.append(f"{S}<tr>")
        lines.append(f"{S}<td></td>")
        lines.append(
            f'{S}<td style="{style} vertical-align:top; text-align:right">'
            "Description:"
            "</td>"
        )
        lines.append(f'{S}<td style="{style}"><pre>\n{short}\n\n{long}</pre></td>')
        lines.append(f"{S}</tr>")

    # sub tests:
    for sub_test in test["sub_tests"]:
        lines.extend(
            test_to_html_table(
                sub_test,
                root_timestamp,
                indent + 1,
                config,
            )
        )

    return lines


def html_table(session_json_dumps, config):
    """
    Get html content showing the test results in a table
    as described by the config dict.

    A default config dict is returned by `get_default_config()`, use
    it as a starting point.
    """
    run_dicts = json.loads(session_json_dumps)
    lines = []
    for run in run_dicts:
        title = "Results on {}".format(time.ctime(run["timestamp"]))
        lines.append(f'<h3 class="session-run">{title}</h3>')
        # "boder-spacing" style is not supported by Qt
        # so we use "cellspacing
        lines.append('<table cellspacing="0">')
        lines.extend(
            test_to_html_table(
                run,
                run["timestamp"],
                0,
                config,
            )
        )
        lines.append("</table>")
    lines = "\n".join(lines)
    return TOP + lines + BOTTOM
