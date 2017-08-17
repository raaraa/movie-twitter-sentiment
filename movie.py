import tmdbsimple as tmdb
from datetime import datetime

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
        SIZE = 'w342'
        path = self.get_info('poster_path')
        url = BASE_URL + SIZE + path
        return url

    def get_title(self):
        return self.get_info('original_title')

    def get_release_date(self):
        #formatting date
        old_format = self.get_info('release_date')
        datetimeobject = datetime.strptime(old_format, '%Y-%m-%d')
        new_format = datetimeobject.strftime('%m-%d-%Y')
        return new_format

    def get_rating(self):
        return self.get_info('vote_average')

    def get_movie(self):
        '''
            title = 0, image = 1, overview = 2
            release = 3, rating = 4
        '''
        movie_details = []
        movie_details.append(self.get_title())
        movie_details.append(self.get_image())
        movie_details.append(self.get_overview())
        movie_details.append(self.get_release_date())
        movie_details.append(self.get_rating())
        return movie_details