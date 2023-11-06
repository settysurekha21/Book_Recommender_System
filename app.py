import pickle
import streamlit as st
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import requests

def main():
    st.header("Books Recommender System")
    model = pickle.load(open(r'E:/book recommender system/artifacts/model.pkl', 'rb'))
    books_name = pickle.load(open(r'E:/book recommender system/artifacts/books_name.pkl', 'rb'))
    final_rating = pickle.load(open(r'E:/book recommender system/artifacts/final_rating.pkl', 'rb'))
    book_pivot = pickle.load(open(r'E:/book recommender system/artifacts/book_pivot.pkl', 'rb'))



    # Define a function to search for a book and retrieve its ISBN
    def search_book_by_name(book_name):
        url = f"https://www.googleapis.com/books/v1/volumes?q={book_name.replace(' ', '+')}"
        response = requests.get(url)
        data = response.json()
        return data

    # Define a function to get book details from the Google Books API using ISBN
    def get_book_details(isbn):
        url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
        response = requests.get(url)
        data = response.json()
        return data

    # Create a horizontal scrollable container for book names and images
    def horizontal_scrollable_container(books_info):
        container = '<div style="white-space: nowrap; overflow-x: auto;">'
        for book_name, img_url in books_info:
            container += f'<div style="display: inline-block; margin: 10px; text-align: center;">'
            container += f'<img src="{img_url}" style="width: 150px; height: 200px;"/><br>'
            container += f'{book_name}'
            container += '</div>'
        container += '</div>'
        st.markdown(container, unsafe_allow_html=True)

    def get_books_with_covers(dataframe, name, n):
        print("\nBooks by same Author:\n")
        au = dataframe['author'].unique()

        data = final_rating[final_rating['title'] != name]

        if au[0] in list(data['author'].unique()):
            k2 = data[data['author'] == au[0]]
            k2 = k2.sort_values(by=['rating'])
            book_list = k2[['title', 'img_url']].drop_duplicates(subset='title').head(n)
            return book_list
        return pd.DataFrame()

    def get_books_with_covers_publisher(dataframe, name, n):
        print("\nBooks by same Publisher:\n")
        au = dataframe['publisher'].unique()

        data = final_rating[final_rating['title'] != name]

        if au[0] in list(data['publisher'].unique()):
            k2 = data[data['publisher'] == au[0]]
            k2 = k2.sort_values(by=['rating'])
            book_list = k2[['title', 'img_url']].drop_duplicates(subset='title').head(n)
            return book_list
        return pd.DataFrame()

    # Define a function to fetch popular books
    def get_popular_books(dataframe,n):
        if n >= 1 and n <= len(dataframe):
            data = pd.DataFrame(dataframe.groupby('ISBN')['rating'].count()).sort_values('rating', ascending=False).head(n)
            result = pd.merge(data, final_rating, on='ISBN')
            return result
        return "Invalid number of books entered!!"

    # Define a function to display popular books in the sidebar
    def display_popular_books():
        st.sidebar.markdown('<p style="color: #FF4B4B;">Top Popular Books</p>', unsafe_allow_html=True)

        #st.sidebar.subheader("Top Popular Books")
        popular_books = get_popular_books(final_rating,10)
    
        seen_titles = set()
    
        for i,  book_data in enumerate(popular_books.iterrows(), start=1):
            book_title = book_data[1]['title']
        
            if book_title not in seen_titles:
                st.sidebar.write(f"{book_title}")
            
                seen_titles.add(book_title)


    def fetch_poster(suggestion):
        book_name = []
        ids_index = []
        poster_url = []

        for book_id in suggestion:
            book_name.append(book_pivot.index[book_id])

        for name in book_name[0]:
            ids = np.where(final_rating['title'] == name)[0][0]
            ids_index.append(ids)

        for idx in ids_index:
            url = final_rating.iloc[idx]['img_url']
            poster_url.append(url)

        return poster_url


    def recommend_books(book_name):
        book_list = []
        book_id = np.where(book_pivot.index == book_name)[0][0]
        distance, suggestion = model.kneighbors(book_pivot.iloc[book_id,:].values.reshape(1,-1), n_neighbors=6)

        poster_url = fetch_poster(suggestion)
        for i in range(len(suggestion)):
            books = book_pivot.index[suggestion[i]]
            for j in books:
                book_list.append(j)
        return book_list, poster_url

       

    def get_non_zero_rating_by_title(title):
        ratings = final_rating[final_rating['title'] == title]
        non_zero_ratings = ratings[ratings['rating'] != 0]
        if not non_zero_ratings.empty:
            return non_zero_ratings['rating'].values[0]
        return "No non-zero ratings available"



    selected_books = st.selectbox(
        "Type or select a book",
        books_name
    )

    display_popular_books()

    recommendation_books, poster_url = recommend_books(selected_books)
    book_title = recommendation_books[0]
    col1, col2 = st.columns(2)
    with col1:
        st.text(book_title)
        st.image(poster_url[0])
        rating = get_non_zero_rating_by_title(recommendation_books[0])
        st.write(f"Rating: {rating}")
    with col2:
        book_info = get_book_details(final_rating[final_rating['title'] == book_title]['ISBN'].values[0])
        if 'items' in book_info:
            book = book_info['items'][0]['volumeInfo']
            st.markdown("<p style='color: #FF4B4B;'><b>Book Details</b></p>", unsafe_allow_html=True)
            st.write(f"Title: {book.get('title', 'Title not found')}")
            st.write(f"Authors: {', '.join(book.get('authors', ['The authors identity is under review, more details coming soon.']))}")
            st.write(f"Description: {book.get('description', 'We are working on the book description, please check back again later.')}")
                
            st.write(f"Genre(s): {', '.join(book.get('categories', ['Genre classification in progress- will be provided shortly.']))}")
                
        else:
            st.markdown("<p style='color: #FF4B4B;'><b>Book Details</b></p>", unsafe_allow_html=True)
            st.write(f"Title: {book_title}")
            st.write(f"Authors: The author's identity is under review, more details coming soon.")
            st.write(f"Description: We're working on the book description, please check back again later.")
            st.write(f"Genre(s): Genre classification in progress- will be provided shortly.")
      

    if st.button('Show Recommendation'):
    
        recommendation_books, poster_url = recommend_books(selected_books)
        st.subheader("You might also like these") 
        for i in range(1,len(recommendation_books)):
            book_title = recommendation_books[i]
            col1, col2 = st.columns(2)
            with col1:
                st.text(book_title)
                st.image(poster_url[i])
                rating = get_non_zero_rating_by_title(recommendation_books[i])
                st.write(f"Rating: {rating}")

            

            with col2:
                book_info = get_book_details(final_rating[final_rating['title'] == book_title]['ISBN'].values[0])
                if 'items' in book_info:
                    book = book_info['items'][0]['volumeInfo']
                    st.markdown("<p style='color: #FF4B4B;'><b>Book Details</b></p>", unsafe_allow_html=True)
                    st.write(f"Title: {book.get('title', 'Title not found')}")
                    st.write(f"Authors: {', '.join(book.get('authors', ['The authors identity is under review, more details coming soon.']))}")
                    st.write(f"Description: {book.get('description', 'We are working on the book description, please check back again later.')}")
                
                    st.write(f"Genre(s): {', '.join(book.get('categories', ['Genre classification in progress- will be provided shortly.']))}")
                
                else:
                    st.markdown("<p style='color: #FF4B4B;'><b>Book Details</b></p>", unsafe_allow_html=True)
                    st.write(f"Title: {book_title}")
                    st.write(f"Authors: The author's identity is under review, more details coming soon.")
                    st.write(f"Description: We're working on the book description, please check back again later.")
                    st.write(f"Genre(s): Genre classification in progress- will be provided shortly.")

        if selected_books in list(final_rating['title'].unique()):
            d = final_rating[final_rating['title'] == selected_books]
            books_by_author = get_books_with_covers(d, selected_books, 10)
            author_name = d['author'].values[0]
            if not books_by_author.empty:  # Check if the DataFrame is not empty
                st.subheader(f"Books by {author_name}")
                books_info = list(zip(books_by_author['title'], books_by_author['img_url']))
                horizontal_scrollable_container(books_info)
            else:
                st.write("No books found by the same Author.")
        
        else:
            st.write("Invalid Book Name!!")

        if selected_books in list(final_rating['title'].unique()):
            d = final_rating[final_rating['title'] == selected_books]
            books_by_publisher = get_books_with_covers_publisher(d, selected_books, 10)
            publisher_name = d['publisher'].values[0]
            if not books_by_publisher.empty:  # Check if the DataFrame is not empty
                st.subheader(f"Books by {publisher_name}")
                books_info = list(zip(books_by_publisher['title'], books_by_publisher['img_url']))
                horizontal_scrollable_container(books_info)
            else:
                st.write("No books found by the same Publisher.")
        else:
            st.write("Invalid Book Name!!")




if __name__ == "__main__":
    main()





    
