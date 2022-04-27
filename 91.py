from lxml import etree
import os
import requests
from bs4 import BeautifulSoup


"""
91pron图片站爬虫
"""


class Pron_91():
    def __init__(self, url):
        self.url = url
        self.domain = "http://" + str(self.url).split('/')[2] + "/"
        self.ua_header = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
            "referer" : "https://t0328.wonderfulday27.live/"
        }
       
    def craw_urls(self):
        response = requests.get(url=self.url,headers=self.ua_header)
        xmlselector = etree.HTML(response.content.decode('utf-8'))
        urls = set(xmlselector.xpath('//div/a[@style="font-weight: bold;color: purple"]/@href'))
        urls_list = []
        for url in urls:
            urls_list.append(self.domain + url)
        return urls_list

    def craw_pic(self,link):
        response = requests.get(url=link,headers=self.ua_header)
        xmlselector = etree.HTML(response.content.decode('utf-8'))
        soup1 = BeautifulSoup(response.content,'lxml')
        soup2 = soup1.title.string.split(' - ')
        soup3 = soup2[0].replace('\\','-')
        title = soup3.replace('/','-')
        if str(title) in os.listdir('d:\\91\\'):
            print('{} --- 资源在文件夹中,将解析下一个'.format(str(title)))
        else:
            pic = xmlselector.xpath('//@file')
            if len(pic) == 0:
                print(title + "内没有图片")
            else:
                os.mkdir('d:\\91\\' + title)
                print(title + "   --->   文件夹创建完成")
                print("共{}张图片,请等待......".format(len(pic)))
                x = 0
                while x < len(pic):
                    print("正在下载第{}图片".format(x))
                    houzhui = pic[x].split('.')
                    picresponse = requests.get(url=pic[x],headers=self.ua_header)
                    with open("d:\\91\\" + title + "\\" + str(x) + "." + houzhui[-1], 'wb') as f:
                        f.write(picresponse.content)
                    x += 1
                #requests.post(url='https://api.telegram.org/bot{TGBOT_ID}/sendMessage?chat_id={TG_账号ID}&text=《' + title + '》已经下载完毕',proxies=self.proxies)
                print(title + "   --->   已经下载完毕")
                print("-" * 30)


if __name__ == '__main__':
    pron = Pron_91("https://t0328.wonderfulday27.live/index.php")
    for link in pron.craw_urls():
        try:
            pron.craw_pic(link=link)
        except:
            continue
