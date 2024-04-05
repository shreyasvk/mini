import streamlit as st
from bs4 import BeautifulSoup
import requests

def search_by_author(quotes, authors, search_author):
    index = [idx for idx, author in enumerate(authors) if search_author.lower() in author]
    if index:
        st.success(f"Quotes by {search_author}:")
        for idx in index:
            display_quote_with_like_button(quotes[idx], authors[idx], idx)  # Pass idx as key

def search_by_keyword(quotes, authors, search_keyword):
    st.success(f"Quotes containing '{search_keyword}':")
    for idx, quote in enumerate(quotes):
        if search_keyword.lower() in quote.lower():
            display_quote_with_like_button(quote, authors[idx], idx)  # Pass idx as key
favorites=[]
def display_quote_with_like_button(quote, author, idx):  # Accept idx as parameter
    st.write(f"- {quote}")
    st.write(f"  - {author}")
    like_button_key = f"Like_{idx}"  # Generate unique key based on idx
    if st.button('like', key=like_button_key):  # Pass key parameter to st.button
        favorites.append(quote)
        
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
logo_path = 'QuotesInn.png'

# Sample hardcoded usernames and passwords
credentials = {
    "user1": "password1",
    "user2": "password2",
    "user3": "password3"
}

# Streamlit app
def main():
    st.sidebar.image(logo_path, use_column_width=False, width=350)

    # Create a session state to track login status and liked quotes
    session_state = st.session_state
    if 'logged_in' not in session_state:
        session_state.logged_in = False
    if 'liked_quotes' not in session_state:
        session_state.liked_quotes = {}

    if not session_state.logged_in:
        auth_option = st.sidebar.radio("Select an option:", ("Login", "Signup"))

        if auth_option == "Login":
            st.sidebar.subheader("Login")
            username = st.sidebar.text_input("Username")
            password = st.sidebar.text_input("Password", type="password")
            if st.sidebar.button("Login"):
                # Check if username and password match
                if username in credentials and credentials[username] == password:
                    session_state.logged_in = True
                    session_state.username = username
                else:
                    st.sidebar.error("Invalid username or password. Please try again.")
        elif auth_option == "Signup":
            st.sidebar.subheader("Signup")
            new_username = st.sidebar.text_input("New Username")
            new_password = st.sidebar.text_input("New Password", type="password")
            if st.sidebar.button("Signup"):
                # Check if username already exists
                if new_username in credentials:
                    st.sidebar.error("Username already exists. Please choose a different one.")
                else:
                    # Add new username and password to credentials
                    credentials[new_username] = new_password
                    st.sidebar.success("Signup successful! You can now login with your new credentials.")
    else:
        st.title("QuotesInn")
        option = st.radio("Select search option:", ("Search by Author", "Search by Keyword"))

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

        # Favorite quotes section
        st.sidebar.header("Favorite Quotes")
        
        if favorites:
            st.sidebar.success("Your favorite quotes:")
            for favorite in favorites:
                st.sidebar.write(f"- {favorite}")
        else:
            st.sidebar.info("You haven't liked any quotes yet.")

if __name__ == "__main__":
    main()

