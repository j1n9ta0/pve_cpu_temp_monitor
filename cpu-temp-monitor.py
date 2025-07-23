#!/usr/bin/env python3
import os
import sys
import time
import json
import configparser
import requests
import hmac
import hashlib
import base64
import argparse

def load_config(config_path):
    """加载配置文件"""
    config = configparser.ConfigParser()
    
    # 设置默认配置
    config['DEFAULT'] = {
        'temp_file': '/sys/class/thermal/thermal_zone0/temp',
        'check_interval': '30',
        'temp_threshold': '70',
        'webhook': '',
        'secret': '',
        'alert_cooldown': '300'
    }
    
    # 检查配置文件是否存在
    if not os.path.exists(config_path):
        print(f"错误: 配置文件 {config_path} 不存在")
        sys.exit(1)
    
    # 读取配置文件
    config.read(config_path)
    print(f"使用配置文件: {config_path}")
    
    return config['monitor']

def get_cpu_temp(temp_file):
    """读取CPU温度"""
    try:
        with open(temp_file, "r") as f:
            temp = int(f.read().strip()) / 1000.0
        return temp
    except Exception as e:
        print(f"读取温度失败: {e}")
        return None

def send_dingtalk_alert(temp, config):
    """发送钉钉告警"""
    webhook = config.get('webhook')
    secret = config.get('secret')
    if not webhook:
        print("错误: 未配置钉钉Webhook，无法发送告警")
        return False
    
    headers = {"Content-Type": "application/json"}
    timestamp = str(round(time.time() * 1000))
    
    # 构建消息内容
    message = {
        "msgtype": "markdown",
        "markdown": {
            "title": "PVE温度告警",
            "text": f"**PVE服务器CPU温度过高！**\n\n"
                    f"- 当前温度: `{temp:.1f}℃`\n"
                    f"- 时间: `{time.ctime()}`\n"
                    f"- 阈值: `{config.get('temp_threshold')}℃`\n"
                    f"- 主机标识: `{config.get('system_id', 'PVE')}`\n\n"
                    "请立即检查服务器散热情况！"
        }
    }
    
    # 签名验证（如果设置了加签）
    if secret:
        string_to_sign = f"{timestamp}\n{secret}"
        secret_enc = secret.encode('utf-8')
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = base64.b64encode(hmac_code).decode('utf-8')
        url = f"{webhook}&timestamp={timestamp}&sign={sign}"
    else:
        url = webhook
    
    try:
        response = requests.post(url, json=message, headers=headers, timeout=10)
        response.raise_for_status()
        result = response.json()
        if result.get("errcode") == 0:
            print("告警发送成功")
            return True
        else:
            print(f"发送失败: {result.get('errmsg')}")
            return False
    except Exception as e:
        print(f"请求异常: {e}")
        return False

def main():
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='CPU温度监控工具')
    parser.add_argument('-c', '--config', 
                        required=True,
                        help='配置文件路径 (必填)')
    args = parser.parse_args()
    
    # 加载配置
    config = load_config(args.config)
    
    # 解析配置值
    temp_file = config.get('temp_file')
    check_interval = config.getint('check_interval')
    temp_threshold = config.getfloat('temp_threshold')
    alert_cooldown = config.getint('alert_cooldown')
    
    last_alert_time = 0  # 上次告警时间
    
    print(f"启动CPU温度监控 (阈值: {temp_threshold}℃, 间隔: {check_interval}秒)")
    
    while True:
        temp = get_cpu_temp(temp_file)
        if temp is None:
            time.sleep(5)
            continue
            
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] CPU温度: {temp:.1f}℃")
        
        current_time = time.time()
        if temp >= temp_threshold and (current_time - last_alert_time) > alert_cooldown:
            print(f"温度超过阈值 {temp_threshold}℃，发送告警...")
            if send_dingtalk_alert(temp, config):
                last_alert_time = current_time
        
        time.sleep(check_interval)

if __name__ == "__main__":
    main()