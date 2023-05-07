import streamlit as st

baseUrl = "https://api.scryfall.com"
st.set_page_config(page_title="MTG Analyzer", page_icon=":shield:")
st.title("MTG Cards Analyzer")
col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Card Analyzer:")
    st.write("• Image of card")
    st.write("• Price for regular and foil")
    st.write("• Legalities for standard and commander")
    st.write("• Rarity")
    st.write("• Set Name")

with col2: 
    st.markdown("")
# st.divider()
#end of Main
