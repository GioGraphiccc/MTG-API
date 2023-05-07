import streamlit as st

def displaySetCardImages(set_images):
    replace = st.empty()
    replace.empty()
    if(set_images == 'noimage'):
        return 0
    col1_images = []
    col2_images = []
    col3_images = []
    col4_images = []
    col1, col2, col3, col4 = st.columns(4)
    i = 0
    while True and i < 8:
        if(i+4 > len(set_images)):
            remaining = len(set_images) - i
            if(remaining == 1):
                col1_images.append(set_images[len(set_images)-1]['img_type_color'][0])
                i = i + 1
                break
            elif(remaining == 2):
                col1_images.append(set_images[i]['img_type_color'][0])
                col2_images.append(set_images[i+1]['img_type_color'][0])
                i = i + 2
                break
            elif(remaining == 3):
                col1_images.append(set_images[i]['img_type_color'][0])
                col2_images.append(set_images[i+1]['img_type_color'][0])
                col3_images.append(set_images[i+2]['img_type_color'][0]) 
                i = i + 3
                break  
        else:
            col1_images.append(set_images[i]['img_type_color'][0])
            col2_images.append(set_images[i+1]['img_type_color'][0])
            col3_images.append(set_images[i+2]['img_type_color'][0])
            col4_images.append(set_images[i+3]['img_type_color'][0])
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
    st.write("numWhiteCards: " + str(info[1]))
    st.write("numBlueCards: "+ str(info[2]))
    st.write("numGreenCards: " + str(info[3]))
    st.write("numBlackCards: " + str(info[4]))
    st.write("numRedCards: " + str(info[5]))
    st.write("Number of Creatures: " + str(info[6]))
    st.write("Number of Instants: " + str(info[7]))
    st.write("Number of Sorceries: " + str(info[8]))
    st.write("Number of Enchantments: " + str(info[9]))
    st.write("Number of Arifacts: " + str(info[10]))
    st.write("oneManaCards: " + str(info[11]))
    st.write("twoManaCards: " + str(info[12]))
    st.write("threeManaCards: " + str(info[13]))
    st.write("fourManaCards: " + str(info[14]))
    st.write("fiveManaCards: " + str(info[15]))
    st.write("sixOrMoreManaCards: " + str(info[16]))
    st.write("List of card prices: " + str(info[17]))
    #st.write(response)