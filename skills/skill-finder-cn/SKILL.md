---
name: skill-finder-cn
description: Skill 查找器 | Skill Finder. 帮助发现和安装 ClawHub Skills。自动搜索 ClawHub 技能库，找到适合当前任务的最佳技能，支持一键安装。触发词：找技能、搜索技能、安装技能、skill finder。
---

# Skill Finder CN

自动在 ClawHub 技能库中搜索和安装技能。

## 使用方式

用户说以下内容时触发：
- "找技能"、"搜索技能"、"安装技能"
- "有没有能做 X 的技能"
- "搜索 ClawHub"
- "skill finder"

## 使用命令

```bash
clawhub search "<关键词>"
```

## 示例

### 搜索技能
```bash
clawhub search "股票 分析"
```

### 查看技能详情
```bash
clawhub inspect <skill-name>
```

### 安装技能
```bash
clawhub install <skill-name>
```

### 搜索多个相关技能
```bash
clawhub search "web scraping"
clawhub search "data analysis"
clawhub search "image processing"
```

## 搜索策略

1. 先理解用户想要什么功能
2. 用中文关键词搜索一次
3. 用英文关键词搜索一次（扩大范围）
4. 列出最相关的 3-5 个选项
5. 询问用户想安装哪个
6. 得到确认后执行安装

## 注意事项

- 安装前先确认技能与当前任务相关
- 检查技能评分（越高越好）
- 注意查看技能描述中的功能说明
- 可疑技能（VirusTotal 标记）先告知用户风险
