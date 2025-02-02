from dataclasses import dataclass
from .device import BluetoothDevice

@dataclass
class Scooter:
    # 滑板车数据模型
    # 存储滑板车状态：锁状态、电量等
    device: BluetoothDevice
    is_locked: bool = True
    battery_level: int = 0
    
    def update_battery_level(self, level: int):
        self.battery_level = level
        
    def update_lock_status(self, is_locked: bool):
        self.is_locked = is_locked 