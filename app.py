import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Interactive IS-LM Simulator")

# --- Sidebar: Slider dei parametri ---
st.sidebar.header("IS Parameters")
C0 = st.sidebar.slider("C0 - Autonomous consumption", 0, 300, 100, 10) # Consumo autonomo
c  = st.sidebar.slider("c - Marginal propensity to consume", 0.0, 1.0, 0.8, 0.01) # Propensione marginale al consumo
T  = st.sidebar.slider("T - Total taxes", 0, 300, 50, 10) # Tasse totali
I0 = st.sidebar.slider("I0 - Autonomous investment", 0, 300, 150, 10) # Investimenti autonomi
b  = st.sidebar.slider("b - Sensitivity of investment to interest rate", 5, 60, 20, 1) # Sensibilità degli investimenti al tasso di interesse
G  = st.sidebar.slider("G - Public spending", 0, 500, 200, 10) # Spesa pubblica

st.sidebar.header("LM Parameters")
M  = st.sidebar.slider("M - Nominal money supply", 200, 4000, 1000, 50) # Offerta di moneta nominale
P  = st.sidebar.slider("P - Price level", 0.5, 5.0, 2.0, 0.1) # Livello dei prezzi
k  = st.sidebar.slider("k - Sensitivity of money demand to income", 0.1, 1.5, 0.5, 0.05) # Sensibilità della domanda di moneta al reddito
h  = st.sidebar.slider("h - Sensitivity of money demand to interest rate", 10, 200, 50, 5) # Sensibilità della domanda di moneta al tasso di interesse

# --- Funzioni IS e LM ---
Y = np.linspace(0, 1200, 600) # Valore minimo, massimo e array di 600 punti asse orizzontale grafico

def i_IS(Y):
    return (C0 + c*(Y - T) + I0 + G - Y) / b # Funzione curva IS

def i_LM(Y):
    return (k*Y - (M/P)) / h # Funzione curva LM

def solve_equilibrium():
    num = -b*(M/P) - h*(C0 + I0 + G - c*T)
    den = h*(c - 1.0) - b*k
    if abs(den) < 1e-10:
        return np.nan, np.nan
    Y_eq = num / den
    i_eq = i_LM(Y_eq)
    return Y_eq, i_eq # Funzione per trovare l'equilibrio IS-LM

# --- Calcolo valori ---
is_vals = i_IS(Y)
lm_vals = i_LM(Y)
Ye, ie = solve_equilibrium()

# --- Disegno grafico ---
fig, ax = plt.subplots(figsize=(7,5)) # Crea una figura (fig) e gli assi (ax)
ax.plot(Y, is_vals, label="IS", color="blue") # Disegno curva IS
ax.plot(Y, lm_vals, label="LM", color="green") # Disegno curva LM
if np.isfinite(Ye) and np.isfinite(ie): # Verifica che i valori di equilibrio (Ye ed ie) non siano infiniti
    ax.plot([Ye], [ie], "ro") # Disegno punto di equilibrio (punto rosso (r) a forma di cerchio (o))
    ax.text(Ye + 10, ie, f"Equilibrium\nY={Ye:.1f}, i={ie:.2f}", color="red") # Scrive un'etichetta accanto al punto, mostrando Y con 1 cifra decimale e i con 2 cifre decimali
ax.set_xlabel("Income (Y)")
ax.set_ylabel("Interest Rate (i)")
ax.set_title("IS-LM Curves")
ax.grid(True)
ax.legend() # Mostra la legenda 

# --- Mostra grafico su Streamlit ---
st.pyplot(fig)
