# Author: Tuhin Mahmud
"""
Quantitative synthesis for the CE dairy review (Section 6.6, Figure 6, Table 7; Appendix C.3).
(1) Effluent strength by stream type, compiled from Slavov (2017, Food Technol Biotechnol 55:14-28, Table 2),
    the Vulta ETP measurements (Al Jobair et al. 2026) and chhana whey COD estimated from composition.
(2) National chhana-whey generation and organic load for Bangladesh: corner bounds and Monte Carlo.
Every input is a cited value or a declared scenario range; nothing is fitted.
"""
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.path.join(_ROOT, "data")       # CSV inputs and outputs
FIG_DIR = _os.path.join(_ROOT, "figures")     # figures are written here
_os.makedirs(FIG_DIR, exist_ok=True)
import csv, itertools
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ---------------- (1) effluent dataset: COD in g/L (low, high), BOD5 (low, high) or None ----------------
# group, stream, COD_lo, COD_hi, BOD_lo, BOD_hi, source note
DATA = [
 ("Plant effluent","Fluid milk",0.95,2.4,0.5,1.3,"Slavov 2017, Table 2 (after Demirel et al. 2005)"),
 ("Plant effluent","Mixed dairy",0.5,10.4,0.24,5.9,"Slavov 2017, Table 2 (16 sources)"),
 ("Plant effluent","Milk reception",2.54,2.54,0.8,0.8,"Slavov 2017, Table 2 (after Janczukowicz et al. 2008)"),
 ("Plant effluent","Whey processing effluent",1.07,2.18,0.59,1.21,"Slavov 2017, Table 2"),
 ("Plant effluent","Ice cream",5.2,5.2,2.45,2.45,"Slavov 2017, Table 2"),
 ("Plant effluent","Yoghurt",6.5,6.5,None,None,"Slavov 2017, Table 2 (after Un and Ozel 2013)"),
 ("Plant effluent","Butter",8.93,8.93,0.22,2.65,"Slavov 2017, Table 2"),
 ("Plant effluent","Washing wastewater",14.64,14.64,3.47,3.47,"Slavov 2017, Table 2 (after Janczukowicz et al. 2008)"),
 ("Plant effluent","Cottage cheese",17.65,17.65,2.6,2.6,"Slavov 2017, Table 2 (after Janczukowicz et al. 2008)"),
 ("Plant effluent","Cheese",1.0,63.3,0.59,5.0,"Slavov 2017, Table 2 (6 sources)"),
 ("By-product stream","Milk permeate",52.94,57.46,None,None,"Slavov 2017, Table 2"),
 ("By-product stream","Soft cheese whey",58.55,58.55,26.77,26.77,"Slavov 2017, Table 2 (after Janczukowicz et al. 2008)"),
 ("By-product stream","Hard cheese whey",73.45,73.45,9.48,9.48,"Slavov 2017, Table 2 (after Janczukowicz et al. 2008)"),
 ("By-product stream","Cottage cheese (acid) whey",79.0,79.0,None,None,"Slavov 2017, Table 2 (after Carvalho et al. 2013)"),
 ("By-product stream","Cheese whey",50.0,102.1,27.0,60.0,"Slavov 2017, Table 2 (8 sources)"),
]
VULTA = (2.221, 2.650, 1.175, 1.331)   # Al Jobair et al. 2026, three seasons

# chhana whey COD estimated from composition
TS_CHW = (0.0415, 0.060)        # total solids, mass fraction: 4.15-5.29% cow milk (Chakraborty et al. 2021); ~6% (Jindal et al. 1992)
# ThOD per g whey solids from chhana whey powder composition (Jindal et al. 1992): per 956 g TS: lactose 750, protein 21, fat 60, ash 65
comp = {"lactose":750/956, "protein":21/956, "fat":60/956}
THOD = {"lactose":1.123, "protein":1.50, "fat":2.88}   # g O2/g: C12H22O11 stoichiometry; typical protein; tripalmitin
cod_ts_thod = sum(comp[k]*THOD[k] for k in comp)
cod_ts_whey = (72/6.2*0.1, 77/6.0*0.1)   # cheese whey COD 72-77 g/kg at 6.0-6.2% TS (Slavov 2017, Table 1) -> g COD per g TS
COD_TS = (min(cod_ts_thod, *cod_ts_whey), max(cod_ts_thod, *cod_ts_whey))
CHW_COD = (TS_CHW[0]*1000*COD_TS[0], TS_CHW[1]*1000*COD_TS[1])     # g/L (whey density taken as 1 kg/L)
print(f"COD/TS: ThOD from composition {cod_ts_thod:.2f}; cheese-whey ratio {cod_ts_whey[0]:.2f}-{cod_ts_whey[1]:.2f} -> range {COD_TS[0]:.2f}-{COD_TS[1]:.2f}")
print(f"Chhana whey COD estimate: {CHW_COD[0]:.0f}-{CHW_COD[1]:.0f} g/L")

with open(_os.path.join(DATA_DIR, "S6_effluent_strength_dataset.csv"),"w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow(["group","stream","COD_low_gL","COD_high_gL","BOD5_low_gL","BOD5_high_gL","source"])
    for r in DATA: w.writerow(r)
    w.writerow(["Plant effluent (Bangladesh)","Vulta ETP influent, three seasons",*VULTA,"Al Jobair et al. 2026"])
    w.writerow(["By-product stream (estimated)","Chhana whey",round(CHW_COD[0],1),round(CHW_COD[1],1),"","","Estimated: TS (Chakraborty et al. 2021; Jindal et al. 1992) x COD/TS (composition, Jindal et al. 1992; cheese whey ratio, Slavov 2017 Table 1)"])

# ---------------- (2) national chhana whey estimate ----------------
P    = 15.538e9     # kg milk per year, DLS Livestock Economy at a Glance 2024-25 (provisional); 14.068e9 in 2022-23
C    = (0.50, 0.55) # share of national milk to sweetmeat channel (UNIDO 2019; RVO 2023)
PHI  = (0.30, 1.00) # fraction of sweetmeat-channel milk coagulated to chhana (scenario, as Section 6.5)
WY   = (0.795, 0.815) # whey mass per mass milk (Chakraborty et al. 2021: 79.5-81.4% across milk types; cow 81.0-81.4%)
TS   = TS_CHW
CT   = COD_TS
BC   = (0.4, 0.8)   # BOD5/COD for dairy streams (Slavov 2017)
PE_BOD = 0.060      # kg BOD5 per person-equivalent per day (Council Directive 91/271/EEC)
Y_CH4, E_CH4 = 0.350, 35.79   # m3/kg COD; MJ/m3
ETA = (0.5, 0.8)    # fraction of COD converted to methane (as Section 6.5)
VULTA_LOAD = 48*np.mean(VULTA[:2])*365/1000   # t COD/yr at 48 m3/d

def model(c,phi,wy,ts,ct,bc,eta):
    whey = P*c*phi*wy                    # kg/yr
    cod  = whey*ts*ct                    # kg COD/yr
    pe   = cod*bc/365/PE_BOD             # persons
    energy = cod*eta*Y_CH4*E_CH4         # MJ/yr
    return whey, cod, pe, energy

corners=[model(*v) for v in itertools.product(C,PHI,WY,TS,CT,BC,ETA)]
arr=np.array(corners)
rng=np.random.default_rng(20260923); N=200_000
u=lambda r: rng.uniform(r[0],r[1],N)
mc=np.array(model(u(C),u(PHI),u(WY),u(TS),u(CT),u(BC),u(ETA)))
def q(x): return np.percentile(x,[5,50,95])
names=["Whey generated (Mt/yr)","COD load (kt/yr)","Population equivalent (million)","Methane energy (PJ/yr)"]
scale=[1e9,1e6,1e6,1e9]
rows=[]
for i,(n,s) in enumerate(zip(names,scale)):
    lo,hi=arr[:,i].min()/s,arr[:,i].max()/s; p5,p50,p95=q(mc[i])/s
    rows.append((n,lo,p5,p50,p95,hi)); print(f"{n:34s} bounds {lo:7.2f}-{hi:7.2f} | MC median {p50:7.2f} (5-95%: {p5:.2f}-{p95:.2f})")
cod_med=np.median(mc[1]); print(f"Median COD load = {cod_med/1e3/VULTA_LOAD:,.0f} x the Vulta ETP influent load ({VULTA_LOAD:.0f} t COD/yr)")
print(f"Methane power, median: {np.median(mc[3])/(365*86400):.1f} MW (thermal, chemical energy)")
with open(_os.path.join(DATA_DIR, "S6_national_whey_estimate.csv"),"w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow(["quantity","min_corner","MC_p5","MC_median","MC_p95","max_corner"])
    for r in rows: w.writerow([r[0]]+[f"{v:.3g}" for v in r[1:]])
# sensitivity: share of variance by input (squared rank correlation, normalised)
inputs={"c":u(C),"phi":u(PHI),"whey yield":u(WY),"TS":u(TS),"COD/TS":u(CT)}
cod_s=model(inputs["c"],inputs["phi"],inputs["whey yield"],inputs["TS"],inputs["COD/TS"],0.6,0.65)[1]
rk=lambda x: np.argsort(np.argsort(x))
r2={k:np.corrcoef(rk(v),rk(cod_s))[0,1]**2 for k,v in inputs.items()}; tot=sum(r2.values())
sens={k:v/tot for k,v in r2.items()}
print("Share of COD-load uncertainty:", {k:f"{v:.0%}" for k,v in sens.items()})
with open(_os.path.join(DATA_DIR, "S6_sensitivity.csv"),"w",newline="") as fh:
    w=csv.writer(fh); w.writerow(["input","share_of_rank_variance"]); [w.writerow([k,f"{v:.3f}"]) for k,v in sens.items()]

# ---------------- Figure 5 ----------------
plt.rcParams.update({"font.family":"serif","font.size":7.5})
fig,(a,b)=plt.subplots(1,2,figsize=(7.2,3.6),gridspec_kw={"width_ratios":[1.45,1]})
items=[(g,s,lo,hi) for g,s,lo,hi,*_ in DATA]
items=sorted([i for i in items if i[0]=="Plant effluent"],key=lambda t:t[3])+[("x","Vulta ETP influent (Bangladesh)",VULTA[0],VULTA[1])]+ \
      sorted([i for i in items if i[0]!="Plant effluent"],key=lambda t:t[3])+[("e","Chhana whey (estimated)",*CHW_COD)]
y=np.arange(len(items))
for yi,(g,s,lo,hi) in zip(y,items):
    col={"Plant effluent":"0.45","x":"k","By-product stream":"0.15","e":"k"}[g]
    if hi/lo<1.08: a.plot([lo],[yi],"o",color=col,ms=3.5)
    else: a.plot([lo,hi],[yi,yi],"-",color=col,lw=3 if g in("x","e") else 2,solid_capstyle="butt")
    if g=="e": a.plot([lo,hi],[yi,yi],color="white",lw=1,ls=(0,(2,1.5)))
a.axvspan(2.3,4.8,color="0.85",lw=0,zorder=0); a.text(3.3,-0.9,"AD self-heating\nthreshold, 5 K",ha="center",va="top",fontsize=6)
a.set_ylim(-2.2,len(items)-0.4)
a.set_xscale("log"); a.set_yticks(y,[i[1] for i in items]); a.set_xlabel("COD (g L$^{-1}$), reported range")
a.axhline(sum(1 for i in items if i[0] in("Plant effluent","x"))-0.5,color="0.6",lw=0.6)
a.text(-0.02,1.03,"(a)",transform=a.transAxes,weight="bold",ha="right")
cod_kt=mc[1]/1e6
b.hist(cod_kt,bins=60,color="0.55",edgecolor="none")
for v,l in zip(q(cod_kt),["5%","median","95%"]): b.axvline(v,color="k",lw=0.8,ls="--" if l!="median" else "-")
b.set_xlabel("Chhana whey COD load (kt yr$^{-1}$)"); b.set_ylabel("Monte Carlo samples"); b.set_yticks([])
p5,p50,p95=q(cod_kt)
b.set_title(f"median {p50:.0f} kt/yr (90%: {p5:.0f}–{p95:.0f})\n≈ {np.median(mc[2])/1e6:.1f} million person-equivalents",fontsize=7)
b.text(-0.08,1.13,"(b)",transform=b.transAxes,weight="bold",ha="right")
fig.tight_layout()
for ext,kw in (("tiff",{"dpi":600,"pil_kwargs":{"compression":"tiff_lzw"}}),("pdf",{}),("png",{"dpi":300})):
    fig.savefig(_os.path.join(FIG_DIR, f"Figure_5_quant_synthesis.{ext}"),**kw)
