import urllib.request as request
from lxml import etree

response = request.urlopen("http://www.linovel.net/book/detail?id=" + input("Bookid > ")).read();
page = etree.HTML(response)

i = 0
for book in page.xpath("//div[@class='chapter-grid row']"):
	i += 1
	print(i)
	tmp = etree.HTML(etree.tostring(book))
	for chapter in tmp.xpath("//div/a/text()"):
		print(chapter)
	for link in tmp.xpath("//div/a/@href"):
		print("http://www.linovel.net" + link)

print("End")