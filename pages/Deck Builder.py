import streamlit as st
import requests
from methods.tools import parsePastedText, display_images_price_stats, collectResponses
from methods.database_methods import fetchCard, init_connection, addSetToDB
from methods.Card import Card

def DeckBuilder():
    baseUrl = "https://api.scryfall.com"
    numCardsAddedToDB = 0
    cards_present_in_DB = []
    cards_not_present_in_DB = []
    pastedText = st.text_area("Paste a deck")
    if(pastedText):
        #progress_text = "Operation in progress. Please wait."
        #progress_bar = st.progress(0, text=progress_text)
        conn = init_connection()
        users_deck = parsePastedText(pastedText, baseUrl)
        
        for users_card in users_deck:
            card = fetchCard(users_card[1], conn)
            
            if(card == 0):
                numCardsAddedToDB = numCardsAddedToDB + 1
                url = baseUrl + "/cards/named"
                response = requests.get(url, params={'exact':users_card[1]}).json()
                card = Card.setCardInformation(response)
                #st.write(card)
                cards_not_present_in_DB.append(card)
            else:
                cards_present_in_DB.append(card)
                
        #st.write(cards_not_present_in_DB)
        addSetToDB(cards_not_present_in_DB) 

        if(numCardsAddedToDB != 0):
            st.success("Successfully added " + str(numCardsAddedToDB) + " cards to the DB!")

        for card in cards_not_present_in_DB:
            cards_present_in_DB.append(card)

        display_images_price_stats(cards_present_in_DB)

        
        
    
    
st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")
DeckBuilder()