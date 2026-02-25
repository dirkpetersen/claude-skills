# Claude Skills Collection

A tool that automatically collects and generates [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skills from multiple sources into a single `.claude/skills/` directory.

## What Are Claude Code Skills?

Skills are markdown files that give Claude Code specialized knowledge — coding standards, API references, tool usage guides, and more. When you or Claude invoke a skill, its content is loaded into context so Claude can follow the instructions precisely.

Each skill lives in its own folder as a `SKILL.md` file with YAML frontmatter:

```yaml
---
name: my-skill
description: Use this skill whenever the user wants to...
---

## Quick Start
Instructions, examples, and reference material here...
```

## What This Tool Does

`collect-skills.py` aggregates skills from three sources:

1. **Local subfolders** — Reads PDFs, markdown, or existing `SKILL.md` files from subfolders in this repo. If no valid skill file exists, it uses AI (Claude CLI or Anthropic SDK) to generate one from the documentation.
2. **GitHub repos** — Scans all public repos of a GitHub user (default: `dirkpetersen`) for `.claude/skills/` folders and `SKILL.md` files. Only repos active in the last 30 days are checked.
3. **URLs in `skills.txt`** — Fetches `SKILL.md` files from GitHub URLs listed one per line.

### Quick Start

```bash
# Run all three sources (default)
python collect-skills.py

# Only process local subfolders
python collect-skills.py --source local

# Preview without writing files
python collect-skills.py --dry-run

# Force regeneration of existing skills
python collect-skills.py --overwrite
```

### CLI Options

```
--dry-run              Show what would happen without writing files
-v, --verbose          Extra output
--source SOURCE [...]  Sources: local, github, urls (default: all three)
--github-user NAME     GitHub user to scan (default: dirkpetersen)
--no-generate          Disable AI generation from PDF/text docs
--overwrite            Replace skills that already exist on disk
```

### Adding Your Own Documentation

1. Create a subfolder (e.g., `my-library/`)
2. Add PDF or markdown documentation to it
3. Run `python collect-skills.py --source local`
4. The tool generates a skill in `.claude/skills/my-library/SKILL.md`

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `GH_TOKEN` or `GITHUB_TOKEN` | Raises GitHub API limit from 60 to 5,000 req/h |
| `ANTHROPIC_API_KEY` | SDK fallback when `claude` CLI is not available |
| `AWS_PROFILE` | AWS profile for Bedrock SDK fallback (default: `bedrock`) |
| `AWS_DEFAULT_REGION` | AWS region for Bedrock (default: `us-west-2`) |
| `ANTHROPIC_MODEL` | Override the model used for generation |

### AI Generation

When a subfolder has documentation but no valid skill file, the tool generates one using AI:

- **Primary**: `claude` CLI in batch mode (`claude -p`). Reads PDFs natively.
- **Fallback**: Anthropic Python SDK (direct API or AWS Bedrock). Requires `pip install 'anthropic[bedrock]'` or `pip install anthropic`.

Generation is skipped if a skill already exists on disk. Use `--overwrite` to force regeneration.

### GitHub Actions

The included workflow (`.github/workflows/collect-skills.yml`) runs daily at 03:00 UTC and on manual trigger. Add `ANTHROPIC_API_KEY` and `GH_TOKEN` as repository secrets.

## Installing Skills in Claude Code

Claude Code looks for skills at three levels. Copy skill folders from `.claude/skills/` to whichever scope you need:

### Project-Level (this repo only)

Skills in `.claude/skills/` of any git repository are automatically available when Claude Code runs in that project. This is the default location where `collect-skills.py` writes skills.

```
your-project/
  .claude/
    skills/
      my-skill/
        SKILL.md
```

### Personal / User-Level (all your projects)

Copy skills to `~/.claude/skills/` to make them available in every project:

```bash
# Copy a single skill
cp -r .claude/skills/aws-sdk-go ~/.claude/skills/

# Copy all skills
cp -r .claude/skills/* ~/.claude/skills/
```

```
~/.claude/
  skills/
    aws-sdk-go/
      SKILL.md
    bash/
      SKILL.md
```

### Enterprise-Level (organization-wide)

Managed by organization admins through enterprise policy. Skills at this level apply to all users in the organization.

### Precedence

When the same skill name exists at multiple levels: **Enterprise > Personal > Project**.

## Using Skills in Claude Code

### Automatic Invocation

Claude reads the `description` field from all available skills. When your request matches a skill's description, Claude automatically loads and follows it. For example, if you ask about AWS SDK for Go, Claude will load the `aws-sdk-go` skill.

### Slash Commands

Type `/` in Claude Code to see all available skills, then select one:

```
/aws-sdk-go
/bash
/pdf my-document.pdf
```

Skills with arguments pass them via `$ARGUMENTS`:

```
/my-skill arg1 arg2
```

### Current Skills

| Skill | Description |
|-------|-------------|
| `agent-deck` | Terminal session manager for AI coding agents |
| `appmotel` | Managing Appmotel PaaS for automation with Claude Code |
| `aws-sdk-go` | AWS SDK for Go v2 — clients, operations, S3, paginators |
| `bash` | Bash coding standards with strict mode and best practices |
| `ec2-cli` | Advanced AWS CLI script for launching EC2 instances |
| `fireworks-ai` | Fireworks AI API — models, function calling, streaming |
| `pdf` | Reading, creating, merging, splitting, and converting PDFs |

## Skill File Format

### Frontmatter (required)

```yaml
---
name: kebab-case-name
description: Use this skill whenever the user wants to...
---
```

- **name**: lowercase, hyphens only, no spaces, no `claude-` or `anthropic-` prefix
- **description**: verbose, starts with "Use this skill whenever...", lists every trigger phrase

### Optional Frontmatter Fields

```yaml
---
name: my-skill
description: Use this skill whenever...
user-invocable: false        # hide from / menu, only Claude can invoke
disable-model-invocation: true  # only user can invoke via /command
allowed-tools: Read, Grep, Bash  # tools permitted without asking
context: fork                # run in isolated subagent context
---
```

### Body (markdown)

Organize with clear sections:

```markdown
## Setup
Installation and configuration steps

## Quick Start
Minimal working examples

## Examples
Detailed, copy-pasteable code snippets with language tags

## Key Concepts
Important patterns and best practices

## References
Links to official documentation
```

### Rules

- No XML angle brackets (`<`, `>`) outside of code fences
- Keep total file under 5,000 words
- Every code example must use fenced blocks with language tags
- Descriptions should be 3-6 sentences (400-900 characters)
