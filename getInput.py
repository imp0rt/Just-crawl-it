from urlparse import urlparse
import optparse
import re
import os


class getInput:
    target = []
    output = "Links"
    threads = 10

    # Get the input from the user
    def checkInput(self):
        parser = optparse.OptionParser("%prog -u <url> [-d <output directory>]")
        parser.add_option("-u", dest="url", help="specify target url")
        parser.add_option("-o", dest="output", help="specify directory for output files")
        parser.add_option("-t", dest="threads", help="specify number of threads")
        (options, args) = parser.parse_args()
        self.saveInput(parser, options)
        self.printInformation()
        return self.target, self.output, self.threads

    # Filter the input and save it to the respective variables
    def saveInput(self, parser, options):
        if options.url:
            self.target += [self.parseUrl(options.url)]
            self.target += [urlparse(self.target[0])[1]]
        else:
            parser.print_help()
            exit(0)
        if options.output != None:
            self.output = options.output
        if options.threads != None:
            self.threads = int(options.threads)
        self.createOutputDirectory(self.output)

    # Create a directory to store the output, if there is not one already
    def createOutputDirectory(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    # Add http to the input hosts
    def parseUrl(self, url):
        expression = re.compile("(http|https)://.")
        if expression.match(url) == None:
            return "http://" + str(url)
        return url

    # Print input information
    def printInformation(self):
        print "Target: " + self.target[1]
        print "Output directory: " + self.output
        print "Threads: " + str(self.threads) + "\n"