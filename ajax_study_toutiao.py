import requests
from urllib.parse import urlencode
import os
from hashlib import md5
from multiprocessing.pool import Pool
import re
import time

def get_page(offset):
	params = {
		'offset': offset,
		'format': 'json',
		'keyword': '街拍',
		'autoload': 'true',
		'count': '20',
		'cur_tab': '1',
		'from': 'search_tab'
	}
	url = 'https://www.toutiao.com/search_content/?' + urlencode(params)
	try:
		response = requests.get(url)
		if response.status_code == 200:
			print('Request Successfully')
			return response.json()
	except requests.ConnectionError:
		print('Request Error')
		return None

def get_image(json1):
	#print(json1)
	if json1.get('data'):
		for item in json1.get('data'):
			title = item.get('title')
			#print(title)
			images = item.get('image_list')
			if images:
				for image in images:
					#print(image.get('url'))
					image_url = re.sub('list','origin',image.get('url'))
					#print(image_url)
					yield{
						'image':'http:' + image_url,
						'title':title
					}
def save_image(item):
	#if not os.path.exists(item.get('title')):
	#	os.mkdir(item.get('title'))#若不存在名为title的文件夹，便创建
	try:
		headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36',
		}
		response = requests.get(item.get('image'),headers=headers)
		if response.status_code == 200:
			file_path = r'C:\Users\hp\Desktop\Spider_study\爬取今日头条街拍\{0}_{1}.{2}'.format(item.get('title'),md5(response.content).hexdigest(),'jpg')
			#print(file_path)
			if not os.path.exists(file_path):
				with open(file_path,'wb') as f:
					f.write(response.content)
			else:
				print('Already Download',file_path)
		else:
			print('Failed,status_code:', response.status_code)
	except requests.ConnectionError:
		print('Failed to Save Image')

def main(offset):
	json1 = get_page(offset)
	for item in get_image(json1):
		#print('从get_image拿到的字典',item)
		save_image(item)

GROUP_START = 1
GROUP_END = 20
if __name__ == '__main__':
    #start_time = time.time()
	pool = Pool()
	groups = ([x * 20 for x in range(1,GROUP_END+1)])
	pool.map(main,groups)
	pool.close()
	pool.join()
    #end_time = time.time()
    #use_time = end_time - start_time
    #print('耗时：{0}.'.format(use_time))
