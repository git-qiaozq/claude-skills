# CLAUDE.md

本文件为 Claude Code (claude.ai/code) 在此仓库中工作时提供指导。

## 仓库目的

这是一个 Claude Skills 学习和开发仓库，服务于：
- 官方 Anthropic 技能的参考集合（通过子模块）
- 社区技能的精选列表（通过子模块）
- 在 `claude-skills-hub/` 中开发自定义技能的工作区

## 仓库结构

### Git 子模块

本仓库使用 Git 子模块来跟踪外部技能仓库：

- **`skills/`** - Anthropic 官方技能仓库 (anthropics/skills)
- **`awesome-claude-skills/`** - 社区精选技能集合 (BehiSecc/awesome-claude-skills)

在新机器上克隆此仓库或更新后：

```bash
# 初始化并更新所有子模块
git submodule update --init --recursive

# 更新子模块到最新版本
git submodule update --remote
```

### 本地开发目录

- **`claude-skills-hub/`** - 自定义技能开发的本地工作区（不被 git 跟踪）
  - 包含正在开发或定制的技能
  - 每个技能应遵循标准技能结构

## 技能开发工作流

### 技能结构

每个技能遵循以下标准结构：

```
skill-name/
├── SKILL.md              # 必需：YAML 前置元数据 + markdown 说明
│   ├── name:             # 前置元数据中的必需字段
│   └── description:      # 前置元数据中的必需字段
├── scripts/              # 可选：可执行代码（Python/Bash）
├── references/           # 可选：按需加载的文档
└── assets/               # 可选：输出用的模板、图片、字体
```

### 常用开发命令

#### 初始化新技能

```bash
cd claude-skills-hub/skill-creator
python3 scripts/init_skill.py <技能名称> --path <输出目录>
```

这将创建一个带有模板结构的新技能目录。

#### 验证技能

```bash
cd claude-skills-hub/skill-creator
python3 scripts/quick_validate.py <技能文件夹路径>
```

检查正确的 YAML 前置元数据、必需字段和结构。

#### 打包技能

```bash
cd claude-skills-hub/skill-creator
python3 scripts/package_skill.py <技能文件夹路径> [输出目录]
```

验证并将技能打包为 `.skill` 文件（带 .skill 扩展名的 zip 格式）。

#### Maven 转换器技能

```bash
cd claude-skills-hub/maven-converter
python3 scripts/maven_converter.py <java项目路径> [选项]
```

常用选项：
- `--dry-run` - 预览更改而不修改文件
- `--group-id <id>` - 设置 Maven groupId（默认：com.example）
- `--artifact-id <id>` - 设置 Maven artifactId（默认：目录名）
- `--version <ver>` - 设置项目版本（默认：1.0-SNAPSHOT）

## 技能设计原则

### 渐进式披露

技能使用三层加载系统来高效管理上下文：

1. **元数据（名称 + 描述）** - 始终加载（约100字）
2. **SKILL.md 主体** - 技能触发时加载（少于5k字，保持在500行以下）
3. **捆绑资源** - Claude 按需加载

### 关键指南

- **保持 SKILL.md 简洁**：假设 Claude 很聪明；只添加 Claude 不知道的内容
- **使用脚本处理重复任务**：Python/Bash 脚本用于确定性操作
- **文档使用参考文件**：将详细文档存储在 `references/` 中以便按需加载
- **输出文件使用资源**：将模板、图片、字体存储在 `assets/` 中用于生成输出
- **避免重复**：信息应存在于 SKILL.md 或参考文件中，而不是两者都有

### Description 字段最佳实践

YAML 前置元数据中的 `description` 是主要触发机制：
- 包含技能的功能和使用场景
- 所有"何时使用"的信息都放在这里（不在主体中）
- 具体说明触发上下文和用例

示例：
```yaml
description: 将 Java 项目转换为标准 Maven 结构，重组目录，转换包名（test→example），并生成 pom.xml。当用户需要将非 Maven Java 项目转换为 Maven，将现有项目重构为 Maven 标准结构，或请求 Maven 项目设置/转换时使用。
```

## 使用子模块

### 查看子模块状态

```bash
git submodule status
```

### 更新特定子模块

```bash
cd skills  # 或 awesome-claude-skills
git pull origin master
cd ..
git add skills
git commit -m "更新技能子模块到最新版本"
```

### 更新所有子模块

```bash
git submodule update --remote --recursive
git add .
git commit -m "更新所有子模块到最新版本"
```

## 文件组织

- **根目录**：配置文件、此 CLAUDE.md、git 子模块配置
- **`skills/`**：官方 Anthropic 技能（子模块，只读参考）
- **`awesome-claude-skills/`**：社区技能集合（子模块，只读参考）
- **`claude-skills-hub/`**：活跃开发工作区
  - 正在开发的自定义技能
  - 现有技能的修改/增强版本
  - 技能开发工具包（skill-creator）

## Git 提交信息规范

**重要**：此仓库中的所有 git commit 信息必须使用简体中文编写。

### 提交信息格式

所有提交使用以下格式：

```
[类型] 简短描述

详细说明（可选）
```

### 提交类型

- **添加** - 新增功能、文件或特性
- **修复** - 修复bug或问题
- **重构** - 代码结构调整，不改变功能
- **优化** - 性能改进或代码优化
- **更新** - 更新依赖、文档、配置等
- **删除** - 移除代码、文件或功能
- **测试** - 添加或修改测试
- **文档** - 仅文档更改

### 示例

```bash
# 好的示例
添加用户认证模块和JWT令牌支持
修复登录页面验证逻辑的空指针异常
重构数据库查询逻辑以提高性能
更新README文档和API使用说明
优化技能加载速度和内存使用

# 避免的示例
Add user authentication  # 不要使用英文
fix bug  # 描述不清晰
update  # 太模糊
```

### 提交信息规则

1. **使用中文** - 所有 commit message 必须用简体中文编写
2. **动词开头** - 使用祈使句形式（添加、修复、更新等）
3. **描述清晰** - 简洁但准确地描述改动内容
4. **避免混用** - 不要混用中英文（除非是专有名词如 API、GitHub、Maven等）
5. **首行简短** - 第一行不超过50个字符
6. **详细说明** - 复杂改动可在空行后添加详细说明

### 子模块更新

更新子模块时，使用清晰的中文描述：

```bash
# 更新技能子模块
更新官方技能库子模块至最新版本

# 更新 awesome-claude-skills
同步社区技能集合子模块
```

## 注意事项

- `.skill` 文件格式是带有 `.skill` 扩展名的 zip 归档
- `claude-skills-hub/` 中的技能用于本地开发，不被主仓库跟踪
- 详细的 Git 子模块文档请参考 `Git-Submodule学习笔记.md`（中文）
- 两个子模块都指向外部仓库，除非你有这些仓库的权限，否则不应直接修改
