# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a learning and development repository for Claude Skills. It serves as:
- A reference collection of official Anthropic skills (via submodule)
- A curated list of community skills (via submodule)
- A workspace for developing custom skills in `claude-skills-hub/`

## Repository Structure

### Git Submodules

This repository uses Git submodules to track external skill repositories:

- **`skills/`** - Anthropic's official skills repository (anthropics/skills)
- **`awesome-claude-skills/`** - Community-curated skills collection (BehiSecc/awesome-claude-skills)

When cloning this repository on a new machine or after updates:

```bash
# Initialize and update all submodules
git submodule update --init --recursive

# Update submodules to their latest versions
git submodule update --remote
```

### Local Development Directory

- **`claude-skills-hub/`** - Local workspace for custom skill development (not tracked by git)
  - Contains skills being actively developed or customized
  - Each skill should follow the standard skill structure

## Skill Development Workflow

### Skill Structure

Each skill follows this standard structure:

```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + markdown instructions
│   ├── name:             # Required field in frontmatter
│   └── description:      # Required field in frontmatter
├── scripts/              # Optional: Executable code (Python/Bash)
├── references/           # Optional: Documentation loaded on-demand
└── assets/               # Optional: Templates, images, fonts for output
```

### Common Development Commands

#### Initialize a New Skill

```bash
cd claude-skills-hub/skill-creator
python3 scripts/init_skill.py <skill-name> --path <output-directory>
```

This creates a new skill directory with template structure.

#### Validate a Skill

```bash
cd claude-skills-hub/skill-creator
python3 scripts/quick_validate.py <path/to/skill-folder>
```

Checks for proper YAML frontmatter, required fields, and structure.

#### Package a Skill

```bash
cd claude-skills-hub/skill-creator
python3 scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

Validates and packages the skill into a `.skill` file (zip format with .skill extension).

#### Maven Converter Skill

```bash
cd claude-skills-hub/maven-converter
python3 scripts/maven_converter.py <java-project-path> [options]
```

Common options:
- `--dry-run` - Preview changes without modifying files
- `--group-id <id>` - Set Maven groupId (default: com.example)
- `--artifact-id <id>` - Set Maven artifactId (default: directory name)
- `--version <ver>` - Set project version (default: 1.0-SNAPSHOT)

## Skill Design Principles

### Progressive Disclosure

Skills use a three-tier loading system to manage context efficiently:

1. **Metadata (name + description)** - Always loaded (~100 words)
2. **SKILL.md body** - Loaded when skill triggers (<5k words, keep under 500 lines)
3. **Bundled resources** - Loaded on-demand by Claude

### Key Guidelines

- **Keep SKILL.md concise**: Assume Claude is smart; only add what Claude doesn't know
- **Use scripts for repeated tasks**: Python/Bash scripts for deterministic operations
- **Reference files for documentation**: Store detailed docs in `references/` to load on-demand
- **Assets for output files**: Store templates, images, fonts in `assets/` for use in generated output
- **Avoid duplication**: Information should exist in SKILL.md OR reference files, not both

### Description Field Best Practices

The `description` in YAML frontmatter is the primary trigger mechanism:
- Include what the skill does AND when to use it
- All "when to use" information goes here (not in body)
- Be specific about trigger contexts and use cases

Example:
```yaml
description: Converts Java projects to standard Maven structure, reorganizes directories, transforms package names (test→example), and generates pom.xml. Use when users need to convert non-Maven Java projects to Maven, restructure existing projects to Maven standards, or request Maven project setup/conversion.
```

## Working with Submodules

### View Submodule Status

```bash
git submodule status
```

### Update a Specific Submodule

```bash
cd skills  # or awesome-claude-skills
git pull origin master
cd ..
git add skills
git commit -m "Update skills submodule to latest version"
```

### Update All Submodules

```bash
git submodule update --remote --recursive
git add .
git commit -m "Update all submodules to latest versions"
```

## File Organization

- **Root level**: Configuration files, this CLAUDE.md, git submodule configuration
- **`skills/`**: Official Anthropic skills (submodule, read-only reference)
- **`awesome-claude-skills/`**: Community skills collection (submodule, read-only reference)
- **`claude-skills-hub/`**: Active development workspace
  - Custom skills being developed
  - Modified/enhanced versions of existing skills
  - Skill development toolkit (skill-creator)

## Notes

- The `.skill` file format is a zip archive with `.skill` extension
- Skills in `claude-skills-hub/` are local development and not tracked by the main repository
- Refer to `Git-Submodule学习笔记.md` for detailed Git submodule documentation (in Chinese)
- Both submodules point to external repositories and should not be modified directly unless you have permissions to those repositories
