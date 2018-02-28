from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = Browser('chrome', headless=False)
    mars_info = {}
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    d = soup.find('div', class_='list_text')
    title_div = d.find('div', class_="content_title")
    teaser_div = d.find('div', class_="article_teaser_body")
    link = title_div.find('a')
    news_title=link.contents[0]
    news_p=teaser_div.contents[0]
    mars_info["NewsTitle"] = news_title
    mars_info["NewsTeaser"] = news_p



    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    l = soup.find('li', class_='slide')
    link = l.find('a')
    featured_image_url="https://www.jpl.nasa.gov"+link["data-fancybox-href"]

    mars_info["FeaturedImage"] = featured_image_url
    print(featured_image_url)


    browser.visit("https://twitter.com/marswxreport")
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    mars_weather=""
    while mars_weather[0:3]!="Sol":
        # Retrieve all elements that contain book information
        l = soup.find('li', class_="js-stream-item stream-item stream-item")
        d = soup.find("div",class_="tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet")
        p = soup.find("p",class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
        mars_weather=p.contents[0]
    mars_info["MarsWeather"] = mars_weather



    url = 'https://space-facts.com/mars/'
    tables = pd.read_html(url)

    df = tables[0]
    df = df.iloc[1:]
    html_table = df.to_html()
    mars_info["MarsFacts"] = html_table

    browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    hemisphere_image_urls = []

    for link in soup.find_all('h3'): 
        browser.click_link_by_partial_text(link.get_text())
        soup = BeautifulSoup(browser.html, 'html.parser')
        div = soup.find("div", class_="downloads")
        a = div.find("a")
        hemisphere_image_urls.append({"title": link.get_text(), "img_url": a["href"]})
        browser.back()
        
    mars_info["MHP"] = hemisphere_image_urls

    return mars_info

        
        
        
        
        
        
        
    
