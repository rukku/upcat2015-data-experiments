from bs4 import BeautifulSoup
import csvkit #because Unicode
import os
import wget

        """
        This script downloads all the results pages for UPCAT 2015 and then extracts the results to a csv file.
        """

def downloadResults():
    """Download all the html files of the results"""
    baseurl = 'http://upcat.up.edu.ph/results/'
    page = "page-%003d.html"
    for i in range(151)[1:]:
        currentpage = page % i
        pageurl = baseurl + currentpage
        #print "Processing %s \n" % currentpage
        if os.path.isfile(currentpage):
            print "%s Already exists \n" % currentpage
            continue
        else:
            wget.download(pageurl)
            print "Downloading %s" % currentpage


def listHTML():
    """Create list of all HTML files to be processed"""
    htmlList = open('html.list.txt','wt')
    for r,d,f in os.walk("."):
        for files in f:
            if files.endswith(".html"):
                #print os.path.join(r,files) 
                out = os.path.join(r,files) + "\n" 
                htmlList.write(out)

def readList():
    """Loads the list of HTML files to be processed from a text file"""
    htmlFile = open('html.list.txt')
    htmlList = []
    for line in htmlFile.readlines():
        htmlList.append(line)
    return htmlList

def process(htmlfile):
    """
    The workhorse program. Iterates through each file and extracts the 
    passers from each HTML file and writes them to a csv file
    """
    page = open(htmlfile)
    soup = BeautifulSoup(page)
    tables = soup.findAll('table', {'class': ['printable']})

    #check if file exists and append if it does
    outfile = 'passers.csv'
    if os.path.isfile(outfile):
        f = open('passers.csv','ab')
        writer = csvkit.writer(f)
    else:
        f = open('passers.csv','wb')
        writer = csvkit.writer(f)
        writer.writerow(("Name", "Campus", "Course"))

    for row in tables[0].findAll('tr')[1:]:
        col = row.findAll('td')
        name = col[0].text
        if name.endswith(")"):
            name = name[:-13]
        campus = col[1].text    
        course = col[2].text
        #print name, campus, course
        writer.writerow( (name, campus, course))
    
    f.close()
    page.close()

def cleanURL(url):
  url = url[2:-1]
  return url

def getPassers():
    downloadResults()
    listHTML()
    htmls = readList()
    for html in htmls:
        html = cleanURL(html)
        process(html)

if __name__ == '__main__':
    getPassers()
