from lxml import html
from WebCrawler import WebCrawler
import os

# This URL should point to the root directory page of the desired data dump. 
DUMP_URL = 'https://wikileaks.org/ciav7p1/cms/index.html'
URL_PREFIX ='/'.join(DUMP_URL.split('/')[0:len(DUMP_URL.split('/')) - 1])
header = {'User-Agent':'web-crawler'}



wc = WebCrawler(header, 10)
tree = wc.requestHTML(DUMP_URL)

fileCategories = tree.xpath('//div[@id="uniquer"]//h3/text()')
fileURLs = tree.xpath('//div[@id="uniquer"]/ul//table//td//div//a/@href')
fileTitles = tree.xpath('//div[@id="uniquer"]/ul//table//td//div//a/text()')


# Format file titles so they can be file names.
for i in range(0, len(fileTitles)):
    fileTitles[i] = fileTitles[i].replace('/', '-')
    fileTitles[i] = fileTitles[i].replace('"', '')
    fileTitles[i] = fileTitles[i].replace('\'', '')

skipExistingData = input(
    'Would you like to skip scraping files that already exist in output?(y/n)')

if skipExistingData == 'y':
    # Check to see if any of the files found on dump page have already been
    # scraped.
    pEF = os.listdir('output/')     # pEF = preExistingFiles

    for i in range(0, len(fileTitles)):
        if fileTitles[i] + '.txt' in pEF:
            fileTitles[i] = ''
            fileURLs[i] = ''

    fileTitles = [e for e in fileTitles if e != '']
    fileURLs = [e for e in fileURLs if e != '']



# Scrape file pages.
index = 0
for url in fileURLs:
    pageTree = wc.requestHTML(URL_PREFIX + '/' + str(url))
    textData = pageTree.xpath('//div[@id="uniquer"]//text()')
    attachmentURLs = pageTree.xpath(
            '//h3[text()="Attachments:"]/following-sibling::ul[1]//a/@href')

    # Download and save page attachments.
    for a in attachmentURLs:
        fullURL = URL_PREFIX + '/' + a      # Full URL of attachment.
        outPath = 'output/' + fileTitles[index] + '/'
        outFName = a.split('/')[1]

        if not os.path.exists(outPath):
            os.makedirs(outPath)

        data = wc.requestFileData(fullURL)
        with open(outPath + outFName, 'wb') as f:
            for chunk in data:
                f.write(chunk)

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
