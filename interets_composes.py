#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 09:12:50 2023

@author: nicolas
"""
import streamlit as st

# import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# import plotly.graph_objects as go

def sep_decimal(nombre):
    chaine = "{:,d}".format(nombre).replace(',',' ')
    return chaine

st.title("Calculatrice d'intérêts composés")

st.subheader("Quel capital souhaitez-vous placer ?")
capital_initial = st.number_input("En euros", value = 100000)

st.subheader("À quel taux annuel ?")
taux = st.slider("En pourcentage", min_value = 0.0, max_value = 20.0, value = 6.0, step = 0.1, help = "Pour 2%, entrez 2")

st.subheader("Pendant combien d'années ?")
nb_annees = st.slider("Années", min_value = 1, max_value = 100, value = 30, step = 1)

capital_initial_s = sep_decimal(int(capital_initial))
taux_s = str(taux).replace(".", ",")
annees_s = str(nb_annees)

capital_final = capital_initial * (1+taux/100) ** nb_annees
interets_simples = capital_initial * taux/100 * nb_annees
interets_composes = capital_final - interets_simples - capital_initial

capital_final_s = sep_decimal(round(capital_final))
interets_simples_s = sep_decimal(round(interets_simples))
interets_composes_s = sep_decimal(round(interets_composes))


st.markdown(f"<h3> ➡️ En plaçant initialement { capital_initial_s } € à un taux annuel de { taux_s } %, et sans toucher ce capital pendant { annees_s} ans, vous obtiendrez à terme un capital de { capital_final_s } €. </h3>", unsafe_allow_html = True)

col1, col2 = st.columns(2)

with col1:
    st.write("Ce montant se décompose en :")
    st.write(f"Dépôt initial : { capital_initial_s} €")
    st.write(f"Intérêts sur ce dépôt : { interets_simples_s } €")
    st.write(f"Intérêts sur les intérêts : { interets_composes_s } €")

##bar chart

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


################## ALTAIR ######################
# # on reset l'indice pour en faire une colonne normale

st.markdown("<h3>Évolution du capital au fil du temps</h3>", unsafe_allow_html = True)

df_show = df[colonnes_a_afficher][1:].reset_index()
melted_df = pd.melt(df_show, id_vars=['Année'], value_vars = colonnes_a_afficher )

bars = alt.Chart(melted_df).mark_bar().encode(
    x='Année:O',
    y=alt.Y('value:Q'),
    color=alt.Color('variable:N',
                    scale=alt.Scale(range=['#272C5F', '#94B5DC', '#1450B9']), sort = colonnes_a_afficher),
    order=alt.Order(sort='ascending')
)

legend = alt.Chart(melted_df).mark_point().encode(
    y=alt.Y('variable:N', axis=alt.Axis(orient='right')),
    color=alt.Color('variable:N',
                    scale=alt.Scale(range=['#272C5F', '#94B5DC', '#1450B9']), sort = colonnes_a_afficher)
)

# values = colonnes_a_afficher[::-1]

st.altair_chart(bars, use_container_width=True)

################## MATPLOT ######################

## pie chart
st.markdown(f"<h3>Origine du capital final de { capital_final_s } €</h3>", unsafe_allow_html = True)


data = { 'label' : ['Votre épargne initiale', 'Les intérêts simples (sur votre capital)', 'Les intérêts composés (intérêts sur les intérêts)'],
        'values' : [capital_initial, interets_simples, interets_composes],
        'colors' : ['#272C5F', '#1450B9', '#94B5DC'] }

df = pd.DataFrame(data)

fig, ax = plt.subplots()

_, _, autotexts = ax.pie(df['values'],
        labels=df['label'],
        colors=data['colors'],
        autopct='%1.1f%%',
        counterclock=False,
        startangle=90
        )

_ = [ autotext.set_color('white') for autotext in autotexts ]

st.pyplot(fig, use_container_width=True)


