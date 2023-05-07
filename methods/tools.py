import streamlit as st
import pandas as pd

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

def bulkParser():
    deck_string = st.text_area("Paste a commander deck here.")
    return