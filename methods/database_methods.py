import streamlit as st
import psycopg2
from psycopg2 import errors
from methods.Card import Card
  
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

def formatQuery(word):
    if('\'' in word and not('\'\'' in word)):
        word = word.replace('\'', '\'\'')  
    return word


def addCardToDB(card, conn):
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
    
    set_name = formatQuery(card.set_name)
    card_name = formatQuery(card.card_name)
    query = "INSERT INTO Cards VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    try:

        with conn.cursor() as cur:
            cur.execute(query, (card.id, card_name, card.card_type, set_name, card.price, card.priceF, card.rarity,
                            card.colors, card.keywords, card.cmc, card.mana_cost, card.legalityC, card.legalityS,
                            card.power_toughness, card.tcgplayer_id, card.img_url, card.desc, card.desc2))
            conn.commit()
        #st.success("Card Added to Database!")
    except errors.UniqueViolation as e:
        return

def addSetToDB(cardlist):
    conn = init_connection()
    #st.write(cardlist)
    for card in cardlist:
        try:
            #card = Card.getCardInformation(card)
            if fetchCard(card.card_name, conn) == 0:
                addCardToDB(card, conn)
        except TypeError as e:
            st.error(e)
            continue
    #st.success(str(len(cardlist)) + "Card(s) Added to Database!")

def fetchCard(card_name, conn):
    #print("CARD NAME\n" + card_name)
    if '\'' in card_name:
        card_name = card_name.replace('\'', '\'\'')
    #st.write(card_name)
    query = "SELECT * FROM Cards WHERE card_name = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(query, (card_name.strip(),))
            results = cur.fetchall()
            if results:
                #st.write(results)
                id = results[0][0]                                           
                card_name = results[0][1]
                card_type = results[0][2]
                set_name  = results[0][3]
                price = results[0][4]
                priceF = results[0][5]
                rarity = results[0][6]
                colors = results[0][7]
                keywords = results[0][8]
                cmc = results[0][9]
                mana_cost = results[0][10]
                legalityS = results[0][11]
                legalityC = results[0][12]
                power_toughness =  results[0][13]
                tcgplayer_id = results[0][14]
                img_url = results[0][15]
                desc = results[0][16]
                desc2 = results[0][17]
                Card_obj = Card(id, card_name, card_type, set_name,  price, priceF, rarity, colors, keywords,
                    cmc, mana_cost, legalityS, legalityC, power_toughness, tcgplayer_id, img_url, desc, desc2)
                return Card_obj
            return 0
    except errors.InFailedSqlTransaction:
        with conn.cursor() as cur:
            cur.execute("ROLLBACK;")
            fetchCard(card_name, conn)
    except UnboundLocalError as e:
        #st.write(card_name + " not in the db")
        st.error(e)
        return 0
