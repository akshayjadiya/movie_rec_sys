# import streamlit as st 
from check_user import check_user
from popular_recommendations import show_popular_recommendations
from model_recommendations import generate_recommendation_svd, get_master_df


import streamlit as st
st.title("Movie Recommender System")


if 'stage' not in st.session_state:
    st.session_state.stage = 0

def set_state(i):
    st.session_state.stage = i

if st.session_state.stage == 0:
    st.button('Begin', on_click=set_state, args=[1])


if st.session_state.stage >= 1:
    # name = st.text_input('Name', on_change=set_state, args=[2])
    text_input = st.text_input("Enter user ID of the customer")
    st.button('Generate Recommendations', on_click=set_state, args=[2]) 
    
    

if st.session_state.stage >= 2:
    int_user_id = int(text_input)
    st.write("Hello User ID : {}".format(int_user_id))
    if(check_user(int_user_id) == 0):
        st.write("User {} is a new user. Please select your favourite genres to get recommendations".format(text_input),
                on_change=set_state, args=[2])

        options = st.multiselect(
            'Select your favourite genres',
            ['Adventure', 'Animation', 'Children', 'Comedy', 'Fantasy',
            'Romance', 'Action', 'Crime', 'Thriller', 'Mystery', 'Horror',
            'Drama', 'War', 'Western', 'Sci-Fi', 'Musical', 'Film-Noir',
            'IMAX', 'Documentary']
        )

        if(len(options) >= 1):
            set_state(3)
    else:
        st.write("Below are the recommendations for User {}".format(text_input),
                on_change=set_state, args=[2])
        rec_df = generate_recommendation_svd(int_user_id,get_master_df())
        st.dataframe(rec_df)

def generate_popular():
    set_state(4)
    
    
if st.session_state.stage >= 3:
    df = show_popular_recommendations(options)
    st.button('Find interesting movies to watch' , on_click=generate_popular)

if st.session_state.stage >= 3:
    st.dataframe(df)
    