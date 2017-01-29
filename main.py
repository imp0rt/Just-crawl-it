from extractLinks import extractLinks
from getInput import getInput
from Queue import Queue
import threading
import time
import sys

output = str()
finished = False

queue = set()
crawled = set()
target = []

links = set()
hosts = set()
mails = set()

start = time.time()

q = Queue()


# Get a url from the queue, extract the links in it and remove it from the queue
def work():
    while True:
        url = q.get()
        getLinks(url)
        feedback()
        q.task_done()


# Extracts all the information from a link using extractLinks()
def getLinks(url):
    try:
        getData = extractLinks(url, target[1], crawled).gatherUrls()
        [queue.add(u) for u in getData[0] if u not in crawled]
        [links.add(link) for link in getData[1]]
        [hosts.add(host) for host in getData[2]]
        [mails.add(mail) for mail in getData[3]]
        crawled.add(url)
    except:
        pass


# Create all the threads running the function work
def createThreads(threads):
    for _ in range(threads):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


# Add the links from the queue set() to the actual q
def checkQueue():
    for link in queue.copy():
        q.put(link)
        queue.remove(link)
    q.join()
    checkFinish()


# Check if there are links on the queue
def checkFinish():
    if len(queue.copy()) > 0:
        checkQueue()
    else:
        exitProgram()


# Returns the running state to the user
def feedback():
    print "\r[*] Hosts: " + str(len(hosts)) + " Links: " + str(len(links)) + " Mails: " + str(len(mails)) + " Queue: " + str(len(queue)),
    sys.stdout.flush()


# Write the output data
def writeData():
    print "\n"
    writeFile("links.txt", links)
    writeFile("hosts.txt", hosts)
    writeFile("mails.txt", mails)


# Creates a file and writes a set in it
def writeFile(filename, index):
    print "[+] Writing " + filename + "\t" + str(len(index))
    linksFile = open(output + "/" + filename, "w")
    for i in sorted(index):
        linksFile.write(i + "\n")
    linksFile.close()


# Write data and close the program savely
def exitProgram():
    writeData()
    print "[*] Crawling proccess took " + str(time.strftime("%H:%M:%S", time.gmtime(time.time() - start)))
    exit(0)


def main():
    global target, output
    target, output, threads = getInput().checkInput()
    queue.add(target[0])
    hosts.add(target[1])
    feedback()
    createThreads(threads)
    checkFinish()


if __name__ == "__main__":
    main()
