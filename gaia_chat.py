#!/usr/bin/env python3
import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import socks
import socket
from datetime import datetime
import pytz

# 用户配置区域
# -----------------------------------------------

# API Keys 列表（用户需填入自己的 API Key）
API_KEYS = [
    # 示例格式，请替换为真实的 API Key
    # "gaia-xxx-xxx-xxx",
    # "gaia-xxx-xxx-xxx",
]

# 问题列表（用户需填入自己的问题）
QUESTIONS = [
    # 示例问题，请根据需求修改
    "美国总统是谁",
    "法国的首都是哪里",
    "太阳是如何工作的",
]

# SOCKS5 代理配置（用户需根据自己的代理信息修改）
PROXY_HOST = "IP地址"
PROXY_PORT = 端口
PROXY_USER = "用户名"
PROXY_PASS = "密码"

# 固定 API 端点
URL = "https://gaias.gaia.domains/v1/chat/completions"

# 程序运行参数
THREAD_COUNT = 60  # 线程数
MAX_TOKENS = 50    # 最大返回 token 数
TIMEOUT = 15       # 请求超时时间（秒）
RETRY_COUNT = 5    # 重试次数
BACKOFF_FACTOR = 2  # 重试间隔因子
STATS_INTERVAL = 60  # 统计间隔（秒）

# -----------------------------------------------

# 全局计数器
success_count = 0
failure_count = 0
start_time = time.time()
last_stats_time = start_time  # 上次统计时间
minute_success = 0  # 每分钟成功次数
minute_failure = 0  # 每分钟失败次数
last_minute_start = start_time  # 每分钟开始时间

# ANSI 颜色代码，用于美化输出
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    PURPLE = '\033[95m'
    RESET = '\033[0m'

# 进度条函数，用于显示成功/失败比例
def progress_bar(success, failure, width=50):
    total = success + failure
    if total == 0:
        return "[暂无请求]"
    success_ratio = success / total
    success_width = int(width * success_ratio)
    failure_width = width - success_width
    return f"{Colors.GREEN}{'█' * success_width}{Colors.RED}{'█' * failure_width}{Colors.RESET} {success}/{total} ({success_ratio:.1%})"

# 设置 SOCKS5 代理
def setup_socks5_proxy():
    socks.set_default_proxy(socks.SOCKS5, PROXY_HOST, PROXY_PORT, username=PROXY_USER, password=PROXY_PASS)
    socket.socket = socks.socksocket
    print(f"{Colors.YELLOW}🔧 已设置 SOCKS5 代理: {PROXY_USER}@{PROXY_HOST}:{PROXY_PORT}{Colors.RESET}")

# 单次 API 请求函数
def chat_with_gaia(api_key, api_index, question, thread_id):
    global success_count, failure_count, minute_success, minute_failure
    headers = {
        "Authorization": f"Bearer {api_key}",
        "accept": "application/json",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {"role": "system", "content": "你是一个有用的助手。"},
            {"role": "user", "content": question}
        ],
        "max_tokens": MAX_TOKENS
    }
    
    session = requests.Session()
    retries = Retry(total=RETRY_COUNT, backoff_factor=BACKOFF_FACTOR, status_forcelist=[500, 502, 503, 504], allowed_methods=["POST"])
    session.mount("https://", HTTPAdapter(max_retries=retries))
    
    # 使用北京时间（CST, UTC+8）
    beijing_tz = pytz.timezone('Asia/Shanghai')
    timestamp = datetime.now(beijing_tz).strftime("%H:%M:%S")
    try:
        response = session.post(URL, headers=headers, json=data, timeout=TIMEOUT)
        response.raise_for_status()
        success_count += 1
        minute_success += 1
        print(f"{Colors.PURPLE}🕒[{timestamp}] {Colors.GREEN}🎉【成功】线程-{thread_id} | 第{success_count}次成功 🌟{Colors.RESET}")
        return "SUCCESS"
    except requests.exceptions.RequestException as e:
        failure_count += 1
        minute_failure += 1
        print(f"{Colors.PURPLE}🕒[{timestamp}] {Colors.RED}💥【失败】线程-{thread_id} | 第{failure_count}次失败 ⚠️{Colors.RESET}")
        if hasattr(e.response, 'status_code'):
            if e.response.status_code == 401:
                print(f"{Colors.PURPLE}🕒[{timestamp}] {Colors.YELLOW}⚠️【错误】API {api_index} | 状态: 401 | API认证失败 🚫{Colors.RESET}")
                return "FAILURE"
            elif e.response.status_code == 402:
                print(f"{Colors.PURPLE}🕒[{timestamp}] {Colors.YELLOW}⚠️【错误】API {api_index} | 状态: 402 | API额度不足，需要充值 🚫{Colors.RESET}")
                return "FAILURE"
        return "FAILURE"

# 主程序：并发聊天
def auto_chat_concurrent():
    global success_count, failure_count, start_time, last_stats_time, minute_success, minute_failure, last_minute_start
    
    # 设置 SOCKS5 代理
    setup_socks5_proxy()
    
    # 打印启动信息
    print(f"{Colors.BLUE}🚀 使用SOCKS5代理启动并发聊天（{THREAD_COUNT}线程，固定端点，每分钟统计） - 按 Ctrl+C 退出 ✨{Colors.RESET}")
    print(f"{Colors.CYAN}📊 总问题数: {len(QUESTIONS)} | 总API数: {len(API_KEYS)} 🌟{Colors.RESET}")
    print(f"{Colors.YELLOW}📡 端点: {URL}{Colors.RESET}\n")
    
    active_api_keys = API_KEYS.copy()  # 使用所有API，不移除
    
    while True:
        try:
            if len(active_api_keys) < THREAD_COUNT:
                print(f"{Colors.YELLOW}⚠️ 注意: 可用API数量 ({len(active_api_keys)}) 小于线程数 ({THREAD_COUNT}) 🚨{Colors.RESET}")
            
            # 随机选择问题和 API Key
            batch_questions = random.sample(QUESTIONS, min(THREAD_COUNT, len(QUESTIONS)))
            batch_api_keys = random.sample(active_api_keys, min(THREAD_COUNT, len(active_api_keys)))
            
            # 使用线程池并发执行
            with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
                futures = [
                    executor.submit(chat_with_gaia, api_key, API_KEYS.index(api_key), q, i+1)
                    for i, (api_key, q) in enumerate(zip(batch_api_keys, batch_questions))
                ]
                
                # 检查结果
                for future in futures:
                    future.result()
            
            # 检查是否到达统计间隔（每分钟）
            current_time = time.time()
            elapsed_time = current_time - last_stats_time
            if elapsed_time >= STATS_INTERVAL:
                total_minutes = int((current_time - start_time) // 60) + 1
                beijing_tz = pytz.timezone('Asia/Shanghai')
                timestamp = datetime.now(beijing_tz).strftime("%H:%M:%S")
                print(f"\n{Colors.BLUE}📈 🕒[{timestamp}] 第{total_minutes}分钟统计: {Colors.GREEN}成功: {success_count}次 🎉 {Colors.RED}失败: {failure_count}次 ⚠️{Colors.RESET}")
                print(f"{Colors.CYAN}📊 本分钟完成: {Colors.GREEN}{minute_success}次成功 🎉 {Colors.RED}{minute_failure}次失败 ⚠️{Colors.RESET}")
                print(f"{Colors.CYAN}📊 成功率: {progress_bar(success_count, failure_count)}{Colors.RESET}")
                print(f"{Colors.YELLOW}⏳ 运行时长: {int(current_time - start_time)}秒{Colors.RESET}\n")
                last_stats_time = current_time
                last_minute_start = current_time  # 重置分钟开始时间
                minute_success = 0  # 重置本分钟成功次数
                minute_failure = 0  # 重置本分钟失败次数
            
            # 如果没有可用API，退出
            if not active_api_keys:
                beijing_tz = pytz.timezone('Asia/Shanghai')
                timestamp = datetime.now(beijing_tz).strftime("%H:%M:%S")
                print(f"{Colors.RED}🚫 🕒[{timestamp}] 所有API均不可用，程序退出 💤{Colors.RESET}")
                break
            
        except KeyboardInterrupt:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            timestamp = datetime.now(beijing_tz).strftime("%H:%M:%S")
            print(f"\n{Colors.BLUE}🎬 🕒[{timestamp}] 程序已退出 | 总成功: {Colors.GREEN}{success_count}次 🎉{Colors.RESET} | 总失败: {Colors.RED}{failure_count}次 ⚠️{Colors.RESET}")
            print(f"{Colors.YELLOW}⏳ 总运行时长: {int(time.time() - start_time)}秒{Colors.RESET}")
            break
        except Exception as e:
            beijing_tz = pytz.timezone('Asia/Shanghai')
            timestamp = datetime.now(beijing_tz).strftime("%H:%M:%S")
            print(f"{Colors.RED}🛑 🕒[{timestamp}] 主线程错误: {e} 🚨{Colors.RESET}")
            time.sleep(5)

if __name__ == "__main__":
    if not API_KEYS or not QUESTIONS:
        print(f"{Colors.RED}❌ 错误: 请在 API_KEYS 和 QUESTIONS 中填入数据 🚫{Colors.RESET}")
    else:
        auto_chat_concurrent()
