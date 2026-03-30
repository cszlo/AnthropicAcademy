import anthropic

SYSTEM_PROMPT = """You are a code reviewer helping a developer improve AI-generated code. Review the provided file and call the `submit_review_comments` tool with your findings.

Only comment if there is a genuine improvement to be made. If the code is already clear, well-named, and reasonably readable, call the tool with an empty array. This is a safety net — not a mandate to find something wrong with every PR.

Tone: Mentor to junior engineer. Instructive, direct, and respectful. Give a brief reason for every suggestion. Never condescending.

Renames: Show a before/after block and explain why the new name is clearer.
Rewrites: Show a before/after diff block and explain the improvement.
Vulnerabilities/efficiency: Explain the risk or cost and what to do instead.
Clarification: If you genuinely cannot infer what a function does, ask one specific question. Do not guess."""

REVIEW_TOOL = {
    "name": "submit_review_comments",
    "description": "Submit inline review comments for the PR.",
    "input_schema": {
        "type": "object",
        "properties": {
            "comments": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "filename": {"type": "string"},
                        "line":     {"type": "integer"},
                        "type":     {"type": "string", "enum": ["rename", "rewrite", "vulnerability", "clarification_needed"]},
                        "body":     {"type": "string"},
                    },
                    "required": ["filename", "line", "type", "body"],
                },
            }
        },
        "required": ["comments"],
    },
}


def _build_user_message(file_data):
    filename = file_data["filename"]
    status = file_data["status"]
    mode = file_data["mode"]

    if mode == "full_file":
        lines = file_data["content"].splitlines()
        numbered = "\n".join(f"{i + 1:4}: {line}" for i, line in enumerate(lines))
        mode_description = f"full_file — New file, {file_data['line_count']} lines. Review the entire file."
        content_block = numbered

    elif mode == "context":
        mode_description = "context — Existing file. Changed lines are marked with [CHANGED]. Focus your review on those only; surrounding context is for reference."
        parts = []
        for entry in file_data["context"]:
            if entry.get("separator"):
                parts.append("   ...")
            else:
                marker = "[CHANGED]" if entry["changed"] else "         "
                parts.append(f"{entry['line_number']:4}: {marker} {entry['content']}")
        content_block = "\n".join(parts)

    elif mode == "diff_only":
        mode_description = f"diff_only — File exceeds 300 lines ({file_data['line_count']} total). Diff only shown. Review only what changed."
        content_block = file_data["patch"]

    else:
        return None

    return (
        f"Reviewing: `{filename}` ({status})\n"
        f"Mode: {mode_description}\n\n"
        f"{content_block}"
    )


def review_files(anthropic_api_key, files):
    client = anthropic.Anthropic(api_key=anthropic_api_key)
    all_comments = []

    for file_data in files:
        if file_data["mode"] == "removed":
            continue

        user_message = _build_user_message(file_data)
        if not user_message:
            continue

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=[REVIEW_TOOL],
            tool_choice={"type": "tool", "name": "submit_review_comments"},
            messages=[{"role": "user", "content": user_message}],
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == "submit_review_comments":
                comments = block.input.get("comments", [])
                print(f"  {file_data['filename']}: {len(comments)} comment(s) from Claude")
                all_comments.extend(comments)

    return all_comments
