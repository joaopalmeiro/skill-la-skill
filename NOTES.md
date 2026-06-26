# Notes

- https://agentskills.io/home
  - https://github.com/agentskills/agentskills
  - https://github.com/anthropics/skills/tree/main/template
  - https://agentskills.io/what-are-skills#how-skills-work
    - "Discovery: At startup, agents load only the name and description of each available skill, just enough to know when it might be relevant."
  - Validation: https://github.com/agentskills/agentskills/tree/main/skills-ref
  - https://agentskills.io/skill-creation/best-practices
  - https://agentskills.io/specification#references%2F
    - "Contains additional documentation that agents can read when needed:"
    - "Keep individual reference files focused. Agents load these on demand, so smaller files mean less use of context."
  - https://agentskills.io/skill-creation/optimizing-descriptions
    - "The `description` field in your `SKILL.md` frontmatter is the primary mechanism agents use to decide whether to load a skill for a given task."
    - "This means the description carries the entire burden of triggering. If the description doesn't convey when the skill is useful, the agent won't know to reach for it."
    - "A simple, one-step request like "read this PDF" may not trigger a PDF skill even if the description matches perfectly, because the agent can handle it with basic tools."
    - "Use imperative phrasing. Frame the description as an instruction to the agent: "Use this skill when..." rather than "This skill does...""
    - "Explicitly list contexts where the skill applies (...)"
    - "The specification enforces a hard limit of 1024 characters."
    - Example: "**Analyze** CSV and tabular data files — compute summary statistics, add derived columns, generate charts, and clean messy data. **Use this skill when** the user has a CSV, TSV, or Excel file and wants to explore, transform, or visualize the data, **even if** they don't explicitly mention "CSV" or "analysis.""
- https://ona.com/
- https://autohand.ai/
- https://sockpuppet.org/blog/2026/03/30/vulnerability-research-is-cooked/
  - https://blog.andymasley.com/p/the-ai-water-issue-is-fake
- https://github.com/vercel-labs/agent-skills
  - https://skills.sh/vercel-labs/agent-skills
  - https://github.com/vercel-labs/agent-skills/blob/73140fc5b3a214ad3222bcf557b397b3c02d11c1/README.md#license: MIT
  - https://github.com/vercel-labs/agent-skills/blob/73140fc5b3a214ad3222bcf557b397b3c02d11c1/skills/react-best-practices/SKILL.md
  - https://github.com/vercel-labs/agent-skills/blob/73140fc5b3a214ad3222bcf557b397b3c02d11c1/AGENTS.md#troubleshooting
    - "- **Keep SKILL.md under 500 lines** — put detailed reference material in separate files"
    - "- **Prefer scripts over inline code** — script execution doesn't consume context (only output does)"
    - "- **File references work one level deep** — link directly from SKILL.md to supporting files"
  - https://github.com/vercel-labs/agent-skills/tree/main/skills/react-best-practices
- https://kiro.dev/docs/skills/
- https://github.com/remotion-dev/skills
- https://github.com/wshobson/agents/tree/main/plugins/javascript-typescript/skills/modern-javascript-patterns
- https://react.dev/learn/you-might-not-need-an-effect
- https://code.claude.com/docs/en/skills#frontmatter-reference
  - "Add `disable-model-invocation: true` if you only want manual invocation"
- https://www.skills.sh/google-gemini/gemini-cli/code-reviewer
- https://github.com/mattpocock/skills

## Snippets

- https://github.com/shuding/better-all/discussions/3
- https://github.com/shuding/better-all
- https://github.com/vercel-labs/agent-skills/blob/73140fc5b3a214ad3222bcf557b397b3c02d11c1/skills/react-best-practices/rules/async-dependencies.md

```ts
const promiseA = getA();
const promiseB = getB();
const promiseC = getC(await promiseA); // or const promiseC = promiseA.then(getC)

const [a, b, c] = await Promise.all([promiseA, promiseB, promiseC]);
```

```ts
const userPromise = fetchUser();
const profilePromise = userPromise.then((user) => fetchProfile(user.id));

const [user, config, profile] = await Promise.all([
  userPromise,
  fetchConfig(),
  profilePromise,
]);
```

- https://github.com/vercel-labs/skills/tree/v1.5.13#creating-skills

```markdown
---
name: my-skill
description: What this skill does and when to use it
---

# My Skill

Instructions for the agent to follow when this skill is activated.

## When to Use

Describe the scenarios where this skill should be used.

## Steps

1. First, do this
2. Then, do that
```

- https://code.claude.com/docs/en/sub-agents#code-reviewer

```markdown
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:

1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:

- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:

- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

- https://github.com/augmentcode/augment-agent/blob/cd94b92e0971d54781546c5889f28e24d5efee77/example-workflows/code-review.yml

```yml
name: Augment Agent - Code Review
on:
  pull_request:
    types: [opened]

jobs:
  code-review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - name: Create instruction file
        env:
          PR_NUMBER: ${{ github.event.pull_request.number }}
          REPOSITORY: ${{ github.repository }}
          BASE_BRANCH: ${{ github.event.pull_request.base.ref }}
          HEAD_BRANCH: ${{ github.event.pull_request.head.ref }}
        run: |
          cat > /tmp/review-instruction.txt << EOF
          Perform a comprehensive code review of the following pull request:

          **Pull Request Information:**
          - PR Number: ${PR_NUMBER}
          - Repository: ${REPOSITORY}
          - Base Branch: ${BASE_BRANCH}
          - Head Branch: ${HEAD_BRANCH}

          **Review Focus:**
          Analyze the modified files and provide detailed feedback on:
          - Code quality and adherence to best practices
          - Potential bugs, errors, or security vulnerabilities
          - Performance implications of the changes
          - Suggestions for improvement or optimization
          - Any missing error handling or edge cases
          - Code maintainability and readability

          Please provide specific, actionable feedback with file and line references where applicable.
          Focus on the actual code changes and their impact on the codebase.

          Please post your review as a review comment on the PR. Do not approve or request changes.
          EOF
      - name: Code Review
        uses: augmentcode/augment-agent@v0
        with:
          augment_session_auth: ${{ secrets.AUGMENT_SESSION_AUTH }}
          github_token: ${{ secrets.GITHUB_TOKEN }}
          instruction_file: /tmp/review-instruction.txt
```

- https://cursor.com/docs/skills#skillmd-file-format

```markdown
---
name: my-skill
description: Short description of what this skill does and when to use it.
---

# My Skill

Detailed instructions for the agent.

## When to Use

- Use this skill when...
- This skill is helpful for...

## Instructions

- Step-by-step guidance for the agent
- Domain-specific conventions
- Best practices and patterns
- Use the ask questions tool if you need to clarify requirements with the user
```

- https://react.dev/learn/you-might-not-need-an-effect

```plain
How to tell if a calculation is expensive?

In general, unless you're creating or looping over thousands of objects, it's probably not expensive. If you want to get more confidence, you can add a console log to measure the time spent in a piece of code:

console.time('filter array');
const visibleTodos = getFilteredTodos(todos, filter);
console.timeEnd('filter array');

Perform the interaction you're measuring (for example, typing into the input). You will then see logs like filter array: 0.15ms in your console. If the overall logged time adds up to a significant amount (say, 1ms or more), it might make sense to memoize that calculation. As an experiment, you can then wrap the calculation in useMemo to verify whether the total logged time has decreased for that interaction or not:

console.time('filter array');
const visibleTodos = useMemo(() => {
  return getFilteredTodos(todos, filter); // Skipped if todos and filter haven't changed
}, [todos, filter]);
console.timeEnd('filter array');

useMemo won't make the first render faster. It only helps you skip unnecessary work on updates.

Keep in mind that your machine is probably faster than your users' so it's a good idea to test the performance with an artificial slowdown. For example, Chrome offers a CPU Throttling option for this.

Also note that measuring performance in development will not give you the most accurate results. (For example, when Strict Mode is on, you will see each component render twice rather than once.) To get the most accurate timings, build your app for production and test it on a device like your users have.
```

- https://kiro.dev/docs/chat/subagents/

```markdown
---
name: code-reviewer
description: Expert code review assistant.
tools: ["read", "@context7"]
model: claude-sonnet-4
---

You are a senior code reviewer.

## Your Responsibilities
- Review code for correctness, performance, and security
...
```
