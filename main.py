import streamlit as st
from streamlit_option_menu import option_menu
# Create a navigation sidebar
selected = option_menu(
    menu_title = None,
    options=["Home", "Recommend","ChatBot", "Languages","About"],
    default_index = 0,
    orientation="horizontal",
    styles ={
        "nav-link": {
             "display": "inline-block",  # Adjust display property to "inline-block"
            "margin-right": "5px",  # Add margin-right for spacing between buttons
            "padding": "5px",  # Adjust padding for cell spacing and button size
            "border-radius": "5px",  # Optional: Add border-radius for rounded corners
            "transition": "background-color 0.3s",  # Optional: Add transition effect
            "width": "131px",  # Set the width for each button
            "text-align": "center",  # Center text within the button
            "white-space": "nowrap",  # Prevent text wrapping
        }
    }
    
)



# Import the pages
from about import main as about
from mood import main as mood
from app import main as recommend
from languages import main as languages
from home import main as home
# Create a dictionary to map page names to functions
pages = {
    "Home": home,
    "Recommend" : recommend,
    "About": about,
    "ChatBot": mood,
    "Languages":languages
}


# Display the selected page
if selected in pages:
    if pages[selected] is not None:
        pages[selected]()
    else:
        st.title("Home Page")
        st.write("This is the home page content.")

