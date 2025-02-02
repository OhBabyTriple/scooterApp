import tkinter as tk
from tkinter import ttk, messagebox
import yaml
from src.controllers.scooter_controller import ScooterController
from src.utils.constants import BluetoothState
from src.utils.logger import setup_logger

logger = setup_logger()

class MainWindow:
    # 图形界面实现
    # - 设备列表显示
    # - 控制按钮
    # - 状态显示
    # - 消息提示
    def __init__(self):
        with open("config/config.yaml", "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)["ui"]
            
        self.controller = ScooterController(self)
        self.setup_ui()
        
    def setup_ui(self):
        self.window = tk.Tk()
        self.window.title(self.config["window_title"])
        self.window.geometry(self.config["window_size"])
        
        self.setup_device_list()
        self.setup_controls()
        self.setup_status()
        
    def setup_device_list(self):
        self.device_frame = ttk.LabelFrame(self.window, text="发现的设备")
        self.device_frame.pack(padx=10, pady=5, fill="x")
        
        self.device_listbox = tk.Listbox(self.device_frame, height=10)
        self.device_listbox.pack(padx=5, pady=5, fill="x")
        
    def setup_controls(self):
        self.control_frame = ttk.LabelFrame(self.window, text="控制")
        self.control_frame.pack(padx=10, pady=5, fill="x")
        
        self.filter_var = tk.BooleanVar(value=True)  # 默认启用过滤
        self.filter_checkbutton = ttk.Checkbutton(
            self.control_frame, 
            text="启用名称过滤", 
            variable=self.filter_var,
            command=self.toggle_filter
        )
        self.filter_checkbutton.pack(padx=5, pady=5, fill="x")
        
        buttons = [
            ("搜索设备", self.controller.start_scan),
            ("连接设备", self.controller.connect_device),
            ("解锁", self.controller.unlock_scooter),
            ("上锁", self.controller.lock_scooter),
            ("断开设备", self.controller.disconnect_device)
        ]
        
        for text, command in buttons:
            btn = ttk.Button(self.control_frame, text=text, command=command)
            btn.pack(padx=5, pady=5, fill="x")
            
    def setup_status(self):
        self.status_label = ttk.Label(self.window, text=f"状态: {BluetoothState.DISCONNECTED.value}")
        self.status_label.pack(padx=10, pady=5)
        
    def update_device_list(self, devices):
        self.device_listbox.delete(0, tk.END)
        for device in devices:
            # 显示设备名称、MAC地址和RSSI
            self.device_listbox.insert(tk.END, f"{device.name} ({device.address}) - RSSI: {device.rssi}dBm")
            
    def update_status(self, state: BluetoothState, device_name: str = None):
        status_text = f"状态: {state.value}"
        if device_name and state == BluetoothState.CONNECTED:
            status_text += f" - {device_name}"
        self.status_label.configure(text=status_text)
        
    def show_error(self, title: str, message: str):
        messagebox.showerror(title, message)
        
    def show_info(self, title: str, message: str):
        messagebox.showinfo(title, message)
        
    def toggle_filter(self):
        """切换名称过滤状态"""
        self.controller.bluetooth.config["enable_name_filter"] = self.filter_var.get()
        logger.info(f"名称过滤 {'启用' if self.filter_var.get() else '禁用'}")
        
    def run(self):
        self.window.mainloop() 