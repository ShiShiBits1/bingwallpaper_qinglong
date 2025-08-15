#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
青龙面板：每日 Bing 4K 壁纸 → Emlog Pro API 发布
无需下载图片，直接引用 Bing 4K 直链
"""
import datetime
import requests

# ========== 只需修改以下 4 项 ==========
DOMAIN      = "https://emlog.xxxx.com"      # 结尾不要 /
API_KEY     = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
AUTHOR_UID  = 1                          # 作者 UID
SORT_ID     = 1                          # 分类 ID
# =======================================

DATE   = datetime.datetime.now()
TODAY  = DATE.strftime("%Y-%m-%d")

# 1. 获取当天 4K 直链
api = "https://www.bing.com/HPImageArchive.aspx"
params = {"format": "js", "idx": 0, "n": 1, "mkt": "zh-CN"}
data = requests.get(api, params=params, timeout=20).json()
img = data["images"][0]
title_zh   = img["copyright"]            # 中文标题
img_url    = f"https://cn.bing.com{img['urlbase']}_UHD.jpg"
img_url_4k    = f"https://cn.bing.com{img['urlbase']}_UHD.jpg"
img_url_1080    = f"https://cn.bing.com{img['urlbase']}_1920x1080.jpg"
# 2. 构造正文
content = f"""
<div style="font-size:16px;line-height:1.8;">
  <p style="margin-bottom:.5em;">📅 <strong>{TODAY}</strong> · Bing 每日 4K 壁纸</p>
  <h2 style="margin:.3em 0 .6em;color:#0066cc;">{title_zh}</h2>

  <!-- 4K 预览图 -->
  <p>
    <img src="{img_url_4k}" alt="{title_zh}"
         style="width:100%;max-width:100%;height:auto;border-radius:8px;box-shadow:0 4px 12px rgba(0,0,0,.15);">
  </p>

  <!-- 下载按钮 -->
  <p style="margin-top:1em;">
    <a href="{img_url_4k}" target="_blank" rel="noopener"
       style="display:inline-block;margin-right:.8em;padding:.6em 1.2em;background:#ff3366;color:#fff;border-radius:4px;text-decoration:none;">
      📥 4K 直链
    </a>
    <a href="{img_url_1080}" target="_blank" rel="noopener"
       style="display:inline-block;padding:.6em 1.2em;background:#3366ff;color:#fff;border-radius:4px;text-decoration:none;">
      📥 1080P 直链
    </a>
  </p>

  <!-- 版权说明 -->
  <p style="font-size:.85em;color:#666;margin-top:1em;">
    图片来源：© Microsoft Bing
  </p>
</div>
"""

# 3. 发布文章
payload = {
    "api_key": API_KEY,
    "title": f"Bing 每日壁纸 {TODAY}",
    "content": content,
    "author_uid": AUTHOR_UID,
    "sort_id": SORT_ID,
    "draft": "n",
    "auto_cover": "y"
}
r = requests.post(f"{DOMAIN}/?rest-api=article_post", data=payload, timeout=20)
r.raise_for_status()
resp = r.json()
if resp.get("code") != 0:
    raise RuntimeError(resp)
print("已发布，文章 ID:", resp["data"]["article_id"])