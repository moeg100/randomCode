from bs4 import BeautifulSoup
import requests as rq

html_doc = rq.get("https://www.example.com")
#print(html_doc.text)

soup = BeautifulSoup(html_doc.text, 'html.parser')

title = soup.find("h1")


print(title)
