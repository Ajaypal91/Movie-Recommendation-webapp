import  movieRecommender.DAO as DB

#function to retrieve movies belonging to list of IDS
def getMoviesFromIDs(movieIDs) :
    db = DB.getDBConnection()
    movieIDs = tuple(movieIDs)
    quer = 'select * from idmovietable where index in %s' %str(movieIDs)
    result = db.query(quer)
    return result.dictresult()
