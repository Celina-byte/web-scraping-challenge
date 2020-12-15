#Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def init_browser():
    executable_path={"executable_path":ChromeDriverManager().install()}
    return Browser("chrome",**executable_path, headless=False)

def scrape():
    #Open browser
    browser=init_browser()
    browser.visit("https://mars.nasa.gov/news/")

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # Searching for titles
    title = soup.find_all('div', class_='content_title')
    # Extract first title and paragraph, and assign to variables
    news_title = title[1].text

    # Search for paragraph 
    p_result= soup.find_all('div', class_="article_teaser_body")
    # Extract first title and paragraph, and assign to variables
    news_p = p_result[1].text



    #JPL Mars Space Images - Featured Image
    #Open Second browser
    browser.visit("https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars")
    #Getting to the images
    browser.links.find_by_partial_text("FULL IMAGE").click()
    browser.links.find_by_partial_text("more info").click()
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    pic1 = soup.find_all('figure', class_="lede")
    pic1_2=pic1[0].a['href']
    featured_img_url = 'https://www.jpl.nasa.gov' + pic1_2


    #Mars Facts
    #Using Pandas
    table= pd.read_html("https://space-facts.com/mars/")

    df_table = table[0]
    df_table.columns=['description', 'value']
  

    #Convert to html

    mars_table=[df_table.to_html()]
    
    #Mars Hemispheres
    #Open Second browser
    url='https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html

    hemisphere_image_urls = []

    # creating the Dictionary of the Hemispheres

    for x in range(0,4):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[x].click()
        sample = browser.find_link_by_text("Sample").first
        hemisphere["img_url"] = sample["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    mar_data = {
        "news_title":news_title,
        "news_p":news_p,
        "featured_img_url":featured_img_url,
        "mars_table":mars_table,
        "hemisphere_image_urls":hemisphere_image_urls
    }

    browser.quit()
    return mar_data