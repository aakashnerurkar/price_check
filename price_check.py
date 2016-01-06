#amazon price change detector
import requests, hashlib, os, time, bs4, sys

#md5 fucntion
def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

#replace with any amazon product url
res = requests.get('Insert amazon.com product link')
res.raise_for_status
if res.status_code != 200:
    print('Status code '+ str(res.status_code))
    print('Something went wrong. Either site is unavailable or check youe internet connection')
    quit()
soupObj = bs4.BeautifulSoup(res.text, "html.parser")
price = soupObj.select('#priceblock_ourprice')

#replace with your current directory
if os.path.exists("yourcurrentdirectory\price.txt") == False:
    pricestr = str(price[0].getText())
    with open('price.txt', 'w') as file:
        file.write(pricestr)


pricemd5 = md5Checksum('price.txt')
print('The MD5 Checksum of price.txt is ' + pricemd5)

timestr = time.strftime("%d-%m-%Y %H-%M-%S")
filename1 = timestr +'price.txt'


new_pricestr = str(price[0].getText())
with open(filename1 , 'w') as file:
    file.write(new_pricestr)

new_pricemd5 = md5Checksum(filename1)
print('The MD5 checksum of '+ filename1 +' is ' + new_pricemd5)

if pricemd5 == new_pricemd5:
	print('Price has not changed. Price is '+ price[0].getText())
	os.remove(filename1)
else:
	print('Price has changed to ' + price[0].getText())
	os.replace(filename1 , 'price.txt')

