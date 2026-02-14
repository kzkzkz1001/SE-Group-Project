import requests
import mysql.connector
import os
import time
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 配置 API
JC_KEY = os.getenv("JC_API_KEY")
STATIONS_URL = f"https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey={JC_KEY}"


def get_db_connection():
    """建立与本地 MySQL 的连接"""
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )


def scrape_bikes():
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 正在爬取都柏林自行车数据...")
    try:
        # 1. 发送请求
        response = requests.get(STATIONS_URL)
        if response.status_code != 200:
            print(f"API 请求失败: {response.status_code}")
            return

        stations_data = response.json()

        # 2. 连接数据库
        conn = get_db_connection()
        cursor = conn.cursor()

        for station in stations_data:
            # A. 更新/插入静态站点信息 (station 表)
            # 使用 ON DUPLICATE KEY UPDATE 确保数据最新且不重复
            sql_st = """INSERT INTO station (number, name, address, pos_lat, pos_lng, bike_stands) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE name=%s, address=%s"""
            cursor.execute(sql_st, (
                station['number'], station['name'], station['address'],
                station['position']['lat'], station['position']['lng'], station['bike_stands'],
                station['name'], station['address']
            ))

            # B. 插入动态可用性数据 (availability 表)
            sql_av = """INSERT INTO availability (number, available_bikes, available_bike_stands, last_update, status) 
                        VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(sql_av, (
                station['number'], station['available_bikes'], station['available_bike_stands'],
                station['last_update'], station['status']
            ))

        # 提交并关闭
        conn.commit()
        cursor.close()
        conn.close()
        print(f"成功更新 {len(stations_data)} 个站点的实时数据。")

    except Exception as e:
        print(f"运行出错: {e}")


if __name__ == "__main__":
    # 第一次运行测试
    scrape_bikes()

    # 如果你想让它每5分钟自动运行，取消下面三行的注释：
    # print("程序已进入持续监控模式，每 5 分钟抓取一次...")
    # while True:
    #     time.sleep(300)
    #     scrape_bikes()
