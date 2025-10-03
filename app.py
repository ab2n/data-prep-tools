import streamlit as st
import pandas as pd

st.title("Splitter de cellules Excel par retour à la ligne")

# Upload du fichier Excel
uploaded_file = st.file_uploader("Choisis un fichier Excel", type=["xlsx"])

if uploaded_file:
    # Lecture du fichier
    df = pd.read_excel(uploaded_file)
    st.write("Aperçu des données :")
    st.dataframe(df.head())

    # Sélection de la colonne contenant les infos à splitter
    colonne_split = st.selectbox("Choisis la colonne à splitter", df.columns)

    # Sélection de la colonne à conserver pour chaque ligne (ex: nom du projet)
    colonne_reference = st.selectbox("Choisis la colonne à garder pour chaque info", df.columns)

    if st.button("Transformer le fichier"):
        # Liste pour stocker les nouvelles lignes
        new_rows = []

        for _, row in df.iterrows():
            infos = str(row[colonne_split]).split('\n')  # Split par retour à la ligne
            for info in infos:
                new_rows.append({
                    colonne_reference: row[colonne_reference],
                    colonne_split: info.strip()
                })

        # Création du nouveau DataFrame
        df_transforme = pd.DataFrame(new_rows)
        st.write("Aperçu du fichier transformé :")
        st.dataframe(df_transforme.head())

        # Téléchargement du nouveau fichier
        output_file = "fichier_transforme.xlsx"
        df_transforme.to_excel(output_file, index=False)
        st.download_button(
            label="Télécharger le fichier transformé",
            data=open(output_file, "rb").read(),
            file_name="fichier_transforme.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
