import streamlit as st
import pandas as pd
import datetime
import json
import os

# Configuration de la page
st.set_page_config(page_title="Hardcore Overload 6-Months", page_icon="💀", layout="wide")

# --- GESTION DE LA SAUVEGARDE ET DE L'HISTORIQUE ---
SAVE_FILE = "hardcore_overload_save.json"

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    return {"xp": 0, "history": []}

def save_data(xp, history):
    clean_history = []
    for h in history:
        item = h.copy()
        if isinstance(item["Date"], (datetime.date, datetime.datetime)):
            item["Date"] = item["Date"].strftime("%Y-%m-%d")
        clean_history.append(item)
    with open(SAVE_FILE, "w") as f:
        json.dump({"xp": xp, "history": clean_history}, f)

saved_state = load_data()
if 'xp' not in st.session_state:
    st.session_state.xp = saved_state["xp"]
if 'history' not in st.session_state:
    st.session_state.history = saved_state["history"]

# --- SYSTÈME DE NIVEAUX EXPONENTIEL (1 À 100) ---
def get_current_level(total_xp):
    level = 1
    while level < 100:
        next_xp_needed = int(150 * (level ** 1.8))
        if total_xp >= next_xp_needed:
            level += 1
        else:
            break
    return level

current_level = get_current_level(st.session_state.xp)
next_level_needed = int(150 * (current_level ** 1.8))

# --- PLAN DE SEMAINE OPTIMISÉ POUR L'HYPERTROPHIE (SANS MATÉRIEL) ---
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
jour_actuel = jours_semaine[datetime.date.today().weekday()]

PROGRAMME_SEMAINE = {
    "Lundi": {
        "Focus": "Pectoraux / Triceps / Avant d'épaules (Push Day)",
        "Exercices": [
            {"nom": "Pompes Déclinées (Pieds surélevés)", "series": 4, "reps": "12-15", "xp_base": 30, "note": "Haut des pectoraux. Ralentir la descente."},
            {"nom": "Dips entre 2 chaises (Lesté Sac d'eau)", "series": 4, "reps": "10-12", "xp_base": 35, "note": "Mettre le sac sur les cuisses."},
            {"nom": "Pompes Diamant (Mains serrées au sol)", "series": 3, "reps": "A l'échec", "xp_base": 25, "note": "Triceps et intérieur des pectoraux."}
        ]
    },
    "Mardi": {
        "Focus": "Dos / Arrière d'épaules / Biceps (Pull Day)",
        "Exercices": [
            {"nom": "Rowing Inversé sous une table solide", "series": 4, "reps": "10-12", "xp_base": 35, "note": "Tracter le buste en bloquant 1s en haut."},
            {"nom": "Soulevé de terre roumain unilatéral", "series": 4, "reps": "12 (par jambe)", "xp_base": 30, "note": "Prendre 1 ou 2 gros sacs d'eau à bout de bras."},
            {"nom": "Curl Biceps unilatéral avec Sac d'eau", "series": 3, "reps": "15", "xp_base": 25, "note": "Isoler le mouvement, dos droit contre un mur."}
        ]
    },
    "Mercredi": {
        "Focus": "Jambes complètes / Sangle Abdominale (Legs & Core)",
        "Exercices": [
            {"nom": "Squats Bulgares (Sacs d'eau)", "series": 4, "reps": "12 (par jambe)", "xp_base": 40, "note": "Un pied surélevé en arrière sur une chaise."},
            {"nom": "Fentes sautées explosives", "series": 3, "reps": "20 (alterné)", "xp_base": 30, "note": "Brûle le gras et développe l'explosivité."},
            {"nom": "Gainage Commando militaire", "series": 4, "reps": "45 secondes", "xp_base": 25, "note": "Passer des coudes aux mains en continu."}
        ]
    },
    "Jeudi": {
        "Focus": "Épaules / Rappel Haut Pectoraux / Triceps",
        "Exercices": [
            {"nom": "Pompes Pike (Fesses en l'air en V)", "series": 4, "reps": "8-10", "xp_base": 35, "note": "Focus épaules. Descendre la tête vers le sol."},
            {"nom": "Élévations Latérales avec Sac d'eau", "series": 4, "reps": "15", "xp_base": 25, "note": "Garder les bras quasi tendus pour élargir la carrure."},
            {"nom": "Pompes classiques au sol (Tempo lent)", "series": 3, "reps": "A l'échec", "xp_base": 25, "note": "3 secondes de descente, 1 seconde de montée."}
        ]
    },
    "Vendredi": {
        "Focus": "Rappel Dos / Élimination des graisses (HIIT)",
        "Exercices": [
            {"nom": "Rowing avec deux Sacs d'eau (Buste penché)", "series": 4, "reps": "15", "xp_base": 35, "note": "Tirez les coudes vers l'arrière en serrant les omoplates."},
            {"nom": "Burpees Hardcore avec pompe", "series": 3, "reps": "12", "xp_base": 35, "note": "Enchaînement ultra rapide sans pause."},
            {"nom": "Crunchs inversés (Bas des abdos)", "series": 4, "reps": "20", "xp_base": 20, "note": "Enrouler le bassin sans élan pour aplatir le ventre."}
        ]
    },
    "Samedi": {
        "Focus": "Conditionnement Athlétique Sec (Full Body Cardio)",
        "Exercices": [
            {"nom": "Squats au poids du corps (Vitesse maximale)", "series": 4, "reps": "30", "xp_base": 30, "note": "Cardio et endurance musculaire."},
            {"nom": "Mountain Climbers intenses", "series": 4, "reps": "1 minute", "xp_base": 30, "note": "Amener les genoux à la poitrine de façon explosive."}
        ]
    },
    "Dimanche": {
        "Focus": "Repos Actif / Oxydation des graisses",
        "Exercices": [
            {"nom": "Marche rapide à jeun (Extérieur)", "series": 1, "reps": "45 minutes", "xp_base": 40, "note": "Force le corps à puiser directement dans le gras."},
            {"nom": "Étirements et mobilité complète", "series": 1, "reps": "15 minutes", "xp_base": 20, "note": "Récupération nerveuse et musculaire."}
        ]
    }
}

ROUTINE_VISAGE = [
    {"nom": "Mewing Strict (Posture de la langue)", "cible": "Dessin global de la mâchoire & Maxillaire", "note": "Plaquer 100% de la langue au palais toute la journée."},
    {"nom": "Drainage Lymphatique Manuel", "cible": "Élimination des joues gonflées & Eau sous-cutanée", "note": "Masser du nez vers les tempes, puis descendre vers le cou."},
    {"nom": "Résistance Mâchoire contre Poing", "cible": "Hypertrophie des muscles Masséters", "note": "Ouvrir la bouche en exerçant une contre-pression forte avec le poing (3 séries de 15 reps)."}
]

# --- DESIGN DE L'INTERFACE UTILISATEUR ---
st.title("💀 HARDCORE OVERLOAD : CODES DE TRANSFORMATION")
st.subheader(f"📅 Aujourd'hui : **{jour_actuel}** | 🎯 Focus : `{PROGRAMME_SEMAINE[jour_actuel]['Focus']}`")

# Profil et Niveaux
col_l, col_x, col_h = st.columns(3)
with col_l:
    st.metric("NIVEAU DU JOUEUR", f"{current_level} / 100")
with col_x:
    st.metric("XP TOTAL", f"{st.session_state.xp} / {next_level_needed} XP")
with col_h:
    st.metric("ENTRAÎNEMENTS ENREGISTRÉS", len(st.session_state.history))

st.write("---")

col_gauche, col_droite = st.columns([2, 1.5])

with col_gauche:
    st.header("💪 Enregistrement de vos Performances Réelles")
    st.caption("Entrez vos données exactes pour calculer votre volume de travail et valider vos XP.")
    
    # Génération dynamique des formulaires pour le jour actuel
    for i, ex in enumerate(PROGRAMME_SEMAINE[jour_actuel]["Exercices"]):
        with st.expander(f"🏋️‍♂️ {ex['nom']} (Objectif : {ex['series']} séries x {ex['reps']} reps)"):
            st.markdown(f"💡 *Consigne : {ex['note']}*")
            
            # Formulaire de saisie utilisateur pour l'exercice
            with st.form(key=f"form_{jour_actuel}_{i}"):
                c1, c2, c3 = st.columns(3)
                with c1:
                    input_series = st.number_input("Séries réelles faites", min_value=0, max_value=10, value=ex['series'], key=f"s_{i}")
                with c2:
                    input_reps = st.number_input("Répétitions par série", min_value=0, max_value=100, value=12, key=f"r_{i}")
                with c3:
                    input_charge = st.number_input("Poids additionnel (kg / Sacs d'eau)", min_value=0.0, max_value=100.0, value=0.0, step=0.5, key=f"p_{i}")
                
                submit_ex = st.form_submit_form("Enregistrer la performance")
                
                if submit_ex:
                    if input_series > 0 and input_reps > 0:
                        # Calcul mathématique du volume d'effort pour l'évolution
                        volume_total = input_series * input_reps
                        xp_gagne = ex['xp_base'] + int(input_charge * 2) # Bonus de points si vous chargez en sacs d'eau
                        
                        st.session_state.xp += xp_gagne
                        st.session_state.history.append({
                            "Date": datetime.date.today().strftime("%Y-%m-%d"),
                            "Type": "Corps",
                            "Exercice": ex['nom'],
                            "Séries": input_series,
                            "Répétitions": input_reps,
                            "Lest (kg)": input_charge,
                            "Volume Total Effort": volume_total,
                            "XP Gagné": xp_gagne
                        })
                        save_data(st.session_state.xp, st.session_state.history)
                        st.success(f"Enregistré ! +{xp_gagne} XP accumulés.")
                        st.rerun()

    st.header("💀 Routine Faciale Quotidienne (Obligatoire)")
    for j, vis in enumerate(ROUTINE_VISAGE):
        with st.expander(f"✨ {vis['nom']} ({vis['cible']})"):
            st.write(f"**Méthode :** {vis['note']}")
            if st.button("Valider la routine faciale", key=f"vis_{j}"):
                st.session_state.xp += 20
                st.session_state.history.append({
                    "Date": datetime.date.today().strftime("%Y-%m-%d"),
                    "Type": "Visage",
                    "Exercice": vis['nom'],
                    "Séries": 1,
                    "Répétitions": 1,
                    "Lest (kg)": 0.0,
                    "Volume Total Effort": 1,
                    "XP Gagné": 20
                })
