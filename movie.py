import tmdbsimple as tmdb

class MovieClient(object):

    def __init__(self,query):
        tmdb.API_KEY = 'da3ad96ab719fd39aacef9cdf21754fd'
        self.query = query

    def set_query(self, query=''):
        self.query = query

    def get_info(self, detail='id'):
        search = tmdb.Search()
        search.movie(query=self.query)
        for s in search.results:
            return s[detail]

    def get_overview(self):
        return self.get_info('overview')

    def get_image(self):
        BASE_URL = 'http://image.tmdb.org/t/p/'
        SIZE = 'w500'
        path = self.get_info('poster_path')
        url = BASE_URL + SIZE + path
        return url

    def get_movie(self):
        movie_details = []
        movie_details.append(self.get_image())
        movie_details.append(self.get_overview())
        return movie_details