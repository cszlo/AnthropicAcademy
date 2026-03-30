import re
import base64

from github import Github

CONTEXT_LINES = 10
LINE_THRESHOLD = 300


def extract_pr_files(github_token, repository, pr_number):
    g = Github(github_token)
    repo = g.get_repo(repository)
    pr = repo.get_pull(int(pr_number))

    results = []
    for f in pr.get_files():
        results.append(_extract_file(repo, pr, f))

    return results


def _extract_file(repo, pr, f):
    filename = f.filename
    status = f.status  # added, modified, removed, renamed

    if status == "removed":
        return {"filename": filename, "status": status, "mode": "removed", "patch": f.patch}

    content, line_count = _fetch_content(repo, pr, filename)

    if line_count > LINE_THRESHOLD:
        return {
            "filename": filename,
            "status": status,
            "mode": "diff_only",
            "line_count": line_count,
            "truncation_warning": f"File exceeds {LINE_THRESHOLD} lines ({line_count} total). Showing diff only.",
            "patch": f.patch,
        }

    if status == "added":
        return {
            "filename": filename,
            "status": status,
            "mode": "full_file",
            "line_count": line_count,
            "content": content,
            "patch": f.patch,
        }

    # Default: changed lines + surrounding context
    return {
        "filename": filename,
        "status": status,
        "mode": "context",
        "context": _extract_with_context(content, f.patch),
        "patch": f.patch,
    }


def _fetch_content(repo, pr, filename):
    try:
        content_file = repo.get_contents(filename, ref=pr.head.sha)
        content = base64.b64decode(content_file.content).decode("utf-8")
        line_count = content.count("\n") + 1
        return content, line_count
    except Exception:
        return None, 0


def _extract_with_context(content, patch):
    if not content or not patch:
        return []

    lines = content.splitlines()
    changed_line_numbers = set()

    current_new_line = 0
    for line in patch.splitlines():
        hunk_match = re.match(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if hunk_match:
            current_new_line = int(hunk_match.group(1)) - 1
            continue

        if line.startswith("+++") or line.startswith("---"):
            continue

        if line.startswith("+"):
            changed_line_numbers.add(current_new_line)
            current_new_line += 1
        elif line.startswith("-"):
            pass  # deleted lines don't advance the new file counter
        else:
            current_new_line += 1

    # Expand each changed line to include surrounding context
    lines_to_include = set()
    for line_num in changed_line_numbers:
        for i in range(
            max(0, line_num - CONTEXT_LINES),
            min(len(lines), line_num + CONTEXT_LINES + 1),
        ):
            lines_to_include.add(i)

    # Build ordered result with separators between non-contiguous sections
    result = []
    last_included = None
    for i, line in enumerate(lines):
        if i not in lines_to_include:
            continue
        if last_included is not None and i > last_included + 1:
            result.append({"separator": True})
        result.append({
            "line_number": i + 1,
            "content": line,
            "changed": i in changed_line_numbers,
        })
        last_included = i

    return result
