import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
my_url='https://www.yucatan.com.mx/'
uClient=uReq(my_url)
page_html=uClient.read()
uClient.close()
page_soup=soup(page_html,"html.parser")
containers=page_soup.findAll("h2",{"itemprop":"name headline"})
filename="url55.txt"
f=open(filename,"w")
#containersx=page_soup.findAll("div",{"class":"img-container"})
#print(len(containersx))
#for container in containersx:
##   print("https://www.milenio.com"+container.a["href"])
  #  f.write("https://www.milenio.com"+container.a["href"]+"\n")

for container in containers:

    print(container.a["href"])
    f.write(container.a["href"]+"\n")

