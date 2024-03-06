# page1.py
import streamlit as st

def main():
    
    st.markdown(
            """
            <style>
                .banner-img {
                    width: 100%;
                    height: auto;
                }
            </style>
            """
        , unsafe_allow_html=True)

    st.image("about-1.png", use_column_width=True, output_format='PNG', )
    st.image("about-2.png", use_column_width=True, output_format='PNG', )
    st.image("about-3.png", use_column_width=True, output_format='PNG', )
    st.image("about-4.png", use_column_width=True, output_format='PNG', )
    

if __name__ == "__main__":
    main()
