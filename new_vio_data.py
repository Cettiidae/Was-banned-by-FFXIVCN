# 获取历史封号记录（新平台）
# 仅可获取一次，获取后不可再次获取。否则可能产生数据重复。
# https://act1.ff.sdo.com/FF14/api/ViolationPlatform/violationRoles?page=1&limit=200
# 有效数据：response["data"]["list"] >> {'role_name': '道枝千鸟', 'group_name': '海猫茶屋', 'vio_reason': '严重破坏游戏环境'}
import requests
import configparser
import mysql.connector


def get_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    return response.json()


# 获取历史总数
def check_count():
    data = get_json("https://act1.ff.sdo.com/FF14/api/ViolationPlatform/violationRoles?page=1&limit=1")
    count = data["data"]["count"]
    count = str(count)
    return count


# 去除无用数据（旧）
def trim_data_history(data):
    date = data["data"]["list"]
    return date


# 去除无用数据（新）
def trim_data_new(data):
    date = data["data"]
    return date


new_vio_api = "https://act1.ff.sdo.com/FF14/api/ViolationPlatform/violationRoles"
# ? page=1 & limit=5104
#   控制页数  控制页输出限制 可在一页直接完全输出

# 生成URL
data_url = new_vio_api + "?page=1&limit=" + check_count()
new_url = "https://act1.ff.sdo.com/FF14/api/ViolationPlatform/newViolationRoles"
# 获取数据【旧】
#response_data = trim_data_history(get_json(data_url))
# 获取数据【新】
response_data = trim_data_new(get_json(new_url))
# 连接数据库
# 读取数据库配置
config = configparser.ConfigParser()
config_path = r'config.ini'
config.read(config_path)

mydb = mysql.connector.connect(
    host=config['Database']['dbHost'],
    user=config['Database']['userName'],
    passwd=config['Database']['password'],
    database=config['Database']['dbName']
)
mycursor = mydb.cursor()

for vio_data in response_data:
    sql = "INSERT INTO banned_list (role_name, server ,reason) VALUES (%s, %s, %s)"
    val = (vio_data["role_name"], vio_data["group_name"], vio_data["vio_reason"])
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "行记录插入成功。")

# if len(response_data) == int(check_count()):
#     for vio_data in response_data:
#         sql = "INSERT INTO banned_list (role_name, server ,reason) VALUES (%s, %s, %s)"
#         val = (vio_data["role_name"], vio_data["group_name"], vio_data["vio_reason"])
#         mycursor.execute(sql, val)
#         mydb.commit()
#         print(mycursor.rowcount, "行记录插入成功。")
# else:
#     print("获取的数据可能存在问题，请检查接口是否需要更新。")
