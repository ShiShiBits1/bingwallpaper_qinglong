# Bing必应每日壁纸项目

## 项目简介
这个项目包含两个主要工具，用于获取Bing每日壁纸并进行不同方式的发布和推送：
1. `bing_emlog.py`: 将Bing每日4K壁纸发布到Emlog Pro博客
2. `BingWallpaper.py`: 下载Bing每日壁纸并推送到飞书群组，并支持自动上传壁纸到GitHub仓库

## 功能特点
- 自动获取Bing每日高清壁纸（支持UHD和1080P分辨率）
- 无需下载图片，直接引用Bing原图链接（适用于博客发布）
- 本地保存壁纸并按年月分类管理
- 飞书群组推送，支持图文卡片展示
- 自动上传每日壁纸到GitHub仓库（需配置Token和仓库信息）
- 异常处理和失败通知
- 支持青龙面板定时执行

## 技术栈
- Python 3
- requests库（网络请求）
- datetime库（日期处理）
- os库（文件系统操作）
- json库（JSON数据处理）

## 文件结构
```
Bing必应每日壁纸/
├── README.md                  # 项目说明文档
├── bing_emlog.py              # Emlog博客发布脚本
├── BingWallpaper.py           # 飞书推送及GitHub上传脚本
└── bingwallpaper/             # 壁纸存储目录
    └── YYYYMM/                # 按年月分类的壁纸文件夹
        └── YYYY-MM-DD.jpg     # 壁纸文件
```

## 安装说明
1. 克隆或下载项目到本地
2. 安装所需依赖：
   ```bash
   pip install requests
   ```

## 配置说明
### bing_emlog.py 配置
编辑文件中的以下参数：
```python
DOMAIN      = "https://emlog.xxxx.com"      # 博客域名，结尾不要加/
API_KEY     = "xxxxxxxxxxxxxxxxxxxxxxxxxxxx"  # Emlog Pro API密钥
AUTHOR_UID  = 1                          # 作者UID
SORT_ID     = 1                          # 分类ID
```

### BingWallpaper.py 配置
编辑文件中的以下参数或设置环境变量：
```python
FS_APP_ID = os.environ.get("FEISHU_APP_ID") or os.getenv("FEISHU_APP_ID") or "xxxx_xxxxxxxxxx"  # 飞书应用ID
FS_APP_SECRET = os.environ.get("FEISHU_APP_SECRET") or os.getenv("FEISHU_APP_SECRET") or "xxxxxxxxxxxxxxxxxxxxxx"  # 飞书应用密钥
FS_CHAT_ID = "oc_xxxxxxxxxxxxxxxxxxxxx"  # 飞书群组ID
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN") or os.getenv("GITHUB_TOKEN")  # GitHub访问Token
GITHUB_REPO = os.environ.get("GITHUB_REPO") or os.getenv("GITHUB_REPO")    # GitHub仓库名
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH") or os.getenv("GITHUB_BRANCH")  # 分支名
GITHUB_PATH = os.environ.get("GITHUB_PATH") or os.getenv("GITHUB_PATH")        # 上传目标路径
```
> 推荐优先使用 `os.environ.get()` 获取环境变量，兼容青龙面板环境。

## 自动上传壁纸到GitHub仓库
- `BingWallpaper.py` 支持自动将每日下载的壁纸图片上传到指定GitHub仓库。
- 需在青龙面板或本地环境设置好 `GITHUB_TOKEN`、`GITHUB_REPO`、`GITHUB_BRANCH`、`GITHUB_PATH` 等变量。
- 上传失败会有异常提示。

## 使用方法
### 手动执行
1. 执行Emlog发布脚本：
   ```bash
   python bing_emlog.py
   ```
2. 执行飞书推送及GitHub上传脚本：
   ```bash
   python BingWallpaper.py
   ```

### 青龙面板定时执行
添加定时任务，例如每天6:00执行：
```
0 6 * * * python /path/to/bing_emlog.py
0 6 * * * python /path/to/BingWallpaper.py
```

## 注意事项
1. 确保网络连接正常，能够访问Bing、飞书API和GitHub API
2. 定期检查配置信息是否有效（特别是API密钥、应用凭证和GitHub Token）
3. 飞书推送脚本会自动创建壁纸存储目录，无需手动创建
4. 如果壁纸已存在，脚本会自动跳过下载和推送
5. 异常情况会通过飞书消息通知（仅飞书推送脚本支持）
6. 青龙面板环境变量建议用 `os.environ.get()` 获取，避免获取不到的问题

## 项目更新日志
- 初始版本：实现Bing壁纸获取、Emlog发布和飞书推送功能
- 优化版本：增加异常处理、图片上传失败降级处理
- 新增功能：自动上传壁纸到GitHub仓库，修复青龙面板环境变量兼容问题

## 许可证
本项目采用MIT许可证，详情请见LICENSE文件。

## 联系方式
如有问题或建议，请联系项目维护者。
