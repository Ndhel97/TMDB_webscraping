import requests
import json
import time
API_KEY = '76ed20e4a784a806bc61c159c303a891'

data_res = {}
# Opening JSON file -- 
f = open('tmdb_movies_id copy.json',)
  
# returns JSON object as 
# a dictionary
data = json.load(f)
# print(data)
  
# Iterating through the json
# list
for i in data:
    data[i] = data[i].split('/')[2]
    response = requests.get('https://api.themoviedb.org/3/movie/' + data[i] + '?api_key=' + API_KEY + '&language=en-US')
    data_res[data[i]] = response.json()
    print(i, response)
    time.sleep(0.05)
  
# Closing file
f.close()

# the json file where the output must be stored 
out_file = open("tmdb_data_api.json", "w") 
    
json.dump(data_res, out_file, indent = 4) 
    
out_file.close() 
