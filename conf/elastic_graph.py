# coding=utf-8

# Database URI, example: mysql://username:password@server/db?charset=utf8mb4
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost:3306/elastic_graph?charset=utf8mb4'

elastic_search_hosts = 'localhost:9200'

neo4j_uri = 'bolt://localhost:7687'
neo4j_auth = ('neo4j', 'password')

# guniflask configuration
guniflask = dict(
)
