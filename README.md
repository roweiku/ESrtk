# ESrtk

**ESrtk** 是一款极致成本控制的高精度cors网络rtk，配套ros驱动，适用于机器人、无人机、农业设备等定位导航测绘。

Hardware: ~~[oshwhub](https://oshwhub.com/xxx)~~   
Bill of Materials: ~~[interactive HTML BOM](./hardware/ESrtk_ibom.html)~~  
Models: ~~[外壳](./hardware/xxx.step)~~  

## Preview

| Hardware                             | RViz                             |
| -------------------------------- | --------------------------------- |
| ![预览](.docs/hardware.png) | ![预览](./docs/rviz.gif) |


## Features

- 高精度cors网络rtk，体积小巧高集成 usb / m.2 接口二选一，支持直插 PC
- 至高20hz厘米级固定解，水平0.8cm+1ppm，高程1.5cm+1ppm
- 选择4g ntrip协议获取差分数据，免部署基准站
- 可配置双天线，同时安装可定向，计算航向解
- 配套ros驱动，输出odom话题，提供tf变换，可接入导航，也可配合rviz_satellite可视化

## Firmware

### 修改 NTRIP 账号密码

```lua
ntrip.setup({
    host = "203.107.45.154",       -- CORS 服务器地址
    port = 8002,                   -- 端口
    user = "qxtmcr00102087",       -- 用户名
    password = "497071c",          -- 密码
    mount = "/RTCM32_GGB",         -- 挂载点（根据服务商选择）
    cb = gnss_write
})
```

### 固件烧录

- 下载并安装 [Luatools](https://docs.openluat.com/common/Luatools/)
- 选择固件  
    `Firmware/firmware/LuatOS-SoC_V2002_Air700ECQ.soc`
- 添加脚本文件  
   `Firmware/demo/main.lua`  
   `Firmware/demo/demo.lua`  
   `Firmware/demo/netready.lua`  
   `Firmware/lib/ntrip.lua`

## ROS 驱动

### 依赖

**ROS**（Noetic / ?）

```bash
sudo apt install python3-pyserial python3-pyproj
sudo apt install ros-noetic-tf ros-noetic-tf2-ros ros-noetic-rviz
```

### 编译

```bash
cd ESrtk/rtk_ws
catkin_make
source devel/setup.zsh
```

### 运行 Demo

UM982 驱动

```bash
roslaunch um982_driver um982.launch
```

TF 转换

```bash
rosrun tf_tran tf_tran.py
```

RViz 可视化

```bash
roslaunch rviz_satellite demo.launch
```

### 话题列表

| 话题 | 类型 | 说明 |
|------|------|------|
| `/gps/fix` | `sensor_msgs/NavSatFix` | GPS 经纬度定位数据 |
| `/gps/utmpos` | `nav_msgs/Odometry` | UTM 坐标位置 + 航向 |
| `/tf` | `tf2_msgs/TFMessage` | earth → base_link 坐标变换 |


## Acknowledgements

ESrtk was based on or inspired by these projects and so on:

- **[luatos-lib-ntrip](https://github.com/wendal/luatos-lib-ntrip)** — ntrip协议客户端 for LuatOS
- **[rviz_satellite](https://github.com/gareth-cross/rviz_satellite)** — About
Display internet satellite imagery in RViz
- **[UM982_driver](xxx)** — xxx

## License

- TODO