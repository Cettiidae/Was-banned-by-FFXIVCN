# 用于获取特定文章ID
# https://ff.web.sdo.com/inc/newdata.ashx?url=List?gameCode=ff&category=5309,5310,5311,5312,5313&pageIndex=107&pageSize=50
# 其中 ：category：5312为 系统封号等相关通知
# pageIndex会根据pageSize调整上限(PageCount)
# {
#     "Code": "0",
#     "Message": "",
#     "PageCount": 11,
#     "TotalCount": 522,
#     "RecordCount": 50,
#     "Data": [
#         {
#             "Id": 292528,
#             "Articletype": 3,
#             "ApplicationCode": 92,
#             "CategoryCode": 5312,
#             "SortIndex": 0,
#             "GroupIndex": 0,
#             "TitleClass": "",
#             "Title": "《最终幻想14》4月20日违规账号处罚公告",
#             "Summary": "为了更好地维护游戏内的游戏秩序，保障各位冒险者良好公正的游戏体验，近期我们对游戏中违规招募、使用非法第三方软件及违反
#                         了其他游戏规定的账号进行了查处。处罚账号共计1435个，给予封停处罚。处罚名单见下。",
#             "Author": "",
#             "PublishDate": "2018/04/20 19:05:41",
#             "OutLink": "",
#             "HomeImagePath": "http://fu5.sdo.com/10036/201804/15242222348009.png"
#         }
#     ]
# }
# 最后输出文章ID至news_id.txt
import requests


def get_json(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/80.0.3987.149 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    return response.json()


# 获取新闻标题
def get_news_title(data):
    title = data["Title"]
    return title


# 判断是否封号文章
def is_ban_news(data):
    ban_title = "违规账号处罚公告"
    flag = ban_title in data
    return flag


# 获取页面长度
def get_pages_count():
    data = get_json(
        "https://ff.web.sdo.com/inc/newdata.ashx?url=List?gameCode=ff&category=5312&pageIndex=1&pageSize=100")
    count = data["PageCount"]
    return count


f = open("news_id.txt", 'a', encoding="utf-8")

for page_count in range(get_pages_count() + 1):
    req_url = "https://ff.web.sdo.com/inc/newdata.ashx?url=List?gameCode=ff&category=5312&pageIndex=" + str(
        page_count) + "&pageSize=100"
    response = get_json(req_url)["Data"]
    for new_detail_count in range(len(response)):
        news_title = get_news_title(response[new_detail_count])
        if is_ban_news(news_title):
            print(news_title)
            print(response[new_detail_count]["Id"])
            f.write(str(response[new_detail_count]["Id"]) + '\n')
