import json
import csv
import urllib.request
import sys

baseUrl = sys.argv[1]
fileOut = sys.argv[2]
url = baseUrl + '/products.json'

def getPage(page):
	reqData = urllib.request.urlopen(url + '?page={}'.format(page))
	data = reqData.read()
	encoding = reqData.info().get_content_charset('utf-8')
	products = json.loads(data.decode(encoding))['products']
	return products

def cleanURL(url):
	newURL = url.split('.jpg')[0] +'_large.jpg'
	return newURL

def genColorSwatch(c):
	swatchURL = 'https://cdn.shopify.com/s/files/1/0856/7558/t/31/assets/'
	c = c.split(' -')[0]
	swatch = swatchURL +c.lower().replace(' ', '-').replace('/', '-')+'.jpg'
	return swatch

with open(fileOut, 'w') as f:
	writer = csv.writer(f)
	writer.writerow(['Title','Product Type','Sku','Price','Color','Color Swatch','Image'])
	page = 1
	products = getPage(page)
	while products:
		for product in products:
			title = product['title']
			type = product['product_type']
			for variant in product['variants']:
				sku = variant['product_id']
				price = variant['price']
				color = variant['option1']
				color_swatch = genColorSwatch(color)
				if(variant['featured_image'] is None):
					image = ''
				else:
					image = cleanURL(variant['featured_image']['src'])
				row = [title, type, sku, price, color.split(' -')[0], color_swatch, image]
				writer.writerow(row)
		page += 1
		products = getPage(page)

