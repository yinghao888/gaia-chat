# 🌟 Gaia Chat 全自动聊天项目

这是一个通过 SOCKS5 代理进行并发聊天的 Python 项目，支持多线程请求（默认 60 线程）、每分钟统计、成功率进度条，并以北京时间显示日志。
---

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
