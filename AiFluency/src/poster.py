import requests


def post_review(github_token, repository, pr_number, comments):
    if not comments:
        print("No comments to post.")
        return

    owner, repo = repository.split("/")
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    commit_sha = _get_commit_sha(owner, repo, pr_number, headers)
    review_comments = [_build_comment(c) for c in comments]

    if _try_post_review(owner, repo, pr_number, commit_sha, review_comments, headers):
        print(f"Posted review with {len(review_comments)} comment(s).")
        return

    # Batch failed — fall back to posting individually, skipping failures
    print("Batch review failed. Falling back to individual comments...")
    posted = 0
    for comment in review_comments:
        if _try_post_review(owner, repo, pr_number, commit_sha, [comment], headers):
            posted += 1
        else:
            print(f"  Skipped comment on {comment['path']}:{comment['line']} (line not in diff)")

    print(f"Posted {posted}/{len(review_comments)} comment(s).")


def _get_commit_sha(owner, repo, pr_number, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["head"]["sha"]


def _build_comment(c):
    return {
        "path": c["filename"],
        "line": c["line"],
        "side": "RIGHT",
        "body": c["body"],
    }


def _try_post_review(owner, repo, pr_number, commit_sha, comments, headers):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
    payload = {
        "commit_id": commit_sha,
        "body": "",
        "event": "COMMENT",
        "comments": comments,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 422:
        return False
    response.raise_for_status()
    return True
