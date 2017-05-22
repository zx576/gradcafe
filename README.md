## 爬取 gradcafe


#### requests 脚本


脚本文件 `gcafe.py` , `git clnoe` 之后运行即可生成 csv 文件。

该脚本使用 request + bs4 + csv 技术，注释见脚本内。


#### scrapy 框架

项目包含在 gradcafe 文件夹内

文件解释:

`items.py` 指定存储哪些数据。
`pipelines.py` 连接 mongodb ，并且数据存入数据库。
`settings.py` 设置 mongodb 信息，设置请求延迟，设置请求头
`spiders/gcafe.py` 爬取网页脚本。
