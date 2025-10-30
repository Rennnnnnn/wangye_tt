#!/bin/bash

# 配置变量
BACKUP_DRIVE="/Volumes/renxiuqing1"
BACKUP_DIR="$BACKUP_DRIVE/微信备份"
NEW_WECHAT_DIR="$HOME/Library/Containers/com.tencent.xinWeChat/Data"
OLD_WECHAT_DIR="$HOME/Library/Containers/com.tencent.wechat.legacy/Data"
CURRENT_DATE=$(date +%Y-%m-%d)
DAILY_BACKUP_DIR="$BACKUP_DIR/$CURRENT_DATE"

# 检查备份驱动器是否已连接
if [ ! -d "$BACKUP_DRIVE" ]; then
    echo "错误：移动硬盘未连接或未正确挂载"
    exit 1
fi

# 创建备份目录结构
mkdir -p "$DAILY_BACKUP_DIR/新微信备份"
mkdir -p "$DAILY_BACKUP_DIR/旧微信备份"

# 使用rsync进行增量备份（新微信）
if [ -d "$NEW_WECHAT_DIR" ]; then
    rsync -av --delete --link-dest="$BACKUP_DIR/latest/新微信备份" "$NEW_WECHAT_DIR/" "$DAILY_BACKUP_DIR/新微信备份/"
else
    echo "警告：新微信目录不存在"
fi

# 使用rsync进行增量备份（旧微信）
if [ -d "$OLD_WECHAT_DIR" ]; then
    rsync -av --delete --link-dest="$BACKUP_DIR/latest/旧微信备份" "$OLD_WECHAT_DIR/" "$DAILY_BACKUP_DIR/旧微信备份/"
else
    echo "警告：旧微信目录不存在"
fi

# 更新最新备份链接
rm -f "$BACKUP_DIR/latest"
ln -s "$DAILY_BACKUP_DIR" "$BACKUP_DIR/latest"

echo "备份完成于: $DAILY_BACKUP_DIR"