import os

# 定义要创建的目录和文件
structure = [
    "app/",
    "app/__init__.py",
    "app/main.py",
    "app/config.py",
    "app/models.py",
    "app/db.py",
    "app/schemas.py",
    "app/crud.py",
    "app/ssh_utils.py",
    "app/monitor.py",
    "app/api/",
    "app/api/__init__.py",
    "app/api/groups.py",
    "app/api/servers.py",
    "app/api/health.py",
    "app/templates/",
    "frontend/",
    "scripts/",
    "scripts/init_db.py",
    "requirements.txt",
    ".env",
    "README.md"
]

# 创建所有目录和文件
for item in structure:
    if item.endswith('/'):
        os.makedirs(item, exist_ok=True)
    else:
        dir_name = os.path.dirname(item)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(item, 'w') as f:
            pass  # 创建空文件

print("项目结构已成功创建！")