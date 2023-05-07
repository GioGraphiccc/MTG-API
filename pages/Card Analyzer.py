import streamlit as st
import requests

from methods.tools import formatWord, collectResponses

def CardAnalyzer():
    baseUrl = "https://api.scryfall.com"

    card_name = st.text_input("Enter card name")
    if(card_name):
        option = ""
        url = baseUrl + "/cards/search"
        response = requests.get(url, params={'q':card_name}).json()
        results = collectResponses(response)

        if results:
            option = st.selectbox(
                'Results',
                results)
        st.divider()
        
        if(option != ""):
            url = baseUrl + "/cards/" + results[option]
            response = requests.get(url).json()
            st.write(response)                                                  #DEBUG LINE
            legalityS = response['legalities']['standard']
            legalityC = response['legalities']['commander']
            price = response['prices']['usd']
            priceF = response['prices']['usd_foil']
            rarity = response['rarity']
            set_name  = response['set_name']

            col1, col2 = st.columns(2)
            with col1:
                #st.write(response)
                st.write(response['name'])
                st.write("Standard: " + formatWord(legalityS))
                st.write("Commander: " + formatWord(legalityC))
                st.write("Rarity: " + rarity)
                st.write("Set: " + set_name)
                if(price is None):
                    st.write("Price: N/A")
                else:
                    st.write("Price: $" + price)
                if(priceF is None):
                    st.write("Foil Price: N/A")
                else:
                    st.write("Foil Price: $" + priceF)

            with col2:
                doubleface = False
                replace = st.empty()
                replaceEnlarge = st.empty()
                try:
                    if(len(response['card_faces']) != 1):
                        doubleface = True
                except:
                    doubleface = False
                enlarge = st.checkbox('Enlarge')
                if(doubleface):
                    replaceEnlarge.empty()
                    with replace.container():
                        st.image(response['card_faces'][0]['image_uris']['small'])
                        st.image(response['card_faces'][1]['image_uris']['small'])
                    
                    if doubleface and enlarge:
                        replace.empty()
                        with replaceEnlarge.container():
                            st.image(response['card_faces'][0]['image_uris']['normal'])
                            st.image(response['card_faces'][1]['image_uris']['normal'])
                else:
                    replaceEnlarge.empty()
                    with replace.container():
                        st.image(response['image_uris']['small'])
                    if(enlarge):
                        replace.empty()
                        with replaceEnlarge.container():
                            st.image(response['image_uris']['normal'])

st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")
CardAnalyzer()