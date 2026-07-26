# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 17:21:10 2026

@author: maria
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os # Ci serve per dire al programma di cercare i file delle foto
import requests

# Link per leggere i dati dal Foglio Google
url_foglio = "https://docs.google.com/spreadsheets/d/1OM4wMHXeal2kTsORf6GhZCsKHP-cfJJ1zdQFWdu1Kpg/export?format=csv"

try:
    st.session_state.eventi = pd.read_csv(url_foglio)
except:
    if 'eventi' not in st.session_state:
        st.session_state.eventi = pd.DataFrame(columns=["Data", "Persona", "Azione", "Punti"])
        
# --- CONFIGURAZIONE PAGINA E STILE ---
st.set_page_config(page_title="Fantasardegna 2026", page_icon="🌊", layout="centered")

st.markdown("""
    <style>
    h1 { text-align: center; color: #007BFF; }
    .stTabs [data-baseweb="tab-list"] { justify-content: center; }
    </style>
""", unsafe_allow_html=True)

st.title("🌊 Fantasardegna 2026")

# --- INIZIALIZZAZIONE DATI ---
if 'eventi' not in st.session_state:
    st.session_state.eventi = pd.DataFrame(columns=["Data", "Persona", "Azione", "Punti"])

personaggi = [
    "Angelo", "Daniele", "Fabio", "Marta", "Matteo", "Mawi", 
    "Mery", "Pippo", "Potto", "Riccardo", "Sandro", "Matilde", "Flavio"
]

regolamento = {
    # --- 🟢 BONUS ---
    "cucina per tutti": 5,
    "ogni drink bevuto": 5,
    "shot bevuto": 2,
    "prepara drink per il gruppo": 7,
    "cavallooo": 10,
    "drink mattutino": 10,
    "selfie con un sardo sconosciuto": 10,
    "bagno di mezzanotte": 15,
    "paccata": 15,
    "far dire al dj 'x ha perso la verginità'": 15,
    "prima paccata della serata": 20,
    "si inventa un coro da stadio per il gruppo e lo fa cantare a tutto il locale": 20,
    "finisce la serata/torna a casa indossando un capo d'abbigliamento non suo": 20,
    "fame chimica eroica": 20,
    "tuffo in acqua dal basso": 5,
    "tuffo in acqua intermedio": 10,
    "tuffo in acqua dall'alto": 20,
    "finta proposta di matrimonio": 25,
    "torna post serata con numero di tel/insta scritto sulla pelle": 25,
    "selfie con sosia di un membro del gruppo/VIP": 25,
    "fa partire un trenino con almeno 10 sconosciuti": 25,
    "ruba un oggetto di arredo urbano e riesce a portarlo in campeggio": 30,
    "va a fare spesa vestito da serata o in pigiama, comprando cose imbarazzanti": 30,
    "mette in scena una rottura drammatica/litigata": 35,
    "bagno di mezzanotte nudo": 40,
    "limona con una figura autoritaria (buttafuori, PR, DJ, barista)": 40,
    "scopata": 50,
    "viene trasportato per almeno 20m su un mezzo non convenzionale": 45,
    "al mattino si sveglia in un posto che non è un letto": 45,
    "al mattino si sveglia a casa di qualcun altro": 45,
    
    # --- 🔴 MALUS ---
    "lamentela ingiustificata": -5,
    "l'ultimo che finisce di prepararsi": -5,
    "telefono scarico prima delle 2 di notte": -5,
    "palo pubblico (max 2 al giorno)": -7,
    "non carica foto sul gruppo entro un giorno post vacanza": -10,
    "sboccata": -10,
    "multa in macchina": -10,
    "problemi con macchina (ruote bucate, motore ecc)": -15,
    "febbre": -15,
    "raffreddore/mal di gola /mal di stomaco": -7,
    "pianto alcolico": -15,
    "perdita di qualcosa di vitale (telefono, documenti, portafoglio...)": -20,
    "si addormenta sui divanetti della discoteca o locale prima delle luci": -20,
    "astensione dall'alcol": -30,
    "litigata con membro del gruppo": -10,
    "neanche una paccata a fine serata": -10,
    "cat calling (fischio)": -5,
    "cat calling (con parole)": -10,
    "si sente male dopo il fumo": -20,
    "non si tuffa in acqua per paura": -2,
    "mancato supporto": -5,
    "calunnia (accusa falsa)": -10
}

# --- CREAZIONE DELLE 4 SCHEDE ---
tab1, tab2, tab3, tab4 = st.tabs(["🏆 Classifica", "📜 Regolamento", "🟢🔴 Bonus & Malus", "⚙️ Cabina di Regia"])

# --- TAB 1: CLASSIFICA E PROFILI ---
with tab1:
    st.header("Classifica Generale")
    
    punteggi_totali = {p: 0 for p in personaggi}
    punteggi_totali["Pippo"] = -5 # Malus iniziale Pippo
    
    for index, row in st.session_state.eventi.iterrows():
        if row["Persona"] in punteggi_totali:
            punteggi_totali[row["Persona"]] += row["Punti"]
            
    df_classifica = pd.DataFrame(list(punteggi_totali.items()), columns=["Persona", "Punti Totali"])
    df_classifica = df_classifica.sort_values(by="Punti Totali", ascending=False).reset_index(drop=True)
    
    st.dataframe(df_classifica, use_container_width=True, hide_index=True)
    
    st.divider()
    
    # SEZIONE PROFILI CLICCABILI
    st.subheader("🔍 Profili Giocatori")
    st.write("Clicca sul nome di un giocatore per vedere i dettagli e le sue azioni!")
    
    for index, row in df_classifica.iterrows():
        persona_corrente = row['Persona']
        punti_correnti = row['Punti Totali']
        
        # Creiamo un blocco a comparsa (expander) per ogni giocatore
        with st.expander(f"👤 {persona_corrente} - Punti: {punti_correnti}"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                cartella_foto = "foto_giocatori"
                foto_trovata = False
                
                # Controllo se la cartella esiste ed è nel posto giusto
                if os.path.exists(cartella_foto):
                    # Guarda tutti i file dentro la cartella
                    for file in os.listdir(cartella_foto):
                        # Se il nome del file (togliendo l'estensione) è uguale al nome del giocatore...
                        if file.split('.')[0].lower() == persona_corrente.lower():
                            st.image(f"{cartella_foto}/{file}", use_column_width=True)
                            foto_trovata = True
                            break # Trovata! Si ferma.
                else:
                    st.error("Non trovo la cartella 'foto_giocatori' accanto ad app.py!")
                    foto_trovata = True # Per nascondere l'altro avviso
                
                if not foto_trovata:
                    st.warning(f"Manca la foto di {persona_corrente}.")
            
            with col2:
                st.write(f"**Punti Attuali:** {punti_correnti}")
                # Mostra la lista degli eventi solo di questo specifico giocatore
                eventi_personali = st.session_state.eventi[st.session_state.eventi['Persona'] == persona_corrente]
                if not eventi_personali.empty:
                    st.write("**Storico Azioni:**")
                    st.dataframe(eventi_personali[['Data', 'Azione', 'Punti']], hide_index=True)
                else:
                    st.write("Nessuna azione registrata finora.")
with tab2:
    st.header("Le Regole del Gioco")
    
    st.markdown("""
    L'obiettivo principale è divertirsi, perciò non prendetela troppo sul serio *(anche perché le stronzate siete capaci di farle e dirle anche senza impegno)*. Si gioca singolarmente, prcioò la tua squadra sei solo tu. La sconfitta, o la vittoria, dipenderà solo da te.

    📸 **L'Onere della Prova:**
    Ogni Bonus e Malus deve essere dimostrato. Sono considerate prove valide: foto, video, screenshot, registrazioni vocali o la conferma di almeno 2 testimoni oculari. Le testimonianze possono ovviamente essere escluse o non ritenute valide in casi particolari (👀) *(non vogliamo una denuncia per registrazione di contenuti vietati ai minori di 18)*.

    ⚖️ **L'Eccezione del Triumvirato:**
    Per Jacopo, Riccardo e Pippo, 2 testimoni oculari non bastano. Ne devono aggiungere un terzo che sia al di fuori del triumvirato.

    🗳️ **La Democrazia:**
    In caso di dubbio o contestazione sull'applicazione di un Bonus o di un Malus, si vota a maggioranza. 

    🤥 **Attenzione alla calunnia:**
    Se un'accusa si rivela falsa, scatta un Malus di -10 punti per menzogna a colui o colei che ha lanciato l'accusa.

    🎭 **Esibizionismo Pubblico:**
    Le finte proposte e le finte litigate sono valide ai fini del punteggio SOLO se riescono ad attirare l'attenzione di almeno 5 passanti.
    """)
    
    st.error("""
    🚨 **! AVVISO DI INFAMIA !** 🚨  
    A colui che non ha supportato la creazione del gioco (non mandando le proprie foto alla creatrice), spetta un Malus di partenza di **-5 punti**. Annullarlo è facile: basta fornire delle sentite scuse all'autrice e promettere solennemente di sostenere le sue future e brillanti creazioni.
    """)

# --- TAB 3: BONUS E MALUS (Solo Tabelle) ---
with tab3:
    st.header("Punteggi Ufficiali")
    df_regole = pd.DataFrame(list(regolamento.items()), columns=["Azione", "Punti"])
    
    st.write("🟢 **Bonus**")
    st.dataframe(df_regole[df_regole["Punti"] > 0].sort_values(by="Punti", ascending=False), use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.write("🔴 **Malus**")
    st.dataframe(df_regole[df_regole["Punti"] < 0].sort_values(by="Punti", ascending=True), use_container_width=True, hide_index=True)

# --- TAB 4: AGGIUNGI EVENTO ---
# --- TAB 4: AGGIUNGI EVENTO ---
with tab4:
    st.header("Assegna Punteggio")
    
    password = st.text_input("Inserisci la password segreta", type="password")
    
    if password == "sardegna2026":
        st.success("Accesso sbloccato! Sei pronta a giudicare.")
        
        with st.form("form_eventi", clear_on_submit=True):
            data_evento = st.date_input("Data", datetime.today())
            persona_selezionata = st.selectbox("Chi ha fatto l'azione?", personaggi)
            azione_selezionata = st.selectbox("Quale azione?", list(regolamento.keys()))
            
            submit_button = st.form_submit_button("➕ Salva Evento", use_container_width=True)
            
            if submit_button:
                punti_assegnati = regolamento[azione_selezionata]
        
        # --- DA QUI IN POI TUTTO DEVE ESSERE SPOSTATO A DESTRA (INDENTATO) ---
                nuovo_dato = {
                    "Data": data_evento.strftime("%d/%m/%Y"),
                    "Persona": persona_selezionata,
                    "Azione": azione_selezionata,
                    "Punti": punti_assegnati
                }
        
                url_script = "https://script.google.com/macros/s/AKfycbzD1n1ZqAJaknD2IOXfPJPDXkDlTuAf9guoe1X9WSRi5CfFEPKS8UDutcoP9--K_1Fp/exec"
        
                try:
                    risposta = requests.post(url_script, json=nuovo_dato)
                    if risposta.status_code == 200:
                        nuovo_evento_df = pd.DataFrame({
                            "Data": [data_evento.strftime("%d/%m/%Y")],
                            "Persona": [persona_selezionata],
                            "Azione": [azione_selezionata],
                            "Punti": [punti_assegnati]
                            })
                        st.session_state.eventi = pd.concat([st.session_state.eventi, nuovo_evento_df], ignore_index=True)
                        
                        st.success(f"Aggiunto e salvato sul Cloud! {persona_selezionata} ha preso {punti_assegnati} punti.")
                    else:
                        st.warning("C'è stato un problema nel salvataggio sul cloud.")
                except Exception as e:
                    st.error(f"Errore di connessione: {e}")
            
                st.rerun()
        
        # --- NUOVA SEZIONE: ELIMINA EVENTO ---
        st.divider() # Linea di separazione visiva
        st.subheader("🗑️ Elimina un inserimento sbagliato")
        
        # Controlliamo se ci sono eventi da poter cancellare
        if not st.session_state.eventi.empty:
            
            # Creiamo una lista leggibile con tutti gli eventi inseriti finora
            lista_eventi = []
            for indice, riga in st.session_state.eventi.iterrows():
                descrizione = f"{indice} - {riga['Data']} | {riga['Persona']} | {riga['Azione']} ({riga['Punti']} pt)"
                lista_eventi.append(descrizione)
                
            # Menu a tendina per scegliere quale evento cancellare
            evento_scelto = st.selectbox("Seleziona l'evento da cancellare:", lista_eventi)
            
            # Tasto per eliminare
            if st.button("❌ Conferma Eliminazione", use_container_width=True):
                # Estraiamo il numero (l'indice) per capire quale riga eliminare dalla tabella
                indice_reale = int(evento_scelto.split(" - ")[0])
                st.session_state.eventi = st.session_state.eventi.drop(indice_reale).reset_index(drop=True)
                
                st.success("Evento cancellato con successo! La classifica è stata ricalcolata.")
                st.rerun() # Ricarica l'app per mostrare la classifica aggiornata
        else:
            st.info("Nessun evento registrato finora.")
            
    elif password != "":
        st.error("Password errata. Non sei degno di assegnare punti! 🛑")
    
    elif password != "":
        st.error("Password errata. Non sei degno di assegnare punti! 🛑")