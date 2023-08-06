from setuptools import setup, find_packages
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="urllib3_1_26_2",
    version="1.26.2.0",
    author="luozhijun",
    author_email="roy_luo18@163.com",
#    packages=['urllib3_1_26_2'],
    packages=find_packages(),
    python_requires='>=3.6',
)

