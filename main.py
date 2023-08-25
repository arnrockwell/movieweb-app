from datamanager.json_data_manager import JSONDataManager

data = JSONDataManager("sample.json")
users = data.get_all_users()
print(users)

movies = data.get_user_movies(1)
print(movies)
