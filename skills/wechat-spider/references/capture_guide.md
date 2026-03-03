# 抓包配置指南

## 使用 Fiddler 抓包获取 Token

### 1. 安装 Fiddler

- **Windows**: 下载 [Fiddler Classic](https://www.telerik.com/fiddler/fiddler-classic) 免费版
- **Mac**: 使用 [Charles Proxy](https://www.charlesproxy.com/) 或 Fiddler Everywhere

### 2. 配置 Fiddler

#### Windows 配置

1. 打开 Fiddler，进入 `Tools` -> `Options`
2. 在 `HTTPS` 标签页：
   - 勾选 `Capture HTTPS CONNECTs`
   - 勾选 `Decrypt HTTPS traffic`
   - 点击 `Actions` -> `Trust Root Certificate` 安装证书
3. 在 `Connections` 标签页：
   - 勾选 `Allow remote computers to connect`
   - 记住端口号（默认 8888）

#### 系统代理配置

**Windows:**
```
设置 -> 网络和 Internet -> 代理 -> 手动设置代理
地址: 127.0.0.1
端口: 8888
```

**Mac:**
```
系统偏好设置 -> 网络 -> 高级 -> 代理
勾选 "安全网页代理(HTTPS)"
地址: 127.0.0.1
端口: 8888
```

### 3. 微信抓包步骤

1. **启动 Fiddler**，确保已经开始捕获流量
2. **打开微信 PC 客户端**
3. **打开任意一篇目标公众号的文章**
4. **点击文章右上角的"查看公众号"**，进入公众号主页
5. **点击"全部消息"**，查看历史文章列表
6. **在 Fiddler 中查找请求**：
   - 找到主机为 `mp.weixin.qq.com` 的请求
   - URL 包含 `profile_ext` 或 `appmsgpublish`
   - 请求方法为 GET

### 4. 提取 Token

在 Fiddler 中选中目标请求：

1. 点击 `Inspectors` 标签
2. 选择 `WebForms` 或 `Raw`
3. 找到 `appmsg_token` 参数的值
4. 复制完整的 URL 或仅复制 token 值

Token 格式示例：
```
appmsg_token=your_token_here
```

### 5. 提取 Cookie（可选）

同样在 Fiddler 中：
1. 查看请求头中的 `Cookie` 字段
2. 复制完整的 cookie 字符串

## 使用 mitmproxy 抓包（高级）

### 安装

```bash
pip install mitmproxy
```

### 启动代理

```bash
mitmweb --web-host 0.0.0.0 --web-port 8081
```

### 安装证书

访问 `http://mitm.it` 下载并安装证书：

- **iPhone**: 安装后需要在 `设置 -> 通用 -> 关于本机 -> 证书信任设置` 中开启信任
- **Android**: 安装到系统证书（可能需要 root）
- **Windows/Mac**: 双击安装到受信任的根证书颁发机构

### 手机抓包

1. 手机和电脑连接同一 WiFi
2. 手机 WiFi 设置中配置代理：
   - 服务器: 电脑IP地址
   - 端口: 8080
3. 在手机上打开微信公众号文章
4. 在 mitmweb 界面查看捕获的请求

## 常见问题

### Q: 抓不到 HTTPS 请求？

A: 确保证书已正确安装并信任。Windows 需要安装到"本地计算机"的"受信任的根证书颁发机构"。

### Q: Token 很快过期？

A: Token 有效期约 2 小时，过期后需要重新抓包获取。建议配合自动化脚本使用。

### Q: 微信提示网络异常？

A: 可能是代理配置问题，检查 Fiddler 是否正常运行，或尝试重启微信。

### Q: 抓包时微信加载很慢？

A: 这是正常现象，代理会增加请求延迟。监控时建议设置合理的请求间隔。

## 安全提示

1. **不要在公共网络使用抓包工具**，避免敏感信息泄露
2. **及时删除抓包记录**，token 和 cookie 包含敏感信息
3. **仅用于个人学习和研究**，遵守相关法律法规
4. **不要分享 token 和 cookie**，这相当于分享你的微信登录状态
