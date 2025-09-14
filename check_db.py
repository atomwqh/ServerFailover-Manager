import sqlite3

def check_tables(db_path: str):
    """检查 SQLite 数据库中所有表"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            print(f"数据库 '{db_path}' 中的表有:")
            for table in tables:
                print(f" - {table[0]}")
        else:
            print(f"数据库 '{db_path}' 当前没有任何表。")
    except Exception as e:
        print("检查数据库表时发生错误:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    db_file = "server_failover.db"  # SQLite 文件路径
    check_tables(db_file)
