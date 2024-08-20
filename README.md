# NewsScrapy

---

## 目录

- [简介](#简介)

- [功能模块](#功能模块)

- [安装](#安装)

- [配置](#配置)

- [使用方法](#使用方法)

  

---

## 简介

本项目旨在开发一个综合性的数据采集和展示平台，结合Scrapy和Flask框架，实现从网易新闻网站爬取数据、存储、分析并展示数据的全流程操作。该平台通过Scrapy定期爬取网易新闻内容，利用中间件动态生成随机请求标头和代理，确保爬取过程的稳定性和隐私保护。爬取到的数据将被存储到数据库中，随后通过Pandas进行深入的数据分析。最终，使用Flask框架将分析结果以Web应用的形式展示

## 功能模块

1. **Scrapy爬虫模块**
   - **网站爬取**：定期从网易新闻网站爬取最新的新闻数据，涵盖多个新闻类别。
   - **中间件随机化**：实现请求的动态标头生成和代理选择，以防止被目标网站屏蔽。
   - **代理池管理**：在爬取过程中动态更新代理池，确保代理的有效性和爬取的连续性。
   - **数据存储**：使用Scrapy的管道功能，将爬取到的新闻数据存储到关系型数据库中。
2. **数据分析模块**
   - **数据清洗**：利用Pandas对存储的数据进行清洗和预处理，去除无效或重复的信息。
   - **数据分析**：通过Pandas进行统计分析和数据聚合，例如新闻类别分布、关键词提取、发布时间统计等。
   - **报告生成**：生成数据分析报告，支持多种输出格式（如CSV、Excel、PDF等）。
3. **Flask展示模块**
   - **Web界面设计**：开发用户友好的Web界面，展示分析后的新闻数据和报告。
   - **数据展示**：实时显示新闻数据的统计信息，如新闻数量、热点新闻、分类分布等。

---

## 安装

当前项目使用环境 python 3.11，MySQL 8.0.30

```bash
# 克隆仓库
git clone https://github.com/your-username/MyPythonProject.git

# 安装依赖
pip install -r requirements.txt


```



## 配置

#### 修改mysql配置(必须修改)

修改 /new/proxy/sql_proxy.py 文件

```python
class sql_proxy:
    def __init__(self, host='localhost',	# 主机地址
                     database='proxy',	# 数据库名
                     user='root',		# 用户名
                     password='xxxxx'):	# 密码


```

修改/new/pipelines.py文件

```python
def dbHandle():
    conn = pymysql.connect(
        host="localhost",	# 主机地址
        user="root",		# 用户名
        passwd="xxxxx",		# 密码
        database='proxy',	# 数据库名
    )
    return conn
```

### 修改爬取间接

/package.json   单位/毫秒

```json
{
    "time": { // 上传爬取时间
        "update": "20240620160225", 
        "crawl": "20240620160223", 
        "getdata": "20240819224328"
    }, 
    "interval": {
        "update": 3600, // 代理更新间隔
        "crawl": 86400, //代理爬取间隔
        "getdata": 300  // 新闻数据爬取间隔
    }
}
```



## 使用方法

确保环境安装正确以及mysql配置修改完成

启动mysql



运行app.py文件 单独启动flask

运行start.py文件 单独启动scrapy

运行main.py同时启动flask和scrapy



确保flask启动后访问http://127.0.0.1:5000

注意：初次运行时，需等scrapy爬取完毕，页面才会有数据。

