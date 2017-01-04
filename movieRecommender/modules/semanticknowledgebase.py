from semnet import *
from tostr import tostr
import Users as US
import HelperFunctions as hp
import pandas as pd

df = pd.read_csv("Data/finalData.csv")

has = Relation("has", 0)
whatHas = Relation("whatHas", 0, has)

belongsTo = Relation("belongsTo", 0)
whatBelongsTo = Relation("whatBelongsTo", 0, belongsTo)

def get_rating_for_movie(movie_id):
    return df.loc[df['ID'] == movie_id, 'UR'].iloc[0]
    
def get_genres_for_movie(movie_id):
    genres = df.loc[df['ID'] == movie_id, 'GENRE'].iloc[0]
    return [g.strip() for g in genres.split('|')]

def create_entities(df):
    movies = []
    for movie_id in df['ID']:
        movies.append(Entity(str(movie_id)))

    genres = []
    for genre in hp.RawDataProcessing.getGenersList():
        genres.append(Entity(genre))
    
    ratings = []
    for rating in range(21):
        ratings.append(Entity('rating'+str(rating)))
        
    return movies, genres, ratings
    
def get_genre_entity(genre, genre_entities):
    for g in genre_entities:
        if tostr(g) == genre:
            return g
            
#def get_rating_entity(rating):
#    for r in ratings:
#        if tostr(r) == rating:
#            return r

def get_movie_entity(movie_id, movie_entities):
    for m in movie_entities:
        if tostr(m) == movie_id:
            return m          
                
def create_network(movies, genres, ratings):
    facts = []
    for movie_id in movies:
        movie_genres = get_genres_for_movie(int(tostr(movie_id)))
        m = get_movie_entity(tostr(movie_id), movies)
        for g in movie_genres:
            genre_entity = get_genre_entity(tostr(g), genres)
            if genre_entity != None:
                facts.append(Fact(m, belongsTo, genre_entity))
        #movie_rating = get_rating_for_movie(int(tostr(movie_id)))    
        #facts.append(Fact(m, has, get_rating_entity(tostr(movie_rating))))
    return facts
    
def get_similar_movies(object):
    movies, genres, ratings = create_entities(df)
    create_network(movies, genres, ratings)    
    liked_movies = [x[0].tolist() for x in object.usr.getUsrHist() if x.tolist()[1] == 1]
    #print liked_movies
    for lm in liked_movies:
        lm_entity = get_movie_entity(str(lm), movies)
        if lm_entity != None:
            liked_genres = lm_entity.getObjects(belongsTo)
            #print tostr(liked_genres)
            for lg in liked_genres:
                lg_entity = get_genre_entity(tostr(lg), genres)
                similar_movies = [tostr(sm) for sm in lg_entity.getObjects(whatBelongsTo)]
    return similar_movies