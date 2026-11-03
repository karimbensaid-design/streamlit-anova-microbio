import numpy as np
import pandas as pd
import plotly.express as px
import scipy.stats as stats
import streamlit as st


# Configuration de la page Streamlit
st.set_page_config(page_title="Microbio ANOVA-1", layout="wide")

st.title("🔬 Application de l'ANOVA 1 en Microbiologie")
st.write(
    "Cette application interactive illustre l'impact de différents traitements "
    "désinfectants sur la charge bactérienne résiduelle (en UFC/mL)."
)

# 1. Barre latérale : Paramètres de simulation pour le cours
st.sidebar.header("⚙️ Paramètres du Cours (Simulation)")
n_samples = st.sidebar.slider("Taille de l'échantillon par groupe (n)", 10, 100, 30)

st.sidebar.subheader("Moyennes théoriques (log10 UFC/mL)")
mu_a = st.sidebar.slider("Désinfectant A", 2.0, 6.0, 5.2, 0.1)
mu_b = st.sidebar.slider("Désinfectant B", 2.0, 6.0, 4.8, 0.1)
mu_c = st.sidebar.slider("Désinfectant C", 2.0, 6.0, 3.5, 0.1)

sigma = st.sidebar.slider("Variabilité intra-groupe (Écart-type σ)", 0.2, 1.5, 0.6, 0.1)

# 2. Génération des données microbiologiques
np.random.seed(42)  # Pour la reproductibilité du cours
data_a = np.random.normal(mu_a, sigma, n_samples)
data_b = np.random.normal(mu_b, sigma, n_samples)
data_c = np.random.normal(mu_c, sigma, n_samples)

df = pd.DataFrame({
    'Désinfectant A': data_a,
    'Désinfectant B': data_b,
    'Désinfectant C': data_c
})

# Transformation en format long pour Plotly et les analyses
df_long = df.melt(var_name='Traitement', value_name='Charge_Bacterienne')

# 3. Affichage des données et des graphiques
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("📊 Résumé descriptif")
    summary = df.describe().loc[['mean', 'std']]
    st.dataframe(summary.style.format("{:.2f}"))
    
    st.info(
        "💡 **Pédagogie :** Modifiez l'écart-type (σ) ou les moyennes dans la barre latérale "
        "pour voir visuellement comment les groupes se chevauchent ou se séparent."
    )

with col2:
    st.subheader("📈 Distribution des charges bactériennes")
    fig = px.box(
        df_long, 
        x='Traitement', 
        y='Charge_Bacterienne', 
        color='Traitement',
        points="all", 
        labels={'Charge_Bacterienne': 'Concentration (log10 UFC/mL)'},
        title="Boîtes à moustaches et points individuels"
    )
    st.plotly_chart(fig, use_container_width=True)

# 4. Calcul de l'ANOVA 1 avec SciPy
f_stat, p_value = stats.f_oneway(data_a, data_b, data_c)

st.divider()
st.subheader("🧪 Résultats du Test Statistique : ANOVA 1")

# Affichage des métriques clés
stat_col1, stat_col2, stat_col3 = st.columns(3)
stat_col1.metric(label="Statistique F (Signal / Bruit)", value=f"{f_stat:.4f}")
stat_col2.metric(label="p-value", value=f"{p_value:.4e}")
stat_col3.metric(label="Seuil de signification α", value="0.05")

# 5. Conclusion automatique interprétée pour les étudiants
st.subheader("📝 Interprétation pour le cours")
if p_value < 0.05:
    st.success(
        f"**Conclusion : Le test est STATISTIQUEMENT SIGNIFICATIF (p < 0.05).**\n\n"
        f"On rejette l'hypothèse nulle ($H_0$). Au moins l'un des désinfectants a un effet "
        f"significativement différent des autres sur la réduction de la charge bactérienne. "
        f"Il y a plus de variations *entre* les groupes que de bruit *dans* les groupes."
    )
else:
    st.error(
        f"**Conclusion : Le test n'est PAS STATISTIQUEMENT SIGNIFICATIF (p ≥ 0.05).**\n\n"
        f"On ne peut pas rejeter l'hypothèse nulle ($H_0$). Les différences observées entre "
        f"les moyennes des désinfectants peuvent être entièrement dues au hasard "
        f"(la variabilité intra-groupe/le bruit est trop fort(e))."
    )
