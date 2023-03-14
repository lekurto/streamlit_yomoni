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

st.title("Quel capital pour une rente de ... € par mois&nbsp;?")

# capital = st.number_input("Quel capital souhaitez-vous placer ? (en euros)", step = 1000, format = "%i")

col1, col2 = st.columns(2, gap = "small")
with col1:
    st.subheader("Quelle rente mensuelle souhaitez-vous obtenir&nbsp;?")
    rente_mensuelle = st.number_input(label = "Par mois, en euros", value = 3000, step = 100)
with col2:
    st.subheader("À quel taux annuel votre capital sera-t-il placé&nbsp;?")
    taux = st.number_input(label = "En pourcentage", value = 5.00, step = 0.25)


rente_annuelle = rente_mensuelle * 12
capital_necessaire = 100 * int(rente_annuelle / taux)
taux_s = str(taux).replace(".", ",")

capital_necessaire_s = sep_decimal(capital_necessaire)
rente_mensuelle_s = sep_decimal(rente_mensuelle)
rente_annuelle_s =  sep_decimal(rente_annuelle)

st.markdown(f"<h3> ➡️  Pour obtenir un revenu mensuel de {rente_mensuelle_s} €,\n en plaçant à un taux annuel de {taux_s} %, il vous faut un capital de :</h3>", unsafe_allow_html = True)


st.markdown("<h3 style ='text-align : center; background-color: #D6E3F3; padding:10px;'>" +
capital_necessaire_s + " € </h3>", unsafe_allow_html=True)

st.write("Revenu brut, hors fiscalité, non indexé sur l'inflation.")

st.write('<style>div.block-container{padding:0 0 0 0};</style>', unsafe_allow_html=True)
st.subheader("Pour aller plus loin:")
st.write("* [Les performances de Yomoni](https://www.yomoni.fr/performances)")

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"]:nth-of-type(2) {
  background-color: #E1DCDC;
  padding:10px;
          }

    div.stMarkdown:nth-of-type(3) {
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
