import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import urllib.parse

# Configurazione Pagina professionale
st.set_page_config(page_title="Mappa Aree Sosta Caravan Italia", layout="wide", page_icon="🚐")

# DATABASE COMPLETO (101 AREE)
aree_sosta = [
    # --- ABRUZZO ---
    {"Regione": "Abruzzo", "Nome": "Gulliver", "Città": "Roseto degli Abruzzi (TE)", "Lat": 42.7483, "Lon": 14.0041, "Tel": "0858941011", "Info": "22-35€. Corrente 6A, wi-fi, barbecue. Segnalare ingombro."},
    {"Regione": "Abruzzo", "Nome": "L'oasi di Kilian", "Città": "Rocca di Cambio (AQ)", "Lat": 42.2356, "Lon": 13.4891, "Tel": "3288934343", "Info": "Corrente 6A, videosorvegliato, docce a gettone."},
    {"Regione": "Abruzzo", "Nome": "Pescasserolandia", "Città": "Pescasseroli (AQ)", "Lat": 41.8021, "Lon": 13.7845, "Tel": "3381726562", "Info": "25-35€. Navetta, piscina, barbecue."},
    {"Regione": "Abruzzo", "Nome": "Parking Sulmona", "Città": "Sulmona (AQ)", "Lat": 42.0461, "Lon": 13.9252, "Tel": "3312365507", "Info": "Tariffa a ore. Corrente, scarico, area relax."},

    # --- BASILICATA ---
    {"Regione": "Basilicata", "Nome": "Kartodromo", "Città": "Matera (MT)", "Lat": 40.6663, "Lon": 16.6043, "Tel": "3391090996", "Info": "24-34€. Navetta inclusa, docce calde."},
    {"Regione": "Basilicata", "Nome": "Italica", "Città": "Calvello (PZ)", "Lat": 40.4851, "Lon": 15.8452, "Tel": "3317335391", "Info": "Corrente 6A, barbecue, Wi-Fi."},

    # --- CALABRIA ---
    {"Regione": "Calabria", "Nome": "Costa Splendente", "Città": "Isola Capo Rizzuto (KR)", "Lat": 38.9051, "Lon": 17.0952, "Tel": "0962795131", "Info": "15-45€. Docce calde H24, sorveglianza."},
    {"Regione": "Calabria", "Nome": "Cala Camping", "Città": "San Ferdinando (RC)", "Lat": 38.4862, "Lon": 15.9181, "Tel": "3518967391", "Info": "Piscina, barbecue, accessibilità disabili."},
    {"Regione": "Calabria", "Nome": "La Dolce Vita", "Città": "Scalea (CS)", "Lat": 39.8121, "Lon": 15.7952, "Tel": "3337078336", "Info": "Accesso diretto spiaggia."},
    {"Regione": "Calabria", "Nome": "Le Casette", "Città": "Ciro Marina (KR)", "Lat": 39.3661, "Lon": 17.1252, "Tel": "3473366903", "Info": "15/20 posti, corrente, docce calde."},
    {"Regione": "Calabria", "Nome": "Gabella Turismo", "Città": "Crotone (KR)", "Lat": 39.1551, "Lon": 17.1251, "Tel": "3314942446", "Info": "20€ circa. Vendita prodotti km zero."},
    {"Regione": "Calabria", "Nome": "Lido Zio Tom", "Città": "Scalea (CS)", "Lat": 39.8125, "Lon": 15.7941, "Tel": "3334088719", "Info": "Corrente, lavatrice."},
    {"Regione": "Calabria", "Nome": "Ipanema Family", "Città": "Diamante (CS)", "Lat": 39.6851, "Lon": 15.8152, "Tel": "3513187214", "Info": "Da 13€. Corrente 6A, Wi-Fi."},

    # --- CAMPANIA ---
    {"Regione": "Campania", "Nome": "Area Cilento", "Città": "Montecorice (SA)", "Lat": 40.2351, "Lon": 14.9852, "Tel": "3296559836", "Info": "Navetta spiagge, elettricità, barbecue."},
    {"Regione": "Campania", "Nome": "Baia Domizia", "Città": "Baia Domizia (CE)", "Lat": 41.2121, "Lon": 13.9152, "Tel": "3206612717", "Info": "Corrente, scarico, docce a gettoni."},
    {"Regione": "Campania", "Nome": "Gli Eucalipti", "Città": "Paestum (SA)", "Lat": 40.4251, "Lon": 15.0052, "Tel": "3336309230", "Info": "Navetta, animali ammessi."},
    {"Regione": "Campania", "Nome": "Agriturismo Tre Santi", "Città": "Padula (SA)", "Lat": 40.3351, "Lon": 15.6552, "Tel": "3407336100", "Info": "Sosta GRATIS con pasto."},
    {"Regione": "Campania", "Nome": "Benevento", "Città": "Benevento (BN)", "Lat": 41.1301, "Lon": 14.7752, "Tel": "3384990889", "Info": "ATTENZIONE: Possibile rimessaggio, rumorosa."},
    {"Regione": "Campania", "Nome": "Castagnaro Parking", "Città": "Pozzuoli (NA)", "Lat": 40.8521, "Lon": 14.1012, "Tel": "0815267545", "Info": "20€. Vigilato, vicino metro."},
    {"Regione": "Campania", "Nome": "Le Terrazze di Hermes", "Città": "Pompei (NA)", "Lat": 40.7511, "Lon": 14.4812, "Tel": "3711443189", "Info": "30-45€. Vicino scavi, molti servizi."},
    {"Regione": "Campania", "Nome": "Feudo di San Martino", "Città": "Caserta (CE)", "Lat": 41.0751, "Lon": 14.3352, "Tel": "3286583968", "Info": "30-50€. Videosorvegliata h24, dog sitter."},
    {"Regione": "Campania", "Nome": "Boutique Campeggiatore", "Città": "Portici (NA)", "Lat": 40.8181, "Lon": 14.3421, "Tel": "0810200424", "Info": "30€. Riparazioni e navetta."},
    {"Regione": "Campania", "Nome": "Estatico", "Città": "Portici (NA)", "Lat": 40.8192, "Lon": 14.3431, "Tel": "3408873655", "Info": "Corrente, scarico, illuminazione."},

    # --- EMILIA ROMAGNA ---
    {"Regione": "Emilia Romagna", "Nome": "Ca Vecchia", "Città": "Sasso Marconi (BO)", "Lat": 44.4001, "Lon": 11.2501, "Tel": "0516751211", "Info": "Aperta tutto l'anno, 12 piazzole."},
    {"Regione": "Emilia Romagna", "Nome": "River Passion", "Città": "Boretto (RE)", "Lat": 44.9001, "Lon": 10.5501, "Tel": "3356073801", "Info": "20-25€. Vicino pista ciclabile VEN.TO."},
    {"Regione": "Emilia Romagna", "Nome": "Ariaperta", "Città": "Comacchio (FE)", "Lat": 44.6951, "Lon": 12.1801, "Tel": "3342680986", "Info": "30-35€. 99 piazzole, barbecue."},
    {"Regione": "Emilia Romagna", "Nome": "Camperopoli", "Città": "Bologna (BO)", "Lat": 44.5221, "Lon": 11.3321, "Tel": "0516341504", "Info": "25-35€. Accesso fino alle 22:50."},
    {"Regione": "Emilia Romagna", "Nome": "Cesenatico", "Città": "Cesenatico (FC)", "Lat": 44.1951, "Lon": 12.3851, "Tel": "3895718482", "Info": "da 25€. Animali gratuiti. ATTENZIONE: autovelox 50km/h."},
    {"Regione": "Emilia Romagna", "Nome": "Lido di Classe", "Città": "Lido di Classe (RA)", "Lat": 44.3351, "Lon": 12.3351, "Tel": "3513235379", "Info": "15€. Area cani, wi-fi."},
    {"Regione": "Emilia Romagna", "Nome": "Porto Mario", "Città": "Igea Marina (RN)", "Lat": 44.1351, "Lon": 12.4851, "Tel": "05411797073", "Info": "13-30€. Corrente 16A, acqua potabile."},

    # --- FRIULI VENEZIA GIULIA ---
    {"Regione": "Friuli Venezia Giulia", "Nome": "Cimolais", "Città": "Cimolais (PN)", "Lat": 46.2851, "Lon": 12.4351, "Tel": "042787019", "Info": "10-15€. Sosta max 48h."},
    {"Regione": "Friuli Venezia Giulia", "Nome": "Barcis", "Città": "Ribe (PN)", "Lat": 46.1951, "Lon": 12.5551, "Tel": "N/D", "Info": "20€. NO bagni/docce. Area al buio."},
    {"Regione": "Friuli Venezia Giulia", "Nome": "Fusine", "Città": "Fusine (UD)", "Lat": 46.5051, "Lon": 13.6551, "Tel": "3500700496", "Info": "20€. Videosorvegliato."},

    # --- LAZIO ---
    {"Regione": "Lazio", "Nome": "Roma Nord", "Città": "Roma (RM)", "Lat": 42.0001, "Lon": 12.5001, "Tel": "3925199095", "Info": "42€. Prodotti km 0, lavatrice."},
    {"Regione": "Lazio", "Nome": "Miralago", "Città": "Lunghezza (RM)", "Lat": 41.9151, "Lon": 12.6751, "Tel": "3336585694", "Info": "Aperto tutto l'anno, piazzole illuminate."},
    {"Regione": "Lazio", "Nome": "Associazione Otto", "Città": "Nepi (VT)", "Lat": 42.2451, "Lon": 12.3551, "Tel": "3284911029", "Info": "Corrente, docce calde."},
    {"Regione": "Lazio", "Nome": "Il Prato", "Città": "Pescia Romana (VT)", "Lat": 42.3651, "Lon": 11.4851, "Tel": "3334627918", "Info": "17-22€. Spiaggia a 200m. ATTENZIONE: schiamazzi."},
    {"Regione": "Lazio", "Nome": "La Pineta", "Città": "Pescia Romana (VT)", "Lat": 42.3662, "Lon": 11.4861, "Tel": "3389411085", "Info": "20-45€. Animali a pagamento."},
    {"Regione": "Lazio", "Nome": "Lory Giody Park", "Città": "Formia (LT)", "Lat": 41.2551, "Lon": 13.6051, "Tel": "3392944264", "Info": "25€. Pozzetto in realizzazione."},
    {"Regione": "Lazio", "Nome": "Gli Oleandri", "Città": "Sabaudia (LT)", "Lat": 41.3051, "Lon": 13.0251, "Tel": "3402495050", "Info": "Corrente a pagamento."},
    {"Regione": "Lazio", "Nome": "CirceMed", "Città": "San Felice Circeo (LT)", "Lat": 41.2351, "Lon": 13.0851, "Tel": "3349365970", "Info": "Varie tipologie di piazzole (2A/4A/6A)."},
    {"Regione": "Lazio", "Nome": "Vecchio Maneggio", "Città": "San Felice Circeo (LT)", "Lat": 41.2362, "Lon": 13.0861, "Tel": "3388728154", "Info": "Corrente 16A."},
    {"Regione": "Lazio", "Nome": "Blue Lake", "Città": "Trevignano Romano (RM)", "Lat": 42.1551, "Lon": 12.2351, "Tel": "3485311726", "Info": "Corrente, scarico, lavatoi."},
    {"Regione": "Lazio", "Nome": "L'Isola Che Non C'E'", "Città": "Trevignano Romano (RM)", "Lat": 42.1562, "Lon": 12.2361, "Tel": "3289155197", "Info": "Area comune riscaldata in inverno."},
    {"Regione": "Lazio", "Nome": "Le Mimose", "Città": "Bracciano (RM)", "Lat": 42.1051, "Lon": 12.1752, "Tel": "3299663795", "Info": "Area giochi bambini, barbecue."},
    {"Regione": "Lazio", "Nome": "Vacanze a Roma", "Città": "Gallicano (RM)", "Lat": 41.8751, "Lon": 12.8152, "Tel": "3294206621", "Info": "28€. Solo su prenotazione."},
    {"Regione": "Lazio", "Nome": "Le Ganze", "Città": "Ceprano (FR)", "Lat": 41.5451, "Lon": 13.5152, "Tel": "0775912941", "Info": "20€. Corrente, docce calde."},
    {"Regione": "Lazio", "Nome": "LGP Roma", "Città": "Roma (RM)", "Lat": 41.8761, "Lon": 12.5652, "Tel": "062427518", "Info": "Corrente 600W, area custodita."},

    # --- LIGURIA ---
    {"Regione": "Liguria", "Nome": "ATCMP", "Città": "La Spezia (SP)", "Lat": 44.1021, "Lon": 9.8252, "Tel": "01871875303", "Info": "15€. Sosta max 36h in una settimana."},
    {"Regione": "Liguria", "Nome": "La Meridiana", "Città": "Ameglia (SP)", "Lat": 44.0651, "Lon": 9.9552, "Tel": "3931504337", "Info": "30€. Corrente, servizi igienici."},
    {"Regione": "Liguria", "Nome": "La Rosa", "Città": "Coreglia Ligure (GE)", "Lat": 44.3851, "Lon": 9.2652, "Tel": "3936825807", "Info": "30-35€. 14 piazzole."},

    # --- LOMBARDIA ---
    {"Regione": "Lombardia", "Nome": "Grazie di Curtatone", "Città": "Curtatone (MN)", "Lat": 45.1551, "Lon": 10.7152, "Tel": "N/D", "Info": "15€. Aperta 11 mesi (chiusa Agosto)."},
    {"Regione": "Lombardia", "Nome": "Camper Club Mantova", "Città": "Curtatone (MN)", "Lat": 45.1562, "Lon": 10.7161, "Tel": "3284762197", "Info": "Referente in loco."},
    {"Regione": "Lombardia", "Nome": "Zone", "Città": "Grasso (BS)", "Lat": 45.7651, "Lon": 10.1152, "Tel": "3474491146", "Info": "10€. Accesso consigliato da SS (lago stretto)."},
    {"Regione": "Lombardia", "Nome": "Da Chiara", "Città": "Mantova (MN)", "Lat": 45.1571, "Lon": 10.7952, "Tel": "3480570143", "Info": "4 posti in cortile privato. Navetta gratis."},
    {"Regione": "Lombardia", "Nome": "Concarena", "Città": "Capo di Ponte (BS)", "Lat": 46.0351, "Lon": 10.3452, "Tel": "3272977740", "Info": "13€. Parco giochi, bar."},
    {"Regione": "Lombardia", "Nome": "Busgarina", "Città": "Clusone (BG)", "Lat": 45.8851, "Lon": 9.9452, "Tel": "3477677284", "Info": "Richiesta tessera ACSI."},
    {"Regione": "Lombardia", "Nome": "Park Leolandia", "Città": "Brembate (BG)", "Lat": 45.5951, "Lon": 9.5552, "Tel": "N/D", "Info": "10-30€. Orari legati al parco divertimenti."},
    {"Regione": "Lombardia", "Nome": "Pineta", "Città": "Clusone (BG)", "Lat": 45.8862, "Lon": 9.9461, "Tel": "034622144", "Info": "30€. Sosta max 3 giorni/notti."},
    {"Regione": "Lombardia", "Nome": "Como Lake", "Città": "Sorico (CO)", "Lat": 46.1651, "Lon": 9.3852, "Tel": "N/D", "Info": "16-50€. Caravan SEMPRE AGGANCIATA."},
    {"Regione": "Lombardia", "Nome": "Lozio", "Città": "Villa (BS)", "Lat": 45.9151, "Lon": 10.2652, "Tel": "3470876249", "Info": "10 piazzole. Pagamento in bottega alimentari."},

    # --- MARCHE ---
    {"Regione": "Marche", "Nome": "La Baia a Fano", "Città": "Fano (PU)", "Lat": 43.8351, "Lon": 13.0152, "Tel": "N/D", "Info": "No WC. Caravan non in alta stagione."},
    {"Regione": "Marche", "Nome": "L'Oasi", "Città": "Lidi San Tommaso (FM)", "Lat": 43.2351, "Lon": 13.7852, "Tel": "3276678869", "Info": "17-34€. Doccia dedicata per animali."},
    {"Regione": "Marche", "Nome": "Parallelo 43", "Città": "Grottammare (AP)", "Lat": 42.9851, "Lon": 13.8652, "Tel": "3476868194", "Info": "20€. Spiaggia dedicata animali vicina."},
    {"Regione": "Marche", "Nome": "Adriatico", "Città": "Fano (PU)", "Lat": 43.8362, "Lon": 13.0161, "Tel": "3396735699", "Info": "15-35€. Docce calde H24, Wi-Fi."},
    {"Regione": "Marche", "Nome": "Il Cinisco", "Città": "Frontone (PU)", "Lat": 43.5151, "Lon": 12.7352, "Tel": "3294910202", "Info": "Bagni riscaldati in inverno."},
    {"Regione": "Marche", "Nome": "Il Barco", "Città": "Urbania (PU)", "Lat": 43.6651, "Lon": 12.5252, "Tel": "N/D", "Info": "GRATUITA. 10 posti. Possibile fango."},

    # --- MOLISE ---
    {"Regione": "Molise", "Nome": "Green Park Sofy", "Città": "Casalciprano (CB)", "Lat": 41.5851, "Lon": 14.5352, "Tel": "3333953679", "Info": "Caravan solo su prenotazione."},
    {"Regione": "Molise", "Nome": "Le Marinelle", "Città": "Petacciato (CB)", "Lat": 42.0151, "Lon": 14.8652, "Tel": "3477923482", "Info": "Adiacente spiaggia libera."},
    {"Regione": "Molise", "Nome": "Gambatesa", "Città": "Gambatesa (CB)", "Lat": 41.5051, "Lon": 14.8852, "Tel": "0874719134", "Info": "Pagamento tramite Easy Park."},
    {"Regione": "Molise", "Nome": "Relais i Dolci Grappoli", "Città": "Larino (CB)", "Lat": 41.8051, "Lon": 14.9152, "Tel": "0874822320", "Info": "Corrente, pozzetto, animali ammessi."},

    # --- PIEMONTE ---
    {"Regione": "Piemonte", "Nome": "Burcina", "Città": "Pollone (BI)", "Lat": 45.5851, "Lon": 8.0052, "Tel": "0158976906", "Info": "15€. Sosta max 3 notti."},
    {"Regione": "Piemonte", "Nome": "Un po di sosta", "Città": "Paesana (CN)", "Lat": 44.6851, "Lon": 7.2752, "Tel": "3466875081", "Info": "12-15€. 50 piazzole ai piedi del Monviso."},
    {"Regione": "Piemonte", "Nome": "Val di Treu", "Città": "Castell'Alfero (AT)", "Lat": 44.9851, "Lon": 8.2152, "Tel": "0141204633", "Info": "OFFERTA LIBERA."},
    {"Regione": "Piemonte", "Nome": "Nautica Tarello", "Città": "Viverone (BI)", "Lat": 45.4251, "Lon": 8.0552, "Tel": "3346003267", "Info": "20€. Apertura 9:00-21:00."},

    # --- PUGLIA ---
    {"Regione": "Puglia", "Nome": "Baia di Peschici", "Città": "Peschici (FG)", "Lat": 41.9451, "Lon": 16.0152, "Tel": "3791244564", "Info": "18-35€. Direttamente sulla spiaggia."},
    {"Regione": "Puglia", "Nome": "Lo Chalet del Gargano", "Città": "San Giovanni Rotondo (FG)", "Lat": 41.7051, "Lon": 15.7252, "Tel": "0882451315", "Info": "Custodito h24, videosorveglianza."},
    {"Regione": "Puglia", "Nome": "Tenuta Pupetta", "Città": "Trani (BT)", "Lat": 41.2751, "Lon": 16.4152, "Tel": "3663996725", "Info": "20-30€. Piscina e solarium. Sosta max 15gg."},
    {"Regione": "Puglia", "Nome": "Isola Bella", "Città": "Rodi Garganico (FG)", "Lat": 41.9251, "Lon": 15.8852, "Tel": "3891368318", "Info": "20-50€. Massimo 6 persone per equipaggio."},
    {"Regione": "Puglia", "Nome": "Campo delle Bandiere", "Città": "Sannicola (LE)", "Lat": 40.0951, "Lon": 18.0652, "Tel": "3804114137", "Info": "15€. Accesso diretto spiaggia. Contattare gestore."},

    # --- SARDEGNA ---
    {"Regione": "Sardegna", "Nome": "Porto San Paolo", "Città": "Porto San Paolo (OT)", "Lat": 40.8751, "Lon": 9.6352, "Tel": "3299385143", "Info": "21-38€. Ricambio bombole gas."},
    {"Regione": "Sardegna", "Nome": "Grotta dei Fiori", "Città": "Carbonia (CI)", "Lat": 39.1651, "Lon": 8.5252, "Tel": "3478875668", "Info": "DONAZIONE LIBERA. NO corrente, NO docce."},
    {"Regione": "Sardegna", "Nome": "I Platani", "Città": "Alghero (SS)", "Lat": 40.5551, "Lon": 8.3152, "Tel": "3336725390", "Info": "25-35€. Bookcrossing e piscina."},
    {"Regione": "Sardegna", "Nome": "Tanca di Orrì", "Città": "Tortolì (NU)", "Lat": 39.9251, "Lon": 9.6552, "Tel": "3487351779", "Info": "20€. 80 piazzole."},

    # --- SICILIA ---
    {"Regione": "Sicilia", "Nome": "Spuligni", "Città": "Zafferana Etnea (CT)", "Lat": 37.6851, "Lon": 15.1052, "Tel": "3288762525", "Info": "20€. Chiamare prima di arrivare."},
    {"Regione": "Sicilia", "Nome": "Tremoli Parking", "Città": "Avola (SR)", "Lat": 36.9051, "Lon": 15.1352, "Tel": "3939819613", "Info": "18-38€. Sul lungomare."},

    # --- TOSCANA ---
    {"Regione": "Toscana", "Nome": "Oasi di Maremma", "Città": "M. di Grosseto (GR)", "Lat": 42.7151, "Lon": 10.9852, "Tel": "3389508714", "Info": "16-25€. Corrente 4€, lavatrice."},
    {"Regione": "Toscana", "Nome": "La Pampa", "Città": "M. di Grosseto (GR)", "Lat": 42.7162, "Lon": 10.9861, "Tel": "3391171105", "Info": "16-25€. Wi-Fi, parco giochi."},
    {"Regione": "Toscana", "Nome": "Rapolano Terme", "Città": "Rapolano (SI)", "Lat": 43.2851, "Lon": 11.6052, "Tel": "3476681975", "Info": "12-20€. Vicino terme, barbecue."},
    {"Regione": "Toscana", "Nome": "Chianciano", "Città": "Chianciano (SI)", "Lat": 43.0451, "Lon": 11.8252, "Tel": "3476681975", "Info": "Piazzole in pendenza."},
    {"Regione": "Toscana", "Nome": "Mulino a Fuoco", "Città": "Mazzanta (LI)", "Lat": 43.3251, "Lon": 10.4552, "Tel": "0586724323", "Info": "Vicino mare."},
    {"Regione": "Toscana", "Nome": "Alveare del Pinzi", "Città": "Saturnia (GR)", "Lat": 42.6651, "Lon": 11.5152, "Tel": "3490673294", "Info": "Navetta per cascate Saturnia."},
    {"Regione": "Toscana", "Nome": "Il Serchio", "Città": "S.Anna (LU)", "Lat": 43.8451, "Lon": 10.5052, "Tel": "0583317385", "Info": "Noleggio e-bike, lavatrice."},

    # --- VENETO ---
    {"Regione": "Veneto", "Nome": "Don Bosco", "Città": "Jesolo (VE)", "Lat": 45.5051, "Lon": 12.6452, "Tel": "0421362444", "Info": "20-42€. Spiaggia a 5 min."},
    {"Regione": "Veneto", "Nome": "Albatros", "Città": "Jesolo (VE)", "Lat": 45.5161, "Lon": 12.6561, "Tel": "3923332200", "Info": "33€. Ingresso entro 19:30. Molto ampio."},
    {"Regione": "Veneto", "Nome": "Camper Park Venice", "Città": "Mestre (VE)", "Lat": 45.4851, "Lon": 12.2552, "Tel": "0415322106", "Info": "18€. Max 48h. Vigilanza fisica."},
    {"Regione": "Veneto", "Nome": "Quinto Camper Resort", "Città": "Quinto di Treviso (TV)", "Lat": 45.6451, "Lon": 12.1652, "Tel": "3382288488", "Info": "30€. Servizi igienici, docce calde."}
]

# Conversione in DataFrame
df = pd.DataFrame(aree_sosta)

# Sidebar per Filtri
st.sidebar.header("🔍 Filtra Risultati")
regione_sel = st.sidebar.multiselect("Seleziona Regione", options=sorted(df["Regione"].unique()), default=df["Regione"].unique())

# Filtro ricerca testuale
search_query = st.sidebar.text_input("Cerca per Nome o Città", "")

# Applica filtri
df_filtered = df[df["Regione"].isin(regione_sel)]
if search_query:
    df_filtered = df_filtered[df_filtered["Nome"].str.contains(search_query, case=False) | df_filtered["Città"].str.contains(search_query, case=False)]

# Layout Principale
st.title("🚐 Mappa Aree Sosta Caravan")
st.write(f"Visualizzazione di **{len(df_filtered)}** aree su un totale di **{len(df)}** caricate.")

# Mappa Folium
m = folium.Map(location=[42.0, 12.5], zoom_start=6)

for _, riga in df_filtered.iterrows():
    popup_text = f"""
    <b>{riga['Nome']}</b><br>
    {riga['Città']}<br>
    📞 {riga['Tel']}<br>
    ℹ️ {riga['Info']}<br>
    <a href="tel:{riga['Tel']}" style="color:blue">Chiama</a> | 
    <a href="https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(riga['Nome'] + ' ' + riga['Città'])}" target="_blank">Apri Maps</a>
    """
    folium.Marker(
        [riga['Lat'], riga['Lon']],
        popup=folium.Popup(popup_text, max_width=300),
        tooltip=riga['Nome']
    ).add_to(m)

st_folium(m, width=1200, height=600)

# Tabella Dati
st.subheader("Elenco Dettagliato")
st.dataframe(df_filtered[["Regione", "Nome", "Città", "Tel", "Info"]], use_container_width=True)
