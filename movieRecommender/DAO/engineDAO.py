import  movieRecommender.DAO as DB

#function to retrieve movies belonging to list of indexes
def getMoviesFromIndex(movieIDs) :
    db = DB.getDBConnection()
    quer = ''
    if len(movieIDs) == 1 :
        quer = 'select * from idmovietable where index = %s' % movieIDs[0]
    else :
        movieIDs = tuple(movieIDs)
        quer = 'select * from idmovietable where index in %s' %str(movieIDs)
    result = db.query(quer)
    return result.dictresult()

#function to retrieve movies belonging to list of IDS
def getMoviesFromIDs(movieIDs) :
    db = DB.getDBConnection()
    quer = ''
    if len(movieIDs) == 1 :
        quer = 'select * from idmovietable where id = %s' % movieIDs[0]
    else :
        movieIDs = tuple(movieIDs)
        quer = 'select * from idmovietable where id in %s' %str(movieIDs)
    result = db.query(quer)
    return result.dictresult()

#get movies from search text
def getSearchResults(searchText,batchno):
    db = DB.getDBConnection()
    searchText = "'%%%s%%'" %searchText.lower()
    querstr = "select * from idmovietable where lower(name) like %s" % searchText
    result  = db.query(querstr)

    final_data = result.dictresult()

    #if no search result found
    if len(final_data) == 0 :
        return False,final_data,0

    batches =  len(final_data) / 10  if  (len(final_data)%10 == 0)  else  len(final_data) / 10 + 1
    batchno = int(batchno)
    if batches >= int(batchno):
        return True, final_data[(batchno - 1) * 10:batchno * 10], batches  # return status, that batch of search result and number of batches