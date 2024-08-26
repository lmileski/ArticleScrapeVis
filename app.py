import streamlit as st
import plotly.express as px
import pandas as pd
import jobs.df_queries as q

st.header("Top Headlines")
st.caption("A program by Luke Mileski and Philip Kay")

histogram_data = q.find_histogram_info()
authors_joined: list[str] = [", ".join(author) for author in histogram_data['Authors']]

df = pd.DataFrame({
    'Entities': histogram_data['Entities'],
    'Frequency': histogram_data['Count'],
    'Authors': authors_joined
})

# creating a histogram
fig = px.bar(df, x='Entities', y='Frequency', hover_data=['Authors'], title='Top Entities')
# customizing the labels
fig.update_layout(
    title=dict(text='Top Entities', x=0.55, y=0.9, xanchor='center', font=dict(size=26)),
    xaxis_title=dict(text='Entities', font=dict(size=18)),
    yaxis_title=dict(text='Frequency', font=dict(size=18))
)
# displaying the histogram in st
st.plotly_chart(fig)

# creating a table of all article info