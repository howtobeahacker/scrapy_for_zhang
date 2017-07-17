'''

|   Author:zhuob
|
|   date:2017/7/17
|
|   Description:scrapy zol for zhangzongyuan
|   the zol don't have robot's txt about img
|   so it is easy to scrapy wallpaper.
|   but i failed firstly. Because i think the finally html web is img
|   
|
|   then i use phantomjs and selenimus to prt sc
|   it's wasting time and i also meet some problems that i can't solve.
|   it is how to cut a threading while the threading use too much time.
|
|   finally,i don't solve it .
|
|   fortunately, i find the img-http under the html web,
|   so i finally the small porject.
|   
|
|   and i learn how to git my project.
|
|   so ,this is my first time to git my formal project. 
'''


import os
import re
import requests
import random
from bs4 import BeautifulSoup
from selenium import webdriver
#第一层页面即中关村壁纸的首页
#第二层页面即壁纸相册的页面
#第三层页面即完整图片的html页面
#第四层页面即完整图片的img页面


def get_second_page_url(type,page):
    original_url="http://sj.zol.com.cn/bizhi/"
    kind_url=original_url+type+"/"+str(page)+".html"

    re_1 = '''a class="pic" href="(\/bizhi\/detail[_][0-9]{3,4}[_][0-9]{3,5}[.]html)" target="_blank"'''
    # print(kind_url)
    r = requests.get(kind_url)
    r.encoding = r.apparent_encoding
    
    html = r.text
    HTML = re.findall(re_1, html)
    
    second_page_url=[]
    
    for i in HTML:
            second_page_url.append("http://sj.zol.com.cn"+i)
    second_page_url=second_page_url[:-3]

    return second_page_url

    

def get_second_img_id(url):#这个url是第二层页面的url
    list=[]
    r = requests.get(url)
    all_ip = re.findall('''\<li id="img[0-9]{1,2}" class=\"show\d "\>\s*\<a href=\"(.*)\"\>''', r.text)
    for i in all_ip:
        list.append(i.split("_")[2].split(".")[0])
    return list
#得到每张图片的id，在第二层页面的
def get_num(url):#这个url是第二层页面的url
    r = requests.get(url)
    all_num = re.findall('''href=\"\/bizhi\/showpic\/480x800(.*?)\"''', r.text)
    num= all_num[0].split("_")[-1]
    return num
#因为每张图片后面加了一个随机数字，找出这个随机数字，最后生成html网址

def get_third_url(url):#这个url是第二层页面的url



    list=[]
    page_url=get_second_img_id(url)
    num=get_num(url)
    for i in  page_url:
        list.append("http://sj.zol.com.cn/bizhi/showpic/480x800_"+str(i)+"_"+str(num))#http://sj.zol.com.cn/bizhi/showpic/480x800_72700_82.html
    return list

def get_third_img(url):#这个url是第三层的htmlulr
    html=re.findall("http\:(.*).jpg",requests.get(url).text)
    URL="http:"+html[0]+".jpg"
    return URL

def download(file_name,r):
    
    
    q= requests.get(r)
    f=open(file_name,"wb")
    f.write(q.content)
    f.close



if __name__ == "__main__":

    # second_url = []
    # for i in range(1, 31):
    #     for i in get_second_page_url("meinv", i):
    #         second_url.append(i)
    #         # print(i)
    #
    # third_url = []
    # for i in second_url:
    #     try:
    #         for i in get_third_url(i):
    #             third_url.append(i)
    #             # print(i)
    #     except Exception:
    #         pass


    f = open("D:\python_codes\\try\img_url.txt", "r")
    third_img=[]
    for eachline in f:
        third_img.append(eachline)

    # third_img = []
    # for i in third_url:
    #     try:
    #         print(get_third_img(i))
    #     except Exception:
    #         pass

    num = 1
    for i in third_img:
        download("D:\python_codes\\try\img2\\" + str(num) + ".jpg", i)
        print("====================" + str(num) + "*************" + "success" + "=================")
        num += 1