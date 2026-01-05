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

## Git Commit Message Guidelines

**IMPORTANT**: All git commit messages in this repository MUST be written in Simplified Chinese (简体中文).

### Commit Message Format

Use the following format for all commits:

```
[类型] 简短描述

详细说明（可选）
```

### Commit Types (提交类型)

- **添加** - 新增功能、文件或特性
- **修复** - 修复bug或问题
- **重构** - 代码结构调整，不改变功能
- **优化** - 性能改进或代码优化
- **更新** - 更新依赖、文档、配置等
- **删除** - 移除代码、文件或功能
- **测试** - 添加或修改测试
- **文档** - 仅文档更改

### Examples (示例)

```bash
# Good examples (好的示例)
添加用户认证模块和JWT令牌支持
修复登录页面验证逻辑的空指针异常
重构数据库查询逻辑以提高性能
更新README文档和API使用说明
优化技能加载速度和内存使用

# Bad examples (避免使用)
Add user authentication  # 不要使用英文
fix bug  # 描述不清晰
update  # 太模糊
```

### Commit Message Rules

1. **使用中文** - 所有commit message必须用简体中文编写
2. **动词开头** - 使用祈使句形式（添加、修复、更新等）
3. **描述清晰** - 简洁但准确地描述改动内容
4. **避免混用** - 不要混用中英文（除非是专有名词如 API、GitHub、Maven等）
5. **首行简短** - 第一行不超过50个字符
6. **详细说明** - 复杂改动可在空行后添加详细说明

### Submodule Updates

When updating submodules, use clear Chinese descriptions:

```bash
# Updating skills submodule
更新官方技能库子模块至最新版本

# Updating awesome-claude-skills
同步社区技能集合子模块
```

## Notes

- The `.skill` file format is a zip archive with `.skill` extension
- Skills in `claude-skills-hub/` are local development and not tracked by the main repository
- Refer to `Git-Submodule学习笔记.md` for detailed Git submodule documentation (in Chinese)
- Both submodules point to external repositories and should not be modified directly unless you have permissions to those repositories
