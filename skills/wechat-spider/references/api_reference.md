# 微信公众号爬虫 API 接口文档

## 接口概述

微信公众号爬虫主要依赖以下 API 接口获取数据。

## 文章列表接口

### 接口地址
```
GET https://mp.weixin.qq.com/mp/profile_ext
```

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| action | string | 是 | 固定值 `getmsg` |
| __biz | string | 是 | 公众号唯一标识 |
| f | string | 是 | 固定值 `json` |
| offset | int | 是 | 偏移量，从0开始 |
| count | int | 是 | 每页数量，建议10 |
| is_ok | int | 是 | 固定值 `1` |
| scene | int | 是 | 固定值 `124` |
| appmsg_token | string | 是 | 从抓包获取的token |
| pass_ticket | string | 否 | 票据（可选） |
| wxtoken | string | 否 | 微信token（可选） |

### 响应示例

```json
{
  "ret": 0,
  "errmsg": "ok",
  "msg_count": 10,
  "can_msg_continue": 1,
  "general_msg_list": "{\"list\":[...]}",
  "next_offset": 10
}
```

### 文章数据结构

```json
{
  "comm_msg_info": {
    "id": 1000000001,
    "type": 49,
    "datetime": 1704067200,
    "fakeid": "..."
  },
  "app_msg_ext_info": {
    "title": "文章标题",
    "digest": "文章摘要",
    "author": "作者",
    "content_url": "文章链接",
    "source_url": "原文链接",
    "cover": "封面图URL",
    "multi_app_msg_item_list": [
      // 多图文时的子文章
    ]
  }
}
```

## 阅读点赞接口

### 接口地址
```
POST https://mp.weixin.qq.com/mp/getappmsgext
```

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| __biz | string | 是 | 公众号biz |
| mid | string | 是 | 消息ID |
| idx | string | 是 | 消息序号 |
| sn | string | 是 | 消息签名 |
| appmsg_token | string | 是 | token |
| x5 | string | 否 | 固定值 `0` |

### 响应示例

```json
{
  "appmsgstat": {
    "read_num": 10000,
    "like_num": 500,
    "old_like_num": 300,
    "is_login": true
  }
}
```

## 评论接口

### 接口地址
```
GET https://mp.weixin.qq.com/mp/appmsg_comment
```

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| action | string | 是 | 固定值 `getcomment` |
| __biz | string | 是 | 公众号biz |
| mid | string | 是 | 消息ID |
| idx | string | 是 | 消息序号 |
| sn | string | 是 | 消息签名 |
| offset | int | 否 | 评论偏移量 |
| limit | int | 否 | 每页评论数 |
| appmsg_token | string | 是 | token |

### 响应示例

```json
{
  "base_resp": {
    "ret": 0,
    "errmsg": "ok"
  },
  "comment": [
    {
      "nick_name": "评论者昵称",
      "content": "评论内容",
      "like_num": 10,
      "create_time": "2024-01-01 12:00:00",
      "reply": {
        "content": "作者回复"
      }
    }
  ]
}
```

## 文章详情接口

### 接口地址
```
GET https://mp.weixin.qq.com/s
```

### 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| __biz | string | 是 | 公众号biz |
| mid | string | 是 | 消息ID |
| idx | string | 是 | 消息序号 |
| sn | string | 是 | 消息签名 |
| chksm | string | 否 | 校验码 |

### 响应内容

返回文章 HTML 页面，需要解析 DOM 提取：

- 标题: `#activity_name` 或 `.rich_media_title`
- 作者: `#js_name` 或 `.profile_nickname`
- 发布时间: `#publish_time`
- 内容: `#js_content`

## 错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| -1 | 系统繁忙 |
| -2 | token 过期或无效 |
| -3 | 参数错误 |
| -6 | 需要登录 |
| -8 | 请求过于频繁 |
| 200003 | 文章不存在或已删除 |

## 注意事项

1. **Token 有效期**: 约 2 小时，过期后需要重新获取
2. **请求频率**: 建议间隔 3-5 秒，过快会被限制
3. **IP 限制**: 频繁请求可能导致 IP 被临时封禁
4. **Cookie 要求**: 部分接口需要有效的微信登录 Cookie
