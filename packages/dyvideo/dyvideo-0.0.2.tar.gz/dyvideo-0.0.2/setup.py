import os
import setuptools

from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))

# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description

# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


# 允许setup.py在任何路径下执行
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="dyvideo",  # 库名，需要在pypi中唯一
    version="0.0.2",  # 版本号
    author="SpartanFuk",  # 作者
    author_email="2383731235@qq.com",  # 作者邮箱（方便使用者发现问题后联系我们）
    description="Download Douyin video without watermark",  # 简介
    long_description=read_file('README.md'),  # 详细描述（一般会写在README.md中）
    long_description_content_type="text/markdown",  # README.md中描述的语法（一般为markdown）
    url="https://github.com/spartanfuk/dyvideo",  # 库/项目主页，一般我们把项目托管在GitHub，放该项目的GitHub地址即可
    packages=setuptools.find_packages(),  # 默认值即可，这个是方便以后我们给库拓展新功能的
    classifiers=[  # 指定该库依赖的Python版本、license、操作系统之类的
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    python_requires='>=3.6',
)


