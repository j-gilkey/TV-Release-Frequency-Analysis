import requests
from bs4 import BeautifulSoup
import mysql_etl_functions

def imdb_season_1_scraper(id_list):
    '''takes in a list of IMDb TV show ids and then scrapes the season 1
    episode ratings and vote counts. Then passes each scraped episode to
    mysql_etl_functions.imdb_episode_rating_etl to insert it into MySQL'''

    for id in id_list:
        if id_list.index(id)%10 == 0:
            print("on show number " + str((id_list.index(id) + 1)) )
        page = requests.get("https://www.imdb.com/title/" + str(id[0]) +  "/episodes?season=1")
        soup = BeautifulSoup(page.content, 'html.parser')
        list = soup.find_all(class_="ipl-rating-star small")
        #get all outer classes containing the rating and vote counts

        episode_number = 1
        if len(list):
            for item in list:
                #loop through each scraped class
                if len(item.find_all(class_="ipl-rating-star__rating")) & len(item.find_all(class_="ipl-rating-star__total-votes")):
                    #check to be sure the info we want exists, then extract what we want
                    imdb_tuple = (id[0], id[1], episode_number, 1 ,  str(item.find_all(class_="ipl-rating-star__rating")[0].string), str(item.find_all(class_="ipl-rating-star__total-votes")[0].string.strip('()')))
                    #tuple elements are as follows: (imdb_show_id, moviedb_show_id, espisode_number, rating, total votes)
                    episode_number += 1
                    #this counter just keeps track of what episode we're on
                    mysql_etl_functions.imdb_episode_rating_etl(imdb_tuple)





def imdb_paginate():
    #this function exists to retrieve IMDb ids from MySQL and then pass them to the scaper fcuntion
    id_list = mysql_etl_functions.get_imdb_id()
    imdb_season_1_scraper(id_list)

#imdb_paginate()
