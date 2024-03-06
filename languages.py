import streamlit as st
import pandas as pd
def main():
    # Load the dataset from the Excel file
    dataset_file = "data/Languages_books.xlsx"  # Replace with the actual filename
    df = pd.read_excel(dataset_file)

    # Get unique languages from the dataset
   
    # Get unique languages from the dataset
    available_languages = [''] + df['Language'].unique().tolist()

    # Streamlit UI
    st.title("Book Recommendation App")

    # Language selection
    selected_language = st.selectbox('Choose language', available_languages)

    # Counter to keep track of displayed books
    book_display_counter = 0
    global display_heading
    display_heading=True
    show_more_button = True

    # Flag to control heading display

    # Function to display books
    def display_books(df, selected_language, selected_genre, counter, num_books=5):
        global display_heading

        if display_heading:
            st.subheader(f"Top {num_books} Books in {selected_genre} for {selected_language}:")
            display_heading = False

        genre_books = df[df['Genre'] == selected_genre].iloc[counter: counter + num_books]

        for index, row in genre_books.iterrows():
            st.write(f"- {row['Book Name']} by {row['Author']}")

    # Filter dataset based on selected language
    if selected_language:
        filtered_df = df[df['Language'] == selected_language]

        # Get unique genres for the selected language
        available_genres = [''] + filtered_df['Genre'].unique().tolist()

        # Genre selection
        selected_genre = st.selectbox('Choose genre', available_genres)

        # Display top 5 books for the selected language and genre
        if selected_genre:
            display_books(filtered_df, selected_language, selected_genre, book_display_counter)

            # Custom HTML to position the "More" button to the right
            col1, col2 = st.columns([3, 1])
            with col2:
                # More button
                more_button_clicked = st.button("More")

                if more_button_clicked:
                    book_display_counter += 5

                    # Check if there are more books
                    if book_display_counter >= len(filtered_df[df['Genre'] == selected_genre]):
                        st.empty()  # Remove the "More" button
                    with col1:
                        st.subheader("Other books are")
                        display_books(filtered_df, selected_language, selected_genre, book_display_counter)

    else:
        st.warning("Please select a language.")

    # Add any additional content or styling as needed
if __name__ == "__main__":
    main()
