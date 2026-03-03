---
name: wechat-spider
description: 微信公众号文章爬取工具。用于指定微信公众号，爬取公众号的文章列表、文章内容、阅读量、点赞数、评论等数据。支持批量采集历史文章和自动化监控新文章。使用场景包括：学术研究、舆情监测、内容分析、数据备份等。当用户需要爬取微信公众号文章、获取公众号历史文章、采集文章互动数据（阅读/点赞/评论）时触发此Skill。
---

# 微信公众号文章爬取工具

## 概述

本Skill提供微信公众号文章爬取的完整解决方案，基于Python实现，支持以下功能：

- 获取公众号主页链接
- 爬取公众号历史文章列表
- 下载文章内容（HTML格式）
- 获取文章互动数据（阅读量、点赞数、评论）
- 支持批量采集和自动化监控

## 技术原理

微信公众号文章爬取主要依赖以下技术方案：

1. **抓包方案**：使用Fiddler/Charles等抓包工具获取微信客户端请求中的token
2. **逆向方案**：通过分析微信客户端API接口，模拟请求获取数据
3. **自动化方案**：使用Playwright/Selenium模拟浏览器操作

## 前置要求

### 必需环境

- Python >= 3.9
- MySQL（数据存储）
- Redis（任务队列，可选）
- 微信PC客户端
- Fiddler/Charles抓包工具

### 安装依赖

```bash
pip install requests playwright beautifulsoup4 pandas openpyxl lxml
playwright install chromium
```

## 使用方法

### 方式一：快速爬取（推荐入门）

使用 `scripts/quick_spider.py` 脚本进行快速爬取：

```bash
python scripts/quick_spider.py --biz <公众号biz> --pages 10
```

参数说明：
- `--biz`: 公众号的biz标识（从公众号文章链接中获取）
- `--pages`: 要爬取的页数（每页约10-15篇文章）
- `--output`: 输出目录（默认：`./wechat_data`）

### 方式二：完整采集（推荐生产环境）

使用 `scripts/full_spider.py` 进行完整采集：

```bash
python scripts/full_spider.py --config config.yaml
```

配置示例见 `references/config_example.yaml`

### 方式三：自动化监控

使用 `scripts/monitor.py` 实现每日自动监控新文章：

```bash
python scripts/monitor.py --accounts accounts.txt --interval 3600
```

## 获取公众号biz的方法

1. 在微信PC端打开任意一篇该公众号的文章
2. 点击右上角"复制链接"
3. 链接格式：`https://mp.weixin.qq.com/s?__biz=MzIxNzg1ODQ0MQ==&mid=...`
4. 提取 `__biz=` 后面的值（如 `MzIxNzg1ODQ0MQ==`）

## 获取Token的方法

### 使用Fiddler抓包

1. 安装并启动Fiddler
2. 配置系统代理或浏览器代理指向Fiddler（默认端口8888）
3. 在微信PC端打开公众号历史消息页面
4. 在Fiddler中查找 `mp.weixin.qq.com` 的请求
5. 找到 `profile_ext` 或 `appmsgpublish` 接口，复制完整URL

### Token有效期

- 获取的token通常有效期为2小时左右
- 过期后需要重新抓包获取

## 数据输出格式

### 文章列表（article_list.xlsx）

| 字段 | 说明 |
|------|------|
| title | 文章标题 |
| link | 文章链接 |
| publish_time | 发布时间 |
| author | 作者 |
| digest | 摘要 |
| cover_url | 封面图链接 |

### 文章详情（article_detail.xlsx）

| 字段 | 说明 |
|------|------|
| title | 文章标题 |
| content | 文章内容（HTML） |
| read_count | 阅读量 |
| like_count | 点赞数 |
| comment_count | 评论数 |
| comments | 评论内容（JSON） |

## 注意事项

1. **合规使用**：本工具仅供学术研究和个人学习使用，请勿用于商业用途
2. **反爬策略**：微信有反爬机制，建议：
   - 控制请求频率（建议间隔3-5秒）
   - 使用代理IP池轮换
   - 避免短时间内大量请求
3. **数据存储**：建议将数据存储在本地，不要公开传播
4. **法律风险**：爬取数据需遵守《网络安全法》和相关法规

## 常见问题

**Q: 为什么获取不到数据？**
A: 检查token是否过期，或请求频率是否过高被限制。

**Q: 如何获取评论数据？**
A: 评论数据需要额外的token，使用功能4（文章详情）可以获取。

**Q: 支持批量采集多个公众号吗？**
A: 支持，在配置文件中添加多个biz即可。

## 参考项目

本Skill参考了以下开源项目：

- [Access_wechat_article](https://github.com/yeximm/Access_wechat_article) - 微信文章爬虫，支持阅读点赞数据
- [wechat-spider](https://github.com/striver-ing/wechat-spider) - 开源微信爬虫，支持自动化监控
- [weixin_crawler](https://github.com/wonderfulsuccess/weixin_crawler) - 稳定工作4年的微信公众号爬虫

## 高级功能

详细的高级功能说明请参考：

- [抓包配置指南](references/capture_guide.md)
- [配置文件说明](references/config_example.yaml)
- [API接口文档](references/api_reference.md)
