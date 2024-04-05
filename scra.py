import streamlit as st
from bs4 import BeautifulSoup
import requests

def search_by_author(quotes, authors, search_author):
    index = [idx for idx, author in enumerate(authors) if search_author.lower() in author]
    if index:
        st.success(f"Quotes by {search_author}:")
        for idx in index:
            st.write(f"- {quotes[idx]}")
    else:
        st.warning("No quotes found for the given author.")

def search_by_keyword(quotes, authors, search_keyword):
    st.success(f"Quotes containing '{search_keyword}':")
    for idx, quote in enumerate(quotes):
        if search_keyword.lower() in quote.lower():
            st.write(f"- {quote}")
            st.write(f"  - {authors[idx]}")

def search_by_genre(quotes, genres, search_genre):
    unique_genres = set(genres)
    print("Unique Genres:", unique_genres)
    
    index = [idx for idx, genre in enumerate(genres) if search_genre.lower() in genre.lower()]
    if index:
        st.success(f"Quotes from {search_genre} genre:")
        for idx in index:
            st.write(f"- {quotes[idx]}")
    else:
        st.warning("No quotes found for the given genre.")


# Scraping quotes
URL = 'https://www.goodreads.com/quotes'
webpage = requests.get(URL)
soup = BeautifulSoup(webpage.text, 'html.parser')

quoteText = soup.find_all('div', attrs={'class': 'quoteText'})
quotes = []
authors = []
genres = []
for i in quoteText:
    quote = i.text.strip().split('\n')[0]
    author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip().lower()
    genre_elem = i.find('a', attrs={'class': 'authorOrTitle'})
    genre = genre_elem.text.strip().lower() if genre_elem else "Unknown Genre"
    quotes.append(quote)
    authors.append(author)
    genres.append(genre)

# Streamlit app
def main():
    st.title("Quote Search")
    option = st.radio("Select search option:", ("Search by Author", "Search by Keyword", "Search by Genre"))

    if option == "Search by Author":
        search_author = st.text_input("Enter the name of the author:")
        if st.button("Search"):
            if search_author:
                search_by_author(quotes, authors, search_author)
            else:
                st.warning("Please enter an author name.")

    elif option == "Search by Keyword":
        search_keyword = st.text_input("Enter the keyword to find a quote:")
        if st.button("Search"):
            if search_keyword:
                search_by_keyword(quotes, authors, search_keyword)
            else:
                st.warning("Please enter a keyword.")

    elif option == "Search by Genre":
        search_genre = st.text_input("Enter the genre:")
        if st.button("Search"):
            if search_genre:
                search_by_genre(quotes, genres, search_genre)
            else:
                st.warning("Please enter a genre.")

if __name__ == "__main__":
    main()
