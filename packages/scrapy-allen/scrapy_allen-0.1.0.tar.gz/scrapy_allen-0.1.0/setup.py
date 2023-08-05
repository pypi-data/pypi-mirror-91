'''
@File       :   setup.py
@Author     :   Shu Huang
@Time       :   2021-01-11 15:30
@Version    :   0.1
@Contact    :   fengyeyouni@163.com
@Dect       :   None
'''

from setuptools import setup, find_packages     # 这个包没有可以pip一下

setup(
    name = "scrapy_allen",      # 这个是pip项目发布的名称
    version = "0.1.0",      # 版本号，pip默认安装最新版
    keywords = ("pip", "scrapy","elasticsearch"),
    description = "模块描述",
    long_description = "模块详细描述",
    license = "MIT Licence",

    # url = "https://github.com/jiangfubang/balabala",       # 项目相关文件地址，一般是github，有没有都行吧
    author = "Shu Huang",
    author_email = "fengyeyouni@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["beautifulsoup4","pandas","elasticsearch"]        # 该模块需要的第三方库
)