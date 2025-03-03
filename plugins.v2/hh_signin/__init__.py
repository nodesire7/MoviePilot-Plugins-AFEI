from typing import Dict, Any
from app.core.module import BaseModule
from app.log import logger

class HHSignin(BaseModule):
    """
    HH论坛自动签到插件
    """

    # 插件名称
    module_name = "憨憨PT站签到"
    # 插件描述
    module_desc = "憨憨PT站自动签到"
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
    module_config_prefix = "hhsignin_"
    # 加载顺序
    module_order = 21
    # 可使用的用户级别
    user_level = 2

    # 私有属性
    _enabled = False
    _cron = None
    _cookie = None

    def init_module(self, config: Dict[str, Any]) -> None:
        self._enabled = config.get("enabled", False)
        self._cron = config.get("cron")
        self._cookie = config.get("cookie")

        if self._enabled:
            # 加载插件
            self._init_plugin()

    def _init_plugin(self):
        """
        插件初始化
        """
        if not self._cookie:
            logger.error(f"HH论坛签到插件启动失败，未配置cookie！")
            return
        
        # TODO: 初始化签到任务
        pass
