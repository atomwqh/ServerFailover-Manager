import paramiko

def run_ssh_command(ip: str, username: str, key_file: str, command: str, timeout: int = 10):
    """
    使用SSH密钥连接远程服务器并执行命令
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, username=username, key_filename=key_file, timeout=timeout)
        stdin, stdout, stderr = ssh.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        return out, err
    except Exception as e:
        return None, str(e)
    finally:
        ssh.close()
