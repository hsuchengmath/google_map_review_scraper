
import pymongo
import requests


class Scrape_By_Google_API:

    def __init__(self):
        place_query = '王品牛排'
        self.google_api_key = 'AIzaSyDtFvIlhh91x1nulxifTD1Gk3UBz3_Fg4A'
        self.search_place_id_url = 'https://maps.googleapis.com/maps/api/place/textsearch/json?input={}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={}'.format(place_query,self.google_api_key)        
        # database part
        self.batch_size = 16
        self.myclient = pymongo.MongoClient("mongodb://localhost:27017/")['Google_Map_Review_Database']
        self.Collection_place_ID_with_pace_name = self.myclient["place_ID_with_pace_name"]


    def search_review_url_func(self,place_id):
        return 'https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=name,rating,formatted_phone_number,reviews&key={}'.format(place_id,self.google_api_key)


    def scrape_in_search_place(self):
        resp = requests.get(url=self.search_place_id_url)
        data = resp.json()['results']
        self.place_id2place_name = dict()
        self.place_id2place_name_for_DB = list()
        for i, element in enumerate(data):
            place_name = element['name']
            place_id = element['place_id']
            self.place_id2place_name[place_id] = place_name
            element_DB = {'place_id':place_id, 'place_name':place_name}
            self.place_id2place_name_for_DB.append(element_DB)
            if i % self.batch_size == 0:
                self.Collection_place_ID_with_pace_name.insert_many(self.place_id2place_name_for_DB)
                self.place_id2place_name_for_DB = []
        if len(self.place_id2place_name_for_DB) != 0:
            self.Collection_place_ID_with_pace_name.insert_many(self.place_id2place_name_for_DB)
    

    def scrape_in_search_review(self):
        element_DB = list()
        place_id_list = list(self.place_id2place_name.keys())
        for i, place_id in enumerate(place_id_list):
            url = self.search_review_url_func(place_id)
            resp = requests.get(url=url)
            data = resp.json()['result']
            place_name = self.place_id2place_name[place_id]
            avg_rating = data['rating']
            review_list = data['reviews']
            # build a new collection
            collection_review = self.store_data_to_db_init(collection_name=place_name)
            collection_data = list()
            for i, element in enumerate(review_list):
                author_name = element['author_name']
                rating = element['rating']
                text = element['text']
                time = element['time']
                element_DB = {
                             'author_name' : author_name,
                             'text' : text,
                             'rating' : rating,
                             'time' : time
                             }
                collection_data.append(element_DB)
            collection_review.insert_many(collection_data)


    def store_data_to_db_init(self, collection_name):
        return self.myclient[collection_name]


    def forward(self):
        self.scrape_in_search_place()
        self.scrape_in_search_review()

        

if __name__ == '__main__':
    SBGA_obj = Scrape_By_Google_API()
    SBGA_obj.forward()
