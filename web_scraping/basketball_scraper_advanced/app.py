# Script to scrape basketball statistics
# Noah Rubin: 2023

from helpers import scrape_bball_stats, download
import streamlit as st
import numpy as np


def main():
    st.markdown("""
            # Basketball Data Scraper App
            
            ### Created By: Noah Rubin
            📊 [LinkedIn](https://www.linkedin.com/in/noah-rubin1/)  
            
            🧑🏽‍💻 [GitHub](https://github.com/noahrubin989)
            """)
    
    years = np.arange(2002, 2023)
    st.write("Below you will see select boxes to determine the years you wish to scrape data for")
    start = st.selectbox("Start Year", years)
    end = st.selectbox("End Year", years[years >= start])
    
    if start and end:
        if st.button("Scrape Data"):
            st.write("Getting your data...")
            driver_path = './chromedriver'
            data = scrape_bball_stats(start, end, driver_path=driver_path)
            
            st.write("Job Done!")
            download(data)

if __name__ == '__main__':
    main()
