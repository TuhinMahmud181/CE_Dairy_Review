# Author: Tuhin Mahmud
"""
Bounding analysis, Section 6.5 and Figure 5 of the article; Appendix C.1-C.2.
Tests whether the verdicts of the verdict table survive the full plausible range of the
parameters that Bangladeshi data do not constrain. No parameter is fitted;
every value is either a physical constant, a figure from a cited source, or an
explicitly declared scenario range.
"""
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.path.join(_ROOT, "data")       # CSV inputs and outputs
FIG_DIR = _os.path.join(_ROOT, "figures")     # figures are written here
_os.makedirs(FIG_DIR, exist_ok=True)
import itertools, csv
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------- physical constants ----------
V_M   = 22.414e-3          # m3/mol, ideal gas at STP (0 C, 1 atm)
M_O2  = 32.0e-3            # kg/mol
LHV_CH4_MOLAR = 802.3e3    # J/mol, lower heating value of methane
Y_CH4 = V_M / (2*M_O2)     # m3 CH4 (STP) per kg COD converted  (CH4 + 2 O2 -> CO2 + 2 H2O)
E_CH4 = LHV_CH4_MOLAR / V_M / 1e6   # MJ per m3 CH4 (STP)
E_COD = Y_CH4 * E_CH4      # MJ per kg COD converted to methane
RHO_CP = 4.18              # MJ per m3 per K (water)

# ---------- measured Bangladeshi data [Al Jobair et al. 2026, Sci Rep 16:13097] ----------
COD_IN = {"monsoon": 2.650, "winter": 2.354, "summer": 2.221}   # kg/m3
BOD_IN = {"monsoon": 1.331, "winter": 1.175, "summer": 1.298}   # kg/m3
Q_ETP  = 48.0                                                   # m3/d, ETP capacity

# ---------- scenario ranges (declared, not measured) ----------
ETA_CH4 = (0.5, 0.8)   # fraction of influent COD converted to methane (removal x (1 - biomass yield) - losses)
ETA_B   = (0.7, 0.9)   # boiler / heat-exchange efficiency using biogas
T_DIG   = 35.0         # C, mesophilic set point

# =============== AD energy balance ===============
print(f"Methane yield            {Y_CH4:.3f} m3 CH4/kg COD")
print(f"Methane energy           {E_CH4:.2f} MJ/m3")
print(f"Energy per kg COD        {E_COD:.2f} MJ/kg COD")

def cod_breakeven(dT, eta, eta_b):
    """Influent COD (kg/m3) at which biogas heat exactly covers raising influent by dT.
    Reactor wall heat loss is neglected, so this is a LOWER bound (favourable to AD)."""
    return RHO_CP*dT/(E_COD*eta*eta_b)

def dT_max(cod, eta, eta_b):
    return cod*E_COD*eta*eta_b/RHO_CP

rows=[]
for season,cod in COD_IN.items():
    lo=dT_max(cod,ETA_CH4[0],ETA_B[0]); hi=dT_max(cod,ETA_CH4[1],ETA_B[1])
    rows.append((season,cod,lo,hi,T_DIG-hi,T_DIG-lo))
    print(f"{season:8s} COD {cod:.3f}  max dT {lo:.2f}-{hi:.2f} K  -> influent must be >= {T_DIG-hi:.1f}-{T_DIG-lo:.1f} C")
cods=list(COD_IN.values())
dTmin=min(dT_max(c,ETA_CH4[0],ETA_B[0]) for c in cods)
dTmax=max(dT_max(c,ETA_CH4[1],ETA_B[1]) for c in cods)
print(f"Envelope over seasons: dT_max {dTmin:.1f}-{dTmax:.1f} K")
for dT in (5,10,15):
    print(f"dT={dT:2d} K breakeven COD {cod_breakeven(dT,ETA_CH4[1],ETA_B[1]):.2f}-{cod_breakeven(dT,ETA_CH4[0],ETA_B[0]):.2f} kg/m3")

# methane energy at Vulta scale
P_lo = Q_ETP*min(cods)*ETA_CH4[0]*E_COD/86.4   # kW (MJ/d -> kW : /86.4)
P_hi = Q_ETP*max(cods)*ETA_CH4[1]*E_COD/86.4
print(f"Biogas chemical energy at 48 m3/d: {P_lo:.1f}-{P_hi:.1f} kW")

with open(_os.path.join(DATA_DIR, "S4_AD_energy_balance.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["season","influent_COD_kg_m3","dT_max_low_K","dT_max_high_K","min_influent_T_best_C","min_influent_T_worst_C"])
    for r in rows: w.writerow([r[0],f"{r[1]:.3f}",f"{r[2]:.2f}",f"{r[3]:.2f}",f"{r[4]:.1f}",f"{r[5]:.1f}"])

# =============== whey location ===============
# R = artisanal chhana whey / industrial whey = (c * phi * k) / (s * f)
C_SWEET = (0.50, 0.55)   # share of national milk to sweetmeat channel [UNIDO 2019; RVO 2023]
PHI     = (0.30, 1.00)   # fraction of sweetmeat-channel milk coagulated to chhana (scenario)
K       = (0.80, 1.25)   # whey yield per L coagulated, artisanal relative to industrial (scenario)
S_IND   = (0.05, 0.10)   # industrial share of national milk ([UNIDO 2019] 5%; upper bound doubled)
F_COAG  = (0.01, 0.30)   # coagulated fraction of industrial throughput (scenario; 0.30 far above indications)

corners=[]
for c,phi,k,s,fc in itertools.product(C_SWEET,PHI,K,S_IND,F_COAG):
    corners.append((c*phi*k/(s*fc),c,phi,k,s,fc))
Rmin=min(corners); Rmax=max(corners)
central=0.55*0.65*1.0/(0.05*0.05)
print(f"Whey ratio R: min {Rmin[0]:.1f} at {Rmin[1:]}, max {Rmax[0]:.0f}, central {central:.0f}")
f_star_min = min(c*phi*k/s for c,phi,k,s in itertools.product(C_SWEET,PHI,K,S_IND))
print(f"Coagulated fraction needed for industrial whey to equal artisanal (most adverse): f* = {f_star_min:.2f}")

with open(_os.path.join(DATA_DIR, "S4_whey_corners.csv"),"w",newline="") as f:
    w=csv.writer(f); w.writerow(["R","c_sweet","phi","k","s_ind","f_coag"])
    for r in sorted(corners): w.writerow([f"{r[0]:.2f}"]+[f"{x:.2f}" for x in r[1:]])

# =============== wastewater volume range ===============
WW=(0.5,20.5)  # L wastewater per L milk, as reported in [Al Jobair et al. 2026]
print(f"Volume ratio span {WW[1]/WW[0]:.0f}x; at 300,000 L/d: {300*WW[0]:.0f}-{300*WW[1]:.0f} m3/d")

# =============== Article Figure 5 (two panels) ===============
plt.rcParams.update({"font.family":"serif","font.size":8})
fig,(axa,axb)=plt.subplots(1,2,figsize=(7.0,2.9))
# (a) whey location
f=np.logspace(-2,0,200)
lo=min(c*phi*k/s for c,phi,k,s in itertools.product(C_SWEET,PHI,K,S_IND))/f
hi=max(c*phi*k/s for c,phi,k,s in itertools.product(C_SWEET,PHI,K,S_IND))/f
axa.axvspan(F_COAG[0],F_COAG[1],color="0.35",alpha=0.12,lw=0,label="Scenario range of $f$")
axa.fill_between(f,lo,hi,color="0.6",lw=0,label="Envelope, all parameter ranges")
axa.axhline(1,color="k",lw=0.8,ls="--"); axa.text(0.012,1.25,"artisanal = industrial",fontsize=7)
axa.set_xscale("log"); axa.set_yscale("log")
axa.set_xlabel("Coagulated share of industrial milk, $f$")
axa.set_ylabel("Artisanal / industrial whey, $R$")
axa.legend(frameon=False,fontsize=6.5,loc="upper right")
axa.text(-0.2,1.02,"(a)",transform=axa.transAxes,weight="bold")
# (b) AD energy balance
dT=np.linspace(0,20,200)
axb.fill_between(dT,cod_breakeven(dT,ETA_CH4[1],ETA_B[1]),cod_breakeven(dT,ETA_CH4[0],ETA_B[0]),color="0.75",lw=0,label="Break-even band")
axb.axhspan(min(cods),max(cods),color="0.3",alpha=0.55,lw=0,label="Measured influent COD, Vulta ETP")
axb.set_xlim(0,20); axb.set_ylim(0,15)
axb.text(0.6,8.0,"biogas covers\nheating",fontsize=7); axb.text(12.5,1.0,"heat deficit",fontsize=7)
axb.set_xlabel("Heating required, $T_{dig}-T_{in}$ (K)")
axb.set_ylabel("Influent COD (kg m$^{-3}$)")
axb.legend(frameon=False,fontsize=6.5,loc="upper left")
axb.text(-0.2,1.02,"(b)",transform=axb.transAxes,weight="bold")
fig.tight_layout()
for ext in ("tiff","pdf","png"):
    kw={"dpi":600} if ext=="tiff" else ({"dpi":300} if ext=="png" else {})
    if ext=="tiff": kw["pil_kwargs"]={"compression":"tiff_lzw"}
    fig.savefig(_os.path.join(FIG_DIR, f"Figure_4_bounding.{ext}"),**kw)
