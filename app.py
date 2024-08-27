import streamlit as st
from tzlocal import get_localzone
import plotly.express as px
import pandas as pd
import jobs.df_queries as q
from libs.format_time import format_time

st.set_page_config(page_title="Top Headlines App")
st.header("Top Headlines Last 24 Hours")
st.caption("A Project by Luke Mileski and Philip Kay")

# adding custom css for tables
table_style = """
<style>
    .wide-table {
        width: 150%;
        margin-left: -165px;
    }
    .justified-table th:nth-child(2) {
        text-align: center;
        transform: translateX(-25px);
    }
</style>
"""
# alerting st that we're using this style
st.markdown(table_style, unsafe_allow_html=True)

headline_data = q.find_top_headline_info()

# organizing data needed for top headlines histogram and table
frequencies, authors, headline_url_and_date = [], [], []
local_tz = get_localzone()

for entity, articles in headline_data.items():
    frequencies.append(len(articles))
    authors.append([])
    headline_url_and_date.append([])
    for article in articles:
        # formats the date to Yesterday/Today, hour:minute AM/PM
        full_date = format_time(article[2], local_tz)

        authors[-1].append(article[-1]) # type: ignore
        # storing headline/url/date as one element (link w/ title - date)
        link = f'<a href="{article[1]}" target="_blank">{article[0]}</a>'
        headline_url_and_date[-1].append(f"{full_date} - {link}<br><br>") # type: ignore

    headline_url_and_date[-1] = "".join(headline_url_and_date[-1])
    authors[-1] = ", ".join(authors[-1])

df = pd.DataFrame({
    'Entities': headline_data.keys(),
    'Frequency': frequencies,
    'Authors': authors
})

# creating the histogram w/ pd.df
fig = px.bar(df, x='Entities', y='Frequency', hover_data=['Authors'], title='Top Entities')
# customizing the labels
fig.update_layout(
    title=dict(text='Top Entities', x=0.54, y=0.9, xanchor='center', font=dict(size=26)),
    xaxis_title=dict(text='Entities', font=dict(size=18)),
    yaxis_title=dict(text='Frequency', font=dict(size=18))
)
# displaying the histogram in st
st.plotly_chart(fig)
# adding space between charts and title
st.markdown("<br>", unsafe_allow_html=True)

# creating a table of all article info
table = pd.DataFrame({
    'Entities': headline_data.keys(),
    'Top Articles': headline_url_and_date
})

# converting article links to html
table = table.to_html(escape=False, index=False, justify='center', classes=['wide-table', 'justified-table'])
# showing table
st.markdown(table, unsafe_allow_html=True)

# creating table with all trending articles and their entities
st.markdown("<br><h2 style='text-align: center; transform: translateX(25px);'>All Trending Articles</h2>", unsafe_allow_html=True)

# grabbing all articles data
articles_list = q.find_all_article_info()
# converting title and url fields into one - for hyperlinks
for i, article in enumerate(articles_list):
    title = article[2]
    url = article[4]
    link = f'<a href="{url}" target="_blank">{title}</a>'
    # rewriting the tuple element w/ only 3 elements - formatted for table use
    articles_list[i] = (link, article[1], format_time(article[3], local_tz), article[5])

all_articles_table = pd.DataFrame(articles_list, columns=['Article', 'Author', 'Date', 'Entities'])

# converting article links to html
all_articles_table = all_articles_table.to_html(escape=False, index=False, justify='center', classes='wide-table')
# showing second table
st.markdown(all_articles_table, unsafe_allow_html=True)