# Claude Skills Learning Hub

A comprehensive learning and development repository for Claude Skills, combining official Anthropic skills, community contributions, and custom skill development.

## Overview

This repository serves three main purposes:
1. **Reference Collection** - Track official Anthropic skills via git submodule
2. **Community Showcase** - Curate community-created skills via git submodule
3. **Development Workspace** - Build and test custom skills in `claude-skills-hub/`

## Features

- Full official Anthropic skills library (synced via submodule)
- Curated community skills collection (synced via submodule)
- Local development environment for custom skills
- Skill creation and validation tools
- Maven project converter for Java development
- Comprehensive documentation in both English and Chinese

## Repository Structure

```
claude-skills/
├── skills/                      # Anthropic official skills (submodule)
│   └── skills/                  # 17+ official skills
├── awesome-claude-skills/       # Community skills collection (submodule)
├── claude-skills-hub/           # Local development workspace
│   ├── maven-converter/         # Java to Maven converter skill
│   └── skill-creator/           # Skill development toolkit
├── CLAUDE.md                    # Repository guidance for Claude Code
├── AGENTS.md                    # Skills system configuration
└── Git-Submodule学习笔记.md    # Git submodule learning notes (Chinese)
```

## Quick Start

### Clone the Repository

```bash
# Clone with all submodules
git clone --recursive <your-repo-url>

# Or initialize submodules after cloning
git clone <your-repo-url>
cd claude-skills
git submodule update --init --recursive
```

### Update Submodules

```bash
# Update all submodules to latest versions
git submodule update --remote --recursive

# Update a specific submodule
cd skills  # or awesome-claude-skills
git pull origin master
cd ..
git add skills
git commit -m "Update skills submodule"
```

## Available Skills

### Official Skills (17+)

Located in `skills/skills/`:

- **algorithmic-art** - Generative art using p5.js
- **brand-guidelines** - Anthropic brand styling
- **canvas-design** - Visual art creation
- **doc-coauthoring** - Structured documentation workflow
- **docx** - Word document manipulation
- **frontend-design** - Production-grade web interfaces
- **internal-comms** - Internal communications templates
- **mcp-builder** - MCP server development guide
- **pdf** - PDF manipulation toolkit
- **pptx** - PowerPoint creation and editing
- **skill-creator** - Skill development guide
- **slack-gif-creator** - Animated GIFs for Slack
- **theme-factory** - Artifact styling themes
- **web-artifacts-builder** - Complex HTML artifacts
- **webapp-testing** - Web app testing with Playwright
- **xlsx** - Spreadsheet manipulation

### Custom Skills

Located in `claude-skills-hub/`:

#### Maven Converter
Automatically converts Java projects to standard Maven structure.

```bash
cd claude-skills-hub/maven-converter
python3 scripts/maven_converter.py <project-path> [options]
```

Options:
- `--dry-run` - Preview changes without modifying files
- `--group-id <id>` - Set Maven groupId (default: com.example)
- `--artifact-id <id>` - Set Maven artifactId (default: directory name)
- `--version <ver>` - Set project version (default: 1.0-SNAPSHOT)

#### Skill Creator
Toolkit for creating, validating, and packaging custom skills.

```bash
cd claude-skills-hub/skill-creator

# Initialize a new skill
python3 scripts/init_skill.py <skill-name> --path <output-directory>

# Validate a skill
python3 scripts/quick_validate.py <path/to/skill-folder>

# Package a skill
python3 scripts/package_skill.py <path/to/skill-folder> [output-directory]
```

## Skill Development Guide

### Skill Structure

Each skill follows this standard structure:

```
skill-name/
├── SKILL.md              # Required: YAML frontmatter + markdown instructions
│   ├── name:             # Required field
│   └── description:      # Required field (include when to use)
├── scripts/              # Optional: Executable code (Python/Bash)
├── references/           # Optional: On-demand documentation
└── assets/               # Optional: Templates, images, fonts
```

### Core Principles

1. **Progressive Disclosure** - Three-tier loading system:
   - Metadata (name + description) - Always loaded
   - SKILL.md body - Loaded when skill triggers
   - Bundled resources - Loaded on-demand

2. **Keep It Concise** - Assume Claude is smart; only add what Claude doesn't know

3. **Use Scripts** - Automate repeated, deterministic tasks

4. **Reference Files** - Store detailed docs separately for on-demand loading

5. **Clear Descriptions** - Include both what the skill does AND when to use it

### Development Workflow

1. Initialize skill structure using skill-creator
2. Write SKILL.md with YAML frontmatter and instructions
3. Add scripts for automated tasks (optional)
4. Add reference documentation (optional)
5. Validate skill structure
6. Package as `.skill` file (zip with .skill extension)

## Documentation

- **CLAUDE.md** - Comprehensive repository guidance for Claude Code
- **AGENTS.md** - Skills system configuration and usage
- **Git-Submodule学习笔记.md** - Detailed Git submodule documentation (Chinese)
- **skills/spec/agent-skills-spec.md** - Official agent skills specification

## Using Skills with Claude Code

Skills are automatically loaded via the `AGENTS.md` configuration file. To use a skill:

```bash
# Claude Code automatically detects available skills
# Simply request tasks that match skill descriptions
```

Skills are invoked through:
```bash
openskills read <skill-name>
```

## Contributing

### Adding Custom Skills

1. Create your skill in `claude-skills-hub/`
2. Follow the standard skill structure
3. Validate using the skill-creator toolkit
4. Test with Claude Code

### Updating Submodules

1. Navigate to submodule directory
2. Pull latest changes
3. Commit the submodule update in parent repository

```bash
cd skills
git pull origin master
cd ..
git add skills
git commit -m "Update skills submodule to latest version"
```

## Resources

- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/BehiSecc/awesome-claude-skills)
- [Claude Code Documentation](https://claude.com/claude-code)
- [Agent Skills Specification](./skills/spec/agent-skills-spec.md)

## License

This repository follows the licenses of its respective components:
- Official skills: See `skills/` submodule license
- Community skills: See `awesome-claude-skills/` submodule licenses
- Custom skills: Individual skill licenses apply

## Notes

- `.skill` files are zip archives with `.skill` extension
- `claude-skills-hub/` is for local development (not tracked by main repository)
- Submodules are read-only references to external repositories
- Use `git submodule update --remote` to sync with upstream changes
