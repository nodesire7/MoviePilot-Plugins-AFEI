from typing import Dict, Any
from app.plugins import _PluginBase
from app.core.config import settings
from app.log import logger
from .sign import HHSignHelper

class HHSignin(_PluginBase):
    """
    憨憨PT站自动签到插件
    """
    # 插件名称
    module_name = "hh_signin"
    # 插件描述
    module_desc = "憨憨PT站自动签到插件"
    # 插件图标
    module_icon = "signin.png"
    # 主题色
    module_color = "#0099FF"
    # 插件版本
    module_version = "1.0"
    # 插件作者
    module_author = "AFEI"
    # 作者主页
    author_url = "https://github.com/nodesire7"
    # 插件配置项ID前缀
    module_config_prefix = "hh_signin_"
    # 加载顺序
    module_order = 21
    # 可使用的用户级别
    user_level = 2

    def init_module(self, config: Dict[str, Any]) -> None:
        self.enabled = config.get("enabled", False)
        self.cron = config.get("cron")
        self.cookie = config.get("cookie")
        self.notify = config.get("notify", True)

        if self.enabled:
            # 加载插件
            self._init_plugin()

    def _init_plugin(self):
        """
        插件初始化
        """
        if not self.cookie:
            logger.error(f"憨憨PT站签到插件启动失败，未配置cookie！")
            return

        # 初始化签到助手
        self.sign_helper = HHSignHelper(self.cookie, chrome=self.chrome)
        
        # 注册定时任务
        self.register_manual_task(
            '憨憨PT站签到',
            '憨憨PT站自动签到任务',
            self.cron,
            self._signin_task
        )

    def _signin_task(self):
        """
        签到任务
        """
        if not self.sign_helper:
            logger.error("签到助手未初始化")
            return False

        # 执行签到
        result = self.sign_helper.sign_in()
        
        # 发送通知
        if self.notify:
            self.send_message(
                title="【憨憨PT站签到】",
                text="签到成功" if result else "签到失败"
            )
            
        return result

from .main import hh_signin

plugin_id = "hh_signin"
plugin_name = "憨憨PT站签到"
plugin_desc = "自动执行憨憨PT站签到任务"
plugin_icon = "signin.png"
plugin_version = "1.0"
plugin_author = "nodesire7"

def init_plugin(config=None):
    """
    加载插件
    """
    return hh_signin(config)
