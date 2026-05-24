# GitHub Stars Monitor

自动监控 GitHub 仓库星标数，当星标数超过阈值时自动执行 git pull 更新。

## 功能特性

- ✅ 定时检查 GitHub 仓库星标数
- ✅ 星标数 > 1000 时自动执行 git pull
- ✅ 支持多仓库监控
- ✅ 发送通知（Telegram / 邮件 / 日志）
- ✅ 配置化管理
- ✅ 异常处理和日志记录
- ✅ 支持 GitHub Token（避免 API 限流）
- ✅ 持续运行模式（守护进程）
- ✅ 单次执行模式

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置文件

编辑 `config.json`：

```json
{
  "github_token": "your_github_token_here",
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "/path/to/openrelay",
      "threshold": 1000,
      "enabled": true,
      "notification": true
    }
  ],
  "check_interval": 3600,
  "notification_method": "log",
  "telegram_token": "your_telegram_token",
  "telegram_chat_id": "your_telegram_chat_id"
}
```

### 3. 配置 GitHub Token

获取 GitHub Token：https://github.com/settings/tokens

生成 Token 时需要以下权限：
- `public_repo` - 读取公开仓库信息

### 4. 配置 Telegram 通知（可选）

获取 Telegram Bot Token：https://t.me/BotFather

获取 Chat ID：https://t.me/userinfobot

### 5. 运行脚本

#### 单次执行模式（推荐测试）

```bash
python github-stars-monitor.py --once
```

#### 持续运行模式（守护进程）

```bash
python github-stars-monitor.py
```

## 配置说明

### github_token
GitHub Personal Access Token，用于避免 API 限流。

**建议：** 每天最多 5000 次请求，足够使用。

### repos
监控的仓库列表，每个仓库包含以下字段：

| 字段 | 类型 | 说明 |
|------|------|------|
| owner | string | 仓库所有者 |
| repo | string | 仓库名称 |
| path | string | 仓库本地路径 |
| threshold | number | 星标数阈值（默认 1000） |
| enabled | boolean | 是否启用（默认 true） |
| notification | boolean | 是否发送通知（默认 true） |

### check_interval
检查间隔（秒），默认 3600（1 小时）。

### notification_method
通知方式：`log` / `telegram` / `email`

### telegram_token & telegram_chat_id
Telegram Bot Token 和 Chat ID，用于发送 Telegram 通知。

### email_smtp & email_from & email_to
SMTP 配置，用于发送邮件通知。

## 使用示例

### 示例 1：监控单个仓库

```json
{
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "/Users/admin/openclaw/workspace/openrelay",
      "threshold": 1000,
      "enabled": true,
      "notification": true
    }
  ]
}
```

### 示例 2：监控多个仓库

```json
{
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "/path/to/openrelay",
      "threshold": 1000,
      "enabled": true
    },
    {
      "owner": "anthropics",
      "repo": "financial-services",
      "path": "/path/to/financial-services",
      "threshold": 500,
      "enabled": true
    },
    {
      "owner": "openclaw",
      "repo": "openclaw",
      "path": "/path/to/openclaw",
      "threshold": 1000,
      "enabled": false
    }
  ]
}
```

### 示例 3：使用 GitHub Token

```bash
# 设置环境变量
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 运行脚本
python github-stars-monitor.py
```

### 示例 4：使用 Cron 定时任务

**Linux / macOS：**

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每小时检查一次）
0 * * * * /usr/bin/python3 /path/to/github-stars-monitor.py >> /path/to/github_stars_monitor.log 2>&1
```

**Windows：**

使用 Task Scheduler 创建定时任务。

## 工作流程

```
┌─────────────────┐
│  定时触发检查    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  调用 GitHub API │
│  获取星标数      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  判断星标数      │
│  > 阈值？        │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
   否         是
    │         │
    │         ▼
    │  ┌──────────────┐
    │  │ 执行 git pull │
    │  └──────┬───────┘
    │         │
    │         ▼
    │  ┌──────────────┐
    │  │ 发送通知      │
    │  └──────────────┘
    │
    ▼
┌─────────────────┐
│  等待下次检查    │
└─────────────────┘
```

## 日志示例

```
2026-05-23 09:00:00 - INFO - GitHub Stars Monitor 启动
2026-05-23 09:00:00 - INFO - 检查间隔：3600 秒
2026-05-23 09:00:00 - INFO - 开始检查仓库：hrudu-dev/openrelay，阈值：1000
2026-05-23 09:00:01 - INFO - 仓库 hrudu-dev/openrelay 星标数：1234
2026-05-23 09:00:01 - WARNING - ⚠️ 仓库 hrudu-dev/openrelay 星标数 1234 超过阈值 1000，触发更新！
2026-05-23 09:00:01 - INFO - 开始执行 git pull，路径：/path/to/openrelay
2026-05-23 09:00:05 - INFO - ✅ git pull 执行成功：Already up to date.
2026-05-23 09:00:05 - INFO - 检查完成，共 1 个仓库触发更新
```

## 高级用法

### 1. 集成到 OpenClaw

在 OpenClaw 中添加一个定时任务：

```python
# 创建定时任务
cron.add(
    name="github-stars-monitor",
    schedule={"kind": "every", "everyMs": 3600000},
    payload={
        "kind": "agentTurn",
        "message": "运行 GitHub Stars Monitor",
        "timeoutSeconds": 60
    }
)
```

### 2. 集成到 Systemd（Linux）

创建服务文件 `/etc/systemd/system/github-stars-monitor.service`：

```ini
[Unit]
Description=GitHub Stars Monitor
After=network.target

[Service]
Type=simple
User=admin
WorkingDirectory=/path/to/github-stars-monitor
ExecStart=/usr/bin/python3 /path/to/github-stars-monitor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable github-stars-monitor
sudo systemctl start github-stars-monitor
```

### 3. 集成到 Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "github-stars-monitor.py"]
```

运行容器：

```bash
docker build -t github-stars-monitor .
docker run -d \
  --name github-stars-monitor \
  -v /path/to/config.json:/app/config.json \
  -v /path/to/logs:/app/logs \
  github-stars-monitor
```

## 故障排除

### 1. GitHub API 限流

**错误信息：**
```
GitHub API 请求次数超限，请稍后重试或配置 GitHub Token
```

**解决方案：**
- 配置 GitHub Token
- 增加检查间隔

### 2. 仓库路径不存在

**错误信息：**
```
仓库路径不存在：/path/to/openrelay
```

**解决方案：**
- 检查 `config.json` 中的 `path` 字段
- 确保路径正确

### 3. git pull 失败

**错误信息：**
```
❌ git pull 执行失败
```

**解决方案：**
- 检查仓库是否有更新
- 检查网络连接
- 检查 git 配置

## 安全建议

1. **不要在代码中硬编码 Token**
   - 使用环境变量或配置文件
   - 配置文件不要提交到 Git

2. **限制 GitHub Token 权限**
   - 只授予必要权限
   - 使用 Token 而非密码

3. **定期更换 Token**
   - 每月更换一次
   - 如果泄露立即撤销

4. **日志文件权限**
   - 限制日志文件访问权限
   - 定期清理旧日志

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！

## 作者

Administrator

## 链接

- GitHub：https://github.com/yourusername/github-stars-monitor
- Issues：https://github.com/yourusername/github-stars-monitor/issues
