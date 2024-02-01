import streamlit as st
import datetime
import requests

from methods.collect_info import SearchSets
from methods.tools import display_images_price_stats, fetchSetCards, addSetNamesToFile, displaySetPreviews
from methods.database_methods import addSetToDB
from methods.Card import Card

def SetAnalyzer(): 
    results = {}
    selected_set = ""
    baseUrl = "https://api.scryfall.com"
    typesOfSets = ("All", "Commander", "Expansion", "Masters", "Alchemy", "Starters", "Core", "Arsenal", "Funny", "premium_deck",
                   "box", "promo", "token", "minigame", "duel_deck", "draft_innovation", "treasure_chest", "planechase", "archenemy",
                    "vangaurd")
    col1, col2 = st.columns(2) #Create Two columns. col1 will be for the Set search bar and col2 will be for the Set Type select box 
    with col2: #place col2 into the screen
        selected_set_type = st.selectbox('Type of sets', typesOfSets) #create a select box for the types of sets

    with col1:
        selected_set = st.text_input("Enter set name")

    placeholder = displaySetPreviews(selected_set_type) #assign placeholder to this so that it can dissapear from view

    if(not selected_set != ""):
        exit()

    placeholder.empty()
    url = baseUrl + "/sets"
    response = requests.get(url).json()
    if selected_set_type == "All":
        for set_type in typesOfSets:
            if set_type == "All": continue
            results.update(SearchSets(response, selected_set, set_type))
    else:
        results = SearchSets(response, selected_set, selected_set_type)

    if results:
        st.write(results)
        addSetNamesToFile(results)
        selected_set = st.selectbox('Results', results, key=1)

    else:
        st.error("Set doesnt exist!")
        st.error("url: " + str(url))
        
    if(selected_set != ""):
        Card_Set = fetchSetCards(selected_set, results, baseUrl)
        

        
    display_images_price_stats(Card_Set) #keep first parameter empty since we cannot obtain from db using Set Analyzer
    results.clear()
    #st.write(Card_Set)
    addSetToDB(Card_Set)
            

st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")         
st.title("MTG Card and Set Analyzer - Scryfall API")
SetAnalyzer()