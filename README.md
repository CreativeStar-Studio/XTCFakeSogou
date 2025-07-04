# 搜狗输入法欺骗工具 XTCFakeSogou

<a href="https://creativestar-studio.github.io/XTCFakeSogou/" style="color: green">查看教程</a>

## 项目描述
这是一个通过欺骗搜狗输入法服务器响应数据包，实现在支持搜狗输入法的XTC智能手表上发送特殊符号和表情的工具。包含两个主要组件：

1. `gui.py` - 图形界面控制程序
2. `server_local.py` - 模拟sogouAPI的本地服务器

## 功能特点

- 🎭 预置15种不同表情符号（也可自定义内容）
- ↩️ 支持发送特殊字符（换行符、制表符）
- 🖥️ 简洁易用的图形界面
- 🔄 自动修改hosts文件实现流量劫持
- ⚡ 一键启动/停止本地欺骗服务器

## 使用说明

### 准备工作
1. 确保已安装Python 3.8+
2. 安装依赖库：
```bash
pip install PySide6 flask flask-cors pywin32
```
3. 下载M2-Team的`NSudoLC.exe`重命名为`NSudoL.exe`丢进`/src/`里

### 启动步骤
1. 以管理员身份运行`gui.py`
2. 在输入框中输入要发送的内容
3. 点击"Start Server"按钮启动服务
4. 在手表上使用搜狗输入法进行测试

### 特殊符号发送
- 通过下拉菜单选择预设的表情符号或特殊字符
- 支持自定义文本输入

## 技术实现

- 通过修改hosts文件将`ltalk.speech.sogou.com`指向本地
- 本地服务器(`server_local.py`)模拟sougouAPI响应
- 使用PySide6构建图形界面
- 需要管理员权限修改系统hosts文件

## 注意事项

⚠️ 使用前请确保关闭其他占用80端口的程序  
⚠️ 修改hosts文件可能需要重启热点或执行`ipconfig /flushdns`才能生效  
⚠️ 本工具仅供学习交流使用

## 文件说明

- `gui.py` - 主控制界面程序
- `server_local.py` - 模拟搜狗输入法API的本地服务器
- `data.hex` - 首次运行标记文件(自动生成)

## 作者
团队成员（XTC-星旬）

## 赞助
本项目需要使用M2-Team NSudo项目的二进制文件
