import streamlit as st
import datetime
import requests

from methods.collect_info import SearchSets
from methods.tools import formatWord, imageView, display_cards_info, display_images_price_stats
from methods.database_methods import addSetToDB, fetchCard, init_connection
from methods.Card import Card

def SetAnalyzer():
    baseUrl = "https://api.scryfall.com"
    typesOfSets = ("Commander", "Expansion", "Masters", "Alchemy", "Starters", "Core", "Arsenal", "Funny", "premium_deck")
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Sets made before... ", datetime.date.today())
    with col2:
        selected_set_type = st.selectbox('Type of sets', typesOfSets)
    if(selected_set_type):
        search = ""
        search = st.text_input("Enter set name")
        if(search != ""):
            option = ""
            url = baseUrl + "/sets"
            response = requests.get(url).json()
            #st.write(response)
            results = SearchSets(response, search, selected_set_type, date)
            if results:
                option = st.selectbox('Results',results, key=1)
            else:
                st.error("Set doesnt exist!")
                st.error("url: " + str(url))
            if(option != ""):
                url = baseUrl + "/sets/" + results[option]
                set_response = requests.get(url).json()
                #st.write(set_response)                                      #DEBUG LINE
                st.divider()
                
                set_name = set_response['name']
                st.header(set_name)
                numCardsInSet = str(set_response['card_count'])
                release_date = set_response['released_at']
                st.image(set_response['icon_svg_uri'])

                url = set_response['search_uri']
                cardlist_response = requests.get(url).json()
                #st.write(cardlist_response)                                          #DEBUG LINE
                Card_Set = []
                for card in cardlist_response["data"]:
                    Card_Set.append(Card.setCardInformation(card))

                if(cardlist_response["has_more"]):
                    cardlist_response = requests.get(cardlist_response['next_page']).json()
                    for card in cardlist_response["data"]:
                        Card_Set.append(Card.setCardInformation(card))
                if(cardlist_response["has_more"]):
                    cardlist_response = requests.get(cardlist_response['next_page']).json()
                    for card in cardlist_response["data"]:
                        Card_Set.append(Card.setCardInformation(card))
                if(cardlist_response["has_more"]):
                    cardlist_response = requests.get(cardlist_response['next_page']).json()
                    for card in cardlist_response["data"]:
                        Card_Set.append(Card.setCardInformation(card))
                if(cardlist_response["has_more"]):
                    cardlist_response = requests.get(cardlist_response['next_page']).json()
                    for card in cardlist_response["data"]:
                        Card_Set.append(Card.setCardInformation(card))

                
                display_images_price_stats(Card_Set) #keep first parameter empty since we cannot obtain from db using Set Analyzer

                #st.write(Card_Set)
                addSetToDB(Card_Set)
                
                



                #     with col2:
                #         set_2_name = ""
                #         displayData = True
                #         search_compare = ""
                #         search_compare = st.text_input("Compare prices with another set.")
                #         if(search_compare != ""):
                #             option_compare = ""
                #             url = baseUrl + "/sets"
                #             response = requests.get(url).json()
                #             results_compare = SearchSets(response, search_compare, selected_set_type, datetime.date.today())
                #             if results_compare:
                #                 option_compare = st.selectbox('Results',results_compare, key=3)
                #             if(option_compare != ""):
                #                 url = baseUrl + "/sets/" + results_compare[option_compare]
                #                 set_response_compare = requests.get(url).json() #root set info
                #                 set_2_name = set_response_compare['name']
                #                 url = set_response_compare['search_uri']
                #                 response_compare = requests.get(url).json() #card data from set
                #     if(st.button("Submit", key=4)):
                #         displayData = True
                #         if(set_2_name != ""):
                #             st.success("Comparing prices with " + set_2_name)
                #             set_2_info = getInformation(response_compare)
                #         else:
                #             st.success("Displaying Prices for " + set_1_name)
                #     tab1_area, tab2_line = st.tabs(["Area", "Line"])
                #     if(displayData):
                #         if(set_2_name != ""):
                #             with tab1_area:
                #                 chart_data = createChart(set_1_info[17], set_1_name, set_2_info[17], set_2_name)
                #                 st.area_chart(chart_data) 
                #             with tab2_line:
                #                 chart_data = createChart(set_1_info[17], set_1_name, set_2_info[17], set_2_name)
                #                 st.line_chart(chart_data)
                #             displayData = False
                #         else:
                #             with tab1_area:
                #                 chart_data = createChart(set_1_info[17], set_1_name, [], "")
                #                 st.area_chart(chart_data) 
                #             with tab2_line:
                #                 chart_data = createChart(set_1_info[17], set_1_name, [], "")
                #                 st.line_chart(chart_data)
                #             displayData = False
                # with tab2:
                #     st.dataframe(getPrices(originalResponse))

st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")
SetAnalyzer()