import asyncio
import threading
from src.utils.constants import BluetoothState, CommandType
from src.utils.logger import setup_logger
from src.controllers.bluetooth_controller import BluetoothController

logger = setup_logger()

class ScooterController:
    # 业务逻辑控制器，连接UI和蓝牙控制器
    # - 处理UI事件
    # - 管理异步操作
    # - 处理错误和状态更新
    def __init__(self, view):
        self.view = view
        self.bluetooth = BluetoothController()
        self.loop = asyncio.new_event_loop()
        self.devices = []
        
    def _run_async(self, coro):
        """在新线程中运行异步代码"""
        def run():
            asyncio.set_event_loop(self.loop)
            self.loop.run_until_complete(coro)
            
        thread = threading.Thread(target=run, daemon=True)
        thread.start()
        
    async def _scan(self):
        self.view.update_status(BluetoothState.SCANNING)
        try:
            self.devices = await self.bluetooth.scan_devices()
            self.view.update_device_list(self.devices)
            self.view.update_status(BluetoothState.DISCONNECTED)
        except Exception as e:
            logger.error(f"扫描失败: {str(e)}")
            self.view.show_error("错误", f"扫描失败: {str(e)}")
            self.view.update_status(BluetoothState.DISCONNECTED)
            
    def start_scan(self):
        """开始扫描设备"""
        self._run_async(self._scan())
        
    async def _connect(self, device):
        self.view.update_status(BluetoothState.CONNECTING)
        try:
            success = await self.bluetooth.connect(device)
            if success:
                self.view.update_status(BluetoothState.CONNECTED, device.name)
                self.view.show_info("成功", f"已连接到 {device.name}")
            else:
                self.view.update_status(BluetoothState.DISCONNECTED)
        except Exception as e:
            logger.error(f"连接失败: {str(e)}")
            self.view.show_error("错误", f"连接失败: {str(e)}")
            self.view.update_status(BluetoothState.DISCONNECTED)
            
    def connect_device(self):
        """连接选中的设备"""
        selection = self.view.device_listbox.curselection()
        if not selection:
            self.view.show_error("错误", "请先选择一个设备")
            return
            
        device = self.devices[selection[0]]
        self._run_async(self._connect(device))
        
    async def _send_command(self, command_type: CommandType):
        try:
            success = await self.bluetooth.send_command(command_type.value)
            if success:
                self.view.show_info("成功", f"{command_type.value}命令发送成功")
            else:
                self.view.show_error("错误", f"{command_type.value}命令发送失败")
        except Exception as e:
            logger.error(f"发送命令失败: {str(e)}")
            self.view.show_error("错误", f"发送命令失败: {str(e)}")
            
    async def unlock_scooter(self):
        if await self.bluetooth.connect_to_scooter():
            await self.bluetooth.send_command("get_key")
            await asyncio.sleep(1)
            await self.bluetooth.send_command("unlock")
            self.view.show_info("成功", "解锁成功！")

    async def lock_scooter(self):
        if await self.bluetooth.connect_to_scooter():
            await self.bluetooth.send_command("get_key")
            await asyncio.sleep(1)
            await self.bluetooth.send_command("lock")
            self.view.show_info("成功", "锁车成功！")

    def disconnect_device(self):
        """断开当前连接的设备"""
        self._run_async(self.bluetooth.disconnect())
        self.view.update_status(BluetoothState.DISCONNECTED)
        self.view.show_info("成功", "设备已断开连接") 