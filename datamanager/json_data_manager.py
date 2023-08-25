import json
from .data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):

    def __init__(self, filename):
        self.filename = filename


    def get_all_users(self):
        # Returns a dictionary containing all the users
        with open(self.filename, "r") as open_file:
            data = json.load(open_file)

        users = { key: value["name"] for (key, value) in data.items() }
        return users


    def get_user_movies(self, user_id):
        # Return a dictionary of all the movies for a given user
        with open(self.filename, "r") as open_file:
            data = json.load(open_file)
        
        user = data.get(str(user_id))
        movies = user["movies"]
        return movies


    def add_user(self, username):
        with open(self.filename, "r") as open_file:
            data = json.load(open_file)
        
        last_id = max(data.keys())
        new_id = int(last_id) + 1
        user_id = str(new_id)
        data[user_id] = { "name": username, "movies": {} }

        with open(self.filename, "w") as update_file:
            json.dump(data, update_file, indent=4)


    def add_movie_data(self, user_id, title, director, year, rating):
        with open(self.filename, "r") as open_file:
            data = json.load(open_file)

        user = data.get(user_id)
        movies = user["movies"]
        if not movies:
            movie_id = str(1)
        else:
            last_id = max(movies)
            new_id = int(last_id) + 1
            movie_id = str(new_id)

        data[user_id]["movies"][movie_id] = {"title": title,
                    "director": director, "year": year, "rating": rating}
        
        with open(self.filename, "w") as update_file:
            json.dump(data, update_file, indent=4)


    def update_movie_data(self, user_id, movie_id, title, director, year, rating):
        with open(self.filename, "r") as open_file:
            data = json.load(open_file)

        user = data.get(user_id)
        movies = user["movies"]
        try:
            data[user_id]["movies"][movie_id] = {"title": title,
                    "director": director, "year": year, "rating": rating}
        except KeyError as e:
            print("Movie doesn't exist. Please try again.", str(e))

        with open(self.filename, "w") as update_file:
            json.dump(data, update_file, indent=4)


    def delete_movie_data(self, user_id, movie_id):
        with open(self.filename, "r") as open_file:
            data = json.load(open_file)

        try:
            del data[user_id]["movies"][movie_id]
        except KeyError as e:
            print("Movie doesn't exist. Please try again.", str(e))

        with open(self.filename, "w") as update_file:
            json.dump(data, update_file, indent=4)
