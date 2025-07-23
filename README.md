在一些Linux发行版中，`/sys/class/thermal/`目录下会有一个或多个名为thermal_zoneX的子目录，其中X是一个数字。每个子目录对应一个传感器，其中一个可以用于读取CPU温度。
运行以下命令来查看可用的传感器： `ls /sys/class/thermal/thermal_zone*` 根据输出的结果，找到对应的传感器，并运行以下命令来读取CPU温度：`cat /sys/class/thermal/thermal_zoneX/temp`
注意：这个命令的输出结果以十进制表示的温度，你需要将其除以1000来得到摄氏温度。
在`cpu-temp-monitor.conf`中修改为相应的温度文件路径。
通过钉钉机器人进行通知。参考（https://open.dingtalk.com/document/orgapp/custom-bot-creation-and-installation）
通过`sh install.sh`命令安装服务
在PVE8.4版本测试正常
通过`journalctl -r -u cpu-temp-monitor.service`命令查看日志
