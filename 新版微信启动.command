#!/bin/bash
# ============================================
# 新版微信启动脚本（支持双开）
# ============================================

echo "新版微信启动中..."
echo "检查是否已运行..."

# 只检查新版微信是否已运行，不强制关闭
if pgrep -q "WeChat$"; then
    echo "新版微信已在运行中"
else
    echo "启动新版微信..."
    # 设置新版微信环境变量
    export WECHAT_DATA_PATH="$HOME/Library/Containers/com.tencent.xinWeChat/Data"
    mkdir -p "$WECHAT_DATA_PATH"
    
    # 启动新版微信
    open -a WeChat
    echo "新版微信已启动"
fi

echo "等待10秒让微信完全启动..."
sleep 10
echo "请登录您的新版微信账号"