在一些Linux发行版中，/sys/class/thermal/目录下会有一个或多个名为thermal_zoneX的子目录，其中X是一个数字。每个子目录对应一个传感器，其中一个可以用于读取CPU温度。
运行以下命令来查看可用的传感器：
ls /sys/class/thermal/thermal_zone*
根据输出的结果，找到对应的传感器，并运行以下命令来读取CPU温度：
cat /sys/class/thermal/thermal_zoneX/temp
注意：这个命令的输出结果以十进制表示的温度，你需要将其除以1000来得到摄氏温度。
在cpu-temp-monitor.conf中修改为相应的温度文件路径。
