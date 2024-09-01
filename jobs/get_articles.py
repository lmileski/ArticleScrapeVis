from libs import headlines, dandelion, db
import pandas as pd 


def main():
    # get headlines 
    article_records = headlines.get_headlines() 

    # insert articles, get back a df of url + primary key
    # for articles that haven't been inserted.
    # append primary key to dataframe

    if len(article_records) == 0:
        print("No new articles found.")
        return 

    try:

        article_ids = db.add_articles(article_records)
        df = pd.DataFrame.from_records(article_ids)
        df = df.merge(
            pd.DataFrame.from_records(article_records),
            on="url",
            how="inner"
        )

        # extract entities for each article 
        df['entity'] = df['title'].apply(lambda title: dandelion.extract_entities(title))
        article_entities = df.explode('entity')[['id', 'entity']].rename(columns={'id': 'article_id'}).to_dict(orient='records')

        # upsert entities for each article
        db.add_entities(article_entities)
        db.con.commit()

    except Exception as e:
        db.con.rollback()
        raise e 
    
    finally:

        db.con.close()
    
