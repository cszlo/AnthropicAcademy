import os
import sys

from diff_extractor import extract_pr_files


def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    anthropic_api_key = os.environ.get("ANTHROPIC_API_KEY")
    repository = os.environ.get("GITHUB_REPOSITORY")
    pr_number = os.environ.get("PR_NUMBER")

    if not github_token:
        print("Error: GITHUB_TOKEN not set", file=sys.stderr)
        sys.exit(1)
    if not anthropic_api_key:
        print("Error: ANTHROPIC_API_KEY not set", file=sys.stderr)
        sys.exit(1)
    if not repository or not pr_number:
        print("Error: Must be run in a pull_request context", file=sys.stderr)
        sys.exit(1)

    print(f"AI Code Reviewer triggered on PR #{pr_number} in {repository}")

    files = extract_pr_files(github_token, repository, pr_number)

    print(f"\nExtracted {len(files)} changed file(s):")
    for f in files:
        mode = f["mode"]
        filename = f["filename"]
        if mode == "full_file":
            print(f"  [{mode}] {filename} ({f['line_count']} lines)")
        elif mode == "diff_only":
            print(f"  [{mode}] {filename} — {f['truncation_warning']}")
        elif mode == "context":
            changed = sum(1 for l in f["context"] if isinstance(l, dict) and l.get("changed"))
            print(f"  [{mode}] {filename} ({changed} changed line(s), ±{10} context)")
        elif mode == "removed":
            print(f"  [{mode}] {filename}")

    # Task 3: analyze with Claude, infer intent, suggest renames/rewrites, flag vulnerabilities
    # Task 4: post inline review comments via GitHub API


if __name__ == "__main__":
    main()
