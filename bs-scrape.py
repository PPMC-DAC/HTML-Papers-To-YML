# Importing BeautifulSoup and 
# it is in the bs4 module
from bs4 import BeautifulSoup
import re # Regular Expressions
  
# Opening the html file. If the file
# is present in different location, 
# exact location need to be mentioned
HTMLFileToBeOpened = open("AsenjoPapers.html", "r")
  
# Reading the file and storing in a variable
contents = HTMLFileToBeOpened.read()
  
# Creating a BeautifulSoup object and
# specifying the parser 
beautifulSoup = BeautifulSoup(contents, 'html.parser')
  
# Using the prettify method to modify the code
#  Prettify() function in BeautifulSoup helps
# to view about the tag nature and their nesting
#print(beautifulSoup.body.prettify())
jcount=0
ccount=0
kcount=0
tcount=0

#results = soup.find(id="ResultsContainer")
papers = beautifulSoup.find_all("li")
for paper in reversed(papers):
    #print(paper, end="\n"*2) #.prettify(formatter='minimal')

    #Title:
    title = paper.find("i")
    print("- title: '{}'".format(title.text.strip("\"").replace("\n"," ")))
    #Authors:
    br = paper.find_all("br",limit=1)[-1]
    author = br.next_sibling
    print("  author: '{}'".format(author.strip().rstrip(".").replace("\n"," ")))
    #Publication:
    pub = paper.find("b")
    pub = pub.text.strip().replace("\n"," ")
    print("  pub: \"{}\"".format(pub))

    #Other:
    br = paper.find_all("br",limit=4)[-1]
    other = br.next_sibling
    other = other.strip().rstrip(".").replace("\n"," ")
    if other:
       print("  other: \"{}\"".format(other))
    #Other2:
    try:
       br2 = paper.find_all("br",limit=5)[-1]
       other2 = br2.next_sibling
       other2 = other2.strip().rstrip(".").replace("\n"," ")
       if other2 != other:
          other2 = " ".join(other2.split())
          print("  other2: \"{}\"".format(other2))
    except:
       pass

    idassigned=False
    url=""
    pdf=""
    paperurls = paper.find_all("a")
    for link in paperurls:
        
        if "pdf" in link.text.lower():
           print("  pdf: '{}'".format(link.get("href")))
        if "UMA-DAC-" in link.text:
              paperid = link.text
              print("  id: '{}'".format(paperid))
              idassigned=True
        if link.get("href"):
            if "long" in link.text.lower():
                temp=link.get("href").split("/")[-1]
                longpdf = temp.replace(".ps.gz",".pdf")
                print("  longpdf: '{}'".format(longpdf))
            elif ".ps.gz" in link.get("href"):
                temp=link.get("href").split("/")[-1]
                pdf = temp.replace(".ps.gz",".pdf")
                print("  pdf: '{}'".format(pdf))
            elif ".pdf" in link.get("href"):
                if pdf == "":
                    pdf=link.get("href").split("/")[-1]
                    print("  pdf: '{}'".format(pdf))
                else:
                    pdf2=link.get("href").split("/")[-1]
                    print("  pdf2: '{}'".format(pdf2))
            elif  "doi" in link.text.lower():
                doi = link.get("href")
                print("  doi: '{}'".format(doi))
            elif url == "":
                url = link.get("href")
                print("  url: '{}'".format(url))
            else:
                url2 = link.get("href")
                print("  url2: '{}'".format(url2))
        
        name = link.get("name")
        if name:
           print("  name: '{}'".format(name))
           if "UMA-DAC-" in link.text and not idassigned:
                paperid = link.text
                print("  id: '{}'".format(paperid))
                idassigned=True

    if not idassigned:
        #print(paper.text)
        m = re.search(r"UMA-DAC-\d+/\d+", paper.text)
        if m.group() != None:
            id = m.group()
            print("  id: '{}'".format(id))

    #year
    if other !="":
        m = re.search(r"(20\d\d)|(19\d\d)",other)
    else:
        m = re.search(r"(20\d\d)|(19\d\d)",pub)
    if m.group() != None:
        year = m.group()
        print("  year: '{}'".format(year))
    else:
        print("  year: ")   
#papertype

    papertype= pub.lower()
    if "journal" in papertype or "j." in papertype or "trans." in papertype:
        type="journal"
        jcount=jcount+1
    elif "keynote" in papertype:
        type="keynote"
        kcount=kcount+1       
    elif "technical" in papertype:
        type="technical"
        tcount=tcount+1
    else:
        type="conference"
        ccount=ccount+1
    print("  count: ")
    print("  type: {}".format(type))
    
    #print("\n------------\n"*2)
    print("\n")

print("j={}, c={}, k={}, t={}".format(jcount,ccount,kcount,tcount))
  
