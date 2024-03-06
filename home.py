import streamlit as st

def main():
    

    # Add banner image
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

    st.image("home-1.png", use_column_width=True, output_format='PNG', )
   

  

if __name__ == "__main__":
    main()
