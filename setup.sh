#!/bin/bash

# 检查Python版本
python3 --version

# 安装Python依赖
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

echo "环境配置完成！"
echo "使用方法："
echo "1. 激活虚拟环境：source venv/bin/activate"
echo "2. 运行示例：python example.py 或 python vehicle_sdk_example.py" 