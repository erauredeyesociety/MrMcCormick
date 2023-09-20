# generate search queries for movie scripts
import webbrowser
from tqdm import tqdm
'''
TLDR: 

1. Identify movie/tv show characters that you want your bot's personality to be based on.
2. Identify the names of the movies/tv shows with these characters
3. Make a list of these movie/tv shows names and if possible, include creation dates
4. Run this python program to do a bunch of google searches to find and download the movie/tv show scripts 
5. when you find a script for a movie/tv show, download it to wherever you want
6. Search for the next movie script by clicking back on this program and pressing 'Enter'


The not TLDR:

The idea behind this chatbot project is that the bot is trained on movie characters
and their dialogues. The bot will be able to generate a response based on the script of the movie

Specifically, this project aims to open-source the process of customizing your own chatbot
to your own needs. The chatbot will be trained on a dataset of movie scripts, and the end result 
should be something that resembles a combination of movie character personalities.
'''

movies = [
    "Dr. No (1962)",
    "From Russia with Love (1963)",
    "Goldfinger (1964)",
    "Thunderball (1965)",
    "You Only Live Twice (1967)",
    "On Her Majesty's Secret Service (1969)",
    "Live and Let Die (1973)",
    "The Man with the Golden Gun (1974)",
    "The Spy Who Loved Me (1977)",
    "Moonraker (1979)",
    "For Your Eyes Only (1981)",
    "Octopussy (1983)",
    "A View to a Kill (1985)",
    "The Living Daylights (1987)",
    "Licence to Kill (1989)",
    "GoldenEye (1995)",
    "Tomorrow Never Dies (1997)",
    "The World Is Not Enough (1999)",
    "Die Another Day (2002)",
    "Casino Royale (2006)",
    "Quantum of Solace (2008)",
    "Skyfall (2012)",
    "Spectre (2015)",
    "No Time to Die (2021)",
    "American Psycho",
    "The Dark Knight",
    "Dark Knight Rises",
    "Joker",
    "Suits (2011-2019)",
    "Iron Man (2008)",
    "Iron Man 2 (2010)",
    "The Avengers (2012)",
    "Iron Man 3 (2013)",
    "Captain America: The Winter Soldier (2014)",
    "Avengers: Age of Ultron (2015)",
    "Captain America: Civil War (2016)",
    "Avengers: Infinity War (2018)",
    "Avengers: Endgame (2019)",
    "Peaky Blinders",
    "Fifty Shades of Grey (2015)",
    "Fifty Shades Darker (2017)",
    "Fifty Shades Freed (2018)",
    "The Punisher (2017-2019)",
    "The Punisher: Season 2 (2019)",
    "Fight Club",
    "Ocean's Eleven (2001)",
    "Ocean's Twelve (2004)",
    "Ocean's Thirteen (2007)",
    "Scarface",
    "Olympus Has Fallen (2013)",
    "London Has Fallen (2016)",
    "Angel Has Fallen (2019)",
    "Terminal List (2021)",
    "American Assassin (2017)",
    "First Blood (1982)"
    "Rambo: First Blood Part II (1985)",
    "Rambo III (1988)",
    "Rambo (2008)",
    "Rambo: Last Blood (2019)",
    "Top Gun (1986)",
    "Top Gun: Maverick (2021)",
    "Jack Ryan",
    "Jack Reacher (2012)",
    "Jack Reacher: Never Go Back (2016)",
    "Night Shift Medical Drama",
    "Yellowstone (2018)",
    "Prison Break (2005-2009)",
    "Pirates of the Caribbean: The Curse of the Black Pearl (2003)",
    "Pirates of the Caribbean: Dead Man's Chest (2006)",
    "Pirates of the Caribbean: At World's End (2007)",
    "Pirates of the Caribbean: On Stranger Tides (2011)",
    "Pirates of the Caribbean: Dead Men Tell No Tales (2017)",
    "Seriously Funny",
    "RV (2006)",
]

def make_query(movie_name):
    start_query = "https://www.google.com/search?q=download+for+"
    movie_name = movie_name.replace(" ", "+")
    end_query = "+dialogue+script"
    query = start_query + movie_name + end_query
    return query

def exec_queries():
    # open a new chrome tab for each query
    for movie in tqdm(movies):
        query = make_query(movie)
        # wait for user to press enter before opening next tab
        input("\nPress enter to open next tab...")
        webbrowser.open_new_tab(query)
    
exec_queries()