import asyncio
from bleak import BleakScanner, BleakClient
import yaml
from src.models.device import BluetoothDevice
from src.utils.logger import setup_logger

logger = setup_logger()

class BluetoothController:
    # 负责与蓝牙设备的直接交互
    # - 扫描设备
    # - 建立连接
    # - 断开连接
    # - 发送命令
    def __init__(self):
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)["bluetooth"]
            
        self.client = None
        self.connected_device = None
        
    async def scan_devices(self):
        logger.info("开始扫描设备")
        devices = await BleakScanner.discover(
            timeout=self.config["scan_timeout"]
        )
        
        scooter_devices = []
        for device in devices:
            # 创建 BluetoothDevice 实例时记录更多信息
            scooter_device = BluetoothDevice.from_bleak_device(device)
            logger.info(f"发现设备: 名称={scooter_device.name}, 地址={scooter_device.address}, RSSI={scooter_device.rssi}")
            scooter_devices.append(scooter_device)
        
        logger.info(f"发现 {len(scooter_devices)} 个设备")
        return scooter_devices
        
    async def connect(self, device: BluetoothDevice):
        logger.info(f"正在连接到设备: {device.name}")
        try:
            self.client = BleakClient(device.address)
            await self.client.connect()
            self.connected_device = device
            logger.info(f"成功连接到设备: {device.name}")
            return True
        except Exception as e:
            logger.error(f"连接失败: {str(e)}")
            return False
            
    async def disconnect(self):
        if self.client and self.client.is_connected:
            await self.client.disconnect()
            self.client = None
            self.connected_device = None
            logger.info("断开连接")
            
    async def send_command(self, command_type: str):
        if not self.client or not self.client.is_connected:
            logger.error("未连接到设备")
            return False
            
        try:
            command = bytes(self.config["commands"][command_type])
            await self.client.write_gatt_char(
                self.config["write_uuid"],
                command
            )
            logger.info(f"发送命令成功: {command_type}")
            return True
        except Exception as e:
            logger.error(f"发送命令失败: {str(e)}")
            return False

    async def connect_to_scooter(self):
        try:
            self.client = BleakClient(self.config["scooter_mac"])
            await self.client.connect()
            logger.info("成功连接到滑板车")
            return True
        except Exception as e:
            logger.error(f"连接滑板车失败: {str(e)}")
            return False 