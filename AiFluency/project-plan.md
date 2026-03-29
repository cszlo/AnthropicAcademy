# AI Code Reviewer — Project Plan

## Task Breakdown & Delegation Analysis

---

### Task 1: GitHub Action Scaffolding
**What it involves:** `action.yml`, Python entry point, PR trigger, GitHub API auth.

**Trigger event:** `pull_request` with type `ready_for_review` — fires when a PR moves from Draft to Ready, not on every commit.

**Skills needed:** GitHub Actions syntax, Python, YAML config.

**Delegation: Almost entirely AI.**
Well-documented, pattern-driven boilerplate. No product judgment required. You own the trigger decision (already made).

---

### Task 2: File Diff Extraction
**What it involves:** Extracting changed files and lines from the PR via GitHub API. Three modes:
1. Changed lines + surrounding context (default)
2. Full file for new files under 300 lines
3. Diff only + truncation warning for files over the threshold

**Skills needed:** GitHub API, diff parsing, token management.

**Delegation: Collaborative.**
You own the thresholds and edge case rules. Claude implements the extraction logic.

---

### Task 3: Claude Prompt / Agent Logic
**What it involves:** How Claude is instructed to analyze code, infer intent, suggest renames, rewrite for readability, and flag vulnerabilities.

**Tone:** Direct and professional — like a senior dev who respects your time. Not cutesy, not a linter. Vulnerabilities get real explanation, rename suggestions get a one-liner reason, rewrites speak for themselves.

**When Claude can't infer intent:** Review what it can, post an inline comment asking a specific question, wait for dev response via `@claude-review` mention.

**Output:** One confident rewrite suggestion per issue — no multiple options.

**Skills needed:** Prompt engineering, output schema design, Claude API.

**Delegation: Human-led.**
You own the tone, output structure, and interaction model. Claude drafts the prompt, you refine it. This is the core product differentiator.

---

### Task 4: GitHub API — Posting the Review
**What it involves:** Mapping Claude's output to GitHub's inline PR review comment format. All comments posted at once as a single review — one notification, everything in one place.

**Skills needed:** GitHub API, comment threading, review submission.

**Delegation: Almost entirely AI.**
Pure plumbing, well-documented, no product judgment needed.

---

### Task 5: Testing
**What it involves:**
- Automated tests for mechanical parts (trigger, diff extraction, API posting, structured output format)
- Fixture files of deliberately bad AI-generated code for manual output quality validation

**Skills needed:** Python testing (pytest), fixture design, judgment on output quality.

**Delegation: Collaborative.**
You own the fixture files — real examples of bad AI-generated code. Claude writes the automated test suite.

---

### Task 6: Agentic Follow-Up Loop
**What it involves:** When Claude posts a comment requesting context, the dev responds by mentioning `@claude-review` in a PR comment. The Action listens for `issue_comment` events, checks for the mention, extracts the context, and triggers a follow-up review pass on the unclear section.

**Why it matters:** Demonstrates multi-turn agentic workflows — the showpiece of the portfolio project.

**Skills needed:** GitHub webhooks, comment parsing, stateful context passing, Claude API.

**Delegation: Mostly AI** once interaction model is defined (already decided: `@claude-review` mention pattern).

---

### Task 7: README / Documentation
**What it involves:** Setup instructions, usage guide, design decisions, example PR review screenshots.

**Skills needed:** Technical writing, product framing for a portfolio audience.

**Delegation: Collaborative.**
You own the framing and what to highlight for a portfolio audience. Claude drafts, you refine.

---

## Summary Table

| Task | Delegation |
|---|---|
| 1. GHA scaffolding | AI |
| 2. File diff extraction | Collaborative (you own thresholds) |
| 3. Claude prompt / agent logic | Human-led |
| 4. GitHub API — post review | AI |
| 5. Testing | Collaborative (you own fixtures) |
| 6. Agentic follow-up loop | Mostly AI |
| 7. README / documentation | Collaborative |
