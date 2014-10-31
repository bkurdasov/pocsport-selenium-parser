# -*- coding: utf-8 -*-
from selenium import webdriver
from string import maketrans
import time
import csv
import sys
sys.setdefaultencoding('utf-8')
BASE_URL='http://pocstorelocator.urbantalk.se/'
WWW='http://www.'
XPATH_LINKS='//img[contains(@src, "poc_o_marker.png")]'
XPATH_ONE_LINK='%s[%s]'% XPATH_LINKS
XPATH_STORES='//div[@class="searchresult_item"]'
XPATH_WEBSITE='p[@class="web_url"]/a'
XPATH_PHONE='p[@class="contact_phone"]/a'
XPATH_DIRECTIONS='p[@class="google_directions"]/a'
XPATH_ADDRESS='p[@class="street_address"]'
XPATH_NAME='h2'

with open('raw-data.csv','wb') as outfile:
    writer=csv.writer(outfile)
    writer.writerow(['Store name','Website','Phone','Street address','GoogleDirections'])
    browser = webdriver.Firefox()
    browser.get(BASE_URL)
    imgs=browser.find_elements_by_xpath(XPATH_LINKS)
    total_links=len(imgs)
    visited=[]
    print "Total links :",total_links
    result_len=0
    cur_link=0
    for link_number in xrange(1,total_links+1):
        cur_link+=1
        xpath=XPATH_ONE_LINK % link_number
        #print 'accessing xpath', xpath
        browser.get(BASE_URL)
        time.sleep(5)   #a bit hackish
        img=browser.find_element_by_xpath(xpath)
        img.click()
        time.sleep(5)
        items=browser.find_elements_by_xpath(XPATH_STORES)
        for item in items:
            store_name=''
            website=''
            address=''
            directions=''
            store_name_tag=item.find_elements_by_xpath(XPATH_NAME)    
            if store_name_tag:
                store_name=store_name_tag[0].text
            website_tag=item.find_elements_by_xpath(XPATH_WEBSITE)
            if website_tag:
                website=website_tag[0].get_attribute('href')
                if len(website)<len(WWW):
                    website=''
            phone_tag=item.find_elements_by_xpath(XPATH_PHONE)
            if phone_tag:
                phone=phone_tag[0].text
            directions_tag=item.find_elements_by_xpath(XPATH_DIRECTIONS)
            if directions_tag:
                directions=directions_tag[0].get_attribute('href').strip()
            address_tag=item.find_elements_by_xpath(XPATH_ADDRESS)
            if address_tag:
                address=address_tag[0].text
            writer.writerow(map(lambda x:x.encode('utf-8',errors='ignore'),[store_name,website,phone,address,directions]))
            outfile.flush()
            result_len+=1
        print
        print "Link %4s of %4s done."%(link_number,total_links) 
        print "Result so far: ",result_len
    print "Done!"
    browser.quit()
