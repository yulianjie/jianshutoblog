'''
https://www.jianshu.com/u/b0218515c59c?order_by=shared_at&page=3
https://www.jianshu.com/u/b0218515c59c?order_by=shared_at&page=2
通过上方的我们可以发现每一页的北荣获取非常简单，就是改了page后的数值

'''

import re
import requests
import random


# UA伪装,收集的UA,就全部那过来了
USER_AGENT_LIST = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
]
USER_AGENT = random.choice(USER_AGENT_LIST)


# 获取登录的csrf
def getcsrf(url):
    headers = {
        'User-Agent': USER_AGENT,
    }
    content = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')

    # <meta name="csrf-token" content="+ulmsYL9BeHtqzGOY4xe5c2xHrqim1UFMKnxRXzCPBBCUiNecLg9UcOQIFKtv9vjVlKmedXdJS/3bySV7YfAFQ==" />
    try:
        pat = re.compile('<meta name="csrf-token" content="(.*?)" />')
        csrf = re.findall(pat, content)[0]
    except:
        csrf = "error"
    return csrf


# 获取小说具体页面的内容
def getText(csrf, url):
    headers = {
        'User-Agent': USER_AGENT,
        "X-INFINITESCROLL": "true",
        "X-Requested-With": "XMLHttpRequest",
        'X-CSRF-Token': csrf,
    }
    content = []
    i = 1
    while True:
        url = url + "?order_by=shared_at&page=" + str(i)
        htmlContent = requests.get(url, headers=headers).content.decode('utf-8', 'ignore')
        if htmlContent == '':
            break
        # print(htmlContent)
        article = re.findall(
            '<a class="wrap-img" href="(.*?)" target="_blank">.*?data-echo="(.*?)".*?<a class="title" target="_blank" href=".*?">(.*?)</a>.*?<p class="abstract">(.*?)</p>',
            htmlContent, re.S)

        content.extend(article)
        if len(article) == 0:
            break
        print("文章数量为：")
        print(len(content))
        i += 1
    return content

# download img to img folder
def downloadimg(url,i):
    r = requests.get(url)
    with open('./img/img'+str(i)+'.jpg', 'wb') as f:
        f.write(r.content)

def writeText(article):
    # 写入总页数
    m = open('num.txt', 'w')
    num = int(len(article) / 9) + 1
    m.write(str(num))
    m.close()
    # 写入txt文件
    j = 1
    i = 0
    tex = ''

    for art in article:
        f = open('jianshu' + str(j) + '.html', 'w')
        art = list(art)
        # print(art)
        # print("---")
        art[3] = art[3].replace('\n', '')
        art[3] = art[3].replace(' ', '')
        if art[1][1] == '/':
            art[1] = art[1].replace('//', 'https://')
        downloadimg(art[1],i)
        tex = tex + '''
<div class="col mb-4">
    <div class="card h-100">
        <img src="./img/img{}.jpg" class="card-img-top" alt="img">
        <div class="card-body">
            <a href="https://www.jianshu.com{}">
                <h5 class="card-title">{}</h5>
            </a>
            <p class="card-text">{}</p>
        </div>
    </div>
</div>
'''.format(i, art[0], art[2], art[3])
        i += 1
        if i % 9 == 0:
            f.write(tex)
            tex = ''
            j = j + 1
        if i == len(article):
            f.write(tex)
    f.close()


def main():
    # for i in range(1,2091):
    # 你的简书主页地址
    url = 'https://www.jianshu.com/u/b0218515c59c'
    csrf = getcsrf(url)
    if csrf == 'error':
        print("获取 X-CSRF-Token 信息失败！")
    else:
        tex = getText(csrf, url)
        writeText(tex)


if __name__ == '__main__':
    main()
