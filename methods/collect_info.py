import streamlit as st
import datetime
import requests

# def getCardInformation(response):
#     #st.write(response)
#     colors = []
#     if 'card_faces' in response:
#         try:
#             colors.append(str(response['card_faces'][0]['colors'])) #collect each char and add to a new array
#             colors.append("/")
#             colors.append(str(response['card_faces'][1]['colors']))
#         except:
#             colors.append(str(response['colors']))

#         mana_cost = response['card_faces'][0]['mana_cost']
#         try:
#             img_url = response['card_faces'][0]['image_uris']['normal']
#             img_url = img_url + "/" + response['card_faces'][1]['image_uris']['normal']
#         except:
#             img_url = response['image_uris']['normal']
#     else:
#         colors = response['colors']
#         mana_cost = response['mana_cost']
#         img_url = response['image_uris']['normal'] 

#     id = response['id']
#     card_name = response['name']
#     card_type = response['type_line']
#     set_name  = response['set_name']                                  
#     keywords = response['keywords']
#     price = response['prices']['usd']               
#     priceF = response['prices']['usd_foil']      
#     rarity = response['rarity']                    
#     cmc = response['cmc']                         
     
#     legalityS = response['legalities']['standard'] 
#     legalityC = response['legalities']['commander']
#     try:             
#         power_toughness = response['power'] + '/' + response['toughness']
#     except:
#         power_toughness = "N/A"
    
#     try:
#         tcgplayer_id = response['tcgplayer_id']
#     except KeyError:
#         tcgplayer_id = "N/A"
    
    
#     info = [id, card_name, card_type, set_name,  price, priceF, rarity, colors, keywords,
#              cmc, mana_cost, legalityS, legalityC, power_toughness, tcgplayer_id, img_url]
#     return info

def filterImages(cards, color, card_types, rarity, enlarge):
    color_sorted_cards = []
    sorted_cards = []
    type_sorted_cards = []
    
    if not color and not card_types:
        return cards

    if color == "Multicolored":
        for card in cards:
            if sum(1 for char in card.colors if char.isalpha()) > 1:
                color_sorted_cards.append(card)
        if not card_types:
            return color_sorted_cards
    else:
        for card in cards:
            if color in card.colors:
                color_sorted_cards.append(card)
        if not card_types and not rarity:
            return color_sorted_cards #ONLY COLOR FILTER SELECTED
        
    if card_types and color_sorted_cards:
        for card in color_sorted_cards:
            for card_type in card_types:
                if card_type in card.card_type:
                    sorted_cards.append(card)
        
        return sorted_cards  #COLOR AND TYPE SELECTED
    
    if card_types and not color:
        for card in cards:
            for card_type in card_types:
                if card_type in card.card_type:
                    type_sorted_cards.append(card)
        return type_sorted_cards  #ONLY TYPE SELECTED
    

def getSetInformation(response):
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

def AddKeywordsToDB(cards):
    keywords_dict = {}
    keywords = []
    for card in cards:
        keywords = str(card.keywords).strip("{}\'[]\"\' ")
        if not keywords:
            continue
        if "," in keywords:
            keywords = keywords.split(",")
            for keyword in keywords:
                if keyword in keywords_dict:
                    keywords_dict[keyword.strip("\"")] += 1
                else:
                    keywords_dict[keyword.strip("\"")] = 1
        else:
            if keywords in keywords_dict:
                keywords_dict[keywords.strip("\"")] += 1 
            else:
                keywords_dict[keywords.strip("\"")] = 1

    with open('methods/keywords.txt', 'r') as file:
        known_keywords = file.read()
    
    for keyword in keywords_dict:
        keyword = keyword.strip("\'[]\"\' ")
        if not (keyword in known_keywords):
            with open('methods/keywords.txt', 'a') as file:
                file.write(keyword + "\n")

    
    with open('methods/keywords.txt', 'r') as file:
        known_keywords = file.read()

    return known_keywords

def CardsWithPhrases(cards, known_phrases):
    return

def getCardsWithKeywords(cards, known_keywords):
    cards_dict = {}
    keywords_list = known_keywords.split('\n')
    keywords_list.pop(-1)
    for card in cards:
        found_keywords = []
        for keyword in keywords_list:
            if keyword in card.desc.title() or keyword in card.desc2.title():
                found_keywords.append(keyword)
        if found_keywords:
            cards_dict.update({card.card_name : found_keywords}) 
    #st.write(cards_dict)

    num_found_keywords = {}
    for card in cards_dict:
        for keyword in cards_dict[card]:
            if keyword in num_found_keywords:
                num_found_keywords[keyword] += 1
            else:
                num_found_keywords[keyword] = 1

    return num_found_keywords

def SearchSets(response, search, set_type, date):
    data = response['data']
    #st.write("Search: " + search)
    setNamesandID = {}
    for i in range(len(data)):
        if (search in data[i]['name'] or search.lower() in data[i]['name'].lower()):
            if(data[i]['set_type'] == set_type.lower()):
               set_name = data[i]['name']
               set_id = data[i]['id']
               setNamesandID.update({set_name:set_id})
    return setNamesandID

def GetCardTypes(cards, detailed):
    lands = ["Plains", "Island", "Swamp", "Mountain", "Forest"]
    card_types = {}

    for card in cards:
        card_type = card.card_type.split("—")
        if detailed and len(card_type) > 1 and card_type[1].strip(" ") in lands:
            card_type = card_type[1]
        else:
            card_type = card_type[0]

        if card_type in card_types:
            card_types[card_type] +=1
        else:
            card_types[card_type] = 1

    return card_types