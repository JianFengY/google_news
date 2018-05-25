import xlwt
import json

wb = xlwt.Workbook()

sheet = wb.add_sheet('news')
sheet.write(0, 0, 'Title')
sheet.write(0, 1, 'Publisher')
sheet.write(0, 2, 'Publish Time')
sheet.write(0, 3, 'Url')
sheet.write(0, 4, 'Content')

i = 1
with open('result3.json', 'r', encoding='utf-8') as f:
	while True:
		line = f.readline()
		if line:
			dict = json.loads(line)
			sheet.write(i, 0, dict['title'])
			sheet.write(i, 1, dict['author'])
			sheet.write(i, 2, dict['pub_time'])
			sheet.write(i, 3, dict['url'])
			sheet.write(i, 4, dict['content'])
			print('第', i, '条…')
			i += 1
		else:
			break
wb.save('news.xlsx')