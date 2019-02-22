#!/usr/bin/env python
# coding: utf-8

# ## Build Mars News website
# Goal is to build a web application that scrapes various websites for data related to the Mission to Mars and displays the information in a single HTML page. 
# 
# ### Step1 - Scrape various NASA websites to obtain required Information
# 
# This ipynb file contains the base code to generate scrape application (later converted to py file).
# 
# Modules key to this program
# - Splinter - used for launching a new browser to open sites that have required information 
# - BeautifulSoup - parses HTML page, finds the required information and returns the required text value
# - Requests - Library used for directly connecting with websites and downloading HTML content

# This is a .py file generated from the .ipynb file


## IMPORT ALL REQUIRED DEPENDENCIES
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
from requests import RequestException
import time

import pandas as pd


# ### URLs / Websites the information will be obtained from

# In[45]:


#URLs to scrape / find information from 
nasa_news_url = "https://mars.nasa.gov/news/"
jpl_imgs_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
jpl_imgs_server = "https://www.jpl.nasa.gov"

twitter_mars_url = "https://twitter.com/marswxreport?lang=en"

mars_fact_url = "http://space-facts.com/mars/"

mars_astro_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
mars_astro_server = "https://astrogeology.usgs.gov"

# SCRAPE Status variables
scrape_status = {"status" : True, "scrape_error_msg" : []}


# ### Function to open browser for visiting websites

# Global Functions
def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "E:/chromeDriver/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# ### Extract Mars related News Headline and News Subtext from the NASA news website

### Get Latest News from NASA News website

def get_latest_marsNews():
    
    news_title = ""
    news_subtxt = ""
    news_date = ""
    
    try:
        with init_browser() as browser:
            browser.visit(nasa_news_url)

            time.sleep(1)

            html = browser.html
            # parse html file using BS4
            mars_cnt = bs(html, "html.parser")
        
        #mars_cnt.prettify()
        news_date = mars_cnt.find('div',class_="list_date").text.strip()
        news_title = mars_cnt.find("div", class_= "content_title").a.text.strip()
        #print(news_title)
        news_subtxt = mars_cnt.find("div", class_= "rollover_description_inner").text.strip()
        #print(news_subtxt)

        return (news_date, news_title, news_subtxt)           
            
        
    except Exception as e:
        scrape_status['status'] = False
        scrape_status['scrape_error_msg'].append("Error@get_latest_news. Failed with reason %s" % (repr(e)))
        return (news_date,news_title, news_subtxt)

#testing
#get_latest_marsNews()


# Get Latest Mars image from JP wesite
def scrape_jps_image():
    mars_img = ""
    mars_img_desc = ""
    mars_img_thumnail = ""
    mars_img_title = ""
    
    try:
        with init_browser() as browser:
        
            browser.visit(jpl_imgs_url)            
            

            time.sleep(1)

            # Scrape page into Soup
            html = browser.html
            img_cnt = bs(html, "html.parser")

            # Get the div section that holds mars images
            #mars_imgs = img_cnt.find("div",class_ = "image_and_description_container").find("div", class_="img").img['src']

            mars_imgs = img_cnt.find("li",class_ = "slide")


            mars_img = jpl_imgs_server+mars_imgs.a['data-fancybox-href']
            mars_img_desc = mars_imgs.a['data-description']
            mars_img_thumnail = jpl_imgs_server+mars_imgs.a['data-thumbnail']
            mars_img_title = mars_imgs.a['data-title']

            # Quite the browser after scraping
            #browser.quit()

            # Return results
            return (mars_img, mars_img_desc, mars_img_thumnail, mars_img_title)
            
    except Exception as e:
        scrape_status['status'] = False
        scrape_status['scrape_error_msg'].append("Error@get_latest_image. Failed with reason %s" % (repr(e)))
        
        return (mars_img, mars_img_desc,mars_img_thumnail, mars_img_title)



#testing
#mars_img_link = scrape_jps_image()
#mars_img_link



def get_latest_marsWeather():
    mars_weather = ""
    try:
        #get html from NASA Twitter URL
        twit_resp = requests.get(twitter_mars_url)
        if(twit_resp.status_code == 200):
            # parse html file using BS4
            mars_wthr_twit = bs(twit_resp.content, "lxml")
            #mars_wthr_twit.prettify()
            wthr_twt = mars_wthr_twit.find("div",{"data-name": "Mars Weather"},class_= "tweet js-stream-tweet js-actionable-tweet js-profile-popup-actionable dismissible-content original-tweet js-original-tweet has-cards has-content")
            mars_weather = wthr_twt.p.text.strip()

            mars_weather = mars_weather.rstrip(wthr_twt.p.a.text.strip())
            #mars_weather = mars_weather.split("\n")[0]
            mars_weather = mars_weather.replace("\n"," ")
            #mars_weather

            return mars_weather
            
            
        else:
            raise RequestException
    except requests.exceptions.RequestException as e:
        scrape_status['status'] = False
        scrape_status['scrape_error_msg'].append("Error@get_mars_weather. Failed with reason %s" % (repr(e)))
        return mars_weather



#testing
#get_latest_marsWeather()


def get_mars_profile():
    
    mars_facts = pd.DataFrame()
    
    try:
        
        mars_facts = pd.read_html(mars_fact_url)[0]
        
        mars_facts.rename(columns = {0:"Profile",1:"Value"}, inplace = True)

        mars_facts.set_index("Profile",inplace = True)

        return mars_facts
    
    except Exception as e:
        scrape_status['status'] = False
        scrape_status['scrape_error_msg'].append("Error@get_mars_profile. Failed with reason %s" % (repr(e)))
        
        return mars_facts


#testing
#df = get_mars_profile()
#df.to_html()


def get_mars_hemis_imgs():
    hemi_imgs = []
    
    try:
        with init_browser() as browser:
        
            browser.visit(mars_astro_url)
            
            time.sleep(1)

            # Scrape page into Soup
            html = browser.html
            astroPg = bs(html, "html.parser")

            hemi_link = astroPg.find_all("h3")

            for hemi in hemi_link:
                img_dict = {}
                browser.click_link_by_partial_text(hemi.text)
                time.sleep(2)

                html = browser.html
                imgPg = bs(html, "lxml")

                img_dict['Title'] = hemi.text
                img_dict['ImgURL'] = imgPg.find("div", class_ = "downloads").a['href']

                hemi_imgs.append(img_dict)
                browser.click_link_by_partial_text("Back")
            
    except Exception as e:
        scrape_status['status'] = False
        scrape_status['scrape_error_msg'].append("Error@get_mars_hemisphere. Failed with reason %s" % (repr(e)))
        

    return hemi_imgs


#testing
#get_mars_hemis_imgs()


def scrape():
    mars_info = {}
    mars_info['NewsDate'],mars_info['NewsTitle'],mars_info['News_subTitle'] = get_latest_marsNews()
    mars_info['mars_LatestImg'],mars_info['mars_LatestImg_desc'], mars_info['mars_img_thumbnail'], mars_info['mars_img_title'] = scrape_jps_image()
    mars_info['mars_latestWthr'] = get_latest_marsWeather()
    mars_info['mars_profile'] = get_mars_profile().to_html(header = False, border = 0, \
                                                            classes = ['table table-striped table-hover borderless'])
    
    mars_info['mars_hemis_imgs'] = get_mars_hemis_imgs()
    
    # TEMPORARY USE - WHEN ASTROGEOLOGY SITE IS DOWN
    # if(not mars_info['mars_hemis_imgs']):
    #   mars_info['mars_hemis_imgs'] = [ { "Title" : "Cerberus Hemisphere Enhanced", "ImgURL" : "https://astrogeology.usgs.gov/cache/images/cfa62af2557222a02478f1fcd781d445_cerberus_enhanced.tif_full.jpg" }, \
    #                                    { "Title" : "Schiaparelli Hemisphere Enhanced", "ImgURL" : "https://astrogeology.usgs.gov/cache/images/3cdd1cbf5e0813bba925c9030d13b62e_schiaparelli_enhanced.tif_full.jpg" }, \
    #                                    { "Title" : "Syrtis Major Hemisphere Enhanced", "ImgURL" : "https://astrogeology.usgs.gov/cache/images/ae209b4e408bb6c3e67b6af38168cf28_syrtis_major_enhanced.tif_full.jpg" }, \
    #                                    { "Title" : "Valles Marineris Hemisphere Enhanced", "ImgURL" : "https://astrogeology.usgs.gov/cache/images/7cf2da4bf549ed01c17f206327be4db7_valles_marineris_enhanced.tif_full.jpg" } ]
    

    return (scrape_status,mars_info)

#testing
#sts, marsinfo = scrape()
#marsinfo 


#sts


# #### Output from scraping - saving it for future use incase of issues with websites
# {'NewsTitle': "NASA's Opportunity Rover Mission on Mars Comes to End",
#  'News_subTitle': "NASA's Opportunity Mars rover mission is complete after 15 years on Mars. Opportunity's record-breaking exploration laid the groundwork for future missions to the Red Planet.",
#  'mars_LatestImg': 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA22928_hires.jpg',
#  'mars_LatestImg_desc': 'In this navigation camera raw image, NASAs Opportunity Rover looks back over its own tracks on Aug. 4, 2010.',
#  'mars_latestWthr': 'Sol 2319 (2019-02-13), high -17C/1F, low -72C/-97F, pressure at 8.12 hPa, daylight 06:46-18:52',
#  'mars_profile': ['<table border="1" class="dataframe table table-striped">\n  <thead>\n    <tr style="text-align: right;">\n      <th></th>\n      <th>Value</th>\n    </tr>\n    <tr>\n      <th>Profile_param</th>\n      <th></th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <th>Equatorial Diameter:</th>\n      <td>6,792 km</td>\n    </tr>\n    <tr>\n      <th>Polar Diameter:</th>\n      <td>6,752 km</td>\n    </tr>\n    <tr>\n      <th>Mass:</th>\n      <td>6.42 x 10^23 kg (10.7% Earth)</td>\n    </tr>\n    <tr>\n      <th>Moons:</th>\n      <td>2 (Phobos &amp; Deimos)</td>\n    </tr>\n    <tr>\n      <th>Orbit Distance:</th>\n      <td>227,943,824 km (1.52 AU)</td>\n    </tr>\n    <tr>\n      <th>Orbit Period:</th>\n      <td>687 days (1.9 years)</td>\n    </tr>\n    <tr>\n      <th>Surface Temperature:</th>\n      <td>-153 to 20 °C</td>\n    </tr>\n    <tr>\n      <th>First Record:</th>\n      <td>2nd millennium BC</td>\n    </tr>\n    <tr>\n      <th>Recorded By:</th>\n      <td>Egyptian astronomers</td>\n    </tr>\n  </tbody>\n</table>'],
#  'mars_hemis_imgs': [{'Title': 'Cerberus Hemisphere Enhanced',
#    'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'},
#   {'Title': 'Schiaparelli Hemisphere Enhanced',
#    'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'},
#   {'Title': 'Syrtis Major Hemisphere Enhanced',
#    'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'},
#   {'Title': 'Valles Marineris Hemisphere Enhanced',
#    'ImgURL': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'}]}
