import re
import requests
import random
import json
from datetime import datetime

# UA Collection
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


def get_content(url, page):
    # get api content,and return json
    headers = {

        'User-Agent': USER_AGENT,
    }
    url = url + '?order_by=shared_at&page='+str(page)

    content = requests.get(
        url, headers=headers).content.decode('utf-8', 'ignore')

    return json.loads(content)


def get_article_info(jsontxt):
    """
    get article info from json
    :param jsontxt: json
    :return: article info

    """
    title = jsontxt['object']['data']['title']
    url = jsontxt['object']['data']['slug']
    img = jsontxt['object']['data']['list_image_url']
    abstract = jsontxt['object']['data']['public_abbr']
    first_shared_at = jsontxt['object']['data']['first_shared_at']
    first_shared_at = datetime.strptime(
        first_shared_at, "%Y-%m-%dT%H:%M:%S.%f%z").strftime("%Y-%m-%d %H:%M:%S")
    veiw_count = jsontxt['object']['data']['views_count']
    return [url, img, title, abstract, first_shared_at, veiw_count]

# download img to img folder


def downloadimg(url, i):

    if url == "":
        img_name = "./img/default.png"
    else:
        print('Downloading img ' + str(i)+'...')
        img_name = './img/img'+str(i)+'.jpg'
        r = requests.get(url)
        with open(img_name, 'wb') as f:
            f.write(r.content)
            print('下载图片成功')
    return img_name


def writeText(article_info):
    """
    write article info to txt
    ---
    :param article = [[url,img,title,abstract,first_shared_at,view_count]]
    """
    # write pages to page.txt
    m = open('page.txt', 'w')
    page = int(len(article_info) / 9) + 1
    m.write(str(page))
    m.close()

    j = 1       # page count
    i = 0       # article count

    tex = ''    # html content

    for art in article_info:
        f = open('jianshu' + str(j) + '.html', 'w', encoding='utf-8')
        tex = tex + '''
<div class="col mb-4">
    <div class="card h-100">
        <div class="img-box">
        <a href="https://www.jianshu.com/p/{}" target="_blank">
            <img src="{}" class="card-img-top" alt="img">
        </a>
        </div>
        <div class="card-body">
            <a href="https://www.jianshu.com/p/{}" target="_blank">
                <h5 class="card-title">{}</h5> 
            </a>
        </div>
            <p class="card-text">{}</p>
            <p class="card-text"><small class="text-muted">Post time: {}  Views: {}</small></p>
        </div>
    </div>
</div>
'''.format(art[0], art[1], art[0], art[2], art[3], art[4], art[5])
        i += 1
        if i % 9 == 0:
            tex = tex+'''
<script>

    var aspectRatio = 16 / 9; // 你想要的宽高比（例如，16:9）
    var img = $(".content .card img");
    var desiredWidth = img.width(); // 设定你想要的宽度

    // 根据宽高比计算高度
    var desiredHeight = desiredWidth / aspectRatio;
    var a_ = $('.content .card .img-box');
    a_.css("height", desiredHeight + 'px'); // 设置图片的高度

</script>
'''
            f.write(tex)
            tex = ''
            j = j + 1
        if i == len(article_info):
            tex = tex+'''
<script>

    var aspectRatio = 16 / 9; // 你想要的宽高比（例如，16:9）
    var img = $(".content .card img");
    var desiredWidth = img.width(); // 设定你想要的宽度

    // 根据宽高比计算高度
    var desiredHeight = desiredWidth / aspectRatio;
    var a_ = $('.content .card .img-box');
    a_.css("height", desiredHeight + 'px'); // 设置图片的高度

</script>
'''
            f.write(tex)
        f.close()


def main():

    user_id = 'b0218515c59c'  # Your jianshu user_id
    url = 'https://www.jianshu.com/asimov/users/slug/'+user_id+"/public_notes"

    page = 1
    article_infos = []
    text = get_content(url, page)
    image_num = 0
    while text != []:

        for t in text:
            # get article info from json
            article_info = get_article_info(t)
            # download img to img folder
            image_name = downloadimg(article_info[1], image_num)
            article_info[1] = image_name
            image_num += 1
            # append article info to article_infos
            article_infos.append(article_info)
        page += 1
        text = get_content(url, page)
        # print(text,len(text))

    writeText(article_infos)


if __name__ == '__main__':
    main()
