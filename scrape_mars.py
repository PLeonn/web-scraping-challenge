from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

mars_data = {}

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {'executable_path': 'C:/Users/Patrick Leon/chromedriver_win32/chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

#This section scrapes the site for Mars News
def scrape():
    browser = init_browser()
    
    scrape_url = "https://mars.nasa.gov/news/"
    browser.visit(scrape_url)
    
    pre_soup = requests.get(scrape_url)
    pre_soup_text = pre_soup.text
    
    title_bs = bs(pre_soup_text, 'html.parser')
    title_soup = title_bs.find('div', class_='content_title').find('a')
    title_text = title_soup.text
    
    html = browser.html
    para_soup = bs(html, 'html.parser')
    
    #Like before, not sure why I need this, but my CS friend said it should be here, and it works better
    time.sleep(4)
    
    para  = para_soup.find('div', class='article_teaser_body')
    
    para_text = para.text
    
    mars_data['title'] = title_text
    mars_data['paragraph'] = para_text
    
#This section scrapes the site for mars images
    img_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    base_url = "https://www.jpl.nasa.gov"
    
    browser.visit(img_url)
    
    big_img = browser.find_by_id('full_image')
    big_img.click()

    #Same as last time.sleep: don't know why I need it, but it works well like this
    time.sleep(4)
    
    #Find  image url and use BS to find titles and paragraph text
    site_html = browser.html
    
    img_soup = bs(site_html, 'html.parser')
    
    feat_img = img_soup.find('img', class_='fancybox-image')
    feat_img_url = base_url + feat_img
    mars_data['img_url'] = feat_img_url
    
    facts_url = "https://space-facts.com/mars/"
    tables = pd.read_html(facts_url)
    mars_df = tables[2]

    mars_df.columns=['Desc', 'Mars']
    mars_df.set_index('Desc', inplace=True)
    mars_df = mars_df.to_html()
    
    mars_data['facts'] = mars_df
    
    