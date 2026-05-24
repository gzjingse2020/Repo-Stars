# GitHub Stars Monitor - 安装指南

## 系统要求

### 最低要求
- **Python:** 3.8+
- **操作系统:** Windows 10+, macOS 10.14+, Linux (Ubuntu 18.04+, Debian 10+)
- **磁盘空间:** 100 MB
- **内存:** 50 MB

### 推荐配置
- **Python:** 3.11+（推荐）
- **操作系统:** Windows 11, macOS 12+, Linux (Ubuntu 22.04+)
- **磁盘空间:** 500 MB
- **内存:** 512 MB+

---

## 安装步骤

### 1. 下载项目

```bash
# 克隆项目
git clone https://github.com/yourusername/github-stars-monitor.git
cd github-stars-monitor

# 或下载 ZIP
wget https://github.com/yourusername/github-stars-monitor/archive/refs/heads/main.zip
unzip main.zip
cd github-stars-monitor-main
```

### 2. 安装 Python（如果未安装）

#### Windows

1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.11.x 安装包
3. 运行安装程序
4. **重要：** 勾选 "Add Python to PATH"
5. 点击 "Install Now"

#### macOS

```bash
# 使用 Homebrew 安装
brew install python@3.11

# 或下载安装包
# https://www.python.org/downloads/macos/
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# CentOS/RHEL
sudo yum install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip
```

### 3. 验证 Python 安装

```bash
python --version
# 或
python3 --version
```

**预期输出：**
```
Python 3.11.0
```

### 4. 安装依赖

```bash
# 创建虚拟环境（推荐）
python3 -m venv venv

# 激活虚拟环境

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

**依赖列表：**
```
requests>=2.31.0
```

### 5. 验证安装

```bash
# 运行测试脚本
python github-stars-monitor.py --once
```

**预期输出：**
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

---

## 配置指南

### 1. 配置文件

创建 `config.json`：

```json
{
  "github_token": "",
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
  "telegram_token": "",
  "telegram_chat_id": "",
  "email_smtp": "",
  "email_from": "",
  "email_to": ""
}
```

### 2. GitHub Token

获取 GitHub Token：https://github.com/settings/tokens

**生成 Token 时需要：**
- 勾选 `public_repo`（读取公开仓库信息）
- 过期时间：推荐 90 天
- 权限范围：只授予必要权限

### 3. Telegram 通知（可选）

#### 获取 Bot Token

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot`
3. 按提示创建机器人
4. 复制 Token

#### 获取 Chat ID

1. 在 Telegram 中搜索 `@userinfobot`
2. 发送任意消息
3. 复制返回的 Chat ID

### 4. 邮件通知（可选）

#### 配置 SMTP

```json
{
  "email_smtp": "smtp.gmail.com:587",
  "email_from": "your-email@gmail.com",
  "email_to": "your-email@gmail.com"
}
```

**Gmail 示例：**
```json
{
  "email_smtp": "smtp.gmail.com:587",
  "email_from": "your-email@gmail.com",
  "email_to": "your-email@gmail.com"
}
```

**QQ 邮箱示例：**
```json
{
  "email_smtp": "smtp.qq.com:587",
  "email_from": "123456789@qq.com",
  "email_to": "your-email@example.com"
}
```

---

## 快速开始

### Windows

```powershell
# 1. 进入目录
cd C:\Users\Administrator\.openclaw\workspace\github-stars-monitor

# 2. 配置环境变量
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 3. 运行脚本
python github-stars-monitor.py

# 4. 单次测试
python github-stars-monitor.py --once
```

### macOS / Linux

```bash
# 1. 进入目录
cd /Users/admin/openclaw/workspace/github-stars-monitor

# 2. 配置环境变量
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 3. 运行脚本
python3 github-stars-monitor.py

# 4. 单次测试
python3 github-stars-monitor.py --once
```

---

## 测试安装

### 测试 1：检查单个仓库

```json
{
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "/path/to/openrelay",
      "threshold": 1000,
      "enabled": true,
      "notification": false
    }
  ]
}
```

### 测试 2：检查多个仓库

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

### 测试 3：禁用所有仓库

```json
{
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "/path/to/openrelay",
      "threshold": 1000,
      "enabled": false
    }
  ]
}
```

---

## 常见安装问题

### 1. Python 版本过低

**错误信息：**
```
SyntaxError: invalid syntax
```

**解决方案：**

升级 Python 到 3.8+：

```bash
# macOS
brew upgrade python@3.11

# Linux
sudo apt install python3.11
```

### 2. 权限错误

**错误信息：**
```
Permission denied: config.json
```

**解决方案：**

```bash
# macOS / Linux
chmod 600 config.json

# Windows
icacls config.json /grant:r "%USERNAME%":F
```

### 3. 依赖安装失败

**错误信息：**
```
ERROR: Could not find a version that satisfies the requirement requests
```

**解决方案：**

```bash
# 升级 pip
pip install --upgrade pip

# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 4. GitHub API 限流

**错误信息：**
```
GitHub API 请求次数超限，请稍后重试或配置 GitHub Token
```

**解决方案：**

配置 GitHub Token：

```bash
# 环境变量
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# 或在 config.json 中配置
```

---

## 下一步

安装完成后，请参考：

1. **DEPLOYMENT.md** - 部署指南（Linux / macOS）
2. **DEPLOYMENT_WINDOWS.md** - 部署指南（Windows）
3. **README.md** - 完整使用文档

---

## 卸载

### Windows

1. 停止并删除 Task Scheduler 任务
2. 删除项目目录
3. 删除环境变量

### macOS / Linux

```bash
# 停止 Cron 任务
crontab -e  # 删除相关行

# 删除项目目录
rm -rf /path/to/github-stars-monitor

# 删除虚拟环境
rm -rf venv
```

---

## 支持

遇到问题？

1. 查看日志文件：`github_stars_monitor.log`
2. 查看 Issues：https://github.com/yourusername/github-stars-monitor/issues
3. 联系：your-email@example.com

---

*安装完成！*
