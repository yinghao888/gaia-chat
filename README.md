# 🌟 Gaia Chat 全自动聊天项目 

这是一个通过 SOCKS5 代理进行并发聊天的 Python 项目，支持多线程请求、每分钟统计、成功率进度条，并以北京时间显示日志。
---

 🌹作者TG：@yinghao66 BUG反馈 动态住宅代理购买 
 
 支持的运行环境 macOS Ubuntu WSL

 注意事项
代理消耗：本项目对代理流量消耗较大，建议使用动态代理。

推荐代理：如果没有动态代理，可以使用 ABC 代理：
官网：[ABC Proxy](https://www.abcproxy.com/?code=RYPC0RI9)

价格：75 元/10G，360 元/50G
请联系作者购买

动态代理效果更佳，推荐购买使用。

## 📋 小白运行指南

### 1. 修改配置文件
- 打开 `gaia_chat.py` 文件，修改以下内容：
  - **API_KEYS**：填入你的 API Key 列表。
    ```python
    API_KEYS = [
        "gaia-xxx-xxx-xxx",
        "gaia-yyy-yyy-yyy",
        # ... 继续添加
    ]
    ```
  - **QUESTIONS**：填入你想提问的问题列表（项目已附带题库）。
    ```python
    QUESTIONS = [
        "美国总统是谁",
        "法国的首都是哪里",
        "太阳是如何工作的",
    ]
    ```
  - **SOCKS5 代理配置**：根据你的动态代理信息修改。
    ```python
    PROXY_HOST = "你的代理主机"
    PROXY_PORT = 你的代理端口
    PROXY_USER = "你的代理用户名"
    PROXY_PASS = "你的代理密码"
    ```

### 2. 安装 Python 3
- 检查 Python 3 是否已安装：
  ```bash
  python3 --version

- 如果未安装，使用 Homebrew 安装：
  ```bash
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
  brew install python

### 3. 安装依赖
- 确保 pip3 可用：
  ```bash
  python3 -m ensurepip --upgrade

  - 安装所需库：：
  ```bash
  pip3 install requests
  pip3 install PySocks  # 用于SOCKS5代理支持
  pip3 install pytz     # 用于北京时间支持

### 4. 保存并编辑脚本
- 将代码保存为 gaia_chat.py（如果文件名不同，请调整）。
- 使用 nano 编辑文件：
  ```bash
  nano gaia_chat.py
- 保存并退出：按 Ctrl+X，输入 Y，然后按回车。

### 5.赋予执行权限
- 给脚本赋予可执行权限
  ```bash
  chmod +x gaia_chat.py

### 6.执行脚本
  ```bash
  ./gaia_chat.py
