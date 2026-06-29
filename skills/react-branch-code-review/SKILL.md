---
name: react-branch-code-review
description: Review the changed code in the current local branch in a React project.
---

Run `git diff origin/develop...HEAD` to get the changes.

Review the code:

- No unnecessary `useEffect` hooks. See [You Might Not Need an Effect](references/you-might-not-need-an-effect.md) for details.

Provide feedback organized by priority and include examples of how to fix the issues:

- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)
