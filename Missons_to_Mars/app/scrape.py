from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import datetime as dt
import requests 

executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

def marsNews():
    mars_url = 'https://mars.nasa.gov/news'
    browser.visit(mars_url)
    html = browser.html
    mars_soup = bs(html, 'html.parser')
    news_article = mars_soup.find('div', class_='list_text')
    news_title = news_article.find('div', class_='content_title').text
    news_p = news_article.find('div', class_='article_teaser_body').text 
    news_info = [news_title, news_p]
    return news_info

def marsFacts():
    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)
    mars_facts_df = tables[0]
    mars_facts_df.columns = ['Description', 'Value']
    mars_facts_df = mars_facts_df.set_index('Description')
    return mars_facts_df.to_html(classes="table table-striped")

def marsHemispheres():
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = bs(html, "html.parser")
    hemispheres = soup.find_all('div', class_ = 'item')
    hemisphere_image_urls = []
    
    for x in hemispheres:
        title = x.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = x.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=bs(html, "html.parser")
        downloads = soup.find("div", class_ = "downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title" : title, "img_url" : image_url})
    return hemisphere_image_urls


def scrape_all():
    first_article = marsNews()
    title = first_article[0]
    paragraph = first_article[1]
 
    facts = marsFacts()
    hemispheres = marsHemispheres()

    mini_scrape = {'news_title' : title,
                        'news_paragraph' : paragraph,
                        'facts' : facts,
                        'hemispheres' : hemispheres}
    return mini_scrape