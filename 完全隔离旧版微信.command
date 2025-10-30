#!/bin/bash
# 完全隔离旧版微信启动脚本

echo "创建完全隔离环境..."

# 创建独立容器
CONTAINER_PATH="$HOME/WeChatContainers/WeChatLegacy"
mkdir -p "$CONTAINER_PATH/Data" "$CONTAINER_PATH/Config" "$CONTAINER_PATH/Cache"

# 复制应用（可选）
if [ ! -d "$CONTAINER_PATH/WeChatLegacy.app" ]; then
    cp -R "/Applications/WeChatLegacy.app" "$CONTAINER_PATH/"
fi

# 设置环境变量
export WECHAT_DATA_PATH="$CONTAINER_PATH/Data"
export WECHAT_CONFIG_DIR="$CONTAINER_PATH/Config"
export WECHAT_CACHE_DIR="$CONTAINER_PATH/Cache"
export HOME="$CONTAINER_PATH"  # 临时修改HOME变量

echo "启动完全隔离的旧版微信..."
"$CONTAINER_PATH/WeChatLegacy.app/Contents/MacOS/WeChatLegacy" &

# 恢复HOME变量
export HOME="/Users/$(whoami)"

# 检查进程
sleep 5
echo "当前运行的微信进程:"
ps aux | grep -i WeChatLegacy | grep -v grep
