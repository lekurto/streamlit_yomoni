import pandas as pd
import streamlit as st
import altair as alt

def sep_decimal(nombre):
    chaine = "{:,d}".format(nombre).replace(',',' ')
    return chaine

st.title("Simulateur de placement mensuel")

# inputs
col1, col2 = st.columns(2, gap = "small")
with col1:
    capital_initial = st.slider("Capital initial", min_value=0, max_value=100000, value=1000, step=10)
    taux_annuel = st.slider("Taux d'intérêt net du placement", min_value=0.0, max_value=10.0, value=5.0, step=0.1)

with col2:
    versement_mensuel = st.slider("Montant des versements mensuels", min_value=0, max_value=1000, value=100, step=10)
    nb_annees = st.slider("Durée du placement (années)", min_value=1, max_value=50, value=10, step=1)

nb_mois = nb_annees * 12

# On crée le dataframe qui va contenir les données
epargne_atteinte = pd.DataFrame(columns=["Mois", "Versement initial", "Capital début de période", "Versement mensuel", "Cumul versements", "Intérêt période", "Capital fin de période"])

taux_mensuel = (1 + taux_annuel /100) ** (1/12) - 1

# Initialize the DataFrame with the starting capital and monthly contribution
epargne_atteinte.loc[0] = [0, capital_initial, capital_initial, versement_mensuel, 0, 0, capital_initial]

# Calculate savings for each month
for mois in range(1, nb_mois + 1):
    capital_debut_periode = epargne_atteinte.loc[mois - 1, "Capital fin de période"]
    interet_periode = (capital_debut_periode * taux_mensuel) # les versements ne portent pas encore interet
    cumul_versements = versement_mensuel * mois
    capital_fin_periode = capital_debut_periode + versement_mensuel + interet_periode
    epargne_atteinte.loc[mois] = [mois, capital_initial, capital_debut_periode, versement_mensuel, cumul_versements, interet_periode, capital_fin_periode]

epargne_atteinte["cumul_interets"] = epargne_atteinte["Intérêt période"].cumsum()


capital_final = epargne_atteinte.loc[nb_mois, "Capital fin de période"]
capital_final_s = sep_decimal(round(capital_final))

total_versements = versement_mensuel * nb_mois
total_versements_s = sep_decimal(round(total_versements))
interets_totaux = capital_final - capital_initial - total_versements
interets_totaux_s = sep_decimal(round(interets_totaux))

pourcents_capital = round(100 * capital_initial / capital_final)
pourcents_versements = round(100 * total_versements / capital_final)
pourcents_interets = round(100 * interets_totaux / capital_final)

st.markdown(f"<h3> ➡️ Avec un versement initial de {capital_initial} € et des versements mensuels de {versement_mensuel} €, placés à un taux annuel de {taux_annuel } % pendant {nb_annees} ans, vous obtiendrez : </h3>", unsafe_allow_html = True)

col1, col2 = st.columns([30,70], gap = "small")

with col1:
    st.write("un capital final de :")
    st.subheader(f"{ capital_final_s } €" )
with col2:
    st.write("Ce montant se décompose en :")
    st.markdown(f"- Dépôt initial : { capital_initial} € \n({ pourcents_capital} % du montant final)" )
    st.markdown(f"- Versements : { total_versements_s } € \n({ pourcents_versements} % du montant final)")
    st.markdown(f"- Intérêts : { interets_totaux_s } € \n({ pourcents_interets} % du montant final)")

#### BAR CHART ####

colonnes_a_afficher = ['Mois', 'Versement initial', 'Cumul versements', 'cumul_interets']

st.markdown("<h3>Évolution du capital au fil du temps</h3>", unsafe_allow_html = True)

df_show = epargne_atteinte[colonnes_a_afficher][1:].reset_index()
melted_df = pd.melt(df_show, id_vars=['Mois'], value_vars = colonnes_a_afficher )

color_range = ['#94B5DC', '#1450B9', '#272C5F']

bars = alt.Chart(melted_df).mark_bar().encode(
    x='Mois:O',
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

labels = [f"Capital initial ({round(pourcents_capital)} %)",
          f"Cumul des versements mensuels ({ round(pourcents_versements) } %)",
          f"Intérêts ({round(pourcents_interets)} %)"]

source = pd.DataFrame( {
                        "Légende": labels,
                        "Montant": [capital_initial, total_versements, interets_totaux ]
                        } )

# on mappe les couleurs
domain = labels
color_range = ['#272C5F', '#1450B9', '#94B5DC']

pie = alt.Chart(source).mark_arc().encode(
    theta=alt.Theta(field="Montant", type="quantitative"),
    color=alt.Color(field="Légende",
                    type="nominal",
                    scale=alt.Scale(domain = domain, range = color_range),
                    legend=alt.Legend(
                        orient='right'))
    )

st.altair_chart(pie, use_container_width=True)

#####################

st.write(epargne_atteinte)


st.markdown(
    """
    <style>

    div[data-testid="stHorizontalBlock"]:nth-of-type(2)  {
  background-color: #E1DCDC;
  padding:10px;
          }

    div[data-testid="stHorizontalBlock"]:nth-of-type(4)  {
  background-color: #D6E3F3;
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

