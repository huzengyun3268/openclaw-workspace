---
name: notebooklm-skill
description: 与 Google NotebookLM 交互，查询用户上传的文档知识库，获取基于 Gemini 的精准回答。触发词：NotebookLM、查询我的笔记本、问知识库。
---

# NotebookLM Research Assistant Skill

与 Google NotebookLM 交互，查询文档知识库。

## 触发条件

用户：
- 提到 NotebookLM
- 分享 NotebookLM URL (https://notebooklm.google.com/notebook/...)
- 想查询笔记本/文档
- 说"问我的 NotebookLM"、"查我的文档"

## 使用方式

需要 Python 环境和相关脚本。

### 查询笔记本
```bash
python scripts/run.py ask_question.py --question "<问题>" --notebook-url "<URL>"
```

### 添加笔记本
```bash
python scripts/run.py notebook_manager.py add --url "<URL>" --name "<名称>" --description "<描述>" --topics "<主题>"
```

### 列出已添加的笔记本
```bash
python scripts/run.py notebook_manager.py list
```

## 注意事项

- 需要 Google 账号和 NotebookLM 笔记本
- 首次使用需要配置 Google API（如需要）
- 笔记本必须是用户自己创建的
