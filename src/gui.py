from PySide6.QtWidgets import QMessageBox, QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QComboBox
from PySide6.QtCore import QProcess
import sys, socket, ctypes, os
import win32com.client  as com 
import subprocess  # 添加导入

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
IP = s.getsockname()[0]

class ServerControlGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.process = QProcess()
        self.init_ui()
        
    def closeEvent(self, event):  # 添加窗口关闭事件处理
        if self.process.state() == QProcess.Running:
            self.process.kill()
            self.modify_hosts('remove')
            subprocess.run(['taskkill','/im','server_local.exe','/f'])
        event.accept()
    
    def init_ui(self):
        self.setWindowTitle("Server Control")
        layout = QVBoxLayout()
        
        self.query_input = QTextEdit()
        self.query_input.setPlaceholderText("Enter query...")
        self.query_input.setAcceptRichText(False)
        self.query_input.setLineWrapMode(QTextEdit.WidgetWidth)
        layout.addWidget(self.query_input)
        
        # 添加预设下拉菜单
        self.preset_combo = QComboBox()
        self.preset_combo.addItem("选择预设...")
        # 添加15个表情包选项
        emojis = ["😂","😊","😍","🤔","😎","😢","😡","🤯","👻","💩","👍","👏","🙏","❤️","🔥"]
        for emoji in emojis:
            self.preset_combo.addItem(emoji)
        # 添加特殊字符选项
        self.preset_combo.addItem("换行符 (\\n)")
        self.preset_combo.addItem("制表符 (\\t)")
        
        self.preset_combo.currentTextChanged.connect(self.apply_preset)
        layout.addWidget(self.preset_combo)
        
        self.start_btn = QPushButton("Start Server")
        self.start_btn.clicked.connect(self.start_server)
        layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("Stop Server")
        self.stop_btn.clicked.connect(self.stop_server)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)
        
        self.status_label = QLabel("Server status: Stopped")
        layout.addWidget(self.status_label)
        
        self.setLayout(layout)
    
    def apply_preset(self, text):
        if text == "换行符 (\\n)":
            self.query_input.setText("\n")
        elif text == "制表符 (\\t)":
            self.query_input.setText("\t")
        elif text != "选择预设..." and len(text) > 0:
            self.query_input.setText(text)
    
    def modify_hosts(self, action='add'):
        """修改hosts文件"""
        cmd = f'NSudoL.exe -UseCurrentConsole -U:T -P:E cmd /c '
        if action == 'add':
            cmd += f'echo {IP} ltalk.speech.sogou.com >C:\\Windows\\System32\\drivers\\etc\\hosts'
        else:

            cmd += 'type nul > C:\\Windows\\System32\\drivers\\etc\\hosts'
        cmd += ' && ipconfig /flushdns && ipconfig /flushdns && ipconfig /flushdns  && powershell Clear-DnsClientCache'
        
        try:
            subprocess.run(cmd, shell=True, check=True)
            print("修改hosts成功")
            if action == 'add':
                QMessageBox.information(self, "提示", "更改需等待几秒并让手表重新连接热点生效<br />若迟迟不生效，请在电脑重启热点或/和执行ipconfig /flushdns<br />有时也许要重启电脑（因为flushdns是《玄》学）")
        except subprocess.CalledProcessError as e:
            print(f"修改hosts失败: {e}")
        
    def start_server(self):
        
        query = self.query_input.toPlainText()
        if not query:
            if not "\n" in query and not "\t" in query and not " " in query:
                self.status_label.setText("Error: Query cannot be empty")
                return
        self.modify_hosts('add')  # 启动前修改hosts   
        # 打印调试信息
        print(f"Starting server with query: {query}")
        
        # 设置工作目录为当前目录
        self.process.setWorkingDirectory("d:\\stapp")
        
        # 启动进程并检查错误
        self.process.start("server_local", [f"--query={query}"])
        if not self.process.waitForStarted(5000):  # 等待5秒
            error = self.process.error()
            self.status_label.setText(f"Error: {error}")
            print(f"Failed to start server: {error}")
            return
            
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.preset_combo.setEnabled(False)  # 禁用预设下拉菜单
        self.status_label.setText("Server status: Running")
    
    def stop_server(self):
        if self.process.state() == QProcess.Running:
            self.process.kill()
            subprocess.run(['taskkill','/im','server_local.exe','/f'])
        self.modify_hosts('remove')  # 停止后清空hosts
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.preset_combo.setEnabled(True)
        self.status_label.setText("Server status: Stopped")
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def set_hotspot_dns():
    try:
        # 使用PowerShell命令设置DNS
        cmd = [
            'powershell',
            'Get-NetAdapter | '
            'Where-Object { $_.InterfaceDescription -match "Microsoft (Wi-Fi Direct|Hosted Network) Virtual Adapter" } | '
            'Set-DnsClientServerAddress -ServerAddresses "192.168.10.100"'
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        os.system('ipconfig /flushdns')
        
        if result.returncode == 0:
            print("成功设置DNS")
        else:
            print(f"设置DNS失败: {result.stderr}")
            
            
            
    except Exception as e:
        os.remove("./data.hex")
        QMessageBox.critical(
            None,
            "Error",
            f"无法配置DNS：{result.stderr if result.stderr else str(e)}"
        )
        print(f"设置DNS时发生错误: {str(e)}")

    


if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
        sys.exit()
    
    app = QApplication(sys.argv)
    if os.path.exists("./data.hex"):
        with open("./data.hex", "r") as e:
            data = e.read()
        if data != "1":
            QMessageBox.information(None, "提示","点击确定为第一次使用做准备", QMessageBox.Ok)
            # subprocess.run('powershell Get-NetAdapter | Where-Object { $_.InterfaceDescription -match "Microsoft (Wi-Fi Direct|Hosted Network) Virtual Adapter" } | Set-DnsClientServerAddress -ServerAddresses ' + IP)
            set_hotspot_dns()
    else:
        QMessageBox.information(None, "提示","点击确定为第一次使用做准备", QMessageBox.Ok)
        # subprocess.run('powershell Get-NetAdapter | Where-Object { $_.InterfaceDescription -match "Microsoft (Wi-Fi Direct|Hosted Network) Virtual Adapter" } | Set-DnsClientServerAddress -ServerAddresses ' + IP)
        set_hotspot_dns()
    with open(file="./data.hex", mode="w") as f:
        f.write("1")
    window = ServerControlGUI()
    window.show()
    sys.exit(app.exec())