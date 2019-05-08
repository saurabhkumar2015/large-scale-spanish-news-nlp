from newsplease import NewsPlease
import bs4
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json



def main():
    articles = []
    arti = []
    data = []
    #fetching articles url
    my_url = 'https://www.elpais.com.co/'
    open_url = urlopen(my_url)

    html = open_url.read()
    open_url.close()

    page_soup = BeautifulSoup(html,"html.parser")

    titles = page_soup.findAll("h2",{"class":"title"})

    

    paid_title = page_soup.find("div",{"class":"container-full zd"})
    paid_url = paid_title.findAll("h2",{"class":"title"})

    for y in paid_url:
        if(y.a['href'].startswith('https://')):
            arti.append(y.a['href'])
        else:
            arti.append("https://www.elpais.com.co" + y.a['href'])

    for x in titles:
        if(x.find("a",{"class":"page-link"})):
            url = x.a['href']
            if(url.startswith('https://')):
                articles.append(url)
            else:
                articles.append("https://www.elpais.com.co" + url)

    for p in arti:
        articles.remove(p)

      
    for post in articles:
        article = NewsPlease.from_url(post)
        data_json = {
            "URL": article.url,
            "Domain": article.source_domain,
            "title": article.title,
            "author": str(article.authors),
            "text": str(article.text),
            "date_published": str(article.date_publish)
        }
        data.append(data_json)
        
    with open('data2.json', 'w') as outfile:
        json.dump(data, outfile)
    


if __name__ == '__main__':
    main()