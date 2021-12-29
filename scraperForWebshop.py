#imports required 
import bs4
import requests 
import csv 
import urllib.request

#create base url, headers 
baseUrl = ''
urlShop = ''
i = 0
var = 22
datas = []
def saveImage(imgSrc, slum):
    global i
    #iterate for name of image
    i+=1 
    #add full path to save image and decorate name a bit 
    urllib.request.urlretrieve(imgSrc, slum+str(i)+".jpg")
    print('downloaded, currently on item: ' + str(i))

def iterateThroughAnItem(href, category, slum):
    global baseUrl
    ## you can find your user agent on google
    headers = {'User-Agent': ''}
    global datas
    global i
    req = requests.get(baseUrl+href, headers=headers)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    productBrand = soup.find('a', 'brand').getText()
    productName = soup.find('h1').getText()
    productCode = soup.find('dd', 'js-code').getText()
    productPrice = soup.find('span', 'product-price')
    if productPrice:
        productPrice = soup.find('span', 'product-price').getText()
        productPrice = productPrice.replace("KM", "")
    else:
        productPrice = '0'
    productDescription = soup.find('div', 'product-description')
    productSpecification = soup.find('div', 'specification')
    if productDescription:
        if productSpecification:
            productDescription = soup.find('div', 'product-description').getText()
            productSpecification = soup.find('div', 'specification').getText()
            productDescription = productDescription + ' ' + productSpecification
        else:
            productDescription = soup.find('div', 'product-description').getText()
    else: 
        productDescription = 'None'
    
    #image = soup.find('img', 'xzoom')
    #if image:
    #    if image.has_attr('xoriginal'):
    #        saveImage(image['xoriginal'], slum)
    #    else: 
    #        saveImage(image['src'], slum)
    i+=1
    print(str(i))
    productCategory = category+", Brendovi > " + productBrand
    images = 'https://www.yoursite.com' + slum + str(i) +".jpg"
    datas.append([productName, productBrand, productPrice, productCategory, images, productDescription, productCode])

def iterateThroughAPage(url, category, slum):
    global i
    i = 0
    headers = {'User-Agent': ''}
    for page in range(1, 22):
        req = requests.get(url+'?page='+str(page), headers=headers)
        soup = bs4.BeautifulSoup(req.text, 'html.parser')
        products = soup.findAll('div', 'item')
        for product in products:
            href = product.find('a')
            iterateThroughAnItem(href['href'], category, slum)

nameOfFile = 'zadnji2'
dictForLoop = {
    "links": [
        #links from which to scrape go here
    ],
    "categories": [
        #category names in following format Parent Category > Daughter > Daughter go here
    ],
    "slums": [
        # slum names go here
    ]
}

length = len(dictForLoop['slums'])
for j in range(0, length):
    percentage = (j/length)*100
    print('Working on: '+ dictForLoop['links'][j] + ' ' + str(percentage) + '%')
    iterateThroughAPage(dictForLoop['links'][j], dictForLoop['categories'][j], dictForLoop['slums'][j])

with open('{0}.csv'.format(nameOfFile), 'w', newline='') as file:
    writer = csv.writer(file)
    headers = ['Name', 'Brand', 'Price', 'Category', 'Images', 'Description', 'SKU']
    writer.writerow(headers)
    for data in datas:
        writer.writerow(data)
print ('csv finished.')