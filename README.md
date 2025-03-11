# Gaia Chat 全自动聊天 项目        

这是一个使用 SOCKS5 代理进行并发聊天的 Python 项目，支持多线程请求（默认60线程）、每分钟统计、成功率进度条，并以北京时间显示日志。项目输出为中文，界面美观，适合需要通过 API 进行批量请求的用户。

小白运行指南
1:打开gaia_chat.py 修改API、问题和动态代理（有附带题库）
2:安装 Python 3：检查版本：:```python3 --version````print("Hello, GitHub!")`
如果需要安装，使用 Homebrew：/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python
3:安装依赖：确保 pip3 可用 print("python3 -m ensurepip --upgrade")`
 安装库：```pip3 install requests
pip3 install PySocks  # 用于SOCKS5代理支持
pip3 install pytz     # 用于北京时间支持
```
4:保存并编辑脚本：
将上述代码保存为 gaia_chat_v3.py。
编辑文件：```nano gaia_chat_v3.py```
在 API_KEYS 中填入你的 API Key，例如：
在 QUESTIONS 中填入问题（已提供中文示例），例如：
在SOCKS5 代理配置。

保存并退出（Ctrl+x，Y，回车）。
5:赋予执行权限：
```chmod +x gaia_chat_v3.py```
6:运行脚本：
```./gaia_chat_v3.py```

需要手动修改API和代理 可以运行在macos ubuntu wsl上

`print("Hello, GitHub!")`


注意：该项目需要消耗代理较大 没有动态代理的可以使用abc代理

https://www.abcproxy.com/?code=RYPC0RI9

动态代理  75元/10G    360元/50G


![image](https://github.com/user-attachments/assets/60c93e6c-60a6-409f-aa09-f09ab0903a46)
