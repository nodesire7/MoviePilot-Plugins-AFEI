import os
import json
import time
from typing import Dict, Any, List, Optional, Union
from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

from app.plugins import _PluginBase
from app.core.config import settings
from app.core.event import eventmanager
from app.schemas.types import EventType
from app.log import logger


class HHSign(_PluginBase):
    # 插件信息
    plugin_id = "hh_signin"
    plugin_name = "憨憨PT站签到"
    plugin_desc = "自动模拟浏览器操作执行PT站签到。"
    plugin_version = "1.0"
    plugin_author = "nodesire7"

    # 私有属性
    _enabled = False
    _cron = None
    _cookie = None
    _notify = False
    _site_url = None
    _retry_count = 0
    _retry_timeout = 60

    def init_plugin(self, config: Dict[str, Any] = None) -> None:
        if config:
            self._enabled = config.get('enabled', False)
            self._cron = config.get('cron')
            self._cookie = config.get('cookie')
            self._notify = config.get('notify', True)
            self._site_url = config.get('site_url', 'https://hhanclub.top/')
            self._retry_count = config.get('retry_count', 3)
            self._retry_timeout = config.get('retry_timeout', 60)

        # 注册定时任务
        self.register_scheduler(self._cron)

    def get_state(self) -> bool:
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        """
        定义远程控制命令
        """
        return [{
            "cmd": "signin",
            "title": "立即签到",
            "description": "立即执行一次憨憨PT站签到"
        }]

    def get_api(self) -> List[Dict[str, Any]]:
        """
        定义API接口
        """
        return [{
            "path": "/signin",
            "endpoint": self.signin,
            "methods": ["GET"],
            "summary": "立即签到",
            "description": "立即执行一次憨憨PT站签到"
        }]

    def __setup_driver(self):
        """
        配置浏览器驱动
        """
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            logger.error(f"浏览器驱动初始化失败：{str(e)}")
            return None

    def signin(self) -> Optional[bool]:
        """
        执行签到
        """
        if not self._enabled or not self._cookie:
            logger.error("签到插件未启用或Cookie未配置")
            return False

        driver = None
        for retry in range(self._retry_count):
            try:
                driver = self.__setup_driver()
                if not driver:
                    raise WebDriverException("浏览器驱动初始化失败")

                # 访问网站
                driver.get(self._site_url)

                # 添加Cookie
                driver.delete_all_cookies()
                for item in self._cookie.split(";"):
                    key, value = item.strip().split("=", 1)
                    driver.add_cookie({"name": key, "value": value})

                driver.refresh()

                # 等待并点击用户头像
                wait = WebDriverWait(driver, 10)
                user_avatar = wait.until(EC.element_to_be_clickable((By.ID, "user-avatar")))
                user_avatar.click()

                # 点击签到链接
                sign_in_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, 'attendance.php')]")))
                sign_in_link.click()

                # 签到成功
                msg = "签到成功"
                logger.info(msg)
                
                if self._notify:
                    self.send_message(
                        title=f"【{self.plugin_name}】",
                        text=msg
                    )

                return True

            except TimeoutException:
                msg = "页面加载超时"
                logger.error(msg)
                if retry == self._retry_count - 1:
                    if self._notify:
                        self.send_message(
                            title=f"【{self.plugin_name}】",
                            text=f"签到失败：{msg}"
                        )
            except Exception as e:
                msg = str(e)
                logger.error(f"签到出错：{msg}")
                if retry == self._retry_count - 1:
                    if self._notify:
                        self.send_message(
                            title=f"【{self.plugin_name}】",
                            text=f"签到失败：{msg}"
                        )
            finally:
                if driver:
                    driver.quit()

            # 重试等待
            if retry < self._retry_count - 1:
                logger.info(f"{self._retry_timeout}秒后重试第{retry + 2}次 ...")
                time.sleep(self._retry_timeout)

        return False

    def register_scheduler(self, cron: Optional[str] = None):
        """
        注册定时任务
        """
        if cron:
            self.register_manual_task(
                task_name=self.plugin_name,
                task_desc=self.plugin_desc,
                task_time=cron,
                task_func=self.signin
            )

    @eventmanager.register(EventType.PluginReload)
    def plugin_reload(self, event):
        """
        插件重载事件
        """
        logger.info(f"插件重载：{self.plugin_name}")
        self.register_scheduler(self._cron)
