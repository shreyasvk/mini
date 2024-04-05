import streamlit as st
from bs4 import BeautifulSoup
import requests
import os  # Import os module for terminal clearing

def search_by_author(quotes, authors, search_author):
    print("Searching by author:", search_author)  # Debugging statement
    index = [idx for idx, author in enumerate(authors) if search_author.lower() in author]
    if index:
        st.success(f"Quotes by {search_author}:")
        for idx in index:
            display_quote_with_like_button(quotes[idx], authors[idx], idx)

def search_by_keyword(quotes, authors, search_keyword):
    print("Searching by keyword:", search_keyword)  # Debugging statement
    st.success(f"Quotes containing '{search_keyword}':")
    for idx, quote in enumerate(quotes):
        if search_keyword.lower() in quote.lower():
            display_quote_with_like_button(quote, authors[idx], idx)

def display_quote_with_like_button(quote, author, idx):
    print("Displaying quote:", quote)  # Debugging statement
    st.write(f"- {quote}")
    st.write(f"  - {author}")
    like_button = st.button("Like", key=f"like_button_{idx}")
    if like_button:
        like_quote(quote)

def like_quote(quote):
    print("Liking quote:", quote)  # Debugging statement
    session_state = st.session_state
    print("Session state before:", session_state)  # Debugging statement
    if 'liked_quotes' not in session_state:
        print("Liked quotes not found in session state. Initializing...")  # Debugging statement
        session_state.liked_quotes = []  # Initialize liked quotes list if it doesn't exist
    liked_quotes = session_state.liked_quotes.copy()  # Create a copy of the liked quotes list
    liked_quotes.append(quote)  # Append the liked quote to the copied list
    st.session_state['liked_quotes'] = liked_quotes  # Update session state with the modified list
    st.success("Quote liked!")  # Display success message
    print("Updated liked quotes:", st.session_state.liked_quotes)  # Debugging statement



def get_quotes():
    print("Getting quotes...")  # Debugging statement
    # Set user-agent header
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    # Scraping quotes
    URL = 'https://www.goodreads.com/quotes'
    webpage = requests.get(URL, headers=headers)
    soup = BeautifulSoup(webpage.text, 'html.parser')

    quoteText = soup.find_all('div', attrs={'class': 'quoteText'})
    quotes = []
    authors = []
    for i in quoteText:
        quote = i.text.strip().split('\n')[0]
        author = i.find('span', attrs={'class': 'authorOrTitle'}).text.strip().lower()
        quotes.append(quote)
        authors.append(author)
    return quotes, authors

def display_quotes(quotes, authors):
    print("Displaying quotes...")  # Debugging statement
    for quote, author in zip(quotes, authors):
        st.write(f"- {quote}")
        st.write(f"  - {author}")

def display_liked_quotes():
    print("Displaying liked quotes...")  # Debugging statement
    if 'liked_quotes' in st.session_state and st.session_state.liked_quotes:
        st.header("Liked Quotes")
        for liked_quote in st.session_state.liked_quotes:
            st.write(f"- {liked_quote}")
    else:
        print("No liked quotes found in session state")  # Debugging statement

# Clear the terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Streamlit app
def main():
    st.title("QuotesInn")

    # Initialize session state if not initialized
    if 'liked_quotes' not in st.session_state:
        st.session_state.liked_quotes = []

    print("Session state:", st.session_state)  # Debugging statement

    option = st.radio("Select search option:", ("Search by Author", "Search by Keyword"))

    quotes, authors = get_quotes()  # Fetch quotes regardless of search
    print("Quotes:", quotes)  # Debugging statement
    print("Authors:", authors)  # Debugging statement

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

    # Display quotes if no search performed
    if option not in ["Search by Author", "Search by Keyword"]:
        display_quotes(quotes, authors)

    # Display liked quotes
    display_liked_quotes()

if __name__ == "__main__":
    main()
