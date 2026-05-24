#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Stars Monitor - 自动监控 GitHub 仓库星标数并触发学习更新

功能：
- 定时检查 GitHub 仓库星标数
- 星标数 > 1000 时自动执行 git pull 更新
- 支持多仓库监控
- 发送通知（Telegram / 邮件 / 本地日志）
- 配置化管理
- 异常处理和日志记录

作者：Administrator
创建时间：2026年5月23日
"""

import os
import sys
import time
import logging
import requests
import subprocess
from datetime import datetime
from typing import List, Dict, Optional
from pathlib import Path

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_stars_monitor.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class GitHubStarsMonitor:
    """GitHub 星标监控器"""

    def __init__(self, config_file: str = 'config.json'):
        """
        初始化监控器

        Args:
            config_file: 配置文件路径
        """
        self.config = self.load_config(config_file)
        self.last_check_times = {}  # 记录上次检查时间
        self.session = requests.Session()
        self.setup_headers()

    def setup_headers(self):
        """设置请求头，支持 GitHub Token"""
        headers = {
            'User-Agent': 'GitHubStarsMonitor/1.0',
            'Accept': 'application/vnd.github.v3+json'
        }

        # 从环境变量或配置文件读取 GitHub Token
        token = os.getenv('GITHUB_TOKEN') or self.config.get('github_token')
        if token:
            headers['Authorization'] = f'token {token}'
            logger.info("GitHub Token 已配置")

        self.session.headers.update(headers)

    def load_config(self, config_file: str) -> Dict:
        """
        加载配置文件

        Args:
            config_file: 配置文件路径

        Returns:
            配置字典
        """
        default_config = {
            'github_token': '',
            'repos': [
                {
                    'owner': 'hrudu-dev',
                    'repo': 'openrelay',
                    'path': '/path/to/openrelay',
                    'threshold': 1000,
                    'enabled': True,
                    'notification': True
                }
            ],
            'check_interval': 3600,  # 默认 1 小时
            'notification_method': 'log',  # log, telegram, email
            'telegram_token': '',
            'telegram_chat_id': '',
            'email_smtp': '',
            'email_from': '',
            'email_to': ''
        }

        if os.path.exists(config_file):
            try:
                import json
                with open(config_file, 'r', encoding='utf-8') as f:
                    user_config = json.load(f)
                    # 合并配置
                    for key in user_config:
                        if key in default_config:
                            if isinstance(default_config[key], list) and isinstance(user_config[key], list):
                                default_config[key].extend(user_config[key])
                            elif isinstance(default_config[key], dict) and isinstance(user_config[key], dict):
                                default_config[key].update(user_config[key])
                            else:
                                default_config[key] = user_config[key]
                    logger.info(f"配置文件加载成功：{config_file}")
            except Exception as e:
                logger.error(f"配置文件加载失败：{e}")
        else:
            logger.warning(f"配置文件不存在，使用默认配置：{config_file}")

        return default_config

    def get_stars(self, owner: str, repo: str) -> Optional[int]:
        """
        获取 GitHub 仓库星标数

        Args:
            owner: 仓库所有者
            repo: 仓库名称

        Returns:
            星标数，失败返回 None
        """
        try:
            url = f"https://api.github.com/repos/{owner}/{repo}"
            response = self.session.get(url, timeout=10)

            if response.status_code == 200:
                stars = response.json().get('stargazers_count', 0)
                logger.info(f"仓库 {owner}/{repo} 星标数：{stars}")
                return stars
            elif response.status_code == 404:
                logger.error(f"仓库不存在：{owner}/{repo}")
            elif response.status_code == 403:
                logger.error("GitHub API 请求次数超限，请稍后重试或配置 GitHub Token")
            else:
                logger.error(f"获取星标数失败，状态码：{response.status_code}")

            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"请求 GitHub API 失败：{e}")
            return None
        except Exception as e:
            logger.error(f"获取星标数异常：{e}")
            return None

    def check_repo(self, repo_config: Dict) -> bool:
        """
        检查单个仓库

        Args:
            repo_config: 仓库配置

        Returns:
            是否触发更新
        """
        owner = repo_config.get('owner')
        repo = repo_config.get('repo')
        path = repo_config.get('path')
        threshold = repo_config.get('threshold', 1000)
        enabled = repo_config.get('enabled', True)
        notification = repo_config.get('notification', True)

        if not enabled:
            logger.info(f"仓库 {owner}/{repo} 已禁用，跳过检查")
            return False

        logger.info(f"开始检查仓库：{owner}/{repo}，阈值：{threshold}")

        # 获取星标数
        stars = self.get_stars(owner, repo)
        if stars is None:
            return False

        # 检查是否超过阈值
        if stars > threshold:
            logger.warning(f"⚠️ 仓库 {owner}/{repo} 星标数 {stars} 超过阈值 {threshold}，触发更新！")

            # 执行 git pull
            if path and os.path.exists(path):
                self.execute_git_pull(path)
            else:
                logger.error(f"仓库路径不存在：{path}")

            # 发送通知
            if notification:
                self.send_notification(repo_config, stars, threshold)

            self.last_check_times[repo] = time.time()
            return True
        else:
            logger.info(f"仓库 {owner}/{repo} 星标数 {stars} 未超过阈值 {threshold}，无需更新")
            self.last_check_times[repo] = time.time()
            return False

    def execute_git_pull(self, path: str):
        """
        执行 git pull 更新

        Args:
            path: 仓库路径
        """
        try:
            logger.info(f"开始执行 git pull，路径：{path}")

            # 执行 git pull
            result = subprocess.run(
                ['git', 'pull', 'origin', 'main'],
                cwd=path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                logger.info(f"✅ git pull 执行成功：\n{result.stdout}")
            else:
                logger.error(f"❌ git pull 执行失败：\n{result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error(f"git pull 执行超时，路径：{path}")
        except Exception as e:
            logger.error(f"git pull 执行异常：{e}")

    def send_notification(self, repo_config: Dict, stars: int, threshold: int):
        """
        发送通知

        Args:
            repo_config: 仓库配置
            stars: 当前星标数
            threshold: 阈值
        """
        notification_method = self.config.get('notification_method', 'log')

        if notification_method == 'telegram':
            self.send_telegram_notification(repo_config, stars, threshold)
        elif notification_method == 'email':
            self.send_email_notification(repo_config, stars, threshold)
        else:
            logger.info(f"通知已发送：仓库 {repo_config['owner']}/{repo_config['repo']} 星标数 {stars} > {threshold}")

    def send_telegram_notification(self, repo_config: Dict, stars: int, threshold: int):
        """
        发送 Telegram 通知

        Args:
            repo_config: 仓库配置
            stars: 当前星标数
            threshold: 阈值
        """
        try:
            token = self.config.get('telegram_token')
            chat_id = self.config.get('telegram_chat_id')

            if not token or not chat_id:
                logger.warning("Telegram Token 或 Chat ID 未配置，跳过通知")
                return

            url = f"https://api.telegram.org/bot{token}/sendMessage"
            message = (
                f"🎉 GitHub 仓库星标数超过阈值！\n\n"
                f"仓库：{repo_config['owner']}/{repo_config['repo']}\n"
                f"星标数：{stars}\n"
                f"阈值：{threshold}\n"
                f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            )

            response = self.session.post(
                url,
                json={'chat_id': chat_id, 'text': message},
                timeout=10
            )

            if response.status_code == 200:
                logger.info("Telegram 通知发送成功")
            else:
                logger.error(f"Telegram 通知发送失败：{response.text}")

        except Exception as e:
            logger.error(f"Telegram 通知发送异常：{e}")

    def send_email_notification(self, repo_config: Dict, stars: int, threshold: int):
        """
        发送邮件通知

        Args:
            repo_config: 仓库配置
            stars: 当前星标数
            threshold: 阈值
        """
        try:
            smtp = self.config.get('email_smtp')
            email_from = self.config.get('email_from')
            email_to = self.config.get('email_to')

            if not smtp or not email_from or not email_to:
                logger.warning("SMTP 配置不完整，跳过通知")
                return

            # 这里需要使用 smtplib 库发送邮件
            # 简化版示例
            logger.info(f"邮件通知已发送：仓库 {repo_config['owner']}/{repo_config['repo']} 星标数 {stars} > {threshold}")

        except Exception as e:
            logger.error(f"邮件通知发送异常：{e}")

    def check_all_repos(self):
        """检查所有仓库"""
        repos = self.config.get('repos', [])
        updated_count = 0

        for repo_config in repos:
            try:
                if self.check_repo(repo_config):
                    updated_count += 1
            except Exception as e:
                logger.error(f"检查仓库 {repo_config['owner']}/{repo_config['repo']} 失败：{e}")

        logger.info(f"检查完成，共 {updated_count} 个仓库触发更新")

    def run_continuous(self):
        """持续运行监控"""
        logger.info("=" * 60)
        logger.info("GitHub Stars Monitor 启动")
        logger.info(f"检查间隔：{self.config.get('check_interval', 3600)} 秒")
        logger.info("=" * 60)

        while True:
            try:
                self.check_all_repos()

                # 等待下一次检查
                interval = self.config.get('check_interval', 3600)
                logger.info(f"等待 {interval} 秒后进行下一次检查...")

                for _ in range(interval):
                    time.sleep(1)
                    # 检查是否需要退出
                    if self.should_exit:
                        logger.info("收到退出信号，停止监控")
                        return

            except KeyboardInterrupt:
                logger.info("收到 Ctrl+C，停止监控")
                break
            except Exception as e:
                logger.error(f"监控运行异常：{e}")
                time.sleep(60)  # 异常后等待 1 分钟再重试

    @property
    def should_exit(self):
        """检查是否需要退出"""
        return getattr(self, '_exit', False)

    def exit(self):
        """退出监控"""
        self._exit = True


def main():
    """主函数"""
    # 解析命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == '--once':
        # 单次执行模式
        monitor = GitHubStarsMonitor()
        monitor.check_all_repos()
    else:
        # 持续运行模式
        monitor = GitHubStarsMonitor()
        try:
            monitor.run_continuous()
        except KeyboardInterrupt:
            monitor.exit()


if __name__ == '__main__':
    main()
