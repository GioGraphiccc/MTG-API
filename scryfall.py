#from mtgsdk import Card, set
import streamlit as st
import requests
import pandas as pd
#import numpy as np
import datetime

def collectResponses(response):
    try: 
        total_cards = response['total_cards']
    except:
        st.error("No cards with that search.")
        return
    results = response['data']
    searchResults = {}
    for i in range(total_cards):
        card_name = results[i]['name']
        card_id = results[i]['id']
        searchResults.update({card_name:card_id})
    return searchResults
    
def formatWord(response):
    if type(response) == list:
        list_response = []
        for i in range(len(response)):
            list_response.append(formatWord(response[i]))
        return list_response
    if(response == "not_legal"):
        return "Not Legal"
    elif(response == "legal"):
        return "Legal"
    elif(response == "White"):
        return "W"
    elif(response == "Blue"):
        return "U"
    elif(response == "Green"):
        return "G"
    elif(response == "Black"):
        return "B"
    elif(response == "Red"):
        return "R"
    elif(response == "Multicolored"):
        return "Multicolored"
    elif(response == "ALL"):
        return ""
    return ""

def CardAnalyzer():    
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
                 

def SearchSets(response, search, set_type, date):
    data = response['data']
    setNamesandID = {}
    for i in range(len(data)):
        if (search in data[i]['name'] or search in data[i]['name'].lower()):
            if(data[i]['set_type'] == set_type.lower() and datetime.datetime.strptime(data[i]['released_at'],'%Y-%m-%d').date() < date):
               set_name = data[i]['name']
               set_id = data[i]['id']
               setNamesandID.update({set_name:set_id})
    return setNamesandID

def obtainInformationOfSet(response):
    cards_data = response['data']
    totalPrice = 0
    listOfPrices = []

    numWhiteCards = 0
    numBlueCards = 0
    numGreenCards = 0
    numBlackCards = 0
    numRedCards = 0
    numMulticolored = 0
    
    numCreatures = 0
    numInstants = 0
    numSorceries = 0
    numEnchantments = 0
    numArifacts = 0
     
    oneManaCards = 0
    twoManaCards = 0
    threeManaCards = 0
    fourManaCards = 0
    fiveManaCards = 0
    sixOrMoreManaCards = 0 

    for i in range(len(cards_data)):
        price_of_card = cards_data[i]['prices']['usd']
        if(price_of_card):
            listOfPrices.append(price_of_card)
            totalPrice = totalPrice + float(price_of_card)
            
        if(len(cards_data[i]['color_identity']) != 0):
            for color in cards_data[i]['color_identity']:
                # color = cards_data[i]['colors'][0]
                if(color == "W"):
                    numWhiteCards = numWhiteCards + 1
                if(color == "U"):
                    numBlueCards = numBlueCards + 1
                if(color == "G"):
                    numGreenCards = numGreenCards + 1
                if(color == "B"):
                    numBlackCards = numBlackCards + 1
                if(color == "R"):
                    numRedCards = numRedCards + 1
            else:
                numMulticolored = numMulticolored + 1

        cardType = cards_data[i]['type_line']
        if "Creature" in cardType :
            numCreatures = numCreatures + 1
        if "Instant" in cardType:
            numInstants = numInstants + 1
        if "Sorcery" in cardType:
            numSorceries = numSorceries + 1
        if "Enchantment" in cardType:
            numEnchantments = numEnchantments + 1
        if "Artifact" in cardType:
            numArifacts = numArifacts + 1
        
        manaCost = cards_data[i]['cmc']
        if(manaCost and manaCost == 1):
            oneManaCards = oneManaCards + 1
        if(manaCost and manaCost == 2):
            twoManaCards = twoManaCards + 1
        if(manaCost and manaCost == 3):
            threeManaCards = threeManaCards + 1
        if(manaCost and manaCost == 4):
            fourManaCards = fourManaCards + 1
        if(manaCost and manaCost == 5):
            fiveManaCards = fiveManaCards + 1
        if(manaCost and manaCost >= 6):
            sixOrMoreManaCards = sixOrMoreManaCards + 1
    info = [totalPrice,                                                                                     #0
            numWhiteCards, numBlueCards, numGreenCards, numBlackCards, numRedCards,                         #1-5
            numCreatures, numInstants, numSorceries, numEnchantments, numArifacts,                          #6-10
            oneManaCards, twoManaCards, threeManaCards, fourManaCards, fiveManaCards, sixOrMoreManaCards,   #11-16
            listOfPrices]                                                                                   #17             
    return  info


def obtainImagesOfSet(dataset_1, dataset_2, color, card_type, enlarge):
    cardImages = []
    colorSortedImages = []
    cards_data = []

    try:
        enlarge = True
        if(enlarge):
            for data in dataset_1:
                cards_data.append({'img_type_color':(data['image_uris']['large'], data['type_line'], data['colors'])})
            
            for data in dataset_2:
                cards_data.append({'img_type_color':(data['image_uris']['large'], data['type_line'], data['colors'])})
        # else:
        #     for data in dataset_1:
        #         cards_data.append({'img_type_color':(data['image_uris']['small'], data['type_line'], data['colors'])})
            
        #     for data in dataset_2:
        #         cards_data.append({'img_type_color':(data['image_uris']['small'], data['type_line'], data['colors'])})
    except:
        st.error("Error: It appears that this set does not contain images.")
        return ['noimage']

    if(len(color) != 0): #if color
        for i in range(len(cards_data)): #first, create colorSortedImages list with line types and color
            for col in cards_data[i]['img_type_color'][2]:

                if(color in col):
                    colorSortedImages.append(cards_data[i])

        if(len(color) != 0 and len(card_type) == 0): #if color not type

            return colorSortedImages
        
        else: #if color and type
            for i in range(len(colorSortedImages)):
                for types in card_type:
                    if(types in colorSortedImages[i]['img_type_color'][1]):
                            cardImages.append(colorSortedImages[i])

    else: #if not color
        if(len(card_type) == 0): #neither color or type
            return cards_data
        
        else: #if not color but type
            for types in card_type:
                for i in range(len(cards_data)):
                    if(types in cards_data[i]['img_type_color'][1]):
                        cardImages.append(cards_data[i])

    return cardImages

def displaySetCardImages(response, color, card_type, enlarge):
    replace = st.empty()
    replace.empty()
    cardImagesOfSet = {}
    cardImagesOfSet = obtainImagesOfSet(response['data'],{},color, card_type, enlarge)
    if(cardImagesOfSet[0] == 'noimage'):
        return
    col1_images = []
    col2_images = []
    col3_images = []
    col4_images = []
    
    col1, col2, col3, col4 = st.columns(4)
    i = 0
    while True:
        if(i+4 > len(cardImagesOfSet)):
            remaining = len(cardImagesOfSet) - i
            if(remaining == 1):
                col1_images.append(cardImagesOfSet[len(cardImagesOfSet)-1]['img_type_color'][0])
                i = i + 1
                break
            elif(remaining == 2):
                col1_images.append(cardImagesOfSet[i]['img_type_color'][0])
                col2_images.append(cardImagesOfSet[i+1]['img_type_color'][0])
                i = i + 2
                break
            elif(remaining == 3):
                col1_images.append(cardImagesOfSet[i]['img_type_color'][0])
                col2_images.append(cardImagesOfSet[i+1]['img_type_color'][0])
                col3_images.append(cardImagesOfSet[i+2]['img_type_color'][0]) 
                i = i + 3
                break  
        else:
            col1_images.append(cardImagesOfSet[i]['img_type_color'][0])
            col2_images.append(cardImagesOfSet[i+1]['img_type_color'][0])
            col3_images.append(cardImagesOfSet[i+2]['img_type_color'][0])
            col4_images.append(cardImagesOfSet[i+3]['img_type_color'][0])
            i = i + 4

    with replace:
        with col1:
            for image in col1_images:
                st.image(image)

        with col2:
            for image in col2_images:
                st.image(image)

        with col3:
            for image in col3_images:
                st.image(image)

        with col4:
            for image in col4_images:
                st.image(image)

def createChart(data1, data_1_name, data2, data_2_name):
    data_1_sorted = []
    data_2_sorted = []
    if(data_2_name == ""):
        for i in range(len(data1)):
            data_1_sorted.append(float(data1[i]))
        data_1_sorted = sorted(data_1_sorted)
        chart_data = pd.DataFrame({data_1_name:data_1_sorted})
    else:
        smallest = len(data1)
        if(len(data2) < smallest):
            smallest = len(data2)
        for i in range(smallest):
            data_1_sorted.append(float(data1[i]))
            data_2_sorted.append(float(data2[i]))
        data_1_sorted = sorted(data_1_sorted)
        data_2_sorted = sorted(data_2_sorted)
        chart_data = pd.DataFrame({data_1_name:data_1_sorted, data_2_name:data_2_sorted})
    return chart_data

def getCardListWithPrices(response):
    data = response['data']
    card_NamePrice = {}
    for i in range(len(data)):
        if(data[i]['prices']['usd'] == None):
            if(data[i]['prices']['usd_foil']== None):
                card_NamePrice.update({data[i]['name']:-1})
            else:
                card_NamePrice.update({data[i]['name']:float(data[i]['prices']['usd_foil'])})
        else:
            card_NamePrice.update({data[i]['name']:float(data[i]['prices']['usd'])})
    return sorted(card_NamePrice.items(), key=lambda x:x[1])

def SetAnalyzer():
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
                enlarge = False
                with tab1:
                    
                    selected_color = []
                    selected_card_type = []
                    col1, col2 = st.columns(2)
                    submitted = False
                    with col1:
                        selected_color = st.radio("Choose a color",
                                        ("ALL", "Multicolored","White", "Blue", "Green", "Black", "Red"))
                        selected_color = formatWord(selected_color)
                    with col2:
                        
                        selected_card_type = st.multiselect("Choose a card type.",
                                                   ("Artifact", "Creature", "Enchantment", "Instant", "Sorcery"))
                        if(not submitted):
                            if(st.button("Submit")):
                                color = selected_color
                                card_type = selected_card_type
                                selected_color = ""
                                selected_card_type = ""
                                submitted = True
                        
                    originalResponse = response
                    top_button = st.empty()
                    pagenum = 0

                    try:
                        next_page = response['next_page']
                    except:
                        next_page = ""
                    #col1_nextpage, col2_enlarge = st.columns(2)

                    #with col1_nextpage:
                    if(top_button.button("Next Page", key=11)):
                        response = requests.get(next_page).json()
                        pagenum = pagenum + 1
                        top_button.empty()
                        displaySetCardImages(response, color, card_type, enlarge)


                    # with col2_enlarge:
                    #     if(st.checkbox("Enlarge (WIP)")):
                    #         enlarge = True
                    #     else:
                    #         enlarge = False

                    if(pagenum > 0):
                        if(top_button.button("Previous Page")):
                            response = requests.get(originalResponse).json()
 
                    displaySetCardImages(response, color, card_type, enlarge)
                    bottom_button = st.empty()
                    if(bottom_button.button("Next Page", key=2)):
                        response = requests.get(next_page).json()
                        pagenum = pagenum + 1
                        displaySetCardImages(response, color, card_type, enlarge)

                    if(pagenum > 0):
                        if(bottom_button.button("Previous Page")):
                            response = requests.get(originalResponse).json()

                    submitted = False
                with tab3:
                    set_1_name = set_name
                    set_1_info = obtainInformationOfSet(response)

                    st.write("Total Price of Set: $%.2f" % set_1_info[0])
                    # st.write("numWhiteCards: " + str(set_1_info[1]))
                    # st.write("numBlueCards: "+ str(set_1_info[2]))
                    # st.write("numGreenCards: " + str(set_1_info[3]))
                    # st.write("numBlackCards: " + str(set_1_info[4]))
                    # st.write("numRedCards: " + str(set_1_info[5]))
                    st.write("Number of Creatures: " + str(set_1_info[6]))
                    st.write("Number of Instants: " + str(set_1_info[7]))
                    st.write("Number of Sorceries: " + str(set_1_info[8]))
                    st.write("Number of Enchantments: " + str(set_1_info[9]))
                    st.write("Number of Arifacts: " + str(set_1_info[10]))
                    # st.write("oneManaCards: " + str(set_1_info[11]))
                    # st.write("twoManaCards: " + str(set_1_info[12]))
                    # st.write("threeManaCards: " + str(set_1_info[13]))
                    # st.write("fourManaCards: " + str(set_1_info[14]))
                    # st.write("fiveManaCards: " + str(set_1_info[15]))
                    # st.write("sixOrMoreManaCards: " + str(set_1_info[16]))
                    # st.write("List of card prices: " + str(set_1_info[17]))
                    #st.write(response)

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
                            set_2_info = obtainInformationOfSet(response_compare)
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
                    st.dataframe(getCardListWithPrices(originalResponse))


baseUrl = "https://api.scryfall.com"
st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Card and Set Analyzer - Scryfall API")

tab1, tab2 = st.tabs(["Card", "Set"])
with tab1: 
    CardAnalyzer()
with tab2:
    SetAnalyzer()
st.divider()
#end of Main
