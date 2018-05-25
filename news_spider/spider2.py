import requests
import re
import json
import time
import random
from pyquery import PyQuery as pq


def get_html(url):
	USER_AGENTS = [
	    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
	    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
	    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
	    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
	    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
	    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
	    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
	    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
	    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
	    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
	    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
	    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
	    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
	    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
	    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
	]

	headers = {'user-agent': random.choice(USER_AGENTS)}
	response = requests.get(url, headers = headers)
	print(response.status_code)
	if response.status_code == 200:
		return response.text
	return None


def get_urls(html):
	doc = pq(html)
	list_div = doc('.g').items()
	pattern = re.compile('^\/url\?q=(.*?)&sa=.*', re.S)
	with open('urls.txt', 'a') as f:
		for div in list_div:
			a = div('h3 a').attr('href')
			url = re.findall(pattern, a)
			f.write(url[0] + '\n')


def save_urls():
	for i in range(38):
		url = "https://www.google.com.tw/search?q=guangzhou+Davos&tbm=nws&ei=XcMEW5HcAYLO8wXPsZmQAg&start="+str(i*10)
		html = get_html(url)
		get_urls(html)
		print('Page ', i + 1, 'done!')


def get_datas(html):
	doc = pq(html)
	list_div = doc('.g').items()
	pattern = re.compile('^\/url\?q=(.*?)&sa=.*', re.S)

	with open('data.json', 'a', encoding='UTF-8') as f:
		for div in list_div:
			dict = {}
			a = div('h3 a').attr('href')
			url = re.findall(pattern, a)
			dict['title'] = div('h3 a').text()
			dict['author'] = div('.slp span').text().split(' - ')[0]
			dict['pub_time'] = div('.slp span').text().split(' - ')[1]
			dict['url'] = url[0]
			json.dump(dict, f, ensure_ascii=False)
			f.write('\n')


def save_datas():
	for i in range(48):
		url = "https://www.google.com.tw/search?q=guangzhou+Davos&tbm=nws&ei=XcMEW5HcAYLO8wXPsZmQAg&start="+str(i*10)
		html = get_html(url)
		get_datas(html)
		print('Page ', i + 1, 'done!')


def get_content(html):
	doc = pq(html)
	items = doc('p').items()
	content = ''
	for item in items:
		content += item.text()+'\n'
	return content


def get_title(html):
	doc = pq(html)
	title = doc('h1').eq(0).text()
	return title


def main():
	# url_pattern = "https://webcache.googleusercontent.com/search?q=cache:(link)&num=1&hl=zh-CN&strip=1&vwsrc=0"
	with open('data.json', 'r', encoding='utf-8') as f:
		try:
			with open('result3.json', 'a', encoding='utf-8') as f2:
				while True:
					line = f.readline()
					if line:
						print("======")
						dict = json.loads(line)
						# url = url_pattern.replace('(link)', dict['url'])
						# print(get_html(url))
						# time.sleep(random.randint(5, 10))
						html = get_html(dict['url'])
						if html:
							# print(html)
							dict['content'] = get_content(html)
							# dict['title'] = get_title(html)
							json.dump(dict, f2, ensure_ascii=False)
							f2.write('\n')
							print(dict['title'])
					else:
						break
		except:
			f.close()


if __name__ == '__main__':
	# save_urls()
	# save_datas()
	main()	