from lxml import html
from WebCrawler import WebCrawler
#import urllib.request
#import urllib.request.urlretrieve

# This URL should point to the root directory page of the desired data dump. 
DUMP_URL = 'https://wikileaks.org/ciav7p1/cms/index.html'
URL_PREFIX ='/'.join(DUMP_URL.split('/')[0:len(DUMP_URL.split('/')) - 1])
OUTFILE = 'Vault7_CIAHackingToolsRevealed.html'
header = {'User-Agent':'web-crawler'}



wc = WebCrawler(header, 10)
tree = wc.requestHTML(DUMP_URL)

fileCategories = tree.xpath('//div[@id="uniquer"]//h3/text()')
fileURLs = tree.xpath('//div[@id="uniquer"]/ul//table//td//div//a/@href')
fileTitles = tree.xpath('//div[@id="uniquer"]/ul//table//td//div//a/text()')

# Format file titles so they can be file titles.
for i in range(0, len(fileTitles)):
    fileTitles[i] = fileTitles[i].replace('/', '-')
    fileTitles[i] = fileTitles[i].replace('"', '')
    fileTitles[i] = fileTitles[i].replace('\'', '')

# Scrape file pages.
index = 0
for url in fileURLs:
    pageTree = wc.requestHTML(URL_PREFIX + '/' + str(url))
    textData = pageTree.xpath('//div[@id="uniquer"]//text()')
    
    # Remove blank lines...
    for i in range(0, len(textData)):
        if textData[i] == '':
            del textData[i]
            i -= 1
    
    # Output file.
    with open('output/' + fileTitles[index] + '.txt', 'w', encoding='utf-8') as f:
        for r in textData:
            f.write(r)

    index += 1
