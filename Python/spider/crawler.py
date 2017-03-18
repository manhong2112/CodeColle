# from lxml import etree
from bs4 import BeautifulSoup
import urllib as request
from urlparse import urljoin
import re
import os


def getHtml(url):
    res = request.urlopen(url)
    try:
        return url, res.read().decode("utf-8")
    except Exception:
        return url, res.read().decode("big5")


def extractLink(url, html):
    soup = BeautifulSoup(html, "html.parser")
    return set(map(lambda i: re.sub("#.*$", "", urljoin(url, i["href"])), soup.findAll('a')))
    # return set(etree.HTML(html).xpath("//a/@href"))


target = "http://example.com/" # 目標網站
startAt = "http://example.com/index.html" # 起始網頁
output = "output" # 輸出
downloadedLink = set()
toBeDownload = set()
toBeDownload.add(startAt)
p = re.compile("https?://.*?/(.*)")

while len(toBeDownload) != 0:
    try:
        url = toBeDownload.pop()
        downloadedLink.add(url)
        if (url.startswith("http") or url.startswith("https")) and not url.startswith(target):
            continue
        print "Downloading " + url
        _, content = getHtml(url)
        m = re.match(p, url)
        m = m.group(1)
        path, file = os.path.split(m)
        try:
            os.makedirs(os.path.join(output, path))
        except Exception:
            pass
        with open(os.path.join(output, m), "w") as f:
            f.write(content.encode('utf8'))
        newUrl = extractLink(url, content).difference(downloadedLink)
        toBeDownload = toBeDownload.union(newUrl)
    except Exception:
        print "Failed to Download " + url
