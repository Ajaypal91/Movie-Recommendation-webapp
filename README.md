# Movie-Recommendation-webapp

<h1>What it is?</h1>

The movie recommendation app uses the concept of content based filtering, neural network as learning algorithm, semantic knowledge base and semantic search for making movie recommendation.

<h1>Technologies used</h1>

1 Python 2.7
2 Flask 
3 PostgreSql 
4 jQuery
5 HTML5
6 CSS3
7 JavaScript
Different Packages Needed: Python's sklearn, scikit, flask, pandas, numpy
Postgresql Database is uploaded on a cloud

<h1>How it works / Technical Details</h1>

Below is the architecure of the whole project's backend. 

![Alt text](/ScreenShots/architecture.png?raw=true "Architecture")

I am not going in great depth for the working of the project. If you are interested in understanding more, please drop me an email provided at the end.
Based on the user history of its likes and dislikes the content based filtering filters out the whole movie corpus and selects only a subset of the data, which is pre-processed and features are created out of it.
The various features taken into consideration are:

![Alt text](/ScreenShots/features.png?raw=true "Features")

The content based filtering is done by using IDF and based on creation of user_profile from the user history

![Alt text](/ScreenShots/cbf.png?raw=true "CBF")

After the data is processed the following Neural network is used to train it.

![Alt text](/ScreenShots/NN.png?raw=true "NN")

Once a NN is trained the recommendations are given in the following manner.
First a semantic graphs are created based on the user_history and filtered dataset.

![Alt text](/ScreenShots/sg.png?raw=true "Semantic Graph Structure")

Then this graph is given as input to the machine learning model which gives the recommendations based on highest probabilities.

<h1>HOW TO USE</h1>

<h2>Working with Database Schema</h2>
Following 3 tables are needed to run this application with following schema

<h3>idmovietable</h3>

```sql
CREATE TABLE public.idmovietable
(
  index bigint,
  id bigint,
  name text
)
WITH (
  OIDS=FALSE
);

```

<h3>user_data</h3>

```sql
CREATE TABLE public.user_data
(
  id integer NOT NULL,
  history character varying,
  historyupdated integer,
  userprofile character varying,
  CONSTRAINT user_history_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
```

<h3>users</h3>

```sql
CREATE TABLE public.users
(
  username character varying,
  password character varying,
  isactive integer,
  id integer NOT NULL DEFAULT nextval('users_userid_seq'::regclass)
)
WITH (
  OIDS=FALSE
);
```

<b>Note:</b> if the online database is not working for some reason. Please create a local schema and just comment out the code in <b>__init__.py file in DAO folder</b> and add relevant local db connection credentials</b> for example. 

```python
return DB(dbname='mydb', host='localhost', port=5432, user='ajay', passwd='1111')
```

Also you have to seed the <i>idmovietable</i> with the data from the <b>MoviesLength.csv</b> file present in Data folder.

Just run the run.py file. It will host a webserver and the login page can be accessed at <a>http://localhost:5000/login</a> where 5000 is default port for flask web server.

<h1>USER INTERFACE</h1> 

<h3>Login Page</h3>

![Alt text](/ScreenShots/loginPage.png?raw=true "Login Page")

<h3>Home Page</h3>

![Alt text](/ScreenShots/userHomePage.png?raw=true "Home Page")

<h3>History Page</h3>

![Alt text](/ScreenShots/userHistoryPage.png?raw=true "User History Page")

<h3>Build User History Page</h3>

![Alt text](/ScreenShots/UserHistoryBuildPage.png?raw=true "Build User History Page")

<h1>TESTING</h1>
As of now only functional testing and different test cases were implemented while building this project. 

Please feel free to contact me at erajaypal91@gmail.com.
