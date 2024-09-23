# Article Scrape Visualization Tool
_a project by Luke Mileski & Filipp Kay_

## Overview 
This tool uses a daily CRON job to get the latest trending news articles using the NewsAPI library, extracts relevant keywords from them using the Dandelion API, stores them in a PostgresDB hosted via Heroku, and visualizes emergent keywords using a Streamlit application.

## Flow 
![image](https://github.com/user-attachments/assets/0a5079c2-1efb-4e3c-947a-5a1a7330b69a)

1. A timed CRON job runs every 24 hours which uses the `top-headlines` endpoint fron NewsAPI to grab the latest headlines for the US.
2. The articles are checked against the PostgreSQL database.
  a. If the article already exists and runs into a uniqueness constraint, the article title is updated to acocunt for edge cases.
  b. Articles are upserted using a SQL insert operation. The query returns a list of IDs corresponding to each article object.
3. Each article headline is used by the dandelion API to generate a list of entities that are also upserted to Postgres with a foreign key association to their respective article.
4. Old articles are deleted during this process.
5. A Streamlit App hosted in Heroku grabs data from a SQL view and renders several charts that highlight prominent entities, their underlying articles, as well as article metadata and URLs.


## Deployment 
### Heroku 
1. Clone this codebase into a new repository with a name of your own choosing.
2. Make a Heroku Account and create a new App with the following configuration:<br>
   Buildpack: `Python 3.11`
   
   Deployment Method: `Github`

   _Log into your github account, select the repo you made in step 1, and choose the default / main branch._
    
5. In `Overview`, configure two add-ons: A Heroku PostgreSQL Database and a CRON To Go instance - choose the cheapest pricing tier for both.
6. Make a <a href="https://newsapi.org/">News API</a> account and get an API Key.
7. Make a <a href="https://dandelion.eu/">Dandelion API</a> account and generate another API Key.
8. In Heroku, navigate to `Settings :: Reveal Config Vars` and validate that you have a `DATABASE_URL` key. You should also see a `CRONTOGO_OGANIZATION_ID`.
9. Generate the following new variables:<br>
```
VERIFY_REQUESTS : 0
ALCHEMY_DATABASE_URL : Copy-paste the value of your DATABASE_URL key but replace the `postgres` prefix with `postgresql+psycopg2`
Your Alchemy URL should look like this: postgresql+psycopg2://jasdasjdhasd:wejqwejasd.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/aaaaaa
NEWS_API_KEY: Your NewsAPI Token
DANDELION_API_KEY: Your Dandelion API Token
```
10. Navigate back to `Deploy` and manually deploy your app from the main branch.
11. Navigate to `Overview :: Installed Add Ons :: CRON To Go Scheduler :: Add Job (+)` and configure the following job:<br>
```python
NickName = Refresh DB (Articles Last 24 Hours)
Schedule = 0 9 * * *
No Jitter
Command: python jobs/get_articles.py
Dyno Size: Eco
```
You can select the elipsis icon for your new job and click `Run Job Now` to validate that you configured your environment properly.
12. From any tab, click `Open App` to verify that your Streamlit front-end is running properly.

## Local Testing 
In order to test out functionality locally, we recommend using a `scratch.py` file for unit testing. This file name will get ignored by the repo, and can reference locally configured env values by accessing 
a `local_config.py` file, which we recommend placing alongside with your scratch file at the root of this direcoty.

```python
# local_config.py
import os
os.environ['ALCHEMY_DATABASE_URL'] = ...
os.environ['VEIRFY_REQUESTS'] = '0'
os.environ['DANDELION_API_KEY'] = ...
os.environ['DATABASE_URL'] = ...
os.environ['NEWS_API_KEY'] = ...
```

at minimum, a well established `local_config.py` file should contain the aforementioned keys, which should be populated with the same values you provided when standing up your Heroku app.
You can utilize it in your `scratch.py` file to run individual units of code:

```python
#scratch.py
try:
  import local_config
except ImportError:
  pass

from libs import headlines
x = headlines.get_headlines()
```

Note that any library will not run locally as it will look for environment variables that can only be configured by first import a local config file.

## News API
The article headline data is collected using the <a href="https://newsapi.org/">News API</a>. Only news headlines in America within the last 24 hours are pulled. To use the API, you can select the developer plan for a free key that grants 100 requests per day.

Integration of the News API is found in the get_headlines() function within `headlines.py`, which does the following:
1. Fetches the API key that was set earlier within local_config.py.
2. Sets the root API URL and specific endpoint for US top-headlines.
3. Makes a GET request to the API and stores the resultant headline data in .json dictionary format.
4. Parses through each headline, adding author, title, date, and URL info to a list of headline dictionaries, which is returned.

## Dandelion API
The top article entity data is collected using the <a href="https://dandelion.eu/">Dandelion API</a>. To use the API, you can select the basic plan for a free key that grands 1000 requests per day.

Integration of the Dandelion API is found in the extract_entities() function within `dandelion.py`, which does the following:
1. Fetches the API key that was set earlier within local_config.py.
2. Sets the root API URL and parameters (key, language, text, min_entity_confidence).
3. Makes a GET requests to the API and stores each resultant entity in a list, which is returned.

## CRON Job Function
The article headline data is updated everyday using a Cron To Go job, which calls main() within `jobs/get_articles.py`. The database and streamlit app are updates as follows:
1. Current headline data from the last 24 hours is collected via NewsAPI.
2. All previous article and entity data is cleared from the database tables.
3. Most current headline data is inserted into the db tables.
4. Headline data is then used to extract most relevant entities, which are then added to the db.
5. Streamlit's auto-reload feature detects the change and refreshes with new db updates.