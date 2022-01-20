from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import requests
import joblib
model = joblib.load('recommendation_engine.pkl')
final_movie = pd.read_pickle('final_movie.pkl')
final_movie_dataset = pd.read_pickle('final_movie_dataset.pkl')
# print(model)
# image1 = {}
# hello
# print(joblib.__version__)

def index(request):
    return render(request, 'index.html')

def recommend(request):
    # return HttpResponse("Hello world")
    if request.method == 'POST':
        movie = request.POST.get('movies')
        ind = final_movie_dataset[final_movie_dataset['title'] == movie].index[0]
        # print(ind)
        res = []
        images = []
        distance, indices = model.kneighbors(final_movie.iloc[ind, :].values.reshape(1, -1), n_neighbors=6)
        cnt = 1
        for arr in indices:
            for ind in arr:
                if cnt == 1:
                    cnt += 1
                    continue
                res.append(final_movie.index[ind])
                cnt += 1

        cnt = 1
        for arr in indices:
            for ind in arr:
                if cnt == 1:
                    cnt += 1
                    continue
                id = final_movie_dataset.iloc[ind]['movie_id']
                print(id)
                data1 = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key=d58ee4111a9d38dce1c1be9f4803a7f0&language=en-US')
                data2 = data1.json()
                #print(data2)
                #break
                url1 = "https://image.tmdb.org/t/p/w500" + str(data2['poster_path'])
                print(url1)
                images.append(url1)
                cnt += 1
        result = zip(res, images)
        context = {'result':result}
        return render(request, 'index.html', context=context)