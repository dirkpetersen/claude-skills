# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository generates Claude Code skills from documentation. Users place PDF or markdown files in subfolders, and Claude Code processes them to create skills saved in `.claude/skills/`.

## Workflow

1. Create a subfolder (e.g., `aws-sdk-go/`)
2. Add PDF or markdown documentation to the subfolder
3. Claude Code reads the content and generates a skill file

## Skill File Format

Generated skills must start with YAML frontmatter:

```yaml
---
name: my-skill-name
description: one line description as accurate as possible
---
```

**Requirements:**
- Name should match the subfolder name (e.g., `aws-sdk-go-v2` for `aws-sdk-go/` folder)
- Description should be a single, accurate line summarizing the skill's purpose
- Use markdown format after frontmatter for the skill content

## Creating Skills from Documentation

When generating a skill:

1. **Extract key information**: Focus on practical usage patterns, API examples, and common tasks
2. **Structure content**: Organize with clear headers (## Setup, ## Quick Start, ## Examples, etc.)
3. **Include code examples**: Provide working, copy-pasteable code snippets with language tags
4. **Reference links**: Include links to official documentation for deeper dives
5. **Keep it concise**: Skills should be quick reference guides, not exhaustive documentation

Look at existing skills in `.claude/skills/` for formatting examples (e.g., `fireworks-ai.md`, `aws-sdk-go-v2.md`).

## Directory Structure

- Root subfolders (e.g., `aws-sdk-go/`, `fireworks-ai/`) contain source documentation
- `.claude/skills/` contains generated skill markdown files
- Source docs can be PDFs or markdown files
