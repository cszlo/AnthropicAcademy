import os
import sys


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

    # Task 2: extract changed files and diff from the PR
    # Task 3: analyze with Claude, infer intent, suggest renames/rewrites, flag vulnerabilities
    # Task 4: post inline review comments via GitHub API


if __name__ == "__main__":
    main()
