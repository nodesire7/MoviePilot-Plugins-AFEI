from typing import Dict, Any
from app.plugins import _PluginBase
from app.core.config import settings
from app.log import logger
from .main import hh_signin

class hh_signin(_PluginBase):
    """
    憨憨PT站自动签到插件
    """
    # 插件名称
    plugin_id = "hh_signin"
    # 插件描述
    plugin_desc = "憨憨PT站自动签到插件"
    # 插件图标
    plugin_icon = "signin.png"
    # 主题色
    plugin_color = "#0099FF"
    # 插件版本
    plugin_version = "1.0"
    # 插件作者
    plugin_author = "nodesire7"
    # 作者主页
    author_url = "https://github.com/nodesire7"
    # 插件配置项前缀
    plugin_config_prefix = "hh_signin_"
    # 加载顺序
    plugin_order = 21
    # 可使用的用户级别
    auth_level = 2

    def init_plugin(self, config: Dict[str, Any]) -> None:
        self._enabled = config.get("enabled", False)
        self._cron = config.get("cron")
        self._cookie = config.get("cookie")
        self._notify = config.get("notify", True)

        if self._enabled:
            # 加载插件
            self._init_plugin()

    def _init_plugin(self):
        """
        插件初始化
        """
        if not self._cookie:
            logger.error(f"憨憨PT站签到插件启动失败，未配置cookie！")
            return

        # 注册定时任务
        self.register_manual_task(
            '憨憨PT站签到',
            '憨憨PT站自动签到任务',
            self._cron,
            self.signin
        )

# 插件入口
def init_plugin(config: Dict[str, Any] = None) -> hh_signin:
    """
    加载插件
    """
    return hh_signin(config)
