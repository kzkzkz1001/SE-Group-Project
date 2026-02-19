import os
from dotenv import load_dotenv
import mysql.connector


load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


def get_db_connection():
    db_pass = os.getenv("DB_PASS")

    # 调试用：如果终端打印出 "Password is None"，说明没读到 .env
    if db_pass is None:
        print("❌ DEBUG: .env file NOT loaded or DB_PASS is missing!")

    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=db_pass,  # 确保这里传了变量
        database=os.getenv("DB_NAME")
    )
