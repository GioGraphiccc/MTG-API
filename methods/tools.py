import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

from methods.collect_info import filterImages, AddKeywordsToDB, getCardsWithKeywords, GetCardTypes
from methods.database_methods import addSetToDB
from methods.Card import Card

def collectResponses(response, searchTerm):
    searchResults = {}
    if(response['object'] == 'list'):
        i = 0
        for card in response['data']:
            if searchTerm.lower() in card['name'].lower():
                card_name = card['name']
                i = i + 1
                searchResults.update({card_name:i})    
    return searchResults
    
def formatWord(response):
    list_response = []
    if type(response) == list:
        for item in response:
            list_response.append(formatWord(item))
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
    elif(response == "W"):
        return "White"
    elif(response == "U"):
        return "Blue"
    elif(response == "G"):
        return "Green"
    elif(response == "B"):
        return "Black"
    elif(response == "R"):
        return "Red"
    elif(response == "Multicolored"):
        return "Multicolored"
    elif(response == "ALL"):
        return ""
    elif('.' in response):
        return response.replace("$", "")
    formattedword = ""
    try:
        for color in response.strip("{}").split(","):
            formattedword = formattedword + formatWord(color) + ' '
        return formattedword
    except:
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

def imageView(cards, color, card_type, rarity, enlarge):
    #st.write(response)
    #st.write(color)
    filteredCards = filterImages(cards, color, card_type, rarity, enlarge)
    displayCardImages(filteredCards)

def parsePastedText(pastedText, baseUrl): #NEW
    pastedText = pastedText.strip()
    list_of_text = pastedText.split("\n")
    card_list = []
    set_name = ""
    collector_num = ""
    for line in list_of_text:
        if line.strip() in ["Commander", "Deck", ""]:
            continue 
        token_line = line.split(" ") #split the line into tokens. returned token array
        if token_line[0].isdigit(): #retieve the num of duplicates from the first token
            num_Duplicates = token_line[0] 
            del token_line[0] #delete the token since we saved it into a var already

        if len(token_line[len(token_line)-1]) > 1 and token_line[len(token_line)-1][0].isdigit(): #check if collector number is present by checking the first letter in the token
                collector_num = token_line[len(token_line)-1]
                token_line.remove(collector_num) #remove collector_num token from array

        for token in token_line: #loop through the token array, remove each token to leave only the name token remaining. 
            if "(" in token and ")" in token: #check to see if the set name is included in between parathensis
                temp = token
                set_name = token.strip("()")
                token_line.remove(temp) #remove set name token after saved in var set_name

        
        name = ' '.join(token_line)
        print(name)
        card_list.append([num_Duplicates, name, set_name, collector_num])
    return card_list

def getDataframePrices(data):
    card_NamePrice = {}
    total_cost = 0

    for i in range(len(data)):
        if(data[i][4] == None): #price
            price = None 
        else:
            price = {data[i][1]:float(data[i][4].replace("$",""))}

        if(data[i][5] == None): #foil price
                foil_price = None
        else:
            foil_price = {data[i][1]:float(data[i][5].replace("$",""))}

        if(price == None and foil_price == None):
            continue
        elif(price != None and foil_price == None):
            total_cost = total_cost + float(data[i][4].replace("$",""))
            card_NamePrice.update(price)
        elif(foil_price != None and price == None):
            total_cost = total_cost + float(data[i][5].replace("$",""))
            card_NamePrice.update(foil_price)
        elif(float(data[i][5].replace("$",""))) > float(data[i][4].replace("$","")):
            total_cost = total_cost + float(data[i][4].replace("$",""))
            card_NamePrice.update(price)
        else:
            total_cost = total_cost + float(data[i][5].replace("$",""))
            card_NamePrice.update(foil_price)

    return sorted(card_NamePrice.items(), key=lambda x:x[1], reverse= True), total_cost

def displayCardImages(cards):
    #st.write(card_images)
    replace = st.empty()
    replace.empty()
    if(cards == ['noimage']):
        return 0
    col1_images = []
    col2_images = []
    col3_images = []
    col4_images = []

    col1_prices = []
    col2_prices = []
    col3_prices = []
    col4_prices = []

    col1, col2, col3, col4 = st.columns(4)
    i = 0
    while True:
        if(i+4 > len(cards)):
            remaining = len(cards) - i
            if(remaining == 0):
                break
            if(remaining == 1):
                col1_images.append(cards[len(cards)-1].img_url)
                col1_prices.append(Card.getBestPrice(cards[len(cards)-1]))
                i = i + 1
                break
            elif(remaining == 2):
                col1_images.append(cards[i].img_url)
                col1_prices.append(Card.getBestPrice(cards[i]))
                col2_images.append(cards[i+1].img_url)
                col2_prices.append(Card.getBestPrice(cards[i+1]))
                
                i = i + 2
                break
            elif(remaining == 3):
                col1_images.append(cards[i].img_url)
                col1_prices.append(Card.getBestPrice(cards[i]))
                col2_images.append(cards[i+1].img_url)
                col2_prices.append(Card.getBestPrice(cards[i+1]))
                col3_images.append(cards[i+2].img_url) 
                col3_prices.append(Card.getBestPrice(cards[i+2])) 
                i = i + 3
                break  
        else:
            col1_images.append(cards[i].img_url)
            col1_prices.append(Card.getBestPrice(cards[i]))
            col2_images.append(cards[i+1].img_url)
            col2_prices.append(Card.getBestPrice(cards[i+1]))
            col3_images.append(cards[i+2].img_url)
            col3_prices.append(Card.getBestPrice(cards[i+2]))
            col4_images.append(cards[i+3].img_url)
            col4_prices.append(Card.getBestPrice(cards[i+3]))
            i = i + 4

    with replace:
        with col1:
            for i in range(len(col1_images)):
                if(col1_images[i].count("http") == 2):
                    st.image(col1_images[i][0:col1_images[i].find("http")-1], caption=col1_prices[i])
                else:
                    st.image(col1_images[i], caption=col1_prices[i])

        with col2:
            for i in range(len(col2_images)):
                if(col2_images[i].count("http") == 2):
                    st.image(col2_images[i][0:col2_images[i].find("http")-1], caption=col2_prices[i])
                else:
                    st.image(col2_images[i], caption=col2_prices[i])

        with col3:
            for i in range(len(col3_images)):
                if(col3_images[i].count("http") == 2):
                    st.image(col3_images[i][0:col3_images[i].find("http")-1], caption=col3_prices[i])
                else:
                    st.image(col3_images[i], caption=col3_prices[i])
        with col4:
            for i in range(len(col4_images)):
                if(col4_images[i].count("http") == 2):
                    st.image(col4_images[i][0:col4_images[i].find("http")-1], caption=col4_prices[i])
                else:
                    st.image(col4_images[i], caption=col4_prices[i])

def display_cards_info(info):
    st.write("total_cost Price of Set: $%.2f" % info[0])
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

    colors.update({"total_cost Price of Set": info[0]})
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

def display_images_price_stats(cards):
    imageTab, PriceTab, StatTab = st.tabs(["Cards Images", "Card List", "Set Statistics"])
    color = []
    card_type = []
    selected_color = []
    selected_card_type = {}
    submitted = False
    default = True
    enlarge = False
    with imageTab:
        color = []
        card_type = []
        rarity = []
        # selected_rarity = []
        # selected_color = []
        # selected_card_type = []
        col1, col2, col3 = st.columns(3)
        with col1:
            color = st.radio("Choose a color",
                            ("ALL", "Multicolored","White", "Blue", "Green", "Black", "Red"))
            if color == "ALL":
                color = []
            # if(st.button("Submit")):
            #     submitted = True
            #     selected_color = formatWord(selected_color)
            #     
            #     card_type = selected_card_type
            #     selected_color = ""
            #     selected_card_type = ""
            
        with col2:
            card_type = st.multiselect("Choose a card type.",
                                        ("Artifact", "Creature", "Enchantment", "Instant", "Sorcery", "Legendary"))
  

        with col3:
            rarity = st.multiselect("Choose a card Rarity.", 
                                                  ("Common", "Uncommon", "Rare", "Mythic"))


        
        st.write(color)

        imageView(cards,"", card_type, rarity, enlarge)

        st.divider()
        
        
        # if(submitted):
        #     
        #     submitted = False
        #     default = False
                
        # elif(default):
        #     imageView(cards, [], [], [], enlarge)
    
    

    with StatTab:
        API_keywords = []
        total_keywords = []
        detailed = False
        known_keywords = AddKeywordsToDB(cards)
        total_keywords = getCardsWithKeywords(cards, known_keywords)

        total_card_types = GetCardTypes(cards, detailed)

        if not detailed:
            total_keywords = {key: value for key, value in total_keywords.items() if value != 1} #remove items with value 1
        total_keywords = dict(sorted(total_keywords.items(), key=lambda item: item[1], reverse=True))

        total_card_types = dict(sorted(total_card_types.items(), key=lambda item: item[1], reverse=True))

        #st.write(total_keywords)
        #st.write(total_card_types)


        col1_metric, col2_metric, col3_metric, col4_metric = st.columns(4, gap="small")
        col1, col2 = createTable(total_keywords)
        col1_metric.table({"Keywords":col1, "#":col2})

        col1, col2 = createTable(total_card_types)
        col2_metric.table({"Types":col1, "#":col2})
        


    with PriceTab:
        st.write("WIP")
        col1, col2 = st.columns(2)
        with col1:
            print()
            # price_df, total_cost_cost = getDataframePrices(response)
            # st.dataframe(price_df)
            # st.write("total_cost: " + str(total_cost_cost))

def createTable(dataset):
    col1 = []
    col2 = []
    if type(dataset) == dict:
        for data in dataset:
            col1.append(data)
            col2.append(dataset[data])
    return col1, col2

def displayColors(colors):
    color_imgs = []
    for color in colors:
        if color == "W":
            color_imgs.append("templates/white.png")
        elif color == "U":
            color_imgs.append("templates/blue.png")
        elif color == "B":
            color_imgs.append("templates/black.png")
        elif color == "R":
            color_imgs.append("templates/red.png")
        elif color == "G":
            color_imgs.append("templates/green.png")

