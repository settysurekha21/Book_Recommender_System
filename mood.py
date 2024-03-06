import streamlit as st
import requests

def main():
    def recommend_books_based_on_mood(moods, num_books):
        # Open Library API base URL
        base_url = "http://openlibrary.org/search.json"

        # Concatenate moods for the query
        query = '+'.join(moods)

        # Form the API request URL
        url = f"{base_url}?q={query}"

        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Extract unique book titles from the response
        unique_books = set()
        recommended_books = []

        for doc in data.get('docs', []):
            title = doc.get('title', '')
            if title not in unique_books:
                unique_books.add(title)
                recommended_books.append(title)

                # Break when the desired number of unique books is reached
                if len(recommended_books) == num_books:
                    break

        return recommended_books

    def recommend_books_based_on_genre(genre, num_books):
        # Open Library Books API base URL
        base_url = "http://openlibrary.org/subjects/"

        # Form the API request URL with genre filter
        url = f"{base_url}{genre}.json?limit={num_books}"

        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Extract book titles from the response
        recommended_books = [work['title'] for work in data.get('works', [])]

        return recommended_books

    # Streamlit UI
    st.title("Book Recommendation Chatbot")

    st.sidebar.header("Select Genre")
    selected_genre = st.sidebar.radio('Choose genre', ['Fiction', 'Non-fiction', 'Mystery', 'Romance', 'Science Fiction', 'Fantasy', 'Biography', 'History', 'Self-help', 'Thriller'])

    num_books_genre = st.sidebar.selectbox('Number of books to recommend', [5, 10, 15], key=f"genre_num_books_{selected_genre.lower()}")

    generate_button_genre = st.sidebar.button(f"Generate {selected_genre} Recommendations", key=f"generate_button_genre_{selected_genre.lower()}")

    if generate_button_genre:
        recommended_books = recommend_books_based_on_genre(selected_genre.lower(), num_books_genre)

        st.sidebar.subheader(f"Recommended Books in {selected_genre} ({num_books_genre} books):")
        for i, book in enumerate(recommended_books, start=1):
            st.sidebar.write(f"{i}. {book}")

    st.header("Select Moods")
    moods = st.multiselect(
        'Choose moods',
        ['Happy', 'Sad', 'Suspenseful', 'Scary', 'Romantic', 'Adventure', 'Mystical', 'Funny', 'Inspirational', 'Dramatic', 'Thoughtful', 'Thrilling', 'Mysterious', 'Whimsical', 'Dark']
    )

    st.header("Select Number of Books to Recommend")
    num_books_mood = st.selectbox('Number of books to recommend', [5, 10, 15], key="mood_num_books")  # Add a unique key here

    if not moods:
        st.warning("Please select at least one mood.")

    else:
        generate_button_mood = st.button("Generate Mood Recommendations", key="generate_button_mood")

        if generate_button_mood:
            recommended_books = recommend_books_based_on_mood(moods, num_books_mood)

            st.subheader(f"Recommended Books ({num_books_mood} books):")
            for i, book in enumerate(recommended_books, start=1):
                st.write(f"{i}. {book}")

if __name__ == "__main__":
    main()
