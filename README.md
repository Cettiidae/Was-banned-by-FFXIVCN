# Was-banned-by-FFXIVCN❓
查询某个ID是否出现在FFXIV国服封神榜上？
本仓库包含几个用于爬取封号数据的脚本。本脚本并未提供直接数据展示能力，如果您有需要，请等待前端编写完成。或使用脚本将数据导入您的MySql服务器。

# 脚本功能介绍
`new_vio_data.py`   
将完整导入`新违规处理平台`的数据至MySQL服务器。  
  
`get_bannews_id.py`  
爬取封号文章的ID并存入`news_id.txt`
  
`article_vio_data.py`  
将获取到的文章ID导入MySQL服务器。
