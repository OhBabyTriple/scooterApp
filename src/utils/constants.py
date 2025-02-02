from enum import Enum

class BluetoothState(Enum):
    # 蓝牙状态枚举
    # 定义各种状态常量
    DISCONNECTED = "未连接"
    SCANNING = "正在搜索..."
    CONNECTING = "正在连接..."
    CONNECTED = "已连接"
    
class CommandType(Enum):
    # 命令类型枚举
    # 定义可用的命令类型
    LOCK = "lock"
    UNLOCK = "unlock" 