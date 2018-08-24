import requests
import re
from lxml import etree
import threading
global rust
threads = []
threads1 = []
s = ""
list = []
list1 = []
base_url = "https://movie.douban.com/j/chart/top_list?type=5&interval_id=100%3A90&action=&start=0&limit=20"
headers = {
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"
}
mubiao = "&start=0&limit=20"
def baseurl():
    global s
    url1 = base_url+mubiao
    rsq = requests.get(url=url1,headers= headers)
    ru = rsq.text.split("\"")
    result = ''
    for i in ru:
        result = result+i
    result = result.replace("\\","")
    ru1 = re.findall("rating:\[(.*?),.*?\],rank:(.*?),cover_url:(.*?),is_playable:.*?,id:.*?,types:\[(.*?)\],regions:\[(.*?)\],title:(.*?),url:(.*?),release_date:(.*?),actor_count:.*?,vote_count:(.*?),score:.*?,actors:\[(.*?)\]",result,re.S)
    for item in ru1:
        rust = {
        "排名": item[1],
        "评分":item[0],
        "电影名":item[5],
        "国家":item[4],
        "类型":item[3],
        "电影的海报链接":item[2],
        "电影播放的链接":item[6],
        "演员名单":item[9],
        "上映日期":item[7],
       "评价人数":item[8],
    }
        list.append(item[6])
        s = s+str(rust)+'\n'
    with open('result1.txt','w') as f:
        f.write(s)
def pingjiaurl(reponse):
    req = requests.get(reponse)
    rsq = etree.HTML(req.text)
    a = rsq.xpath('//html/body/div/div/div/div/div[@id ="comments-section"]/div[@class ="mod-hd"]/h2/span[@class ="pl"]/a/@href')
    list1.append(a)
def dp(url):
    rsq = requests.get(url)
    req = etree.HTML(rsq.text)
    h = req.xpath('//head/title/text()')
    a = req.xpath('//div[@class="avatar"]/a/@title')
    b = req.xpath('//div[@class="comment"]/h3/span[@class="comment-vote"]/span/text()')
    c = req.xpath('//div[@class="comment"]/h3/sp    an[@class="comment-vote"]/a/text()')
    d = req.xpath('//div[@class="comment"]/a/span[@class="comment-info"]/sapn[@class="allstar50 rating"]/@title')
    e = req.xpath('//div[@class="comment"]/a/span[@class="comment-info"]/sapn[@class="comment-time"]/@title')
    #with open('短评.txt','w') as f:
        #f.write(str(a))
    print(h)
baseurl()
for i in range(len(list)):
    t = threading.Thread(target=pingjiaurl,args=[list[i],])
    threads.append(t)
for i in range(len(list)):
    threads[i].start()
for i in range(len(list)):
    threads[i].join()
for j in range(len(list1)):
    t2 = threading.Thread(target=dp, args=[list1[j][0], ])
    threads1.append(t2)
for j in range(len(list1)):
    threads1[j].start()
for j in range(len(list1)):
    threads1[j].join()