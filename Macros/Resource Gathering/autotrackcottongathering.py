# Name: Auto-Track Cotton Gathering
# Description: Auto-Track Cotton Gathering
# Author: zny05
# Shard: New World 2025
# Date: Tue Jan 20 2026

# 名称: 自动追踪采棉花 (语法修复版)
# Name: Auto-Track Cotton Gathering (Syntax Fixed Version)
# 修正: 移除了自定义函数，改为纯扁平化循环，解决缩进导致的语法错误
# Fix: Removed custom functions in favor of a flat loop to resolve indentation syntax errors.
# 状态: 兼容性最强
# Status: Maximum Compatibility

from Assistant import Engine

# --- 配置区 ---
# --- Configuration Section ---
# 棉花 ID 列表
# Cotton ID List
COTTON_IDS = [0x0C51, 0x0C52, 0x0C53, 0x0C54]
# 搜索半径
# Search Radius
SEARCH_RANGE = 12 
# --------------

# 遍历屏幕内物品
# Iterate through items on screen
for item in Engine.Items:
    # 检查是否为棉花
    # Check if item is cotton
    if item.ID in COTTON_IDS:
        # 检查距离
        # Check distance
        if item.Distance <= SEARCH_RANGE:
            target_serial = item.Serial
            tx = item.X
            ty = item.Y
            
            # 1. 距离太远，执行移动
            # 1. Target too far: Execute movement
            if item.Distance > 2:
                px = Engine.Player.X
                py = Engine.Player.Y
                
                # 精简的移动判定逻辑
                # Streamlined movement logic
                if px < tx and py < ty: Run("South")
                elif px > tx and py > ty: Run("North")
                elif px < tx and py > ty: Run("East")
                elif px > tx and py < ty: Run("West")
                elif px < tx: Run("East")
                elif px > tx: Run("West")
                elif py < ty: Run("South")
                elif py > ty: Run("North")
                
                # 移动步进延迟
                # Movement step delay
                Pause(200)
                # 终止本次循环，让角色移动一步后重新检测坐标
                # Terminate current loop: Allow character to step once before re-scanning coordinates
                break

            # 2. 距离足够近，执行采集
            # 2. Target within range: Execute harvesting
            if item.Distance <= 2:
                UseObject(target_serial)
                # 针对 XmlSpawner: 加入忽略列表
                # Specific to XmlSpawner: Add to ignore list
                IgnoreObject(target_serial)
                SysMessage("采集完成，前往下一处...Harvesting complete, moving to the next location...")
                Pause(600)
                break

# 脚本基础循环延迟
# Base script loop delay
Pause(100)