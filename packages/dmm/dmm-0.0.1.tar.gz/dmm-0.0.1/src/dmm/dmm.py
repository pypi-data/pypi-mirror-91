import requests


class DMM():

    END_POINT = 'https://api.dmm.com/affiliate/v3/'

    def __init__(self, api_id, affiliate_id):
        self.__api_id = api_id
        self.__affiliate_id = affiliate_id

    @property
    def api_id(self):
        return self.__api_id

    @property
    def affiliate_id(self):
        return self.__affiliate_id

    def __create_url_params(self, params):
        url_params = ''
        for key, value in params.items():
            url_params += '&' + key + '=' + value
        return url_params

    def __get(self, content_type, params):
        url = f'{DMM.END_POINT}/' + content_type \
              + f'?api_id={self.__api_id}&affiliate_id={self.__affiliate_id}' \
              + self.__create_url_params(params)
        return requests.get(url)

    def get_items(self, params):
        return self.__get('ItemList', params)

    def get_item_by_id_dmm(self, cid):
        return self.get_items({'site': 'DMM.com', 'cid': cid})

    def get_item_by_id_fanza(self, cid):
        return self.get_items({'site': 'FANZA', 'cid': cid})

    def get_floors(self, params):
        return self.__get('FloorList', params)

    def get_floors_dmm(self):
        res = self.get_floors({})
        floors = res.json()
        return floors['result']['site'][0]

    def get_floors_fanza(self):
        res = self.get_floors({})
        floors = res.json()
        return floors['result']['site'][1]

    def get_actresses(self, params):
        return self.__get('ActressSearch', params)

    def get_actress_by_id(self, actress_id):
        return self.get_actresses({'actress_id': actress_id})

    def get_genres(self, params):
        return self.__get('GenreSearch', params)

    def get_makers(self, params):
        return self.__get('MakerSearch', params)

    def get_series(self, params):
        return self.__get('SeriesSearch', params)

    def get_authors(self, params):
        return self.__get('AuthorSearch', params)
