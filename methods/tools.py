import streamlit as st
import pandas as pd
import requests

from methods.collect_info import getImages, getInformation

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

def imageView(response, color, card_type, enlarge):
    #st.write(response)
    firstpage, secondpage = st.tabs(["1", "2"])
    with firstpage:
        cardImagesOfSet = getImages(response,color, card_type, enlarge)
        displayCardImages(cardImagesOfSet)
    with secondpage:
        try:
            next_page = response['next_page']
        except:
            next_page = ""
        if(next_page != ""):
            response = requests.get(next_page).json()
            cardImagesOfSet = getImages(response,color, card_type, enlarge)
            if(displayCardImages(cardImagesOfSet) == 0):
                st.error("Could not get images of cards for some reason.")
        else:
            st.error("No more cards from this set :(")

def parsePastedText(pastedText, baseUrl):
    list_of_text = pastedText.split("\n")
    card_list = []
    for line in list_of_text:
        numOfSpacesInLine = line.count(" ")
        if(numOfSpacesInLine == 3):
            numOfDuplicates, name, set_name, collector_number = line.split(" ")
        else:
            info = line.split(" ")
            collector_number = info.pop(len(info)-1)
            set_name = info.pop(len(info)-1)
            numOfDuplicates = info.pop(0)
            name = ' '.join(info)
        url = baseUrl + "/cards/" + set_name.strip("()") + "/" + str(collector_number)
        response = requests.get(url).json()
        card_list.append(response)

    return card_list

def getDataframePrices(response):
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

def displayCardImages(card_images):
    #st.write(card_images)
    replace = st.empty()
    replace.empty()
    if(card_images == 'noimage'):
        return 0
    col1_images = []
    col2_images = []
    col3_images = []
    col4_images = []
    col1, col2, col3, col4 = st.columns(4)
    i = 0
    while True and i < 8:
        if(i+4 > len(card_images)):
            remaining = len(card_images) - i
            if(remaining == 1):
                col1_images.append(card_images[len(card_images)-1]['img_type_color'][0])
                i = i + 1
                break
            elif(remaining == 2):
                col1_images.append(card_images[i]['img_type_color'][0])
                col2_images.append(card_images[i+1]['img_type_color'][0])
                i = i + 2
                break
            elif(remaining == 3):
                col1_images.append(card_images[i]['img_type_color'][0])
                col2_images.append(card_images[i+1]['img_type_color'][0])
                col3_images.append(card_images[i+2]['img_type_color'][0]) 
                i = i + 3
                break  
        else:
            col1_images.append(card_images[i]['img_type_color'][0])
            col2_images.append(card_images[i+1]['img_type_color'][0])
            col3_images.append(card_images[i+2]['img_type_color'][0])
            col4_images.append(card_images[i+3]['img_type_color'][0])
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

def display_cards_info(info):
    st.write("Total Price of Set: $%.2f" % info[0])
    st.write("WhiteCards: " + str(info[1]))
    st.write("BlueCards: "+ str(info[2]))
    st.write("GreenCards: " + str(info[3]))
    st.write("BlackCards: " + str(info[4]))
    st.write("RedCards: " + str(info[5]))
    st.write("Number of Creatures: " + str(info[6]))
    st.write("Number of Instants: " + str(info[7]))
    st.write("Number of Sorceries: " + str(info[8]))
    st.write("Number of Enchantments: " + str(info[9]))
    st.write("Number of Arifacts: " + str(info[10]))
    st.write("1 ManaCards: " + str(info[11]))
    st.write("2 ManaCards: " + str(info[12]))
    st.write("3 ManaCards: " + str(info[13]))
    st.write("4 ManaCards: " + str(info[14]))
    st.write("5 ManaCards: " + str(info[15]))
    st.write("6 or more ManaCards: " + str(info[16]))
    #st.write("List of card prices: " + str(info[17]))
    #st.write(response)

def convert_cards_info_to_Dataframe(info):
    colors = {}
    types = {}
    costs = {}

    colors.update({"Total Price of Set": info[0]})
    if(info[1] > 0):
        colors.update({"White Cards ": info[1]})
    if(info[2] > 0):
        colors.update({"Blue Cards " :info[2]})
    if(info[3] > 0):
        colors.update({"Green Cards " : info[3]})
    if(info[4] > 0):
        colors.update({"Black Cards " : info[4]})
    if(info[5] > 0):
        colors.update({"Red Cards " : info[5]})

    types.update({"Creatures": info[6]})
    types.update({"Instants" : info[7]})
    types.update({"Sorceries" : info[8]})
    types.update({"Enchantments" : info[9]})
    types.update({"Arifacts" : info[10]})

    costs.update({"1 ManaCards" : info[11]})
    costs.update({"2 ManaCards" : info[12]})
    costs.update({"3 ManaCards" : info[13]})
    costs.update({"4 ManaCards" : info[14]})
    costs.update({"5 ManaCards" : info[15]})

    costs.update({"6 or more ManaCards":info[16]})

    #st.write("List of card prices: " + str(info[17]))
    #st.write(response)
    return colors, types, costs
def display_images_price_stats(response):

    imageTab, PriceTab, StatTab = st.tabs(["Cards Images", "Card List", "Set Statistics"])
    color = []
    card_type = []
    selected_color = []
    selected_card_type = {}
    submitted = False
    default = True
    enlarge = False
    with imageTab:
        
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
    info = getInformation(response)
    colors_df, types_df, costs_df,  = convert_cards_info_to_Dataframe(info)

    with PriceTab:
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(getDataframePrices(response))



