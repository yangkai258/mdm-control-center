#!/usr/bin/env python3
"""
MQTT 高并发压测脚本
用于模拟海量设备同时向 EMQX 发送心跳包

依赖安装:
pip install paho-mqtt

运行:
python mqtt_stress_test.py
或指定参数:
python mqtt_stress_test.py --host 192.168.1.100 --port 1883 --devices 1000
"""

import os
import sys
import json
import time
import random
import threading
import argparse
from datetime import datetime
from typing import Dict, List
import uuid

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("错误: 请先安装 paho-mqtt 库")
    print("运行: pip install paho-mqtt")
    sys.exit(1)


class DeviceSimulator:
    """设备模拟器"""
    
    def __init__(self, device_id: str, client_id: str, broker: str, port: int):
        self.device_id = device_id
        self.client_id = client_id
        self.broker = broker
        self.port = port
        self.client = None
        self.connected = False
        self.messages_sent = 0
        self.last_error = None
        
    def connect(self) -> bool:
        """连接到 MQTT Broker"""
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.connected = True
                global connected_count
                connected_count += 1
            else:
                self.last_error = f"连接失败, 返回码: {rc}"
                
        def on_disconnect(client, userdata, rc):
            self.connected = False
            global connected_count
            if connected_count > 0:
                connected_count -= 1
                
        def on_publish(client, userdata, mid):
            self.messages_sent += 1
            global messages_count
            messages_count += 1
        
        self.client = mqtt.Client(client_id=self.client_id)
        self.client.on_connect = on_connect
        self.client.on_disconnect = on_disconnect
        self.client.on_publish = on_publish
        
        try:
            self.client.connect(self.broker, self.port, keepalive=60)
            self.client.loop_start()
            time.sleep(0.5)  # 等待连接
            return self.connected
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def publish_heartbeat(self) -> bool:
        """发送心跳包"""
        if not self.connected or not self.client:
            return False
            
        topic = f"/mdm/device/{self.device_id}/up/status"
        
        payload = {
            "device_id": self.device_id,
            "timestamp": datetime.now().isoformat(),
            "connection_status": "online",
            "battery_level": random.randint(0, 100),
            "charging_status": random.choice([True, False]),
            "current_mode": random.choice(["sleeping", "roaming", "listening", "talking", "idle"]),
            "rssi": random.randint(-90, -30)
        }
        
        try:
            result = self.client.publish(topic, json.dumps(payload), qos=1)
            return result.rc == mqtt.MQTT_ERR_SUCCESS
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def disconnect(self):
        """断开连接"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()


class StressTest:
    """压力测试主类"""
    
    def __init__(self, host: str, port: int, num_devices: int):
        self.host = host
        self.port = port
        self.num_devices = num_devices
        self.devices: List[DeviceSimulator] = []
        self.running = False
        
    def setup_devices(self):
        """初始化设备"""
        print(f"[*] 正在创建 {self.num_devices} 个虚拟设备...")
        
        for i in range(self.num_devices):
            device_id = str(uuid.uuid4())
            client_id = f"stress_test_{device_id}"
            device = DeviceSimulator(
                device_id=device_id,
                client_id=client_id,
                broker=self.host,
                port=self.port
            )
            self.devices.append(device)
            
        print(f"[*] 正在连接设备到 {self.host}:{self.port}...")
        
        # 批量连接设备
        threads = []
        for device in self.devices:
            t = threading.Thread(target=device.connect)
            t.start()
            threads.append(t)
            # 控制连接速度，避免瞬间太大压力
            if i % 50 == 0:
                time.sleep(0.1)
        
        # 等待所有连接完成
        for t in threads:
            t.join()
        
        # 统计连接结果
        connected = sum(1 for d in self.devices if d.connected)
        failed = self.num_devices - connected
        
        print(f"[+] 连接完成: 成功 {connected}, 失败 {failed}")
        return connected
    
    def run_heartbeat_test(self, interval: int = 30):
        """运行心跳测试"""
        self.running = True
        print(f"[*] 开始心跳测试，每 {interval} 秒发送一次...")
        
        try:
            while self.running:
                # 并发发送心跳
                threads = []
                for device in self.devices:
                    if device.connected:
                        t = threading.Thread(target=device.publish_heartbeat)
                        t.start()
                        threads.append(t)
                
                # 等待发送完成
                for t in threads:
                    t.join()
                
                # 打印统计
                self.print_stats()
                
                # 等待下一次发送
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n[*] 测试被用户中断")
    
    def print_stats(self):
        """打印统计信息"""
        now = datetime.now().strftime("%H:%M:%S")
        
        connected = sum(1 for d in self.devices if d.connected)
        messages_sent = sum(d.messages_sent for d in self.devices)
        
        print(f"[{now}] 连接: {connected}/{self.num_devices}, "
              f"消息发送: {messages_sent}, "
              f"成功率: {connected/self.num_devices*100:.1f}%")
    
    def cleanup(self):
        """清理资源"""
        print("[*] 正在清理...")
        self.running = False
        
        for device in self.devices:
            device.disconnect()
        
        print("[+] 清理完成")


# 全局计数器
connected_count = 0
messages_count = 0


def main():
    parser = argparse.ArgumentParser(description="MQTT 高并发压测工具")
    parser.add_argument("--host", default=os.environ.get("MQTT_HOST", "localhost"),
                        help="MQTT Broker 地址")
    parser.add_argument("--port", type=int, default=int(os.environ.get("MQTT_PORT", "1883")),
                        help="MQTT Broker 端口")
    parser.add_argument("--devices", type=int, default=1000,
                        help="虚拟设备数量")
    parser.add_argument("--interval", type=int, default=30,
                        help="心跳发送间隔(秒)")
    
    args = parser.parse_args()
    
    print("=" * 60)
    print(" MQTT 高并发压测工具")
    print("=" * 60)
    print(f"Broker: {args.host}:{args.port}")
    print(f"设备数: {args.devices}")
    print(f"心跳间隔: {args.interval}秒")
    print("=" * 60)
    
    # 创建测试实例
    test = StressTest(args.host, args.port, args.devices)
    
    # 初始化设备
    connected = test.setup_devices()
    
    if connected == 0:
        print("[-] 错误: 没有任何设备成功连接到 Broker")
        sys.exit(1)
    
    # 运行测试
    try:
        test.run_heartbeat_test(args.interval)
    except KeyboardInterrupt:
        print("\n[*] 收到中断信号，正在停止...")
    finally:
        test.cleanup()
        
        # 最终统计
        total_messages = sum(d.messages_sent for d in test.devices)
        print("\n" + "=" * 60)
        print(" 测试完成 - 最终统计")
        print("=" * 60)
        print(f"设备总数: {args.devices}")
        print(f"消息总数: {total_messages}")
        print(f"平均每设备: {total_messages/args.devices:.1f} 条")


if __name__ == "__main__":
    main()
