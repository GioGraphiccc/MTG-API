import streamlit as st
import requests

from methods.tools import formatWord, collectResponses
from methods.database_methods import addCardToDB, fetchCard, init_connection
from methods.Card import Card

def CardAnalyzer():
    
    baseUrl = "https://api.scryfall.com"
    card_name = st.text_input("Enter card name")
    results = ""
    if(card_name): 
        url = baseUrl + "/cards/search"
        response = requests.get(url, params={'q':card_name}).json()
       
        results = collectResponses(response, card_name)
        #st.write(results)
        if results != None:
            conn = init_connection()
            selected_card = st.selectbox(
            'Results',
            results)
            card = fetchCard(selected_card, conn)
            if not card: #if not in the DB
                url = baseUrl + "/cards/named" 
                selected_response = requests.get(url, params={'exact':selected_card}).json()
                card = Card.setCardInformation(selected_response) 
                addCardToDB(card, conn)

            # id = info[0]                                           
            # card_name = info[1]
            # card_type = info[2]
            # set_name  = info[3]
            # price = info[4]
            # priceF = info[5]
            # rarity = info[6]
            # colors = info[7]
            # keywords = info[8]
            # cmc = info[9]
            # mana_cost = info[10]
            # legalityS = info[11]
            # legalityC = info[12]
            # power_toughness =  info[13]
            # tcgplayer_id = info[14]
            # img_url = info[15]

            st.divider()

            if(card.price is None):
                price = "N/A"
            else:
                price = str(card.price)

            if(card.priceF is None):
                priceF = "N/A"
            else:
                priceF = str(card.priceF)
            
            col1, col2 = st.columns(2, gap="small")
            with col1:
                #st.write(response)
                st.header(card.card_name)
                st.subheader(card.rarity.title())
                #st.write(formatWord(card.colors))

                col1_metric, col2_metric = st.columns(2, gap="small")

                if price == "N/A":
                    col1_metric.metric("", "Price", price, delta_color="off")
                else:
                    col1_metric.metric("", "Price", price)
                if priceF == "N/A":
                    col1_metric.metric("", "Foil Price", priceF)
                else:
                    col1_metric.metric("", "Foil Price", price)

                col2_metric.metric("", "Standard", ("+" if formatWord(card.legalityS) == "Legal" else "-") + formatWord(card.legalityS),label_visibility='hidden')
                col2_metric.metric("", "EDH", ("+" if formatWord(card.legalityC) == "Legal" else "-") + formatWord(card.legalityC),label_visibility='hidden')
                
                
                
                
                st.write("Set: " + card.set_name)
            with col2:
                #replace = st.empty()
                if(card.img_url.count("http") == 2):
                    #replace.empty()
                    st.image(card.img_url[0:card.img_url.find("http")-1])
                    st.image(card.img_url[0:card.img_url.find("http")-1].replace("front", "back"))
                    #col1_metric, col2_metric = st.columns(2, gap="small")
                    #col1_metric.metric("", "Standard", ("+" if formatWord(card.legalityS) == "Legal" else "-") + formatWord(card.legalityS),label_visibility='hidden')
                    #col2_metric.metric("", "Commander", ("+" if formatWord(card.legalityC) == "Legal" else "-") + formatWord(card.legalityC),label_visibility='hidden')
                else:
                    st.image(card.img_url)
                    #col1_metric, col2_metric = st.columns(2, gap="small")
                    #col1_metric.metric("", "Standard", ("+" if formatWord(card.legalityS) == "Legal" else "-") + formatWord(card.legalityS),label_visibility='hidden')
                    #col2_metric.metric("", "Commander", ("+" if formatWord(card.legalityC) == "Legal" else "-") + formatWord(card.legalityC),label_visibility='hidden')


st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")

CardAnalyzer()