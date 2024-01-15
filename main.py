# _*_ codign:utf8 _*_
"""====================================
@Author:Sadam·Sadik
@Email：1903249375@qq.com
@Date：2024/1/16
@Software: PyCharm
@disc:
======================================="""
import datetime
import logging
import time

import psutil
import requests
import click


def get_server_performance():
    # 获取服务器性能参数
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent

    return {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage
    }


def upload_to_central_server(api_url, api_key, data):
    # 上传数据到中央服务器
    response = requests.post(api_url, json=data)
    return response.status_code


@click.command()
@click.option('--api-url', prompt='请输入接口地址', required=True, help='是上传数据的回传地址')
@click.option('--api-key', prompt='请输入接口密钥', required=True, help='是上传数据的回传密钥')
@click.option('--interval', required=False, type=int, default=5 * 60, help='呼吸间隔')
def main(api_url, api_key, interval):
    # 定期获取性能参数并上传到中央服务器
    epoch_num = 0
    while True:
        epoch_num += 1
        server_performance_data = get_server_performance()
        status_code = upload_to_central_server(api_url, api_key, server_performance_data)
        if status_code == 200:
            logging.info(f'Epoch {epoch_num}, {datetime.datetime.now()},  {status_code}')
        else:
            logging.error(f'Epoch {epoch_num}, {datetime.datetime.now()},  {status_code}')
        # 间隔一段时间再次获取性能参数
        time.sleep(interval)  # 间隔5分钟


if __name__ == "__main__":
    main()
