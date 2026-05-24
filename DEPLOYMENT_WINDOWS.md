# GitHub Stars Monitor - Windows 部署指南

## 快速开始（Windows）

### 1. 安装 Python

下载并安装 Python 3.11+：
https://www.python.org/downloads/

**重要：** 安装时勾选 "Add Python to PATH"

### 2. 安装依赖

打开 PowerShell，进入项目目录：

```powershell
cd C:\Users\Administrator\.openclaw\workspace\github-stars-monitor

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

#### 方法 1：临时设置（当前 PowerShell 会话）

```powershell
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

#### 方法 2：永久设置（系统环境变量）

1. 右键 "此电脑" → "属性" → "高级系统设置"
2. 点击 "环境变量"
3. 在 "用户变量" 或 "系统变量" 中点击 "新建"
4. 变量名：`GITHUB_TOKEN`
5. 变量值：你的 GitHub Token
6. 点击 "确定" 保存

### 4. 配置文件

编辑 `config.json`：

```json
{
  "github_token": "",
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "C:\\Users\\Administrator\\openclaw\\workspace\\openrelay",
      "threshold": 1000,
      "enabled": true,
      "notification": true
    }
  ],
  "check_interval": 3600,
  "notification_method": "log",
  "telegram_token": "",
  "telegram_chat_id": ""
}
```

**重要：** Windows 路径使用反斜杠 `\`，例如：`C:\path\to\repo`

### 5. 测试运行

#### 单次执行模式

```powershell
python github-stars-monitor.py --once
```

#### 持续运行模式

```powershell
python github-stars-monitor.py
```

按 `Ctrl+C` 停止运行。

---

## Task Scheduler 定时任务

### 创建定时任务

#### 方法 1：图形界面

1. 打开 "任务计划程序"
2. 点击右侧 "创建基本任务"
3. 填写任务名称：`GitHub Stars Monitor`
4. 触发器：
   - 选择 "每天"
   - 设置时间：`09:00:00`
   - 重复间隔：1 小时
   - 重复：每天
5. 操作：
   - 选择 "启动程序"
   - 程序：`python.exe`
   - 参数：`C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\github-stars-monitor.py`
   - 起始于：`C:\Users\Administrator\.openclaw\workspace\github-stars-monitor`
6. 完成向导

#### 方法 2：PowerShell 命令

```powershell
# 创建定时任务
$action = New-ScheduledTaskAction `
    -Execute "python.exe" `
    -Argument "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\github-stars-monitor.py" `
    -WorkingDirectory "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor"

$trigger = New-ScheduledTaskTrigger -Daily -At 9am -RepetitionInterval (New-TimeSpan -Hours 1)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

Register-ScheduledTask `
    -TaskName "GitHub Stars Monitor" `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -RunLevel Highest
```

### 测试定时任务

1. 右键任务 → "运行"
2. 检查任务历史记录

### 管理定时任务

#### 启动任务

```powershell
Start-ScheduledTask -TaskName "GitHub Stars Monitor"
```

#### 停止任务

```powershell
Stop-ScheduledTask -TaskName "GitHub Stars Monitor"
```

#### 禁用任务

```powershell
Disable-ScheduledTask -TaskName "GitHub Stars Monitor"
```

#### 启用任务

```powershell
Enable-ScheduledTask -TaskName "GitHub Stars Monitor"
```

#### 删除任务

```powershell
Unregister-ScheduledTask -TaskName "GitHub Stars Monitor" -Confirm:$false
```

#### 查看任务状态

```powershell
Get-ScheduledTaskInfo -TaskName "GitHub Stars Monitor"
```

### 查看任务日志

1. 打开 "事件查看器"
2. 展开 "Windows 日志" → "应用程序"
3. 查找 "任务计划程序" 类别

---

## Windows 服务（高级）

### 使用 NSSM 安装为 Windows 服务

#### 1. 下载 NSSM

下载地址：https://nssm.cc/download

解压到 `C:\nssm`

#### 2. 安装服务

```powershell
# 进入 NSSM 目录
cd C:\nssm\bin

# 安装服务
.\nssm install GitHubStarsMonitor "C:\Python311\python.exe" "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\github-stars-monitor.py"

# 设置工作目录
.\nssm set GitHubStarsMonitor AppDirectory "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor"

# 设置启动类型为自动
.\nssm set GitHubStarsMonitor Start SERVICE_AUTO_START

# 设置日志
.\nssm set GitHubStarsMonitor AppStdout "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\logs\stdout.log"
.\nssm set GitHubStarsMonitor AppStderr "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\logs\stderr.log"

# 启动服务
.\nssm start GitHubStarsMonitor
```

#### 3. 管理服务

```powershell
# 启动服务
.\nssm start GitHubStarsMonitor

# 停止服务
.\nssm stop GitHubStarsMonitor

# 重启服务
.\nssm restart GitHubStarsMonitor

# 查看服务状态
.\nssm status GitHubStarsMonitor

# 删除服务
.\nssm remove GitHubStarsMonitor confirm
```

#### 4. 查看日志

```powershell
# 查看标准输出
Get-Content "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\logs\stdout.log" -Tail 50

# 查看错误输出
Get-Content "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\logs\stderr.log" -Tail 50
```

---

## 日志管理

### 日志位置

默认日志文件：`github_stars_monitor.log`

### 查看日志

```powershell
# 实时查看日志
Get-Content github_stars_monitor.log -Wait -Tail 50

# 查看最近 100 行
Get-Content github_stars_monitor.log -Tail 100

# 搜索错误日志
Select-String -Path "github_stars_monitor.log" -Pattern "ERROR"

# 搜索警告日志
Select-String -Path "github_stars_monitor.log" -Pattern "WARNING"
```

### 日志轮转

使用 PowerShell 脚本实现日志轮转：

创建 `rotate_logs.ps1`：

```powershell
$logPath = "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\github_stars_monitor.log"
$maxFiles = 7
$maxSizeMB = 10

# 检查日志文件大小
if ((Get-Item $logPath).Length -gt ($maxSizeMB * 1MB)) {
    # 备份并轮转日志
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupPath = "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\logs\github_stars_monitor_$timestamp.log"

    # 创建日志目录
    New-Item -ItemType Directory -Force -Path "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\logs"

    # 移动日志到备份
    Move-Item -Path $logPath -Destination $backupPath -Force

    # 删除旧日志（保留最近 maxFiles 个）
    $logFiles = Get-ChildItem "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\logs" -Filter "github_stars_monitor_*.log"
    $logFiles | Sort-Object LastWriteTime -Descending | Select-Object -Skip $maxFiles | Remove-Item -Force

    Write-Host "日志已轮转：$backupPath"
}
```

### 添加到 Task Scheduler

1. 创建新的定时任务
2. 操作：启动程序
3. 程序：`powershell.exe`
4. 参数：`-ExecutionPolicy Bypass -File "C:\path\to\rotate_logs.ps1"`
5. 起始于：`C:\path\to\`

---

## 常见问题

### 1. Python 路径找不到

**错误信息：**
```
'python' 不是内部或外部命令
```

**解决方案：**

方法 1：使用完整路径

```powershell
python.exe C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\github-stars-monitor.py
```

方法 2：添加 Python 到 PATH

1. 检查 Python 安装路径：`C:\Python311\python.exe`
2. 添加到系统环境变量 PATH

### 2. 路径错误

**错误信息：**
```
仓库路径不存在：C:\path\to\repo
```

**解决方案：**

1. 检查路径是否正确
2. Windows 路径使用反斜杠 `\`
3. 使用 `Get-ChildItem` 检查路径是否存在

```powershell
Test-Path "C:\Users\Administrator\.openclaw\workspace\openrelay"
```

### 3. 权限问题

**错误信息：**
```
Permission denied
```

**解决方案：**

1. 以管理员身份运行 PowerShell
2. 检查文件权限

```powershell
# 检查文件权限
icacls "C:\Users\Administrator\.openclaw\workspace\github-stars-monitor\config.json"
```

### 4. Task Scheduler 任务不执行

**检查：**

1. 任务是否启用
2. 触发器是否正确
3. 操作是否正确
4. 账户是否有权限

**解决方案：**

1. 右键任务 → "运行"
2. 检查任务历史记录
3. 尝试以不同账户运行

---

## 性能优化

### 1. 减少检查频率

修改 `config.json`：

```json
{
  "check_interval": 1800  // 从 3600 秒改为 1800 秒（30 分钟）
}
```

### 2. 限制监控仓库数量

只监控必要的仓库：

```json
{
  "repos": [
    {
      "owner": "hrudu-dev",
      "repo": "openrelay",
      "path": "C:\\Users\\Administrator\\.openclaw\\workspace\\openrelay",
      "threshold": 1000,
      "enabled": true
    }
  ]
}
```

### 3. 禁用通知

```json
{
  "notification_method": "log",
  "telegram_token": "",
  "telegram_chat_id": ""
}
```

---

## 监控和告警

### 检查服务状态

```powershell
# 检查 Python 进程
Get-Process python -ErrorAction SilentlyContinue

# 检查定时任务状态
Get-ScheduledTaskInfo -TaskName "GitHub Stars Monitor"

# 检查 Windows 服务状态
Get-Service GitHubStarsMonitor -ErrorAction SilentlyContinue
```

### 检查日志错误

```powershell
# 检查最近 100 行日志
Get-Content github_stars_monitor.log -Tail 100

# 搜索错误
Select-String -Path "github_stars_monitor.log" -Pattern "ERROR" -Context 2,2

# 统计错误数量
Select-String -Path "github_stars_monitor.log" -Pattern "ERROR" | Measure-Object
```

---

## 备份和恢复

### 备份配置

```powershell
# 备份配置文件
Copy-Item config.json "config.json.backup.$(Get-Date -Format 'yyyyMMdd')"

# 备份日志
Compress-Archive -Path "github_stars_monitor.log" -DestinationPath "github-stars-monitor-backup-$($env:USERNAME)-$(Get-Date -Format 'yyyyMMdd').zip"
```

### 恢复配置

```powershell
# 恢复配置
Copy-Item "config.json.backup.20260523" config.json

# 恢复日志
Expand-Archive -Path "github-stars-monitor-backup.zip" -DestinationPath "."
```

---

## 总结

### 推荐部署方式

| 场景 | 推荐方式 |
|------|---------|
| 测试 | 本地运行 |
| 个人使用 | Task Scheduler |
| 生产环境 | Windows 服务（NSSM） |

### 部署检查清单

- [ ] 安装 Python 3.11+
- [ ] 安装依赖
- [ ] 配置环境变量
- [ ] 配置 config.json
- [ ] 测试单次执行
- [ ] 创建 Task Scheduler 任务
- [ ] 配置日志轮转
- [ ] 设置备份策略
- [ ] 测试故障恢复
- [ ] 文档更新

---

*部署完成！*
