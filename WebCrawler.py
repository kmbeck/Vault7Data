from lxml import html
import Logger
import requests
import time

###
# Kyle Beck, 2/18/2017
# This class provides a simple interface for requesting html from webpages. It
# will automatically track important information such as the number of requests
# made and the average rate of reqeusts, and makes it easy to scale your
# request rate off of the response time of the target server.
###

class WebCrawler:

    def __init__(self, headers, reqRateFactor):
        self.headers = headers
        self.reqRateFactor = reqRateFactor
        self.reqsMade = 0
        self.successfulReqs = 0
        self.failedReqs = 0    
        self.prevResponseTime = 0.0
        


    # Requests and returns html from target url. Will return None if request
    # fails.
    def requestHTML(self, tgtURL):

        # Wait before making request. Wait time based on response time of
        # server.
        time.sleep(self.prevResponseTime * self.reqRateFactor)

        # Request page.
        start = time.time()
        page = requests.get(tgtURL, self.headers)
        end = time.time()
        
        # Update data/metadata.
        self.prevResponseTime = end - start
        self.reqsMade += 1
        

        if page.status_code == 200:
            print('Request on: ' + tgtURL + ' -- SUCCESS')
            tree = html.fromstring(page.text)
            self.successfulReqs += 1
            return tree
        else:
            print('Request on: ' + tgtURL + ' -- FAILED')
            self.failedReqs += 1
            return None

    # Reqeusts and returns file data from target url.
    def requestFileData(self, tgtURL):
 
        # Wait before making request. Wait time based on response time of
        # server.
        time.sleep(self.prevResponseTime * self.reqRateFactor)

        # Request page.
        start = time.time()
        data = requests.get(tgtURL, self.headers)
        end = time.time()
        
        # Update data/metadata.
        self.prevResponseTime = end - start
        self.reqsMade += 1
        

        if data.status_code == 200:
            print('Request on: ' + tgtURL + ' -- SUCCESS')
            self.successfulReqs += 1
            return data
        else:
            print('Request on: ' + tgtURL + ' -- FAILED')
            self.failedReqs += 1
            return None   

