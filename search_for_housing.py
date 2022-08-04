# make sure following modules are installed
# used with Python 3.7.5
import os
import time
from bs4 import BeautifulSoup as bs
from requests import Session

nMax    =   5
sites = { 'craigslist': 'https://santabarbara.craigslist.org/search/apa?sort=date&availabilityMode=0&max_price=5500&min_bedrooms=3&postal=93117&search_distance=12' }
#sites = { 'trulia': 'https://www.trulia.com/for_rent/34.26964,34.60235,-119.90349,-119.59622_xy/3p_beds/0-5500_price/APARTMENT,APARTMENT_COMMUNITY,APARTMENT%7CCONDO%7CTOWNHOUSE,CONDO,COOP,LOFT,SINGLE-FAMILY_HOME,TIC,TOWNHOUSE_type/' }

houses  =   {}

def house_hunt( site, url ):
    if site == 'craigslist':
        with Session() as s:
            site = s.get(url)                                                                     #connect to login page
            time.sleep(7)
            soup = bs(site.content, "html.parser")                                                #convert html in more readable format
            results     =   soup.findAll("div",{"class":"result-info"})
            for result in results[:nMax]:
                house_id    = result.find("h3",{"class":"result-heading"}).find("a")['data-id']
                bedroom     = result.find("span",{"class":"result-meta"}).find("span",{"class":"housing"}).text.split()[0]
                price       = result.find("span",{"class":"result-meta"}).find("span",{"class":"result-price"}).text.split()[0]
                link        = result.find("h3",{"class":"result-heading"}).find("a")['href']
                if house_id not in houses.keys():
                    houses[str(house_id)]   = {}
                    houses[str(house_id)]['bedrooms']   = str(bedroom)
                    houses[str(house_id)]['price']      = str(price)
                    houses[str(house_id)]['link']       = str(link)
                    if len(houses.keys()) > nMax:
                        os.system("./send_message_to_chat.sh %s"%(str(link)))
                    time.sleep(7)
    if site == 'trulia':
        with Session() as s:
            site = s.get('https://www.trulia.com/login')
            soup = bs(site.content, "html.parser")                                                #convert html in more readable format
            login_data = {"email":'frannythekid@gmx.com',"password":'atleast8characters'}    #store login credentials
            time.sleep(7)
            s.post('https://www.trulia.com/login',login_data)
            time.sleep(3)
            site = s.get(url)                                                                     #connect to login page
            soup = bs(site.content, "html.parser")                                                #convert html in more readable format
            results     =   soup.find("div",{"id":"main-content"})
            print(soup)
            sys.exit()
            for result in results[:nMax]:
                house_id    = result.find("a").find("address",{"class":"list-card-addr"}).text
                link        = result.find("a")['href']
                bedroom     = result.find("div",{"class":"list-card-heading"}).find("ul",{"class":"list-card-details"}).findAll("li")[0]["class"].text.split()[0]
                price       = result.find("div",{"class":"list-card-heading"}).find("div",{"class":"list-card-price"}).text.split()[0]
                print(house_id)
                print(link)
                print(bedroom)
                print(price)
                break

# start the website session
while True:
    for site, url in sites.items():
        house_hunt( site, url )
    time.sleep(5*60)
