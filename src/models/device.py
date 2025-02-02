from dataclasses import dataclass

@dataclass
class BluetoothDevice:
    # 蓝牙设备数据模型
    # 存储设备的基本信息：名称、地址、信号强度
    name: str
    address: str
    rssi: int
    
    @classmethod
    def from_bleak_device(cls, device):
        return cls(
            name=device.name or "Unknown",
            address=device.address,
            rssi=device.rssi or 0
        ) 