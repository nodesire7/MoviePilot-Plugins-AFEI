from typing import Tuple, List, Dict, Any
from app.core.event import eventmanager
from app.schemas.types import EventType
from app.log import logger

@eventmanager.register(EventType.CommandExec)
def command_exec(cmd: List[str], data: Dict[str, Any]) -> Tuple[bool, str]:
    """
    执行命令
    """
    if not cmd:
        return False, "命令错误"
    
    # 手动签到命令
    if cmd[0] == "hhsignin":
        # TODO: 执行签到逻辑
        return True, "开始执行HH论坛签到..."
        
    return False, "未知命令"
