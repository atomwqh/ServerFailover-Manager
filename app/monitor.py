import subprocess
import paramiko
from app.db import SessionLocal
from app.models import Server
import time
import threading

# Ping 服务器
def ping_server(ip: str) -> bool:
    """
    返回 True 表示在线，False 表示不可达
    """
    try:
        output = subprocess.run(
            ["ping", "-n", "1", "-w", "1000", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        return output.returncode == 0
    except Exception as e:
        print(f"Ping {ip} 出错: {e}")
        return False

# SSH 执行补救脚本
def ssh_fix(ip: str, username: str, password: str, script: str):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=username, password=password, timeout=5)
        stdin, stdout, stderr = ssh.exec_command(script)
        out = stdout.read().decode()
        err = stderr.read().decode()
        ssh.close()
        print(f"[{ip}] SSH 输出: {out}, 错误: {err}")
    except Exception as e:
        print(f"[{ip}] SSH 连接失败: {e}")

# 定时监控所有服务器
def monitor_loop(interval: int = 60):
    """
    每 interval 秒检查一次数据库中所有服务器
    """
    db = SessionLocal()
    while True:
        servers = db.query(Server).all()
        for server in servers:
            online = ping_server(server.ip)
            if not online:
                print(f"[{server.ip}] 不可达，执行补机脚本...")
                # 查询所属组的脚本
                group_script = server.group.script if server.group else ""
                # 假设 SSH 用户和密码统一配置，可改为每台不同
                ssh_fix(server.ip, "root", "password123", group_script)
        time.sleep(interval)

# 启动后台线程
def start_monitor(interval: int = 60):
    t = threading.Thread(target=monitor_loop, args=(interval,), daemon=True)
    t.start()
