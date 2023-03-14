#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 09:12:50 2023

@author: nicolas
"""
import streamlit as st
import pandas as pd
import altair as alt

def sep_decimal(nombre):
    chaine = "{:,d}".format(nombre).replace(',',' ')
    return chaine

st.title("Calculatrice d'intérêts composés")

col1, col2 = st.columns([99,1])
with col1:
    st.subheader("Montant initial : Quel capital souhaitez-vous placer ?")
    capital_initial = st.number_input("En euros", value = 100000, step = 1000)

col1, col2 = st.columns(2)
with col1:
    st.subheader("À quel taux annuel ?")
    taux = st.slider("En pourcentage", min_value = 0.0, max_value = 20.0, value = 6.0, step = 0.1, help = "Pour 2%, entrez 2")
with col2:
    st.subheader("Combien d'années ?")
    nb_annees = st.slider("Nombre d'années", min_value = 1, max_value = 50, value = 10, step = 1)

capital_initial_s = sep_decimal(int(capital_initial))
taux_s = str(taux).replace(".", ",")
annees_s = str(nb_annees)

capital_final = round(capital_initial * (1+taux/100) ** nb_annees, 2)
interets_simples = capital_initial * taux/100 * nb_annees
interets_composes = capital_final - interets_simples - capital_initial

capital_final_s = sep_decimal(round(capital_final))
interets_simples_s = sep_decimal(round(interets_simples))
interets_composes_s = sep_decimal(round(interets_composes))

pourcents_capital = round(100 * capital_initial / capital_final)
pourcents_int_simples = round(100 * interets_simples / capital_final)
pourcents_int_composes = round(100 * interets_composes / capital_final)

st.markdown(f"<h3> ➡️ En plaçant initialement { capital_initial_s } € à un taux annuel de { taux_s } %, et sans toucher ce capital pendant { annees_s} ans, vous obtiendrez à terme : </h3>", unsafe_allow_html = True)

col1, col2 = st.columns([30,70], gap = "small")

with col1:
    st.write("un capital final de :")
    st.subheader(f"{ capital_final_s } €" )
with col2:
    st.write("Ce montant se décompose en :")
    st.markdown(f"- Dépôt initial : { capital_initial_s} € \n({ pourcents_capital} % du montant final)")
    st.markdown(f"- Intérêts sur ce dépôt : { interets_simples_s } € \n({ pourcents_int_simples} % du montant final)")
    st.markdown(f"- Intérêts sur les intérêts : { interets_composes_s } € \n({ pourcents_int_composes} % du montant final)")

#### ALTAIR BAR CHART ####
# Create dataframe with year, capital, simple interest, and compound interest columns
df = pd.DataFrame(columns=['Capital initial', 'Capital début de période', 'Intérêt de la période', 'dont intérêt sur le capital', 'dont intérêt composé', 'Capital en fin de période'])
df.index.name = "Année"

# Set initial values for year 0
df.loc[0] = [capital_initial, capital_initial, 0, 0, 0, capital_initial]

for annee in range(1, nb_annees + 1):
    capital_debut_periode = df.loc[annee - 1 , 'Capital en fin de période']
    interet = capital_debut_periode * taux / 100
    capital_fin = capital_debut_periode + interet
    dont_int_simple = capital_initial * taux / 100
    dont_int_com = interet - dont_int_simple

    df.loc[annee] = [capital_initial, capital_debut_periode, interet, dont_int_simple, dont_int_com, capital_fin]

df["Intérêts simples"] = df["dont intérêt sur le capital"].cumsum()
df["Intérêts composés"] = round(df["dont intérêt composé"].cumsum())

colonnes_a_afficher = ['Capital initial', 'Intérêts simples', 'Intérêts composés']

st.markdown("<h3>Évolution du capital au fil du temps</h3>", unsafe_allow_html = True)

df_show = df[colonnes_a_afficher][1:].reset_index()
melted_df = pd.melt(df_show, id_vars=['Année'], value_vars = colonnes_a_afficher )

color_range = ['#94B5DC', '#1450B9', '#272C5F']

bars = alt.Chart(melted_df).mark_bar().encode(
    x='Année:O',
    y=alt.Y('value:Q', title = "Capital"),
    color=alt.Color('variable:N',
                    scale=alt.Scale(range=color_range), sort = colonnes_a_afficher[::-1],  title = "Legende"),
    order=alt.Order(sort='ascending')
)

legend = alt.Chart(melted_df).mark_point().encode(
    y=alt.Y('variable:N', axis=alt.Axis(orient='right', title = "Legende")),
    color=alt.Color('variable:N',
                    scale=alt.Scale(range=color_range), sort = colonnes_a_afficher[::-1], title = "Legende")
)

# values = colonnes_a_afficher[::-1]

st.altair_chart(bars, use_container_width=True)

################## PIE CHART ######################

st.markdown("<h3>D'où provient ce capital ?</h3>", unsafe_allow_html = True)

labels = [f"Capital initial ({pourcents_capital} %)",
          f"Intérêts sur le capital({ pourcents_int_simples } %)",
          f"Intérêts sur les intérêts ({pourcents_int_composes} %)"]

source = pd.DataFrame( {
                        "Légende": labels,
                        "Montant": [capital_initial, interets_simples, interets_composes]
                        } )

# on mappe les couleurs
domain = labels
color_range = ['#94B5DC', '#1450B9', '#272C5F'][::-1]

pie = alt.Chart(source).mark_arc().encode(
    theta=alt.Theta(field="Montant", type="quantitative"),
    color=alt.Color(field="Légende",
                    type="nominal",
                    scale=alt.Scale(domain = domain, range = color_range),
                    legend=alt.Legend(
                        orient='right'))
    )

st.altair_chart(pie, use_container_width=True)
st.markdown(
    """
    <style>

    div[data-testid="stHorizontalBlock"]:nth-of-type(2)  {
  background-color: #E1DCDC;
  padding:10px;
          }

    div[data-testid="stHorizontalBlock"]:nth-of-type(3)  {
  background-color: #E1DCDC;
  padding:10px;
          }

    div[data-testid="stHorizontalBlock"]:nth-of-type(5)  {
  background-color: #D6E3F3;
  padding:10px;
          }

    div[data-testid="column"] {
  padding:10px;
          }

    div.egzxvld4 {
  padding: 0px;
}

            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .viewerBadge_link__1S137 {visibility: hidden;}
    </style>
    """,unsafe_allow_html=True)