from BeautifulSoup import BeautifulSoup
from urlparse import urlparse
import urllib2
import re


class extractLinks:
    urlsFound = set()
    linksFound = set()
    hostsFound = set()
    mailsFound = set()

    def __init__(self, baseurl, hosts, crawled):
        self.baseurl = baseurl
        self.hosts = hosts
        self.crawled = crawled

    # Main method
    def gatherUrls(self):
        if "mailto:" in self.baseurl:
            try:
                self.parseMails(self.baseurl)
            except:
                pass
        elif self.baseurl not in self.crawled:
            try:
                self.extractLinks(self.baseurl)
                self.hostsFound.add(urlparse(self.baseurl)[1])
            except:
                pass
        return [self.urlsFound, self.linksFound, self.hostsFound, self.mailsFound]

    # Checks if there is a mail in the url (mailto)
    def parseMails(self, url):
        expression = r"mailto:(\w.{1,20}(@|<at>)\w{1,15}\.[a-zA-Z0-9.]{1,8})"
        mail = re.search(expression, url).group(1)
        mail = mail.replace("<at>", "@")
        self.mailsFound.add(mail)

    # Gets a url and extracts all its links, saving them to the respective set
    def extractLinks(self, baseurl):
        html = urllib2.urlopen(baseurl).read()
        links = self.findLinks(html)
        for link in links:
            if link != None:
                url = self.parseLink(baseurl, link)
                host = urlparse(url)[1]
                if (url not in self.crawled) and (host == self.hosts):
                    self.urlsFound.add(url)
                self.linksFound.add(url)
                self.hostsFound.add(host)

    # Finds links on the source code
    def findLinks(self, html):
        result = set()
        for link in BeautifulSoup(html).findAll("a"):
            result.add(link.get("href"))
        return result

    # Convert the links to urls
    def parseLink(self, base, link):
        link = link.rstrip("/")
        if link[:4] == "http":
            return link
        else:
            url = "http://" + urlparse(base)[1]
            if link[:1] == "/":
                url += link
            elif link[:2] == "//":
                url += link[1:]
            else:
                url += "/" + link
            return url
