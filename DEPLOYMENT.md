# GitHub Stars Monitor - 部署指南

## 部署方式

### 方式 1：本地运行（推荐测试）

#### Windows

```powershell
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置 config.json
# 3. 运行脚本
python github-stars-monitor.py

# 4. 单次测试
python github-stars-monitor.py --once
```

#### macOS / Linux

```bash
# 1. 安装依赖
pip3 install -r requirements.txt

# 2. 配置 config.json
# 3. 运行脚本
python3 github-stars-monitor.py

# 4. 单次测试
python3 github-stars-monitor.py --once
```

---

### 方式 2：Cron 定时任务（Linux / macOS）

#### 编辑 crontab

```bash
crontab -e
```

#### 添加定时任务

**每小时检查一次：**

```bash
0 * * * * /usr/bin/python3 /path/to/github-stars-monitor.py >> /path/to/github_stars_monitor.log 2>&1
```

**每 30 分钟检查一次：**

```bash
*/30 * * * * /usr/bin/python3 /path/to/github-stars-monitor.py >> /path/to/github_stars_monitor.log 2>&1
```

**每天凌晨 3 点检查一次：**

```bash
0 3 * * * /usr/bin/python3 /path/to/github-stars-monitor.py >> /path/to/github_stars_monitor.log 2>&1
```

#### 保存并退出

保存文件，退出编辑器。

#### 验证 crontab

```bash
crontab -l
```

---

### 方式 3：Systemd 服务（Linux）

#### 创建服务文件

```bash
sudo nano /etc/systemd/system/github-stars-monitor.service
```

#### 添加以下内容：

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
StandardOutput=append:/path/to/github_stars_monitor.log
StandardError=append:/path/to/github_stars_monitor.log

[Install]
WantedBy=multi-user.target
```

#### 启动服务

```bash
# 重新加载 systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start github-stars-monitor

# 设置开机自启
sudo systemctl enable github-stars-monitor

# 查看服务状态
sudo systemctl status github-stars-monitor

# 查看日志
sudo journalctl -u github-stars-monitor -f
```

#### 停止服务

```bash
sudo systemctl stop github-stars-monitor
```

#### 重启服务

```bash
sudo systemctl restart github-stars-monitor
```

---

### 方式 4：Windows Task Scheduler

#### 创建任务

1. 打开 "任务计划程序"
2. 点击 "创建基本任务"
3. 填写任务名称：`GitHub Stars Monitor`
4. 触发器：
   - 选择 "每天"
   - 设置时间：例如 `09:00:00`
   - 重复间隔：1 小时
5. 操作：
   - 选择 "启动程序"
   - 程序：`python.exe`
   - 参数：`/path/to/github-stars-monitor.py`
   - 起始于：`/path/to/github-stars-monitor`

#### 配置运行账户

1. 右键任务 → 属性
2. 常规 → 勾选 "使用最高权限运行"
3. 高级 → 勾选 "如果任务失败，重新启动"

#### 测试任务

1. 右键任务 → 运行
2. 检查任务历史记录

---

### 方式 5：Docker 部署

#### 创建 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 安装 Python 依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 创建日志目录
RUN mkdir -p /app/logs

# 暴露端口（可选）
# EXPOSE 8080

# 运行脚本
CMD ["python", "github-stars-monitor.py"]
```

#### 构建 Docker 镜像

```bash
docker build -t github-stars-monitor:latest .
```

#### 运行 Docker 容器

```bash
# 运行容器
docker run -d \
  --name github-stars-monitor \
  -v /path/to/config.json:/app/config.json \
  -v /path/to/logs:/app/logs \
  github-stars-monitor:latest

# 查看日志
docker logs -f github-stars-monitor

# 停止容器
docker stop github-stars-monitor

# 删除容器
docker rm github-stars-monitor
```

#### 使用 Docker Compose

创建 `docker-compose.yml`：

```yaml
version: '3.8'

services:
  github-stars-monitor:
    build: .
    container_name: github-stars-monitor
    restart: always
    volumes:
      - ./config.json:/app/config.json
      - ./logs:/app/logs
    environment:
      - TZ=Asia/Shanghai
```

运行：

```bash
docker-compose up -d
```

---

### 方式 6：Python Gunicorn（Linux / macOS）

#### 安装 Gunicorn

```bash
pip install gunicorn
```

#### 创建启动脚本

```bash
# 创建 gunicorn 配置文件
cat > gunicorn_config.py << EOF
bind = "127.0.0.1:8000"
workers = 1
worker_class = "sync"
timeout = 3600
EOF

# 启动服务
gunicorn -c gunicorn_config.py github-stars-monitor:main
```

---

## 配置示例

### 完整配置文件（config.json）

```json
{
  "github_token": "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "/Users/admin/openclaw/workspace/openrelay",
      "threshold": 1000,
      "enabled": true,
      "notification": true
    },
    {
      "owner": "anthropics",
      "repo": "financial-services",
      "path": "/Users/admin/openclaw/workspace/financial-services",
      "threshold": 500,
      "enabled": true,
      "notification": true
    }
  ],
  "check_interval": 3600,
  "notification_method": "telegram",
  "telegram_token": "123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
  "telegram_chat_id": "123456789",
  "email_smtp": "smtp.gmail.com:587",
  "email_from": "your-email@gmail.com",
  "email_to": "your-email@gmail.com"
}
```

---

## 环境变量

### Linux / macOS

```bash
# 设置 GitHub Token
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 运行脚本
python3 github-stars-monitor.py
```

### Windows (PowerShell)

```powershell
# 设置 GitHub Token
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 运行脚本
python github-stars-monitor.py
```

---

## 监控和日志

### 查看日志

#### 日志文件

```bash
tail -f github_stars_monitor.log
```

#### Systemd 日志

```bash
sudo journalctl -u github-stars-monitor -f
```

#### Docker 日志

```bash
docker logs -f github-stars-monitor
```

### 日志轮转

#### Linux / macOS（logrotate）

创建 `/etc/logrotate.d/github-stars-monitor`：

```
/path/to/github_stars_monitor.log {
    daily
    rotate 7
    compress
    missingok
    notifempty
    create 0644 admin admin
}
```

---

## 故障排除

### 1. Cron 任务不执行

**检查：**
```bash
# 查看 cron 日志
tail -f /var/log/syslog | grep CRON

# 查看 cron 状态
sudo systemctl status cron
```

**解决：**
- 检查 cron 服务是否运行
- 检查路径是否正确
- 检查权限

### 2. Systemd 服务失败

**检查：**
```bash
# 查看服务状态
sudo systemctl status github-stars-monitor

# 查看详细日志
sudo journalctl -u github-stars-monitor -n 50
```

**解决：**
- 检查配置文件路径
- 检查 Python 路径
- 检查文件权限

### 3. Docker 容器无法启动

**检查：**
```bash
# 查看容器日志
docker logs github-stars-monitor

# 检查容器状态
docker ps -a
```

**解决：**
- 检查配置文件挂载路径
- 检查日志目录权限
- 检查网络连接

---

## 更新和升级

### 更新脚本

```bash
# 停止服务
sudo systemctl stop github-stars-monitor

# 备份旧版本
cp github-stars-monitor.py github-stars-monitor.py.backup

# 下载新版本
git pull origin main

# 重启服务
sudo systemctl start github-stars-monitor
```

### Docker 升级

```bash
# 停止容器
docker stop github-stars-monitor

# 删除旧容器
docker rm github-stars-monitor

# 重新构建镜像
docker build -t github-stars-monitor:latest .

# 启动新容器
docker run -d \
  --name github-stars-monitor \
  -v /path/to/config.json:/app/config.json \
  -v /path/to/logs:/app/logs \
  github-stars-monitor:latest
```

---

## 性能优化

### 1. 调整检查间隔

```json
{
  "check_interval": 1800  // 从 3600 秒改为 1800 秒（30 分钟）
}
```

### 2. 并发检查多个仓库

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
    }
  ]
}
```

### 3. 使用 GitHub Token

```bash
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

---

## 安全加固

### 1. 文件权限

```bash
# 配置文件权限（仅所有者可读）
chmod 600 config.json

# 日志文件权限
chmod 644 github_stars_monitor.log
```

### 2. 环境变量

```bash
# 创建 .env 文件
cat > .env << EOF
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
EOF

# 修改脚本读取环境变量
```

### 3. 防火墙配置

```bash
# 如果使用 Systemd，确保防火墙允许服务端口
sudo ufw allow 8000/tcp
```

---

## 备份和恢复

### 备份配置文件

```bash
# 备份配置
cp config.json config.json.backup

# 备份日志
tar -czf github-stars-monitor-backup-$(date +%Y%m%d).tar.gz github_stars_monitor.log
```

### 恢复配置

```bash
# 恢复配置文件
cp config.json.backup config.json

# 恢复日志
tar -xzf github-stars-monitor-backup-20260523.tar.gz
```

---

## 监控和告警

### 添加监控

#### Prometheus + Grafana

1. 安装 Prometheus
2. 配置抓取脚本
3. 添加 Grafana 仪表板

#### 自定义监控脚本

```bash
# 检查监控器状态
ps aux | grep github-stars-monitor

# 检查日志错误
grep "ERROR" github_stars_monitor.log
```

---

## 总结

### 推荐部署方式

| 场景 | 推荐方式 |
|------|---------|
| 测试 | 本地运行 |
| 个人使用 | Cron 定时任务 |
| 生产环境 | Systemd 服务 |
| Docker 环境 | Docker 部署 |
| 多实例 | Docker Compose |

### 部署检查清单

- [ ] 安装 Python 和依赖
- [ ] 配置 config.json
- [ ] 设置 GitHub Token
- [ ] 测试单次执行
- [ ] 配置定时任务
- [ ] 设置日志轮转
- [ ] 配置监控告警
- [ ] 设置备份策略
- [ ] 测试故障恢复
- [ ] 文档更新

---

*部署完成！*
