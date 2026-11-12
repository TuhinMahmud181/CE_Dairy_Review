# Author: Tuhin Mahmud
"""
Robustness checks for the national chhana-whey COD estimate (Section 6.6; Appendix C.3).
Inputs, ranges and model are imported unchanged from quant_synthesis.py.
(1) Alternative distribution: symmetric triangular on each range instead of uniform.
(2) Correlated inputs: Gaussian copula on the uniform marginals, testing the pairs most plausibly dependent
    (TS with COD/TS; whey yield with TS; c with phi), at rank correlation +/-0.8.
(3) One-at-a-time: each input fixed at its midpoint in turn; change in the 90% interval.
"""
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.path.join(_ROOT, "data")       # CSV inputs and outputs
FIG_DIR = _os.path.join(_ROOT, "figures")     # figures are written here
_os.makedirs(FIG_DIR, exist_ok=True)
import csv, io, contextlib
import numpy as np
from scipy.stats import norm
with contextlib.redirect_stdout(io.StringIO()):
    import quant_synthesis as Q          # re-runs the base analysis silently
N=200_000; SEED=20260923
R={"c":Q.C,"phi":Q.PHI,"whey yield":Q.WY,"TS":Q.TS,"COD/TS":Q.CT}
BC_MID, ETA_MID = 0.6, 0.65
def cod(v): return Q.model(v["c"],v["phi"],v["whey yield"],v["TS"],v["COD/TS"],BC_MID,ETA_MID)[1]/1e6  # kt/yr
def summ(x): p5,p50,p95=np.percentile(x,[5,50,95]); return p50,p5,p95
rows=[]
rng=np.random.default_rng(SEED)
base={k:rng.uniform(a,b,N) for k,(a,b) in R.items()}
rows.append(("Base case: uniform, independent",*summ(cod(base))))
rng=np.random.default_rng(SEED)
tri={k:rng.triangular(a,(a+b)/2,b,N) for k,(a,b) in R.items()}
rows.append(("Triangular, independent",*summ(cod(tri))))
def copula(pair,rho):
    rng=np.random.default_rng(SEED); keys=list(R); z=rng.standard_normal((N,len(keys)))
    i,j=keys.index(pair[0]),keys.index(pair[1])
    rp=2*np.sin(np.pi*rho/6)               # Spearman -> Pearson for Gaussian copula
    z[:,j]=rp*z[:,i]+np.sqrt(1-rp**2)*z[:,j]
    u=norm.cdf(z); return {k:R[k][0]+u[:,n]*(R[k][1]-R[k][0]) for n,k in enumerate(keys)}
for pair in [("TS","COD/TS"),("whey yield","TS"),("c","phi")]:
    for rho in (0.8,-0.8):
        rows.append((f"Uniform, rank corr. {pair[0]}–{pair[1]} = {rho:+.1f}",*summ(cod(copula(pair,rho)))))
for k in R:
    rng=np.random.default_rng(SEED); v={kk:rng.uniform(a,b,N) for kk,(a,b) in R.items()}
    v[k]=np.full(N,np.mean(R[k])); rows.append((f"Uniform, {k} fixed at midpoint",*summ(cod(v))))
with open(_os.path.join(DATA_DIR, "S6_robustness.csv"),"w",newline="",encoding="utf-8") as fh:
    w=csv.writer(fh); w.writerow(["case","median_kt_COD_yr","p5","p95","interval_width_kt"])
    for r in rows: w.writerow([r[0]]+[f"{x:.0f}" for x in r[1:]]+[f"{r[3]-r[2]:.0f}"])
for r in rows: print(f"{r[0]:48s} median {r[1]:5.0f}  90%: {r[2]:4.0f}-{r[3]:4.0f}  width {r[3]-r[2]:4.0f}")
