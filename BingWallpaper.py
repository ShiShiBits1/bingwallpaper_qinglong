#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
青龙面板：Bing 每日壁纸 + 飞书群推送
成功：发送 UHD 壁纸图片
失败：发送文本报警
"""

import os
import sys
import json
import requests
from datetime import datetime

# ------------- 用户配置 -------------
# 飞书机器人应用配置
FS_APP_ID = os.getenv("FEISHU_APP_ID") or "xxxx_xxxxxxxxxx"
FS_APP_SECRET = os.getenv("FEISHU_APP_SECRET") or "xxxxxxxxxxxxxxxxxxxxxx"
FS_CHAT_ID = "oc_xxxxxxxxxxxxxxxxxxxxx"  # 指定群组ID
# ------------- 用户配置 -------------

TIMEOUT = 20
BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bingwallpaper")
TODAY = datetime.now().strftime("%Y-%m-%d")
YEAR_MONTH = datetime.now().strftime("%Y%m")
SAVE_DIR = os.path.join(BASE_DIR, YEAR_MONTH)
os.makedirs(SAVE_DIR, exist_ok=True)
SAVE_PATH = os.path.join(SAVE_DIR, f"{TODAY}.jpg")

# ---------- 工具函数 ----------
def get_tenant_access_token():
    """获取飞书应用的tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": FS_APP_ID,
        "app_secret": FS_APP_SECRET
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=TIMEOUT)
        result = response.json()
        if result.get("code") == 0:
            return result["tenant_access_token"]
        else:
            raise RuntimeError(f"获取token失败: {result}")
    except Exception as e:
        raise RuntimeError(f"获取token异常: {e}")

def fs_send_card(title: str, content: str, image_key: str = None):
    """发送卡片消息到飞书群组"""
    token = get_tenant_access_token()
    
    # 构建卡片内容
    card_elements = [
        {
            "tag": "div",
            "text": {
                "content": content,
                "tag": "lark_md"
            }
        }
    ]
    
    # 如果有图片，添加图片元素
    if image_key:
        card_elements.append({
            "tag": "img",
            "img_key": image_key,
            "alt": {
                "tag": "plain_text",
                "content": "Bing每日壁纸"
            }
        })
    
    card_content = {
        "config": {
            "wide_screen_mode": True
        },
        "elements": card_elements,
        "header": {
            "title": {
                "content": title,
                "tag": "plain_text"
            },
            "template": "blue"
        }
    }
    
    # 发送消息
    url = "https://open.feishu.cn/open-apis/im/v1/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=utf-8"
    }
    params = {"receive_id_type": "chat_id"}
    data = {
        "receive_id": FS_CHAT_ID,
        "msg_type": "interactive",
        "content": json.dumps(card_content)
    }
    
    try:
        response = requests.post(url, headers=headers, params=params, json=data, timeout=TIMEOUT)
        result = response.json()
        print("[飞书卡片]", result)
        return result
    except Exception as e:
        print(f"[飞书卡片] 发送失败: {e}")
        raise

def fs_upload_image(image_path: str):
    """上传图片到飞书并返回image_key"""
    token = get_tenant_access_token()
    
    url = "https://open.feishu.cn/open-apis/im/v1/images"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        with open(image_path, "rb") as f:
            # 修复：使用正确的文件上传格式
            files = {
                "image": (os.path.basename(image_path), f, "image/jpeg")
            }
            data = {"image_type": "message"}
            response = requests.post(
                url, 
                headers=headers, 
                files=files, 
                data=data,  # 使用data而不是params
                timeout=TIMEOUT
            )
            
        result = response.json()
        print(f"[图片上传] 响应: {result}")  # 添加调试信息
        
        if result.get("code") == 0:
            return result["data"]["image_key"]
        else:
            raise RuntimeError(f"上传图片失败: {result}")
    except Exception as e:
        raise RuntimeError(f"上传图片异常: {e}")

def fs_send_text_card(text: str):
    """发送纯文本卡片消息"""
    fs_send_card("📢 Bing壁纸通知", text)

def fs_send_image_card(image_path: str, image_info: dict = None):
    """发送带图片的卡片消息"""
    try:
        image_key = fs_upload_image(image_path)
        title = f"🖼️ Bing每日壁纸 - {TODAY}"
        
        # 构建卡片内容，包含图片介绍
        content_parts = ["**今日壁纸已更新**\n"]
        
        if image_info:
            # 添加图片标题
            if image_info.get('title'):
                content_parts.append(f"📖 **{image_info['title']}**\n")
            
            # 添加图片描述
            if image_info.get('copyright'):
                content_parts.append(f"📝 {image_info['copyright']}\n")
            
            # 添加拍摄地点（如果有）
            if image_info.get('copyrightlink'):
                content_parts.append(f"🔗 [了解更多]({image_info['copyrightlink']})\n")
        
        # 添加基本信息
        content_parts.extend([
            f"📅 日期：{TODAY}",
            f"🎨 来源：Bing官方",
            f"📱 分辨率：UHD高清"
        ])
        
        content = "\n".join(content_parts)
        fs_send_card(title, content, image_key)
    except Exception as e:
        # 如果图片发送失败，降级为文本消息
        fs_send_text_card(f"✅ [{TODAY}] 壁纸下载成功，但图片上传失败：{e}")

# ---------- 主逻辑 ----------
if os.path.exists(SAVE_PATH):
    print(f"[{TODAY}] 壁纸已存在，跳过")
    sys.exit(0)

# 1. 获取壁纸地址和信息
api = "https://www.bing.com/HPImageArchive.aspx"
params = {"format": "js", "idx": 0, "n": 1, "mkt": "zh-CN"}

try:
    response = requests.get(api, params=params, timeout=TIMEOUT)
    bing_data = response.json()
    image_data = bing_data["images"][0]
    
    urlbase = image_data["urlbase"]
    
    # 提取图片信息
    image_info = {
        'title': image_data.get('title', ''),
        'copyright': image_data.get('copyright', ''),
        'copyrightlink': image_data.get('copyrightlink', ''),
        'quiz': image_data.get('quiz', ''),
        'wp': image_data.get('wp', True),
        'hsh': image_data.get('hsh', ''),
        'drk': image_data.get('drk', 1),
        'top': image_data.get('top', 1),
        'bot': image_data.get('bot', 1)
    }
    
    print(f"[图片信息] 标题: {image_info['title']}")
    print(f"[图片信息] 版权: {image_info['copyright']}")
    
except Exception as e:
    fs_send_text_card(f"❌ [{TODAY}] 获取 Bing API 失败：{e}")
    sys.exit(1)

# 2. 下载图片
for size in ["_UHD.jpg", "_1920x1080.jpg"]:
    img_url = f"https://www.bing.com{urlbase}{size}"
    try:
        r = requests.get(img_url, stream=True, timeout=TIMEOUT)
        r.raise_for_status()
        with open(SAVE_PATH, "wb") as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
        break
    except Exception:
        continue
else:
    fs_send_text_card(f"❌ [{TODAY}] 壁纸下载失败，所有分辨率均不可用")
    sys.exit(1)

# 3. 发送成功通知（带图片和介绍的卡片）
fs_send_image_card(SAVE_PATH, image_info)
print(f"[{TODAY}] 壁纸下载并推送成功")
