import streamlit as st
import datetime



def getImages(response, color, card_type, enlarge):
    
    response = response['data']
    #st.write(response)
    cardImages = []
    colorSortedImages = []
    cards_data = []

    try:
        enlarge = True
        if(enlarge):
            for data in response:
                #st.write(data)
                cards_data.append({'img_type_color':(data['image_uris']['large'], data['type_line'], data['colors'])})
            
            # for data in dataset_2:
            #     cards_data.append({'img_type_color':(data['image_uris']['large'], data['type_line'], data['colors'])})
    except:
        st.error("Error: It appears that this set does not contain images.")
        return ['noimage']
    #st.write(cards_data)
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
            #st.write(cards_data)                #DEBUG LINE DEBUG
            return cards_data
        
        else: #if not color but type
            for types in card_type:
                for i in range(len(cards_data)):
                    if(types in cards_data[i]['img_type_color'][1]):
                        cardImages.append(cards_data[i])
    #st.write(cardImages)
    return cardImages

def getInformation(response):
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
