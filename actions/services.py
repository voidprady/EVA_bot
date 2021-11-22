from numpy.core.numeric import indices
import pandas as pd
import numpy as np
from rapidfuzz import utils, process

# load data
imdb_movies = pd.read_csv(r"~\Documents\EVA_bot\db\IMDB_movies.csv", low_memory=False)
imdb_people = pd.read_csv(r"~\Documents\EVA_bot\db\IMDB_names.csv", low_memory=False)
imdb_ratings = pd.read_csv(r"~\Documents\EVA_bot\db\IMDB_ratings.csv", low_memory=False)
imdb_roles = pd.read_csv(r"~\Documents\EVA_bot\db\IMDB_title_principals.csv", low_memory=False)
rt_reviews = pd.read_csv(r"~\Documents\EVA_bot\db\rotten_tomatoes_critic_reviews.csv", low_memory=False)
rt_tomatoes_movies = pd.read_csv(r"~\Documents\EVA_bot\db\rotten_tomatoes_movies.csv", low_memory=False)

imdb_indices = list(imdb_movies['imdb_title_id'])

#find movies by genre
def rec_movie_by_genre(x, prev_rec):
    movies_list = []
    imdb_movies.sort_values(by='year', ascending=False, inplace=True)
    recommend = prev_rec
    for i in range(len(imdb_movies)):
        if all(word in imdb_movies.genre[i].lower() and len(x) == len(imdb_movies.genre[i].split(', ')) for word in x):
            movies_list.append([imdb_movies.original_title[i], imdb_movies.avg_vote[i], imdb_movies.votes[i], imdb_movies.year[i], imdb_movies.director[i]])
            movies_list.sort(key=lambda y: (y[2], y[1]), reverse=True)
            if(len(movies_list) > 100):
                break
    if(len(movies_list) == 0):
        return []
    else:
        movies_list = np.array(movies_list)
        if(prev_rec is None):
            movies_list = movies_list[np.random.randint(len(movies_list)-1, size=1)][0]
            recommend = str(movies_list[0])
        else:
            while(recommend.lower() == prev_rec.lower()):
                movies_list = movies_list[np.random.randint(len(movies_list)-1, size=1)][0]
                recommend = str(movies_list[0])
        return recommend

# find similar person
def is_this_your_person(person):
    person1 = person
    persons_choices = imdb_people.name.to_list()
    title_orgs = [utils.default_process(org) for org in persons_choices]
    scores = process.extract(person1, title_orgs, score_cutoff=95)
    return scores


# show me films with actor
def get_movies_by_actor(x):
    name_id = ''
    for i in range(len(imdb_people)):
        if imdb_people.name[i].lower() == x.lower():
            name_id = imdb_people.imdb_name_id[i]
            break
    title_id = []
    for a in range(len(imdb_roles)):
        if ((imdb_roles.imdb_name_id[a] in name_id) & ((imdb_roles.category[a].lower() == 'actress') | (imdb_roles.category[a].lower() == 'actor'))):
            title_id.append(imdb_roles.imdb_title_id[a])
            if(len(title_id) > 3):
                break
    list_of_films = imdb_movies[imdb_movies['imdb_title_id'].isin(title_id)]
    movies_str =  ', '.join(str(i) for i in list_of_films.original_title)
    return movies_str

# show me films by director
def find_movies_by_director(x):
    name_id = []
    for i in range(len(imdb_people)):
        if imdb_people.name[i].lower() == x.lower():
            name_id.append(imdb_people.imdb_name_id[i])
            break
    title_id = []
    for d in range(len(imdb_roles)):
        if (imdb_roles.imdb_name_id[d] in name_id) & (imdb_roles.category[d].lower() == 'director'):
            title_id.append(imdb_roles.imdb_title_id[d])
            if(len(title_id) > 3):
                break
    list_of_films = imdb_movies[imdb_movies['imdb_title_id'].isin(title_id)]
    return ', '.join(str(i) for i in list_of_films.original_title)

#no. of titles
def get_number_of_titles(title):
    print("title", title)
    num_titles = len(imdb_movies[imdb_movies.original_title.str.lower() == title.lower()])
    return num_titles

# find similar title
def is_this_your_movie(title):
    title_query = title
    title_choices = imdb_movies.original_title.to_list()
    title_orgs = [utils.default_process(org) for org in title_choices]
    scores = process.extract(title_query, title_orgs, score_cutoff=95)
    print("scores similar title", scores)
    return scores

# find the movie with all the data
def get_movie_data(title):
    movie = imdb_movies[imdb_movies.original_title.str.lower() == title.lower()]
    print("movie", movie)
    returnStr = []
    if(not movie.empty):
        for index, row in movie.iterrows():
            director = row['director']
            cast = row['actors']
            language = row['language']
            genre = row['genre']
            released = row['year']
            imdb_rate = row['avg_vote']
            returnStr.append("Director: {}\n"\
                "Cast: {} \n"\
                "Language: {} \n" \
                "Genre: {} \n"\
                "Released: {} \n"\
                "IMDb Rating: {} \n".format(director, cast, language, genre, released, imdb_rate))
    return returnStr

#find all the movies with matching title
def get_movies(title):
    films = []
    movie = (imdb_movies[imdb_movies.original_title.str.lower() == title.lower()])
    for i in range(len(movie)):
        film = movie.iloc[i]['title', 'director', 'year']
        films.append(film)
    return ', '.join(str(i) for i in films)