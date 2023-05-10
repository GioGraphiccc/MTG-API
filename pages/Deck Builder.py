import streamlit as st

from methods.tools import parsePastedText, display_images_price_stats


def DeckBuilder():
    baseUrl = "https://api.scryfall.com"
    pastedText = st.text_area("Paste a deck")
    if(pastedText):
        users_deck = parsePastedText(pastedText, baseUrl)
        display_images_price_stats({'data':users_deck})


    
st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")
DeckBuilder()