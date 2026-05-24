# GitHub Stars Monitor - 发布到 GitHub 快速指南

## 方法 1：使用 Python 脚本（推荐）

### 1. 设置 GitHub Token

#### 获取 Token
1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 选择权限：
   - ✅ `public_repo`（读取公开仓库信息）
4. 点击 "Generate token"
5. 复制 Token

### 2. 设置环境变量

**PowerShell：**
```powershell
$env:GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

**CMD：**
```cmd
set GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**永久设置（PowerShell）：**
```powershell
[System.Environment]::SetEnvironmentVariable('GITHUB_TOKEN', 'ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', 'User')
```

### 3. 运行发布脚本

**Windows（CMD）：**
```cmd
publish-to-github.bat
```

**Windows（PowerShell）：**
```powershell
.\publish-to-github.ps1
```

**Linux / macOS：**
```bash
python github-manager.py
```

---

## 方法 2：手动发布

### 1. 创建 GitHub 仓库

1. 访问：https://github.com/new
2. 填写信息：
   - Repository name: `github-stars-monitor`
   - Description: `自动监控 GitHub 仓库星标数，当星标数超过阈值时自动执行 git pull 更新`
   - 选择 Public 或 Private
3. 点击 "Create repository"

### 2. 上传文件

**使用 Git（推荐）：**

```bash
# 克隆仓库
git clone https://github.com/yourusername/github-stars-monitor.git
cd github-stars-monitor

# 复制文件
cp -r /path/to/workspace/* .

# 提交
git add .
git commit -m "Initial commit"

# 推送
git branch -M main
git push -u origin main
```

**使用 Python 脚本：**

```bash
python github-manager.py
```

### 3. 创建 Release

1. 访问：https://github.com/yourusername/github-stars-monitor/releases
2. 点击 "Create a new release"
3. 填写信息：
   - Tag: `v1.0.0`
   - Release title: `GitHub Stars Monitor v1.0.0`
   - Description: （参考 README.md）
4. 点击 "Publish release"

---

## 方法 3：使用 GitHub CLI（gh）

### 1. 安装 GitHub CLI

**Windows：**
```powershell
winget install --id GitHub.cli
```

**macOS：**
```bash
brew install gh
```

**Linux：**
```bash
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh
```

### 2. 登录 GitHub

```bash
gh auth login
```

按提示选择：
- ? What account do you want to log into? → GitHub.com
- ? What is your preferred protocol for Git operations? → HTTPS
- ? Authenticate Git with your GitHub credentials? → Yes
- ? How would you like to authenticate GitHub CLI? → Login with a web browser

### 3. 创建仓库

```bash
gh repo create github-stars-monitor --public --source=. --remote=origin --description="自动监控 GitHub 仓库星标数，当星标数超过阈值时自动执行 git pull 更新" --push
```

### 4. 创建 Release

```bash
gh release create v1.0.0 --title "GitHub Stars Monitor v1.0.0" --notes "$(cat << 'EOF'
## GitHub Stars Monitor v1.0.0

自动监控 GitHub 仓库星标数，当星标数超过阈值时自动执行 git pull 更新。

### 功能特性
- ✅ 定时检查 GitHub 仓库星标数
- ✅ 星标数 > 1000 时自动执行 git pull
- ✅ 支持多仓库监控
- ✅ 发送通知（Telegram / 邮件 / 日志）
- ✅ 配置化管理
- ✅ 异常处理和日志记录
- ✅ 支持 GitHub Token（避免 API 限流）
- ✅ 持续运行模式（守护进程）
- ✅ 单次执行模式

### 快速开始
\`\`\`bash
pip install -r requirements.txt
python github-stars-monitor.py --once
\`\`\`

### 许可证
MIT License
EOF
)"
```

---

## 项目结构

```
github-stars-monitor/
├── github-stars-monitor.py      # 主程序
├── github-manager.py            # GitHub 管理器
├── config.json                  # 配置文件
├── requirements.txt             # 依赖列表
├── README.md                    # 主文档
├── INSTALL.md                   # 安装指南
├── DEPLOYMENT.md                # 部署指南（Linux/macOS）
├── DEPLOYMENT_WINDOWS.md        # 部署指南（Windows）
├── PUBLISH_GUIDE.md             # 发布指南
├── .gitignore                   # Git 忽略文件
├── .env.example                 # 环境变量示例
└── .github/
    └── ISSUE_TEMPLATE/
        ├── bug_report.md        # Bug 报告模板
        ├── feature_request.md   # 功能请求模板
        ├── bug_report_en.md     # Bug 报告模板（英文）
        └── feature_request_en.md # 功能请求模板（英文）
```

---

## 发布检查清单

- [ ] 设置 GitHub Token
- [ ] 测试 Python 脚本
- [ ] 创建 GitHub 仓库
- [ ] 上传所有文件
- [ ] 创建 README.md
- [ ] 创建 Release
- [ ] 添加 Star 徽章
- [ ] 添加 Issues 模板
- [ ] 测试文档链接
- [ ] 发布到社交媒体

---

## 后续工作

### 1. 添加 Star 指引
在 README.md 顶部添加：
```markdown
---

## ⭐ 如果这个项目对你有帮助，请给个 Star！

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/github-stars-monitor&type=Date)](https://star-history.com/#yourusername/github-stars-monitor&Date)
```

### 2. 推广到社交媒体
- Twitter
- Reddit
- Hacker News
- GitHub Discussions

### 3. 监控 Issue 和 PR
- 定期检查 Issue
- 回复用户反馈
- 处理 Pull Request

### 4. 持续更新
- 添加新功能
- 修复 Bug
- 更新文档
- 优化性能

---

## 常见问题

### Q: Token 权限不够？
A: 确保选择 `public_repo` 权限。

### Q: 发布失败？
A: 检查网络连接和 Token 是否正确。

### Q: 文件上传失败？
A: 检查文件路径和权限。

### Q: Release 创建失败？
A: 确保仓库名称和 Tag 格式正确。

---

## 获取帮助

- GitHub Issues：https://github.com/yourusername/github-stars-monitor/issues
- 联系：your-email@example.com

---

*发布完成！*
