# Issue tracker: GitHub

Issues and specs for this repo live as GitHub issues in `aswathas/ai-lab-m0-engineering`. Use the `gh` CLI for all operations.

**This repo's issues are learning work items.** One issue per exercise or artifact
within the module. Issue #N is task N. The chain is sequential: #N is blocked by #(N-1),
so exactly one issue is startable at a time.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Blocking**: GitHub's native issue dependencies. Add an edge with `gh issue create --blocked-by <n>` or `gh issue edit <child> --add-blocked-by <blocker>` (gh 2.94+). Fallback for older gh: a `Blocked by: #<n>` line at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Count open blockers**: `gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by` (open blockers only; 0 means startable).
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: post the explanation with `gh issue comment <number> --body "..."`, then `gh issue close <number>`.

Infer the repo from `git remote -v`; `gh` does this automatically inside a clone.

File issues only into the user's own repo. Before the first `gh issue create` of a
session, check the target with `gh repo view --json nameWithOwner`.

## Pull requests as a triage surface

**PRs as a request surface: no.** _(/triage reads this flag.)_

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Read it as in **Read an issue** above.
