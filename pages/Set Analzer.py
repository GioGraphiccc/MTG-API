import streamlit as st
import datetime
import requests

from methods.display_info import displaySetCardImages, display_cards_info
from methods.collect_info import getPrices, getImages, getInformation, SearchSets
from methods.tools import formatWord, createChart


def imageView(response, color, card_type, enlarge):
    firstpage, secondpage = st.tabs(["1", "2"])
    with firstpage:
        cardImagesOfSet = getImages(response,color, card_type, enlarge)
        if(displaySetCardImages(cardImagesOfSet) == 0):
            st.error("Could not get images of cards for some reason.")
    with secondpage:
        try:
            next_page = response['next_page']
        except:
            next_page = ""
        if(next_page != ""):
            response = requests.get(next_page).json()
            cardImagesOfSet = getImages(response,color, card_type, enlarge)
            if(displaySetCardImages(cardImagesOfSet) == 0):
                st.error("Could not get images of cards for some reason.")
        else:
            st.error("No more cards from this set :(")

def SetAnalyzer():
    baseUrl = "https://api.scryfall.com"
    typesOfSets = ("Commander", "Expansion", "Masters", "Alchemy", "Starters", "Core", "Arsenal", "Funny")
    #col1, col2 = st.columns(2)
    #with col1:
    date = st.date_input("Sets made before... ", datetime.date.today())
    #with col2:
    selected_set_type = st.selectbox('Type of sets', typesOfSets)
    if(selected_set_type):
        search = ""
        search = st.text_input("Enter set name")
        if(search != ""):
            option = ""
            url = baseUrl + "/sets"
            response = requests.get(url).json()
            results = SearchSets(response, search, selected_set_type, date)
            if results:
                option = st.selectbox('Results',results, key=1)
            else:
                st.error("Set doesnt exist!")
            if(option != ""):
                url = baseUrl + "/sets/" + results[option]
                set_response = requests.get(url).json()
                st.write(set_response)                                      #DEBUG LINE
                st.divider()
                
                set_name = set_response['name']
                st.header(set_name)
                numCardsInSet = str(set_response['card_count'])
                release_date = set_response['released_at']
                st.image(set_response['icon_svg_uri'])

                url = set_response['search_uri']
                response = requests.get(url).json()
                st.write(response)                                          #DEBUG LINE
    
                tab1, tab2, tab3 = st.tabs(["Cards Images", "Card List", "Set Statistics"])
                color = []
                card_type = []
                selected_color = []
                selected_card_type = {}
                submitted = False
                default = True
                enlarge = False
                with tab1:
                    
                    selected_color = []
                    selected_card_type = []
                    col1, col2 = st.columns(2)
                    with col1:
                        selected_color = st.radio("Choose a color",
                                        ("ALL", "Multicolored","White", "Blue", "Green", "Black", "Red"))
                        
                    with col2:
                        
                        selected_card_type = st.multiselect("Choose a card type.",
                                                   ("Artifact", "Creature", "Enchantment", "Instant", "Sorcery"))
                        if(st.button("Submit")):
                            submitted = True
                            selected_color = formatWord(selected_color)
                            color = selected_color
                            card_type = selected_card_type
                            selected_color = ""
                            selected_card_type = ""
                if(submitted):
                    imageView(response, color, card_type, enlarge)
                    submitted = False
                    default = False
                     
                elif(default):
                    imageView(response, [], [], enlarge)
                
                originalResponse = response
                with tab3:
                    set_1_name = set_name
                    set_1_info = getInformation(response)

                    display_cards_info(set_1_info)

                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("Release Date: " + release_date)
                        st.write("Number of Cards:  " + numCardsInSet)
                    
                    with col2:
                        set_2_name = ""
                        displayData = True
                        search_compare = ""
                        search_compare = st.text_input("Compare prices with another set.")
                        if(search_compare != ""):
                            option_compare = ""
                            url = baseUrl + "/sets"
                            response = requests.get(url).json()
                            results_compare = SearchSets(response, search_compare, selected_set_type, datetime.date.today())
                            if results_compare:
                                option_compare = st.selectbox('Results',results_compare, key=3)
                            if(option_compare != ""):
                                url = baseUrl + "/sets/" + results_compare[option_compare]
                                set_response_compare = requests.get(url).json() #root set info
                                set_2_name = set_response_compare['name']
                                url = set_response_compare['search_uri']
                                response_compare = requests.get(url).json() #card data from set
                    if(st.button("Submit", key=4)):
                        displayData = True
                        if(set_2_name != ""):
                            st.success("Comparing prices with " + set_2_name)
                            set_2_info = getInformation(response_compare)
                        else:
                            st.success("Displaying Prices for " + set_1_name)
                    tab1_area, tab2_line = st.tabs(["Area", "Line"])
                    if(displayData):
                        if(set_2_name != ""):
                            with tab1_area:
                                chart_data = createChart(set_1_info[17], set_1_name, set_2_info[17], set_2_name)
                                st.area_chart(chart_data) 
                            with tab2_line:
                                chart_data = createChart(set_1_info[17], set_1_name, set_2_info[17], set_2_name)
                                st.line_chart(chart_data)
                            displayData = False
                        else:
                            with tab1_area:
                                chart_data = createChart(set_1_info[17], set_1_name, [], "")
                                st.area_chart(chart_data) 
                            with tab2_line:
                                chart_data = createChart(set_1_info[17], set_1_name, [], "")
                                st.line_chart(chart_data)
                            displayData = False
                with tab2:
                    st.dataframe(getPrices(originalResponse))

st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")
SetAnalyzer()