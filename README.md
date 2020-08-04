# 简书主页-->个人博客
基于简书的个人博客网站

![blog](blog.png)

## 基本方法

基于Python3，爬取个人简书主页的所有文章，然后写入jianshu*.html，然后用ajax加载。

## 使用

* 修改img文件夹中的logo_black.png,logo.ico为你自己的logo图片。

* 在`jiansshuspideer.py`中151行修改url为你的简书主页url，然后执行。

  ```shell
  python3 jiansshuspideer.py
  ```

* 最后部署到服务器的时候，可以写一个定时任务执行`jiansshuspideer.py`。

* 最后的博客运行时间请`blogtime.js`文件30行中的内容

  ```javascript
  var create_time = Math.round(new Date(Date.UTC(2020, 6, 28, 18, 0, 0))
  ```

  这里面的月份比较特殊，是从0开始的，如这里的6代表7月。

## TODO

1.突然想起来还没加上文章写作时间，下次吧

2.about界面还没写