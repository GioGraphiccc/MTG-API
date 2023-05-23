import streamlit as st
import psycopg2
from psycopg2 import errors
  
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

def formatQuery(word):
    if('\'' in word and not('\'\'' in word)):
        word = word.replace('\'', '\'\'')  
    return word
#def FetchCard(card_name):

def addCard(info, conn):
    
    id = info[0]                                           
    card_name = info[1]
    card_type = info[2]
    set_name  = info[3]
    price = info[4]
    priceF = info[5]
    rarity = info[6]
    colors = info[7]
    keywords = info[8]
    cmc = info[9]
    mana_cost = info[10]
    legalityS = info[11]
    legalityC = info[12]
    power_toughness =  info[13]
    tcgplayer_id = info[14]  
    img_url = info[15]
    
    set_name = formatQuery(set_name)
    card_name = formatQuery(card_name)
    query = "INSERT INTO Cards VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    with conn.cursor() as cur:
        cur.execute(query, (id, card_name, card_type, set_name, price, priceF, rarity,
                        colors, keywords, cmc, mana_cost, legalityC, legalityS,
                        power_toughness, tcgplayer_id, img_url))
        conn.commit()
        #st.success("Card Added to Database!")

def fetchCard(card_name, conn):
    info = [0]
    if '\'' in card_name:
        card_name = card_name.replace('\'', '\'\'')
    query = "SELECT * FROM Cards WHERE card_name = %s;"
    try:
        with conn.cursor() as cur:
            cur.execute(query, (card_name.strip(),))
            results = cur.fetchall()
            for row in results:
                id = row[0]                                           
                card_name = row[1]
                card_type = row[2]
                set_name  = row[3]
                price = row[4]
                priceF = row[5]
                rarity = row[6]
                colors = row[7]
                keywords = row[8]
                cmc = row[9]
                mana_cost = row[10]
                legalityS = row[11]
                legalityC = row[12]
                power_toughness =  row[13]
                tcgplayer_id = row[14]
                img_url = row[15]
                break
            info = [id, card_name, card_type, set_name,  price, priceF, rarity, colors, keywords,
                cmc, mana_cost, legalityS, legalityC, power_toughness, tcgplayer_id, img_url]
            
            return info
    except errors.InFailedSqlTransaction:
        with conn.cursor() as cur:
            cur.execute("ROLLBACK;")
            fetchCard(card_name, conn)
    except UnboundLocalError as e:
        st.write(card_name + " not in the db")
        st.write(e)
        return info
