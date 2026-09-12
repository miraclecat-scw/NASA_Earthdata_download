import xarray as xr
import pandas as pd
import numpy as np
import time
from pathlib import Path
# === 说明 ===
# 下载 HYCOM 年的 u 和 v 数据，并保存为 numpy 格式。
# 保存文件为npz其中包含u、v、time三个维度（类似于matlab的结构体）
# 每次运行会额外保存一个经纬度网格文件 lon_lat_grid.npz
# 运行前请先配置好相关参数，感谢您的使用！
# === 基本配置 ===
url = "https://tds.hycom.org/thredds/dodsC/GLBv0.08/expt_57.7"
outdir = Path("D:/data/HYCOM/Heichao_region/original_u_v_data/GLBv0.08_140_152_32_40") # 输出目录
outdir.mkdir(parents=True, exist_ok=True)

lon_range = slice(140, 152)
lat_range = slice(32, 40)
depth_level = 0
max_retry = 5 # 最大重试次数
pause_between = 5 # 重试间隔（秒）

# === 打开远端数据 ===
ds = xr.open_dataset(url, decode_times=False)

# 时间坐标转换
time_hours = ds["time"].values
ref_time = pd.to_datetime("2000-01-01 00:00:00")
time_coord = ref_time + pd.to_timedelta(time_hours, unit="h")
ds = ds.assign_coords(time=("time", time_coord))

# 提取经纬度网格（固定的，可以提前存一份）
lon = ds["lon"].sel(lon=lon_range).values
lat = ds["lat"].sel(lat=lat_range).values
np.savez(outdir / "lon_lat_grid.npz", lon=lon, lat=lat)
print("✅ 经纬度网格已保存：lon_lat_grid.npz")

# === 逐天保存为 npz ===
for day in pd.date_range("2017-06-01", "2017-09-31", freq="D"):
    outfile = outdir / f"HYCOM_uv_{day.strftime('%Y%m%d')}.npz"
    if outfile.exists():
        print(f"⏭️ 已存在：{outfile.name}")
        continue

    day_end = day + pd.Timedelta(days=1)
    print(f"/n▶ 下载 {day.strftime('%Y-%m-%d')} 数据...")

    success = False
    for attempt in range(1, max_retry + 1):
        try:
            ds_sub = ds.sel(
                lon=lon_range,
                lat=lat_range,
                depth=depth_level,
                time=slice(day, day_end)
            ).load()

            # 转成 numpy
            u = ds_sub["water_u"].values  # shape: (time, lat, lon)
            v = ds_sub["water_v"].values
            t = ds_sub["time"].values

            # 存成 npz
            np.savez(outfile, u=u, v=v, time=t)
            print(f"✅ 成功保存：{outfile}")
            success = True
            break
        except Exception as e:
            print(f"⚠️ 第 {attempt} 次失败：{e}")
            time.sleep(pause_between)

    if not success:
        print(f"❌ {day.strftime('%Y-%m-%d')} 下载失败，放弃")
