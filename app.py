# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 08:46:40 2026

@author: maria
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 17:21:10 2026

@author: maria
"""

# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from datetime import datetime
import os 
import requests
import time # IMPORTANTE: Ci serve per ingannare la memoria cache di Google

# Link diretto per leggere i dati dal Foglio Google (con la L MAIUSCOLA corretta!)
url_foglio = "https://docs.google.com/spreadsheets/d/1OM4wMHXeaL2kTsORf6GhZCsKHP-cfJJ1zdQFWdu1Kpg/export?format=csv"

# --- CARICAMENTO DATI INTELLIGENTE ---
# L'app legge i dati da Google SOLO la prima volta che apri la pagina o quando serve
if 'eventi' not in st.session_state:
    try:
        # Aggiungiamo il tempo attuale al link per costringere Google a darci i dati freschi
        url_fresco = f"{url_foglio}&t={time.time()}"
        st.session_state.eventi = pd.read_csv(url_fresco)
    except:
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

personaggi = [
    "Angelo", "Daniele", "Fabio", "Marta", "Matteo", "Mawi", 
    "Mery", "Pippo", "Potto", "Riccardo", "Sandro", "Matilde", "Flavio"
]

regolamento = {
    # --- 🟢 BONUS ---
    "guidare per le serate" : 5,
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
    "verginità persa" : 80, 
    "verginità levata" : 70, 
    "fontana di alcol" : 30,
    "metà fontana di alcol" : 15,
    "stile": 5,
    "vittoria a un gioco di squadra" : 5,
    "vittoria solitaria a un gioco" : 7,
    
    # --- 🔴 MALUS ---
    "nominare il fantasardegna per compiere un bonus/malus":-20,
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
with col1:
    cartella_foto = "foto_giocatori"
    foto_trovata = False
                
    if os.path.exists(cartella_foto):
        for file in os.listdir(cartella_foto):
            if file.split('.')[0].lower() == persona_corrente.lower():
                try:
                                # use_container_width è il comando più aggiornato che non va in blocco
                    st.image(f"{cartella_foto}/{file}", use_container_width=True)
                    foto_trovata = True
                    break 
                except Exception:
                    st.error(f"⚠️ Impossibile caricare la foto di {persona_corrente}. Il file potrebbe essere danneggiato o in un formato finto.")
                    foto_trovata = True
                    break
            else:
                st.error("Non trovo la cartella 'foto_giocatori' accanto ad app.py!")
                foto_trovata = True 
                
            if not foto_trovata:
                st.warning(f"Manca la foto di {persona_corrente}.")

# --- TAB 2: REGOLAMENTO ---
with tab2:
    st.header("Le Regole del Gioco")
    
    st.markdown("""
    L'obiettivo principale è divertirsi, perciò non prendetela troppo sul serio *(anche perché le stronzate siete capaci di farle e dirle anche senza impegno)*. Si gioca singolarmente, perciò la tua squadra sei solo tu. La sconfitta, o la vittoria, dipenderà solo da te.

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

    🍹 **Regola sui drink:**
    Il bonus inerente ai drink bevuti verra contato solo dal secondo drink in poi (secondo escluso) per le donne, dal terzo in poi (terzo escluso) per gli uomini.
    """)
    
    st.error("""
    🚨 **! AVVISO DI INFAMIA !** 🚨  
    A colui che non ha supportato la creazione del gioco (non mandando le proprie foto alla creatrice), spetta un Malus di partenza di **-5 punti**. Annullarlo è facile: basta fornire delle sentite scuse all'autrice e promettere solennemente di sostenere le sue future e brillanti creazioni.
    """)

# --- TAB 3: BONUS E MALUS ---
with tab3:
    st.header("Punteggi Ufficiali")
    df_regole = pd.DataFrame(list(regolamento.items()), columns=["Azione", "Punti"])
    
    st.write("🟢 **Bonus**")
    st.dataframe(df_regole[df_regole["Punti"] > 0].sort_values(by="Punti", ascending=False), use_container_width=True, hide_index=True)
    
    st.divider()
    
    st.write("🔴 **Malus**")
    st.dataframe(df_regole[df_regole["Punti"] < 0].sort_values(by="Punti", ascending=True), use_container_width=True, hide_index=True)

# --- TAB 4: CABINA DI REGIA ---
# --- TAB 4: CABINA DI REGIA ---
with tab4:
    st.header("Assegna Punteggio")
    
    password = st.text_input("Inserisci la password segreta", type="password")
    
    if password == "sardegna2026":
        st.success("Accesso sbloccato! Sei pronta a giudicare.")
        
        st.divider()
        
        # --- LA SCELTA ORA È FUORI DAL FORM COSÌ SI AGGIORNA SUBITO! ---
        tipo_evento = st.radio("Che tipo di azione vuoi inserire?", 
                               ["📚 Da Regolamento (Usa la tendina)", "✍️ Evento Personalizzato (Scrivi tu)"])
        
        st.markdown("---")
        
        # --- INIZIO DEL MODULO DI SALVATAGGIO ---
        with st.form("form_eventi", clear_on_submit=True):
            data_evento = st.date_input("Data", datetime.today())
            persona_selezionata = st.selectbox("Chi ha fatto l'azione?", personaggi)
            
            st.divider()
            
            # Mostra i campi giusti in base alla scelta del pallino (che ora funziona in tempo reale)
            if tipo_evento == "📚 Da Regolamento (Usa la tendina)":
                azione_definitiva = st.selectbox("Azione da Regolamento:", list(regolamento.keys()))
                punti_assegnati = regolamento[azione_definitiva]
                st.info(f"💡 Punti calcolati in automatico: {punti_assegnati}")
                
            else:
                azione_definitiva = st.text_input("📝 Scrivi il motivo dell'evento:")
                punti_assegnati = st.number_input("🔢 Scegli i punti (Usa il tasto - per togliere punti):", value=0, step=1)
            
            st.divider()
            
            submit_button = st.form_submit_button("➕ Salva Evento", use_container_width=True)
            
            if submit_button:
                # Controllo anti-errore: se scegli "Personalizzato" ma lasci vuoto il testo
                if tipo_evento == "✍️ Evento Personalizzato (Scrivi tu)" and str(azione_definitiva).strip() == "":
                    st.warning("⚠️ Devi scrivere un motivo per l'evento personalizzato!")
                else:
                    nuovo_dato = {
                        "Data": data_evento.strftime("%d/%m/%Y"),
                        "Persona": persona_selezionata,
                        "Azione": azione_definitiva,
                        "Punti": punti_assegnati
                    }
                    
                    # 🚨 RICORDATI DI INCOLLARE QUI IL TUO VERO LINK DI GOOGLE APPS SCRIPT! 🚨
                    url_script = "https://script.google.com/macros/s/AKfycbylsTZQn9yVirYFqUebj-36xkMC9UTo4P4T6erO697SF48psqPDEbhCQ4zJ54hhRL44rw/exec"
            
                    try:
                        risposta = requests.post(url_script, json=nuovo_dato)
                        try:
                            esito = risposta.json()
                        except:
                            esito = {"status": "error", "message": "Impossibile leggere la risposta di Google"}
                            
                        if esito.get("status") == "success":
                            nuovo_evento_df = pd.DataFrame({
                                "Data": [data_evento.strftime("%d/%m/%Y")],
                                "Persona": [persona_selezionata],
                                "Azione": [azione_definitiva],
                                "Punti": [punti_assegnati]
                            })
                            st.session_state.eventi = pd.concat([st.session_state.eventi, nuovo_evento_df], ignore_index=True)
                            st.success(f"Aggiunto e salvato sul Cloud! {persona_selezionata} ha preso {punti_assegnati} punti.")
                            time.sleep(1.5)
                            st.rerun() 
                        else:
                            st.error(f"❌ Google ha bloccato il salvataggio. Errore: {esito.get('message')}")
                    except Exception as e:
                        st.error(f"Errore di connessione: {e}")
        
        # --- SEZIONE: ELIMINA EVENTO ---
        st.divider() 
        st.subheader("🗑️ Elimina un inserimento sbagliato (Solo Locale)")
        if not st.session_state.eventi.empty:
            lista_eventi = []
            for indice, riga in st.session_state.eventi.iterrows():
                descrizione = f"{indice} - {riga['Data']} | {riga['Persona']} | {riga['Azione']} ({riga['Punti']} pt)"
                lista_eventi.append(descrizione)
                
            evento_scelto = st.selectbox("Seleziona l'evento da cancellare:", lista_eventi)
            
            if st.button("❌ Conferma Eliminazione", use_container_width=True):
                indice_reale = int(evento_scelto.split(" - ")[0])
                st.session_state.eventi = st.session_state.eventi.drop(indice_reale).reset_index(drop=True)
                st.success("Evento cancellato con successo! (Ricorda di cancellarlo anche dal Foglio Google se era stato salvato).")
                time.sleep(1.5)
                st.rerun() 
        else:
            st.info("Nessun evento registrato finora.")
            
    elif password != "":
        st.error("Password errata. Non sei degno di assegnare punti! 🛑")
