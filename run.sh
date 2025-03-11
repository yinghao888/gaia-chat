#!/bin/bash

# 设置颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # 无颜色

# 检查 Python3 是否安装
echo -e "${YELLOW}正在检查 Python3 环境...${NC}"
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}错误: 未找到 Python3，请先安装 Python3！${NC}"
    echo -e "${YELLOW}建议使用以下命令安装（macOS）:${NC}"
    echo "  /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    echo "  brew install python"
    exit 1
fi
echo -e "${GREEN}✔ Python3 已安装！${NC}"

# 检查 pip3 是否可用
echo -e "${YELLOW}正在检查 pip3...${NC}"
if ! command -v pip3 &> /dev/null; then
    echo -e "${YELLOW}pip3 未找到，正在安装...${NC}"
    python3 -m ensurepip --upgrade
fi
echo -e "${GREEN}✔ pip3 已准备好！${NC}"

# 安装依赖
echo -e "${YELLOW}正在安装依赖...${NC}"
pip3 install -r requirements.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✔ 依赖安装成功！${NC}"
else
    echo -e "${RED}错误: 依赖安装失败，请检查网络或 requirements.txt 文件！${NC}"
    exit 1
fi

# 运行程序
echo -e "${YELLOW}正在启动程序...${NC}"
python3 gaia_chat.py
