# Truth Social 爬虫使用说明

## 简介

这是一个用于爬取特朗普 Truth Social 媒体网站最新资讯的 Python 爬虫。

## 文件位置

```
/root/.openclaw/workspace/scripts/truth_social_scraper.py
```

## 功能特性

- ✅ 获取指定用户的最新帖子（默认 @realDonaldTrump）
- ✅ 获取热门 Truth 内容
- ✅ 搜索特定关键词
- ✅ 支持 JSON 和 Markdown 格式导出
- ✅ 自动处理 HTML 内容清理

## 使用方法

### 1. 直接运行

```bash
cd /root/.openclaw/workspace
python3 scripts/truth_social_scraper.py
```

### 2. 作为模块导入使用

```python
from scripts.truth_social_scraper import TruthSocialScraper

# 创建爬虫实例
scraper = TruthSocialScraper()

# 获取特朗普的最新帖子
truths = scraper.get_user_truths(username="realDonaldTrump", limit=20)

# 保存为 JSON
scraper.save_to_json(truths, "output.json")

# 保存为 Markdown
scraper.save_to_markdown(truths, "output.md")
```

### 3. 搜索特定内容

```python
from scripts.truth_social_scraper import TruthSocialScraper

scraper = TruthSocialScraper()

# 搜索包含 "America" 的帖子
results = scraper.search_truths(query="America", limit=10)

# 打印结果
for item in results:
    print(f"时间: {item['created_at']}")
    print(f"内容: {item['content'][:100]}...")
    print(f"互动: 💬{item['replies_count']} 🔄{item['reblogs_count']} ❤️{item['favourites_count']}")
    print("-" * 50)
```

## API 说明

### TruthSocialScraper 类

#### `get_user_truths(username, limit)`
获取指定用户的 Truth 帖子

- **参数:**
  - `username` (str): 用户名，默认 "realDonaldTrump"
  - `limit` (int): 获取帖子数量，默认 20
- **返回:** List[Dict] 帖子列表

#### `search_truths(query, limit)`
搜索 Truth 内容

- **参数:**
  - `query` (str): 搜索关键词
  - `limit` (int): 返回结果数量，默认 20
- **返回:** List[Dict] 搜索结果列表

#### `get_trending(limit)`
获取热门 Truth

- **参数:**
  - `limit` (int): 返回结果数量，默认 20
- **返回:** List[Dict] 热门帖子列表

#### `save_to_json(truths, filename)`
保存数据到 JSON 文件

- **参数:**
  - `truths` (List[Dict]): 帖子数据
  - `filename` (str): 文件名，可选

#### `save_to_markdown(truths, filename)`
保存数据到 Markdown 文件

- **参数:**
  - `truths` (List[Dict]): 帖子数据
  - `filename` (str): 文件名，可选

## 数据结构

每条 Truth 包含以下字段:

```json
{
  "id": "帖子ID",
  "content": "帖子内容（已清理HTML）",
  "created_at": "创建时间",
  "replies_count": 回复数,
  "reblogs_count": 转发数,
  "favourites_count": 点赞数,
  "url": "帖子链接",
  "media_attachments": [
    {
      "type": "媒体类型",
      "url": "媒体链接",
      "preview_url": "预览图链接"
    }
  ]
}
```

## 注意事项

1. **API 限制**: Truth Social 可能有访问频率限制，建议适当控制请求频率
2. **认证要求**: 某些 API 可能需要登录认证，如果遇到 401 错误，可能需要添加认证头
3. **内容过滤**: 爬取的内容已自动清理 HTML 标签
4. **合法性**: 请遵守 Truth Social 的服务条款和相关法律法规

## 故障排除

### 无法获取数据

如果返回空列表或报错，可能原因：
- API 端点变更
- 需要登录认证
- IP 被限制

**解决方法:**
1. 检查网络连接
2. 尝试添加代理
3. 检查 Truth Social 网站是否有更新

### 中文显示乱码

数据已使用 UTF-8 编码保存，如果显示乱码，请确保使用支持 UTF-8 的编辑器打开。

## 更新记录

| 日期 | 版本 | 更新内容 |
|------|------|---------|
| 2026-03-04 | 1.0 | 初始版本，基础爬虫功能 |

## 参考

- Truth Social 网站: https://truthsocial.com
- Mastodon API 文档 (Truth Social 基于 Mastodon): https://docs.joinmastodon.org/api/
