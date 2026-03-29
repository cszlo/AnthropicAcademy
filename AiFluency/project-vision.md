# AI Code Reviewer — Project Vision

## Project Summary

A Python-based GitHub Action that triggers on pull requests targeting `main`. It analyzes changed files using Claude, posts inline review comments directly on the PR diff with confident rename suggestions, readability rewrites, and a vulnerability/efficiency report. It infers code intent automatically and only requests context from the developer when it genuinely cannot determine what the code does. Built in Python, designed for teams and solo devs who rely heavily on AI-generated code.

---

## Problem Statement

AI coding tools (Claude Code, GitHub Copilot, etc.) write functional code but often produce output that is hard for humans to read and maintain — poor function/variable names, no comments, no doc blocks. This tool addresses that gap.

---

## Target User

Developers — hobbyist and professional — who use AI agents to generate code and need help making that output readable, maintainable, and secure.

---

## Core Loop

1. Developer opens a pull request targeting `main`
2. GitHub Action triggers (not on every commit — token efficiency)
3. Tool analyzes changed files using Claude
4. Claude infers code intent automatically; only asks for context when it cannot determine what the code does
5. Tool posts inline PR comments with:
   - Confident rename suggestions for functions/variables (with reasoning)
   - Readability rewrites (diff-style, original vs. suggested)
   - Vulnerability and efficiency report

---

## Key Design Decisions

- **Trigger**: PR open/update targeting `main` — not every push
- **Output**: Inline GitHub PR comments (familiar, fits existing workflow)
- **Rewrites**: One confident suggestion, not multiple options
- **Context**: Only requested from user when Claude cannot infer intent
- **Scope**: Language agnostic
- **Stack**: Python + Anthropic SDK

---

## Success Criteria

A file with function names like `funcA1()` and variables like `varA`, `varB`, `num1` gets returned with inferred, meaningful names and a clear explanation of why — without the developer having to explain what the code does.
