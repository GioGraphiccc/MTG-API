import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from streamlit_image_select import image_select
from methods.collect_info import AddKeywordsToDB, getCardsWithKeywords, GetCardTypes
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

def imageView(cards, colors, card_type, rarity, enlarge, priceSort):
    #st.write(response)
    #st.write(colors)
    filteredCards = filterImages(cards, colors, card_type, rarity, enlarge, priceSort)
    displayCardImages(filteredCards)

def filterImages(cards, colors, card_types, rarities, enlarge, priceSort):
    if(colors):
        temp = []
        for color in colors:
            temp.append(formatWord(color))
        colors = temp
    color_sorted_cards = []
    rarity_sorted_cards = []
    card_type_sorted_cards = []
    sorted_cards = []
    type_sorted_cards = []
    multicolored_sorted_cards = []
    
    if not colors and not card_types and not rarities:
        st.write("No Filter Selected.")
        return SortCardsByPrice(cards)
    
    if "Gray" in colors:
        st.write("Gray Filter Selected.")
        colors.remove("Gray")
        for card in cards:
            if len(card.colors) == 0:
                sorted_cards.append(card)
    else:
        sorted_cards = cards

    if "Multicolored" in colors:
        st.write("Multicolored Filter Selected")
        colors.remove("Multicolored")
        for card in sorted_cards:
            if sum(1 for char in card.colors if char.isalpha()) > 1:
                multicolored_sorted_cards.append(card)
        sorted_cards = multicolored_sorted_cards

    #CARDS THAT CONTAIN ANY ONE OF THE SELECTED COLORS
    # if colors:
    #     st.write("Other Color Filter Selected.")
    #     for color in colors:
    #         for card in sorted_cards:    
    #             for card_color in card.colors:
    #                 if formatWord(color) == card_color:
    #                     color_sorted_cards.append(card)
    
    #CARDS THAT CONTAIN ALL OF THE SELECTED COLORS
    if colors:
        st.write(colors)
        for card in sorted_cards:    
            if len(list(set(colors) & set(card.colors))) == len(colors):
                color_sorted_cards.append(card)
        sorted_cards = color_sorted_cards

    if card_types:                                 #Card Type Sort
        st.write("Card Type Filter Selected.")

        for card_type in card_types:
            for card in sorted_cards:
                if card_type in card.card_type:
                    card_type_sorted_cards.append(card)
        sorted_cards = card_type_sorted_cards
        
    if rarities:                                  #Rarity Sort
        st.write("Rarity Filter Selected.")
        if not sorted_cards:
            sorted_cards = cards
        for rarity in rarities:
            for card in sorted_cards:
                if rarity in card.rarity:
                    rarity_sorted_cards.append(card)
        sorted_cards = rarity_sorted_cards
      
    if(priceSort):                                #Price Sort
        sorted_cards = SortCardsByPrice(sorted_cards)
    return sorted_cards
    


def SortCardsByPrice(cards):
    noPriceCards = []
    card_price_dict = {}
    sorted_cards = []
    for card in cards:
        if(Card.getBestPrice(card) == "N/A"):
            noPriceCards.append(card)
            continue
        card_price = Card.getBestPrice(card)
        #print(card_price.strip("$"))
        card_price_dict.update({card:card_price.strip("$")})

    card_price_dict = dict(sorted(card_price_dict.items(), key=lambda item: item[1]))
                
   
    for card_price in card_price_dict:
        print(card_price.card_name + ": " + str(Card.getBestPrice(card_price)))
        sorted_cards.append(card_price)

    sorted_cards.reverse()

    for noPrice_card in noPriceCards:
        sorted_cards.append(noPrice_card)

    return sorted_cards

    # price_sorted = []
    # NoPriceCards = []
    # temp = []
    # maxNumCards = len(cards)
    # for card in cards:
        
    #     cardPrice = Card.getBestPrice(card)
    #     sorted_card_index = 0

    #     if(cardPrice == "N/A"):
    #         NoPriceCards.append(card)
    #         cards.remove(card)
    #         continue

    #     elif(len(price_sorted) == 0):
    #         price_sorted.append(card)

    #     elif(Card.getBestPrice(price_sorted[len(price_sorted)-1]) < Card.getBestPrice(card)):
    #         price_sorted.append(card)
    #         sorted_card_index += 1

    #     elif(Card.getBestPrice(price_sorted[0]) > Card.getBestPrice(card)):
    #         price_sorted.insert(0, card)
        
    #     for sorted_card in price_sorted:
    #         sorted_card_price = Card.getBestPrice(sorted_card)

    #         if(sorted_card_index == maxNumCards):
    #             break
    #         if(sorted_card_price >= cardPrice and not(sorted_card.card_name == card.card_name)):
    #             price_sorted.insert(sorted_card_index, card)
    #             print(Card.getBestPrice(card) + " " + str(sorted_card_index) + " " + str(len(price_sorted)))
    #             sorted_card_index += 1
    #             continue
            
            
        # if(sorted_card_index == maxNumCards):
        #     break


            

    # file = open("methods\pricelist.txt", "w")       
    # file.write(Card.getBestPrice(card) + "\n")
    

        
    # file.close()

    # return price_sorted
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
        #print(name)
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
    #st.write(cards)
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

    col1_uri = []
    col2_uri = []
    col3_uri = []
    col4_uri = []

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
                col1_uri.append(cards[len(cards)-1].uri)
                i = i + 1
                break
            elif(remaining == 2):
                col1_images.append(cards[i].img_url)
                col1_prices.append(Card.getBestPrice(cards[i]))
                col1_uri.append(cards[i].uri)

                col2_images.append(cards[i+1].img_url)
                col2_prices.append(Card.getBestPrice(cards[i+1]))
                col2_uri.append(cards[i+1].uri)
                i = i + 2
                break
            elif(remaining == 3):
                col1_images.append(cards[i].img_url)
                col1_prices.append(Card.getBestPrice(cards[i]))
                col1_uri.append(cards[i].uri)

                col2_images.append(cards[i+1].img_url)
                col2_prices.append(Card.getBestPrice(cards[i+1]))
                col2_uri.append(cards[i+1].uri)

                col3_images.append(cards[i+2].img_url) 
                col3_prices.append(Card.getBestPrice(cards[i+2])) 
                col3_uri.append(cards[i+2].uri)
                i = i + 3
                break  
        else:
            col1_images.append(cards[i].img_url)
            col1_prices.append(Card.getBestPrice(cards[i]))
            col1_uri.append(cards[i].uri)

            col2_images.append(cards[i+1].img_url)
            col2_prices.append(Card.getBestPrice(cards[i+1]))
            col2_uri.append(cards[i+1].uri)

            col3_images.append(cards[i+2].img_url)
            col3_prices.append(Card.getBestPrice(cards[i+2]))
            col3_uri.append(cards[i+2].uri)

            col4_images.append(cards[i+3].img_url)
            col4_prices.append(Card.getBestPrice(cards[i+3]))
            col4_uri.append(cards[i+3].uri)

            i = i + 4

    with replace:
        with col1:
            for i in range(len(col1_images)):
                if(col1_images[i].count("http") == 2):
                    st.image(col1_images[i][0:col1_images[i].find("http")-1], caption=col1_prices[i])
                    st.button("View Card",key=col1_uri[i], use_container_width=True)
                else:
                    st.image(col1_images[i], caption=col1_prices[i])
                    st.button("View Card",key=col1_uri[i], use_container_width=True)

        with col2:
            for i in range(len(col2_images)):
                if(col2_images[i].count("http") == 2):
                    st.image(col2_images[i][0:col2_images[i].find("http")-1], caption=col2_prices[i])
                    st.button("View Card",key=col2_uri[i], use_container_width=True)
                else:
                    st.image(col2_images[i], caption=col2_prices[i])
                    st.button("View Card",key=col2_uri[i], use_container_width=True)

        with col3:
            for i in range(len(col3_images)):
                if(col3_images[i].count("http") == 2):
                    st.image(col3_images[i][0:col3_images[i].find("http")-1], caption=col3_prices[i])
                    st.button("View Card",key=col3_uri[i], use_container_width=True)
                else:
                    st.image(col3_images[i], caption=col3_prices[i])
                    st.button("View Card",key=col3_uri[i], use_container_width=True)
        with col4:
            for i in range(len(col4_images)):
                if(col4_images[i].count("http") == 2):
                    st.image(col4_images[i][0:col4_images[i].find("http")-1], caption=col4_prices[i])
                    st.button("View Card",key=col4_uri[i], use_container_width=True)
                else:
                    st.image(col4_images[i], caption=col4_prices[i])
                    st.button("View Card",key=col4_uri[i], use_container_width=True)

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
        #colors = []
        card_type = []
        rarity = []
        # selected_rarity = []
        # selected_color = []
        # selected_card_type = []
        col1, col2, col3 = st.columns(3)
        with col1:
            colors = st.multiselect("Choose a color",
                            ("Gray", "Multicolored","White", "Blue", "Green", "Black", "Red"))       
        with col2:
            card_type = st.multiselect("Choose a card type.",
                                        ("Artifact", "Creature", "Enchantment", "Instant", "Sorcery", "Legendary"))
        with col3:
            rarity = st.multiselect("Choose a card Rarity.", 
                                                  ("Common", "Uncommon", "Rare", "Mythic"))
            
        #st.button("Sort By Price")
        priceSort = True
        imageView(cards, colors, card_type, rarity, enlarge, priceSort)

        st.divider()   

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
def displaySetPreviews(selected_set_type):
    placeholder = st.empty()
    with placeholder.container():
        st.image("templates\Murders_At_Karlov_Manor.jpg")
        st.image("templates\Fallout.png")
    return placeholder

def fetchSetCards(selected_set, results, baseUrl):
    url = baseUrl + "/sets/" + results[selected_set]
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

    while cardlist_response["has_more"]:
        if(cardlist_response["has_more"]):
            cardlist_response = requests.get(cardlist_response['next_page']).json()
            for card in cardlist_response["data"]:
                Card_Set.append(Card.setCardInformation(card))
        if not cardlist_response["has_more"]:
            break
    return Card_Set

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

def addSetNamesToFile(results):
    file = open("methods\Set_Names.txt", "r")
    set_list = file.read().split("\n")
    file.close()
    

    file = open("methods\Set_Names.txt", "a")
    for set_name in results:
        if set_name in set_list:
            continue
        else:
            file.write(set_name + "\n")
    file.close()

