import streamlit as st
import pickle
import requests
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

movies_list=pickle.load(open('movies.pkl', 'rb'))
st.set_page_config(layout="wide")
tmdb_api_key = st.secrets["api"]["tmdb_key"]
cv=CountVectorizer(max_features=5000,stop_words='english')
vectors=cv.fit_transform(movies_list['tags']).toarray()
similarity=cosine_similarity(vectors)

def fetch_poster(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={movie_name}"
    data = requests.get(url).json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    recommend_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    lis=[]
    recommend_movies_posters=[]
    for i in recommend_movies:
        temp=movies_list.iloc[i[0]]['title']
        recommend_movies_posters.append(fetch_poster(temp))
        lis.append(temp)
    return lis, recommend_movies_posters

movies_lst=movies_list['title'].values
st.title("🎬 Movie Recommender System")
selected_movie_name = st.selectbox(
    'Choose your favorite Movie:',
    movies_lst
)
if st.button('Recommend Movie'):
    names, posters = recommend(selected_movie_name)

    st.subheader("🎬 Top 5 Movie Recommendations")

    cols = st.columns(5)

    for idx, col in enumerate(cols):
        with col:
            st.image(posters[idx], width=250)  # 👈 Set width (increase from default)
            st.markdown(
                f"<p style='text-align:center; font-size:20px; font-weight:bold'>{names[idx]}</p>",
                unsafe_allow_html=True
            )