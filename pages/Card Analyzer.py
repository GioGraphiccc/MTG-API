import streamlit as st
import requests

from methods.tools import formatWord, collectResponses
from methods.database_methods import addCard, fetchCard, init_connection
from methods.collect_info import getCardInformation

def CardAnalyzer():
    
    baseUrl = "https://api.scryfall.com"
    card_name = st.text_input("Enter card name")
    results = ""
    if(card_name): 
        url = baseUrl + "/cards/search"
        response = requests.get(url, params={'q':card_name}).json()
        results = collectResponses(response)

    if results != "":
        conn = init_connection()
        selected_card = st.selectbox(
        'Results',
        results)
        info = fetchCard(selected_card, conn)
        if(info[0] == 0):
            url = baseUrl + "/cards/" + results[selected_card]
            response = requests.get(url).json()
            st.divider()
            #st.write(response)
            info = getCardInformation(response) 
            addCard(info, conn)
            

        id = info[0]                                           
        card_name = info[1]
        card_type = info[2]
        set_name  = info[3]
        price = info[4]
        priceF = info[5]
        rarity = info[6]
        colors = info[7]
        keywords = info[8]
        cmc = info[9]
        mana_cost = info[10]
        legalityS = info[11]
        legalityC = info[12]
        power_toughness =  info[13]
        tcgplayer_id = info[14]
        img_url = info[15]

        col1, col2 = st.columns(2)
        with col1:
            #st.write(response)
            st.write(card_name)
            st.write("Standard: " + formatWord(legalityS))
            st.write("Commander: " + formatWord(legalityC))
            st.write("Rarity: " + rarity)
            st.write("Set: " + set_name)
            st.write(colors)
            if(price is None):
                st.write("Price: N/A")
            else:
                st.write("Price: $" + formatWord(price))
            if(priceF is None):
                st.write("Foil Price: N/A")
            else:
                st.write("Foil Price: $" + formatWord(priceF))

        with col2:
            #replace = st.empty()
            if(img_url.count("http") == 2):
                #replace.empty()
                st.image(img_url[0:img_url.find("http")-1])
                st.image(img_url[0:img_url.find("http")-1].replace("front", "back"))
                    
            else:
                st.image(img_url)
    

st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")

CardAnalyzer()