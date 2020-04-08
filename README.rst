=============
elastic-graph
=============

Getting Started
===============

1. 安装数据库:

+ mysql>=5.6
+ elasticsearch>=7.0
+ neo4j>=3.5

2. 下载项目代码::

    $ git clone https://github.com/jadbin/elastic-graph

3. 安装项目依赖::

    $ pip install -r requirements/app.txt


4. 在 ``conf/elastic_graph.py`` 中配置数据库:

.. code-block:: python

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost:3306/elastic_graph?charset=utf8mb4'

    elastic_search_hosts = 'localhost:9200'

    neo4j_uri = 'bolt://localhost:7687'
    neo4j_auth = ('neo4j', 'password')

5. 调试模式运行项目::

    $ bash bin/manage debug

