-1、配置环境：
 -conda create --name podaac_env python==3.10
 -conda activate podaac_env
 -python -m pip install --upgrade pip
 -python -m pip install earthaccess podaac-data-subscriber
2、配置netrc文件
python -c "import earthaccess; earthaccess.login(strategy='interactive', persist=True)"
输入账号&密码
Copy-Item "$env:USERPROFILE\.netrc" "$env:USERPROFILE\_netrc" # 复制一份确保有_netrc .netrc两份文件
3、下载测试 （加--dry run 表示测试）
podaac-data-downloader -c L3S_LEO_PM-STAR-v2.81 -d "E:\data\VIIRS_L3S\PM_Night_KE" -sd 2024-01-01T00:00:00Z -ed 2024-12-31T23:59:59Z -b "140,32,152,40" -gr "*_LEO_PM_N-ACSPO_V2.81-*" -e ".nc" --subset --dry-run
4、正式下载
1）全球区域下载
podaac-data-downloader -c L3S_LEO_PM-STAR-v2.81 -d "E:\data\VIIRS_L3S\PM_Night_KE" -sd 2024-01-01T00:00:00Z -ed 2024-12-31T23:59:59Z -gr "*_LEO_PM_N-ACSPO_V2.81-*" -e ".nc"

2）区域下载
podaac-data-downloader -c L3S_LEO_PM-STAR-v2.81 -d "E:\data\VIIRS_L3S\PM_Night_KE" -sd 2024-01-01T00:00:00Z -ed 2024-12-31T23:59:59Z -b "140,32,152,40" -gr "*_LEO_PM_N-ACSPO_V2.81-*" -e ".nc" --subset
-c 数据库简短名称
-d 保存文件路径
-sd 起始时间
-ed 终止时间
-gr 通配符匹配
-b 经纬度范围 （lon_min,lat_min,lon_max,lat_max）
-c 文件后缀
--subset 调用 Harmony 对文件内部数据进行空间裁剪

5、详细参数帮助文档
podaac-data-downloader -h
