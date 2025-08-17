import math
from scipy.optimize import minimize_scalar
from scipy.stats import poisson
import streamlit as st

# ----------------- Funciones -----------------
def implied_prob(over_odds, under_odds):
    inv_over = 1 / over_odds
    inv_under = 1 / under_odds
    p_over = inv_over / (inv_over + inv_under)
    return p_over

def estimate_lambda(p_over, line=2.5):
    def objective(lmbda):
        prob = 1 - poisson.cdf(math.floor(line), lmbda)
        return abs(prob - p_over)
    res = minimize_scalar(objective, bounds=(0.1, 6), method="bounded")
    return res.x

def expected_goal_times(lmbda, max_goals=3):
    results = []
    for k in range(1, max_goals + 1):
        mean_time = 90 * k / lmbda
        median_time = (math.log(2) * 90 * k) / lmbda
        results.append((k, round(mean_time, 2), round(median_time, 2)))
    return results

# ----------------- Interfaz -----------------
st.set_page_config(page_title="Estimador de goles en fútbol", page_icon="⚽")

st.title("⚽ Estimador de minutos esperados de goles")
st.markdown("Introduce las cuotas **Over/Under** para la línea de goles:")

col1, col2 = st.columns(2)
with col1:
    over_odds = st.number_input("Cuota Over 2.5", min_value=1.01, value=2.10, step=0.01)
with col2:
    under_odds = st.number_input("Cuota Under 2.5", min_value=1.01, value=1.75, step=0.01)

if st.button("Calcular"):
    # 1) Probabilidad implícita
    p_over = implied_prob(over_odds, under_odds)

    # 2) Estimar lambda
    lmbda = estimate_lambda(p_over, line=2.5)

    # 3) Calcular tiempos
    times = expected_goal_times(lmbda, max_goals=3)

    st.subheader("📊 Resultados")
    st.write(f"**Probabilidad Over 2.5 (ajustada):** {p_over:.2%}")
    st.write(f"**Goles esperados (λ):** {lmbda:.2f}")

    st.table(
        {"Gol": [t[0] for t in times],
         "Media (min)": [t[1] for t in times],
         "Mediana (min)": [t[2] for t in times]}
    )
