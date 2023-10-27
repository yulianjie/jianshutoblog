# 简书主页-->个人博客

[English](README.md)|中文

基于简书的个人博客网站

![blog](blog-0816.png)

## 基本方法

基于Python3，爬取个人简书主页的所有文章，然后写入jianshu*.html，然后用ajax加载。

## 使用

### 修改

* 修改img文件夹中的logo_white.png,logo.ico为你自己的logo图片。

* 在`getInfoFromJianshuApi.py`中151行修改url为你的简书主页url，然后执行。

  ```shell
  python3 jiansshuspideer.py
  ```

* 最后部署到服务器的时候，可以写一个定时任务执行`getInfoFromJianshuApi.py`。

* 最后的博客运行时间请`blogtime.js`文件30行中的内容

  ```javascript
  var create_time = Math.round(new Date(Date.UTC(2020, 6, 28, 18, 0, 0))
  ```

  这里面的月份比较特殊，是从0开始的，如这里的6代表7月。

### 使用github的action自动爬取

具体请看注释

```yml
name: jianshutoblog

on: #每一次提交或者每天早上5点开始爬取
  push:
  schedule:
    - cron: '0 21 * * *'

jobs:
  build:
    runs-on: ubuntu-latest #一般来说使用Ubuntu最新版本没说什么问题
    steps:
    - name: checkout actions
      uses: actions/checkout@v1
    - name: Set up Python 3.7 # 使用Python3.7的环境
      uses: actions/setup-python@v1
      with:
        python-version: 3.7
    - name: spider
      run: | #安装requests库并执行Python文件
        pip3 install requests
        python3 getInfoFromJianshuApi.py
    - name: commit
      run: |
        git config --global user.email jackyu0915@gmail.com #改成你的邮箱
        git config --global user.name JackietYu #改成你的用户名
        git add .
        git commit -m "Everyday update" -a
    - name: Push changes
      uses: ad-m/github-push-action@master
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
```

## TODO

~~1.突然想起来还没加上文章写作时间，下次吧~~

2.about界面还没写

## 更新说明

- 20-08-16 添加文章显示时间，优化了前端界面。
- 23-10-27 获取文章信息的方式更改为简书 api,详见 [issue 1](https://github.com/yulianjie/jianshutoblog/issues/1).