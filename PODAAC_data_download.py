"""
    @Author: Su Changwei
    @Date: 2026-08-03
    @Description: Harmony method for NASA PODAAC regional data downloading
"""
from pathlib import Path
from datetime import datetime

import earthaccess
from harmony import Client, Collection, Request, BBox

# ------------------- 参数设置 -----------------------

# PM v2.81 Collection Concept ID
COLLECTION_ID = "C2805331435-POCLOUD"

START_TIME = datetime(2026, 1, 1, 0, 0, 0)
END_TIME = datetime(2026, 7, 31, 23, 59, 59)

# 顺序必须是：西、南、东、北
WEST = 140.0
SOUTH = 32.0
EAST = 152.0
NORTH = 40.0

SAVE_DIR = Path("E:/data/VIIRS_L3S/PM_Night_KE_nc")
SAVE_DIR.mkdir(parents=True, exist_ok=True)

#-----------------------------------------------------

# 登录
# 第一次登录可改为：
# earthaccess.login(strategy="interactive", persist=True)

earthaccess.login(strategy="netrc") # 要在用户名下配置好.netrc或_netrc文件，里面包含Earthdata的用户名和密码

# Harmony 会读取 _netrc 中的 Earthdata 账号
client = Client()

# 构造空间、时间和变量裁剪请求

request = Request(
    collection=Collection(id=COLLECTION_ID),

    spatial=BBox(
        WEST,
        SOUTH,
        EAST,
        NORTH,
    ),

    temporal={
        "start": START_TIME,
        "stop": END_TIME,
    },

    # 仅选择 PM 夜间文件
    granule_name=["*-LEO_PM_N-ACSPO_V2.81-*"],

    # 只保留研究中常用变量
    variables=[
        "sea_surface_temperature",
        "quality_level",
        "sses_bias",
        "sses_standard_deviation",
        "sst_dtime",
        "sst_count",
        "sst_source",
        "satellite_zenith_angle",
        "wind_speed",
        "sst_front_position",
        "sst_gradient_magnitude",
        "lat",
        "lon",
        "time",
    ],

    format="application/x-netcdf4",

    # 每个原始日期分别输出文件
    concatenate=False,
    ignore_errors=False,
)

if not request.is_valid():
    raise ValueError("Harmony 请求参数不合法")

# 提交任务
job_id = client.submit(request)

print(f"Harmony Job ID: {job_id}")
print("正在进行服务端空间裁剪……")

client.wait_for_processing(job_id,show_progress=True,)

# 下载裁剪后的文件
download_futures = client.download_all(job_id,directory=str(SAVE_DIR),overwrite=False,)

downloaded_files = []
for future in download_futures:
    try:
        file_path = future.result()
        downloaded_files.append(file_path)
        print(f"下载完成：{file_path}")
    except Exception as exc:
        print(f"文件下载失败：{exc}")

print(f"全部完成，共下载 {len(downloaded_files)} 个区域裁剪文件")
