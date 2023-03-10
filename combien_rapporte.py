#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 09:12:50 2023

@author: nicolas
"""
import streamlit as st

def sep_decimal(nombre):
    chaine = "{:,d}".format(nombre).replace(',',' ')
    return chaine

st.title("Combien peut rapporter votre capital&nbsp;?")

# capital = st.number_input("Quel capital souhaitez-vous placer ? (en euros)", step = 1000, format = "%i")

col1, col2 = st.columns(2, gap = "small")
with col1:
    st.subheader("Quel capital souhaitez-vous placer ?")
    capital = st.number_input(label = "  Entrez une valeur en euros", value = 10000)
with col2:
    st.subheader("À quel taux annuel ce capital sera placé ?")
    taux = st.slider(label = "En pourcentage", min_value = 0.00, max_value = 20.0, value = 5.00, step = 0.05)

revenu_annuel = int(capital * taux / 100)
revenu_mensuel = int(revenu_annuel / 12)
capital = int(capital)

capital_s = sep_decimal(capital)
taux_s = str(taux).replace(".", ",")
revenu_annuel_s =  sep_decimal(revenu_annuel)
revenu_mensuel_s = sep_decimal(revenu_mensuel)


st.markdown(f"<h3> ➡️ En plaçant {capital_s} € à un taux annuel de {taux_s} %, vous toucherez :</h3>", unsafe_allow_html = True)

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) {
  background-color: #E1DCDC;
  padding:10px;
          }

    div[data-testid="stHorizontalBlock"]:nth-of-type(5) {
  background-color: #D6E3F3;
  padding:10px;
          }

    div[data-testid="column"] {
  padding:10px;
          }
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .viewerBadge_link__1S137 {visibility: hidden;}

    </style>
    """,unsafe_allow_html=True)
col1, col2 = st.columns(2, gap = "medium")

with col1:
    st.write("des intérêts annuels de ")
    st.subheader(f"{revenu_annuel_s} € par an")
with col2:
    st.write("soit")
    st.subheader(f"{revenu_mensuel_s} € par mois")

st.write('<style>div.block-container{padding:0 0 0 0};</style>', unsafe_allow_html=True)
st.subheader("Pour aller plus loin:")
# st.markdown(["Les performances de Yomoni"]("https://www.yomoni.fr/performances") )
st.write("* [Les performances de Yomoni](https://www.yomoni.fr/performances)")
st.write("* Notre article [Quel capital pour devenir rentier ?](https://blog.yomoni.fr/devenir-rentier-combien-comment/)")
