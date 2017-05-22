# coding : utf-8
import requests
import csv
import threading
import time
import bs4
import re

# 使用 requests + bs4 + csv 爬取 gradcafe 数据

# 请求头
header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}

# 初始化一个总页面，10 为一个大于 1 的值
TOTALPAGE = 10
# 判断是否获取了最终的页面
GET_PAGE = True


def fetch(url):
    global TOTALPAGE
    global GET_PAGE
    '''爬取某一页面的信息'''
    req = requests.get(url,headers = header,timeout=20)
    page = req.text

    soup = bs4.BeautifulSoup(page,'lxml')
    soup_table = soup.find('table',class_='results narrow-table')
    soup_tr = soup_table.tbody.find_all('tr')
    # data 保存所有数据
    data = []
    for tr in soup_tr:
        # row_data 保存一行数据
        row_data = []
        soup_td = tr.find_all('td')

        # 逐个提取数据
        institution = soup_td[0].get_text(strip=True)
        program = soup_td[1].string

        # decision 和 date 有多种情况，分开获取
        decision_tag = soup_td[2].span
        if decision_tag:
            decision = decision_tag.string
            date = list(soup_td[2].strings)[1]
        else:
            decision = 'default'
            date = soup_td[2].string

        # st 可能为空
        st = soup_td[3].string if soup_td[3].string else 'default'
        date_added = soup_td[4].string

        # notes 可能为空，并且字符串中可能带有换行符，需要去掉
        notes = soup_td[5].get_text(strip=True)
        notes = notes.replace('\n','') if notes else 'default'

        for i in [institution,program,decision,date,st,date_added,notes]:
            row_data.append(i)

        data.append(row_data)

    # 第一次请求时，寻找总页面
    if GET_PAGE:
        soup_div = soup.find('div',class_='pagination')
        page_string = soup_div.get_text()
        pattern = re.compile('over (\d+) pages')
        totalpage = re.findall(pattern,page_string)[0]
        TOTALPAGE = int(totalpage)

        GET_PAGE = False

    # 保存信息
    save(data)


# 保存信息
write_head=True
def save(info):
    # 使用一个全局变量判断是否添加标题行，第一次执行会写入标题行
    global write_head
    # newline 参数去除 csv 空行
    with open('data.csv','a+',encoding='utf-8',newline='')as f:
        writer = csv.writer(f)
        if write_head:
            # 首次执行添加标题行
            writer.writerow(['Institution','Program','Decision','Date','St','Date_Added','Notes'])
            write_head = False
        for i in info:
            writer.writerow(i)


def main():
    # global TOTALPAGE
    # 过去一个月、每页 250 条信息 链接
    url = 'http://thegradcafe.com/survey/index.php?t=m&pp=250&o=&p='
    count = 1
    # 直到总页面，抓取停止
    while count <= TOTALPAGE:

        the_url = url + str(count)
        print('正在获取第{0}页信息，url为{1}'.format(count,the_url))
        threading.Thread(target=fetch,args=(the_url,)).start()
        # 仅开 3 个线程
        while threading.active_count() > 3 :
            time.sleep(3)

        # 防止请求过快
        time.sleep(1)
        count += 1

if __name__ == '__main__':
    main()
