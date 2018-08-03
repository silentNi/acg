import os
import sys
from scrapy.cmdline import execute

print(__file__)
os.path.dirname(__file__)
# sys.path="E:/Silent/python-silent/tutorial/"
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
print(sys.path)
execute(["scrapy","crawl","acgimages"])