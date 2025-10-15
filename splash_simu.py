# ==============================================================
# === Simulation d'impact et immersion d'un objet dans l'eau ===
# ==============================================================
#
# Ce script simule la chute d'un objet (cylindre ou cône) dans l'eau :
#  - Prend en compte le poids, la poussée d'Archimède, et les frottements
#    quadratiques dans l'air et dans l'eau.
#  - Calcule l'évolution de la position (z), vitesse (v) et accélération (a)
#    au cours du temps via solve_ivp (Runge-Kutta).
#  - Détermine la durée d'impact, la profondeur maximale, et la profondeur
#    au pic d'accélération.
#  - Affiche 3 graphiques : Hauteur, Vitesse, Accélération en fonction du temps.
#
# === Mode d'emploi ===
# 1. Choisir un objet en décommentant le bloc de paramètres souhaité
#    (Ech 10, Ech 4, Ech 2, Ech 1, BFS réel).
# 2. Définir la forme de l'objet avec SHAPE = "cylinder" ou "cone".
# 3. Régler z0 (altitude de départ, négatif = au-dessus de l'eau),
#    v0 (vitesse initiale), et CHOC_BRUTAL (True = immersion instantanée).
# 4. Lancer le script pour générer les résultats et courbes.
#
# === Résultats affichés ===
# - Durée d'impact (temps entre entrée dans l'eau et pic d'accélération)
# - Profondeur maximale atteinte
# - Courbes de hauteur, vitesse et accélération
#
# === Troubleshoot ===
# Si vous ne voyez pas le choc dans les graphiques (fenêtre de simulation trop courte),
# augmentez la fenêtre en modifiant la variable t_span (l'augmenter petit à petit)
#
# ============================================================
# %%
# ==== Imports ====
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
# ==== Configuration ====
'''
objet = "Ech 10"
g = 9.81
rho_eau = 1000
rho_air = 1.225
C_d = 0.8
r = 0.075
A = np.pi*r**2
m = 0.774
h_cone = 0.055
h = 0
'''

'''
objet = "Ech 4"
g = 9.81
rho_eau = 1000
rho_air = 1.225
C_d = 0.8
r = 0.185
A = np.pi*r**2
m = 3.7
h_cone = 0.1
h = 0
'''

'''
objet = "Ech 2"
g = 9.81
rho_eau = 1000
rho_air = 1.225
C_d = 0.9
r = 0.7
A = np.pi*r**2
m = 10
h_cone = 0
h = 0.25
'''

'''
objet = "Ech 1"
g = 9.81
rho_eau = 1000
rho_air = 1.225
C_d = 0.9
r = 0.7
A = np.pi*r**2
m = 37
h = 0.5
h_cone = 0
'''


objet = "BFS réel"
g = 9.81
rho_eau = 1000
rho_air = 1.225
C_d = 0.7
r = 0.75
A = np.pi*r**2
m = 50
# h_cone = 0.43             # cône à 60 degrés (0.75*tan(30))
h_cone = 0.26               # cône à 70 degrés (0.75*tan(20))
h = 0


SHAPE = "cone"  # "cone" ou "cylinder"
z0 = -5                    # alt de départ
v0 = 0                      # v init
CHOC_BRUTAL = False         # Activation/désactivation du volume immergé progressif

if SHAPE == "cone":
    V_total = 1/3 * np.pi * r**2 * h_cone
else:
    V_total = np.pi * r**2 * h  # volume cylindre

k_air = 0.5*rho_air*C_d*A   # coeff frottements quadra air
k_eau = 0.5*rho_eau*C_d*A   # coeff frottements quadra eau

# ===========================
# ==== Fonctions de simu ====


def V_immerge(z):
    """Volume immergé selon la profondeur z (positif sous l'eau)."""
    if CHOC_BRUTAL:
        return V_total if z >= 0 else 0
    if z <= 0:
        return 0

    if SHAPE == "cone":
        if z < h_cone:
            return V_total * (z / h_cone)**3
        return V_total
    else:  # cylindre
        if z < h:
            return np.pi * r**2 * z
        return V_total


def k_effectif(z):
    """Interpolation du coefficient de frottement air/eau."""
    if CHOC_BRUTAL:
        return k_eau if z >= 0 else k_air
    if z <= 0:
        return k_air
    if SHAPE == "cone":
        alpha = min(z / h_cone, 1)
    else:
        alpha = min(z / h, 1)
    return (1 - alpha) * k_air + alpha * k_eau


def system(t, y):
    z, v = y
    V_imm = V_immerge(z)
    k = k_effectif(z)

    F_archi = rho_eau*g*V_imm           # poussée archi
    F_poids = m*g
    F_frott = k*v*abs(v)                # Force frottements k*v*|v|

    a = (F_poids-F_archi-F_frott)/m     # Acceleration = somme des forces
    return [v, a]


y0 = [z0, v0]   # vecteur d'état initial

t_span = (0, 8)                         # temps de simu
t_eval = np.linspace(*t_span, 1000000)  # nb de points de calcul

sol = solve_ivp(system, t_span, y0, t_eval=t_eval, method='RK45')  # résolution par runge kutta

t = sol.t     # solution de temps
z = sol.y[0]  # solution de hauteur
v = sol.y[1]  # solution de vitesse

a = (m*g - rho_eau*g*np.array([V_immerge(zi) for zi in z]) - np.array([k_effectif(zi) for zi in z])*v*np.abs(v))/m  # accel

v_max = np.max(v)                               # vmax
v_terminal = np.sqrt((2*m*g)/(rho_air*A*C_d))   # vterm
a_max = np.min(a)                               # accel max (m/s²)
a_max_g = abs(a_max)/9.81                       # accel max (g)
pourcentage = 100 * v_max/v_terminal            # % de vterm
altitude_lancement = abs(z0)
vitesse_init = v0

# Durée d'impact :
# - t_eau : premier instant où z >= 0 (contact avec l'eau)
idx_eau = np.argmax(z >= 0)
t_eau = t[idx_eau]

# - t_a_max : instant où accélération est minimale (valeur absolue max)
idx_a_max = np.argmin(a)
t_a_max = t[idx_a_max]

duree_impact = t_a_max - t_eau

# Profondeur max
prof_max = np.max(z)
# Profondeur au pic d'accélération
prof_choc = z[idx_a_max]  # z à l'instant du pic d'accélératio

print(f"Objet : {objet} ({SHAPE})")
print(f"Durée d'impact : {duree_impact:.6f} s")
print(f"Profondeur max : {prof_max:.3f} m")
print(f"Profondeur au pic d'accélération : {prof_choc:.3f} m")

# =========================================
# ==== Fonctions d'affichage graphique ====

plt.figure(figsize=(14, 6))
plt.suptitle(
    f"{objet} ({SHAPE})\nDurée impact: {duree_impact:.3f} s, Profondeur max: {prof_max:.2f} m",
    fontsize=14, color='blue', fontweight='bold'
)

plt.subplot(1, 3, 1)
plt.plot(t, -z, label='Hauteur (m)')
plt.axhline(0, color='gray', linestyle='--', label='Surface eau')
plt.axhline(-h_cone, color='blue', linestyle='--', label='Immersion complète')
plt.axhline(-prof_max, color='purple', linestyle='--', label=f'Profondeur max = {prof_max:.2f} m')
plt.axvline(t_eau, color='black', linestyle=':', label='Contact eau')
plt.axvline(t_a_max, color='red', linestyle=':', label='Accélération max')
plt.xlabel('Temps (s)')
plt.ylabel('Hauteur (m)')
plt.legend()
plt.grid()

plt.subplot(1, 3, 2)
plt.plot(t, v, label='Vitesse (m/s)', color='orange')
plt.axhline(v_max, color='red', linestyle='--', label=f'Vitesse max = {v_max:.2f} m/s')
plt.axhline(v_terminal, color='purple', linestyle='--', label=f'V_term = {v_terminal:.2f} m/s\n({pourcentage:.2f} %)')
plt.xlabel('Temps (s)')
plt.ylabel('Vitesse (m/s)')
plt.legend()
plt.grid()

plt.subplot(1, 3, 3)
plt.plot(t, a, label='Accélération (m/s²)', color='green')
plt.axhline(y=a_max, color='red', linestyle='--', label=f'Max = {a_max_g:.2f} g')
plt.axvline(t_a_max, color='red', linestyle=':')
plt.axvline(t_eau, color='black', linestyle=':')
plt.xlabel('Temps (s)')
plt.ylabel('Accélération (m/s²)')
plt.legend()
plt.grid()

plt.tight_layout()
plt.show()
