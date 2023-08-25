from abc import ABC, abstractmethod


class DataManagerInterface(ABC):

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_movies(self, user_id):
        pass

    @abstractmethod
    def add_user(self, username):
        pass

    @abstractmethod
    def add_movie_data(self, user_id, title):
        pass

    @abstractmethod
    def update_movie_data(self, user_id, movie_id, title, rating):
        pass

    @abstractmethod
    def delete_movie_data(self, user_id, movie_id):
        pass
