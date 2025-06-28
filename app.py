# import pickle
# import streamlit as st
# import requests

# def fetch_poster(movie_id):
#     url="https://api.themoviedb.org/3/movie/{}?api_key=aa069f1b664ca9098eaff1ad93535e5e&language=en-US".format(movie_id)
#     data=requests.get(url)
#     data=data.json()
#     poster_path=data['poster_path']
#     full_path="http://image.tmdb.org/t/p/w500/" + poster_path
#     return full_path

# def recommend(movie):
#     index=movies[movies['title'] == movie].index[0]
#     distances=sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
#     recommendedmoviesname=[]
#     recommendedmoviesposter=[]
#     for i in distances[1:6]:
#         movie_id=movies.iloc[i[0]].movie_id
#         recommendedmoviesname.append(movies.iloc[i[0]].title)
#         recommendedmoviesposter.append(fetch_poster(movie_id))
#     return recommendedmoviesname, recommendedmoviesposter
        

# st.header("Movie Recommendation System")
# movies=pickle.load(open('artifacts/movie_list.pkl', 'rb'))
# similarity=pickle.load(open('artifacts/similarity.pkl', 'rb'))

# movie_list=movies['title'].values
# selectedmovie=st.selectbox(
#     'type or select a movie to get recommendations',
#     movie_list
# )

# if st.button('Show Recommendation'):
#     recommendedmoviesname, recommendedmoviesposter = recommend(selectedmovie)
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         st.text(recommendedmoviesname[0])
#         st.image(recommendedmoviesposter[0])

#     with col2:
#         st.text(recommendedmoviesname[1])
#         st.image(recommendedmoviesposter[1])    

#     with col3:
#         st.text(recommendedmoviesname[2])
#         st.image(recommendedmoviesposter[2])

#     with col4:
#         st.text(recommendedmoviesname[3])
#         st.image(recommendedmoviesposter[3])

#     with col5:
#         st.text(recommendedmoviesname[4])
#         st.image(recommendedmoviesposter[4])
import pickle
import streamlit as st
import requests

st.markdown("""
    <style>
        /* 🔵 App background & text */
        .stApp {
            background-color: #87CEEB;
            color: black;
        }

        /* 📝 General text */
        h1, h2, h3, h4, h5, h6, p, label, span, div {
            color: black !important;
        }

        /* 🔘 Button */
        .stButton > button {
            background-color: white;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
        }
        .stButton > button:hover {
            background-color: #87CEEB ;
        }

        /* ⬇️ Selectbox */
        .stSelectbox > div[data-baseweb="select"] {
            background-color: white !important;
            color: black !important;
            border-radius: 5px;
        }

        /* 🔽 Dropdown items */
        div[role="listbox"] {
            background-color: white !important;
            color: black !important;
        }

        /* 🧾 Text inputs (if any) */
        input[type="text"] {
            background-color: white !important;
            color: black !important;
        }

        /* Placeholder text */
        ::placeholder {
            color: gray !important;
        }
    </style>
""", unsafe_allow_html=True)

# Safely fetch poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=aa069f1b664ca9098eaff1ad93535e5e&language=en-US"
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json'
    }

    fallback_image = "https://i.imgur.com/5sJcZlF.png"  # ✅ Real poster

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return fallback_image

        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return fallback_image
    except Exception:
        return fallback_image


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_names = []
    recommended_posters = []
    for i in distances[1:6]:  # Always get 5
        movie_id = movies.iloc[i[0]].movie_id
        recommended_names.append(movies.iloc[i[0]].title)
        poster_url = fetch_poster(movie_id)  # Will show fallback if missing
        recommended_posters.append(poster_url)
    return recommended_names, recommended_posters



# Streamlit UI
st.header("🎬 Movie Recommendation System")

# Load data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    '📽️ Type or select a movie to get recommendations:',
    movie_list
)

# Show results
if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)
    for i in range(5):
        # if "Error" in posters[i]:
        #     continue
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])
            if posters[i] == "https://i.imgur.com/5sJcZlF.png":
                st.markdown("⚠️ Poster not found. Please refresh the page.", unsafe_allow_html=True)