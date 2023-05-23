import streamlit as st
import requests
from methods.tools import parsePastedText, display_images_price_stats, collectResponses
from methods.collect_info import getCardInformation
from methods.database_methods import addCard, fetchCard, init_connection

def DeckBuilder():
    baseUrl = "https://api.scryfall.com"
    numCardsAddedToDB = 0
    deck_info = []
    pastedText = st.text_area("Paste a deck")
    if(pastedText):
        conn = init_connection()
        users_deck = parsePastedText(pastedText, baseUrl)
        #st.write(users_deck)
        for card in users_deck:
            info = fetchCard(card[1], conn)
            if(info[0] == 0):
                numCardsAddedToDB = numCardsAddedToDB + 1
                url = baseUrl + "/cards/search"
                response = requests.get(url, params={'q':card[1]}).json()
                result = collectResponses(response)
                url = baseUrl + "/cards/" + result.popitem()[1]
                response = requests.get(url).json()
                info = getCardInformation(response)
                addCard(info,conn)
            deck_info.append(info)
        #st.write(deck_info)
        if(numCardsAddedToDB != 0):
            st.success("Successfully added " + str(numCardsAddedToDB) + " cards to the DB!")
        display_images_price_stats(deck_info)
    
    
st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")
DeckBuilder()