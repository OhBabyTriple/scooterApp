import asyncio
from bleak import BleakScanner, BleakClient
import tkinter as tk
from tkinter import ttk, messagebox
import threading

class ScooterControllerUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Scooter 控制器")
        self.window.geometry("400x500")
        
        # 设备列表
        self.device_frame = ttk.LabelFrame(self.window, text="发现的设备")
        self.device_frame.pack(padx=10, pady=5, fill="x")
        
        self.device_listbox = tk.Listbox(self.device_frame, height=10)
        self.device_listbox.pack(padx=5, pady=5, fill="x")
        
        # 控制按钮
        self.control_frame = ttk.LabelFrame(self.window, text="控制")
        self.control_frame.pack(padx=10, pady=5, fill="x")
        
        self.scan_button = ttk.Button(self.control_frame, text="搜索设备", command=self.start_scan)
        self.scan_button.pack(padx=5, pady=5, fill="x")
        
        self.connect_button = ttk.Button(self.control_frame, text="连接设备", command=self.connect_device)
        self.connect_button.pack(padx=5, pady=5, fill="x")
        
        self.unlock_button = ttk.Button(self.control_frame, text="解锁", command=self.unlock_scooter)
        self.unlock_button.pack(padx=5, pady=5, fill="x")
        
        self.lock_button = ttk.Button(self.control_frame, text="上锁", command=self.lock_scooter)
        self.lock_button.pack(padx=5, pady=5, fill="x")
        
        # 状态显示
        self.status_label = ttk.Label(self.window, text="状态: 未连接")
        self.status_label.pack(padx=10, pady=5)
        
        self.devices = {}
        self.connected_device = None
        self.loop = asyncio.new_event_loop()

    def start_scan(self):
        self.scan_button.configure(state="disabled")
        self.device_listbox.delete(0, tk.END)
        self.status_label.configure(text="状态: 正在搜索...")
        
        threading.Thread(target=self.scan_devices, daemon=True).start()

    def scan_devices(self):
        async def scan():
            devices = await BleakScanner.discover()
            self.devices.clear()
            for device in devices:
                if device.name and "SCOOTER" in device.name.upper():
                    self.devices[device.name] = device
                    self.device_listbox.insert(tk.END, device.name)
            
            self.window.after(0, lambda: self.scan_button.configure(state="normal"))
            self.window.after(0, lambda: self.status_label.configure(text="状态: 搜索完成"))
        
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(scan())

    def connect_device(self):
        selection = self.device_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个设备")
            return
            
        device_name = self.device_listbox.get(selection[0])
        device = self.devices[device_name]
        
        threading.Thread(target=self.connect_to_device, args=(device,), daemon=True).start()

    def connect_to_device(self, device):
        async def connect():
            try:
                client = BleakClient(device.address)
                await client.connect()
                self.connected_device = client
                self.window.after(0, lambda: self.status_label.configure(text=f"状态: 已连接到 {device.name}"))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("错误", f"连接失败: {str(e)}"))
        
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(connect())

    def unlock_scooter(self):
        if not self.connected_device:
            messagebox.showwarning("警告", "请先连接设备")
            return
        
        threading.Thread(target=self.send_unlock_command, daemon=True).start()

    def lock_scooter(self):
        if not self.connected_device:
            messagebox.showwarning("警告", "请先连接设备")
            return
        
        threading.Thread(target=self.send_lock_command, daemon=True).start()

    def send_unlock_command(self):
        async def unlock():
            try:
                # 根据协议发送解锁命令 (0x81)
                command = bytes([0x81, 0x01])  # 示例命令
                await self.connected_device.write_gatt_char("YOUR_CHARACTERISTIC_UUID", command)
                self.window.after(0, lambda: messagebox.showinfo("成功", "解锁成功"))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("错误", f"解锁失败: {str(e)}"))
        
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(unlock())

    def send_lock_command(self):
        async def lock():
            try:
                # 根据协议发送上锁命令
                command = bytes([0x81, 0x00])  # 示例命令
                await self.connected_device.write_gatt_char("YOUR_CHARACTERISTIC_UUID", command)
                self.window.after(0, lambda: messagebox.showinfo("成功", "上锁成功"))
            except Exception as e:
                self.window.after(0, lambda: messagebox.showerror("错误", f"上锁失败: {str(e)}"))
        
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(lock())

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ScooterControllerUI()
    app.run() 