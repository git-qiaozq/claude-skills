# Claude Skills 学习中心

一个全面的 Claude Skills 学习和开发仓库，整合了官方 Anthropic 技能、社区贡献和自定义技能开发。

## 概述

本仓库服务于三个主要目的：
1. **参考集合** - 通过 git 子模块跟踪官方 Anthropic 技能
2. **社区展示** - 通过 git 子模块精选社区创建的技能
3. **开发工作区** - 在 `claude-skills-hub/` 中构建和测试自定义技能

## 特性

- 完整的官方 Anthropic 技能库（通过子模块同步）
- 精选的社区技能集合（通过子模块同步）
- 自定义技能的本地开发环境
- 技能创建和验证工具
- 用于 Java 开发的 Maven 项目转换器
- 中英文双语全面文档

## 仓库结构

```
claude-skills/
├── skills/                      # Anthropic 官方技能（子模块）
│   └── skills/                  # 17+ 官方技能
├── awesome-claude-skills/       # 社区技能集合（子模块）
├── claude-skills-hub/           # 本地开发工作区
│   ├── maven-converter/         # Java 到 Maven 转换器技能
│   └── skill-creator/           # 技能开发工具包
├── CLAUDE.md                    # Claude Code 仓库指导
├── AGENTS.md                    # 技能系统配置
└── Git-Submodule学习笔记.md    # Git 子模块学习笔记（中文）
```

## 快速开始

### 克隆仓库

```bash
# 克隆并包含所有子模块
git clone --recursive <your-repo-url>

# 或者在克隆后初始化子模块
git clone <your-repo-url>
cd claude-skills
git submodule update --init --recursive
```

### 更新子模块

```bash
# 更新所有子模块到最新版本
git submodule update --remote --recursive

# 更新特定子模块
cd skills  # 或 awesome-claude-skills
git pull origin master
cd ..
git add skills
git commit -m "更新技能子模块"
```

## 可用技能

### 官方技能（17+）

位于 `skills/skills/`：

- **algorithmic-art** - 使用 p5.js 创建生成艺术
- **brand-guidelines** - Anthropic 品牌样式
- **canvas-design** - 视觉艺术创作
- **doc-coauthoring** - 结构化文档工作流
- **docx** - Word 文档操作
- **frontend-design** - 生产级 Web 界面
- **internal-comms** - 内部沟通模板
- **mcp-builder** - MCP 服务器开发指南
- **pdf** - PDF 操作工具包
- **pptx** - PowerPoint 创建和编辑
- **skill-creator** - 技能开发指南
- **slack-gif-creator** - Slack 动画 GIF
- **theme-factory** - 工件样式主题
- **web-artifacts-builder** - 复杂 HTML 工件
- **webapp-testing** - 使用 Playwright 进行 Web 应用测试
- **xlsx** - 电子表格操作

### 自定义技能

位于 `claude-skills-hub/`：

#### Maven 转换器
自动将 Java 项目转换为标准 Maven 结构。

```bash
cd claude-skills-hub/maven-converter
python3 scripts/maven_converter.py <项目路径> [选项]
```

选项：
- `--dry-run` - 预览更改而不修改文件
- `--group-id <id>` - 设置 Maven groupId（默认：com.example）
- `--artifact-id <id>` - 设置 Maven artifactId（默认：目录名）
- `--version <ver>` - 设置项目版本（默认：1.0-SNAPSHOT）

#### 技能创建器
用于创建、验证和打包自定义技能的工具包。

```bash
cd claude-skills-hub/skill-creator

# 初始化新技能
python3 scripts/init_skill.py <技能名称> --path <输出目录>

# 验证技能
python3 scripts/quick_validate.py <技能文件夹路径>

# 打包技能
python3 scripts/package_skill.py <技能文件夹路径> [输出目录]
```

## 技能开发指南

### 技能结构

每个技能遵循以下标准结构：

```
skill-name/
├── SKILL.md              # 必需：YAML 前置元数据 + markdown 说明
│   ├── name:             # 必需字段
│   └── description:      # 必需字段（包含使用场景）
├── scripts/              # 可选：可执行代码（Python/Bash）
├── references/           # 可选：按需加载的文档
└── assets/               # 可选：模板、图片、字体
```

### 核心原则

1. **渐进式披露** - 三层加载系统：
   - 元数据（名称 + 描述）- 始终加载
   - SKILL.md 主体 - 技能触发时加载
   - 捆绑资源 - 按需加载

2. **保持简洁** - 假设 Claude 很聪明；只添加 Claude 不知道的内容

3. **使用脚本** - 自动化重复的确定性任务

4. **参考文件** - 将详细文档单独存储以便按需加载

5. **清晰描述** - 包含技能的功能和使用场景

### 开发工作流

1. 使用 skill-creator 初始化技能结构
2. 编写带有 YAML 前置元数据和说明的 SKILL.md
3. 添加自动化任务的脚本（可选）
4. 添加参考文档（可选）
5. 验证技能结构
6. 打包为 `.skill` 文件（带 .skill 扩展名的 zip）

## 文档

- **CLAUDE.md** - Claude Code 的全面仓库指导
- **AGENTS.md** - 技能系统配置和使用
- **Git-Submodule学习笔记.md** - 详细的 Git 子模块文档（中文）
- **skills/spec/agent-skills-spec.md** - 官方代理技能规范

## 在 Claude Code 中使用技能

技能通过 `AGENTS.md` 配置文件自动加载。使用技能：

```bash
# Claude Code 自动检测可用技能
# 只需请求与技能描述匹配的任务
```

技能通过以下方式调用：
```bash
openskills read <技能名称>
```

## 贡献

### 添加自定义技能

1. 在 `claude-skills-hub/` 中创建你的技能
2. 遵循标准技能结构
3. 使用 skill-creator 工具包进行验证
4. 使用 Claude Code 进行测试

### 更新子模块

1. 导航到子模块目录
2. 拉取最新更改
3. 在父仓库中提交子模块更新

```bash
cd skills
git pull origin master
cd ..
git add skills
git commit -m "更新技能子模块到最新版本"
```

## 资源

- [Anthropic Skills 仓库](https://github.com/anthropics/skills)
- [Awesome Claude Skills](https://github.com/BehiSecc/awesome-claude-skills)
- [Claude Code 文档](https://claude.com/claude-code)
- [代理技能规范](./skills/spec/agent-skills-spec.md)

## 许可证

本仓库遵循其各个组件的许可证：
- 官方技能：参见 `skills/` 子模块许可证
- 社区技能：参见 `awesome-claude-skills/` 子模块许可证
- 自定义技能：应用各个技能许可证

## 注意事项

- `.skill` 文件是带有 `.skill` 扩展名的 zip 归档
- `claude-skills-hub/` 用于本地开发（不被主仓库跟踪）
- 子模块是对外部仓库的只读引用
- 使用 `git submodule update --remote` 与上游更改同步
