# Author: Tuhin Mahmud
"""
Publication counts (Appendix B) and Figures 2 and 6 of the article.
Queries OpenAlex (free API key required) for the five intervention families, 2010-2026, and writes:
  S3_family_counts.csv        record counts per family (all / CE-framed)      -> Table B.1, Section 7.1
  S3_family_regions.csv       author-country shares by region per family       -> Figure 3b, Table 4
  S3_family_years.csv         records per year per family                       -> trend plot (not in the article)
  Figure_2_provenance.(tiff|pdf|png), Figure_6_inversion.*, Figure_S1_trend.*
Run:   python S3_openalex_family_counts.py YOUR_API_KEY
       (free key: create an account at openalex.org, then copy the key from openalex.org/settings/api;
        since 13 February 2026 OpenAlex requires a key for every request. The key can also be set
        in the environment variable OPENALEX_API_KEY. About 20 calls are made, well within the free daily allowance.)
Test the plotting only (synthetic numbers, figures stamped DEMO):  python S3_openalex_family_counts.py --demo
Redraw the figures from the saved CSV files, without calling OpenAlex:  python S3_openalex_family_counts.py --replot
"""
# ============================================================================
# PASTE YOUR OPENALEX API KEY BETWEEN THE QUOTES BELOW, SAVE, THEN RUN THE FILE.
# (Free key: log in at openalex.org and copy it from openalex.org/settings/api)
MY_API_KEY = ""
# ============================================================================

import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.path.join(_ROOT, "data")       # CSV inputs and outputs
FIG_DIR = _os.path.join(_ROOT, "figures")     # figures are written here
_os.makedirs(FIG_DIR, exist_ok=True)
import sys, os, csv, json, time, datetime, urllib.parse, urllib.request, urllib.error
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

print("Output folder:", os.getcwd())
DEMO = "--demo" in sys.argv
REPLOT = "--replot" in sys.argv
API_KEY = (MY_API_KEY.strip() or next((a for a in sys.argv[1:] if not a.startswith("--")), "")
           or os.environ.get("OPENALEX_API_KEY", ""))
if not DEMO and not REPLOT and not API_KEY:
    raise SystemExit("No API key found. Open this file, paste your key into MY_API_KEY = \"...\" near the top, "
                     "save, and run it again. (Free key: openalex.org/settings/api)")
DAIRY = '(dairy OR "milk processing" OR creamery)'
FAMILIES = {
    "Whey valorization":          f'whey AND (valorisation OR valorization OR "resource recovery" OR "circular economy" OR "by-product") AND {DAIRY}',
    # The dairy restriction was added on 12 November 2026 so that all five queries are like for like.
    # Without it the query returned 2,406 records on that date; the 11,447 recorded on 23 September 2026
    # came from the hyphen in "by-product" being read as two separate words.
    "Anaerobic digestion":        f'("anaerobic digestion" OR UASB OR biogas OR methane) AND {DAIRY} AND (wastewater OR effluent)',
    "Membrane reclamation":       f'(membrane OR "reverse osmosis" OR nanofiltration OR ultrafiltration) AND {DAIRY} AND (wastewater OR effluent) AND (reuse OR reclamation OR recycling)',
    "Residual solids recovery":   f'("white water" OR "cleaning-in-place" OR "clean-in-place" OR CIP OR rinse) AND {DAIRY} AND (recovery OR valorisation OR valorization)',
    "Thermal integration":        f'("heat integration" OR "pinch analysis" OR "heat recovery" OR "energy efficiency" OR "waste heat") AND {DAIRY}',
}
CE = '("circular economy" OR "resource recovery" OR valorisation OR valorization)'
WINDOW = "from_publication_date:2010-01-01,to_publication_date:2026-12-31"
# Verdict order from the verdict table (1 = least obstructed). Membrane and solids share a verdict.
APPLICABILITY = {"Thermal integration":1, "Anaerobic digestion":2, "Membrane reclamation":3.5,
                 "Residual solids recovery":3.5, "Whey valorization":5}
REGIONS = {
 "EU, UK and EFTA": "AT BE BG HR CY CZ DK EE FI FR DE GR HU IE IT LV LT LU MT NL PL PT RO SK SI ES SE GB NO CH IS".split(),
 "North America": "US CA".split(),
 "Oceania": "AU NZ".split(),
 "East Asia": "CN JP KR TW HK".split(),
 "South Asia": "IN PK BD NP LK".split(),
 "Latin America": "BR MX AR CL CO PE UY EC VE CU".split(),
 "Africa": "ZA EG NG KE ET TN MA DZ GH TZ UG".split(),
 "Middle East": "IR TR SA IQ IL JO AE QA KW OM LB".split(),
}
ORIGINATING = ["EU, UK and EFTA", "North America", "Oceania"]

def api(params):
    params = dict(params); params["api_key"] = API_KEY
    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
    shown = url.replace(API_KEY, "YOUR_API_KEY")
    req = urllib.request.Request(url, headers={"User-Agent": "CE-dairy-review S3 script (python urllib)"})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r), shown
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:400]
            print(f"  attempt {attempt+1}: HTTP {e.code} {e.reason}\n  {body}")
            if e.code in (400, 401, 403, 409): break      # not fixed by retrying
            time.sleep(5)
        except Exception as e:
            print(f"  attempt {attempt+1}: {e}"); time.sleep(5)
    raise SystemExit("OpenAlex request failed: " + shown +
                     "\nCheck the message above. 401/403/409 usually means a missing or wrong API key; "
                     "429 means the daily allowance is used up.")

def flt(q): return f"title_and_abstract.search:{q},{WINDOW}"
def count(q):   d,u = api({"filter": flt(q), "per-page": "1"}); return d["meta"]["count"], u
def groups(q, by):
    d,_ = api({"filter": flt(q), "group_by": by, "per-page": "200"}); return d["group_by"]

def region_of(code):
    for r, cs in REGIONS.items():
        if code in cs: return r
    return "Other"

today = datetime.date.today().isoformat()
counts, regions, years = {}, {}, {}
if DEMO:
    rng = np.random.default_rng(1)
    for i,f in enumerate(FAMILIES):
        counts[f] = (int(3000/(i+1)), int(900/(i+1)), "demo")
        sh = rng.dirichlet(np.ones(len(REGIONS)+1)); regions[f] = dict(zip(list(REGIONS)+["Other"], sh))
        years[f] = {y: int(counts[f][0]/17*(0.5+(y-2010)/16)) for y in range(2010,2027)}
elif REPLOT:
    with open(_os.path.join(DATA_DIR, "S3_family_counts.csv"),encoding="utf-8") as fh:
        for r in csv.DictReader(fh): counts[r["family"]] = (int(r["records_2010_2026"]), int(r["records_CE_framed"]), r["url"]); today = r["date_run"]
    with open(_os.path.join(DATA_DIR, "S3_family_regions.csv"),encoding="utf-8") as fh:
        for r in csv.DictReader(fh): regions[r["family"]] = {k: float(r[k]) for k in list(REGIONS)+["Other"]}
    with open(_os.path.join(DATA_DIR, "S3_family_years.csv"),encoding="utf-8") as fh:
        for r in csv.DictReader(fh): years[r["family"]] = {int(k): int(v) for k,v in r.items() if k != "family"}
else:
    for f,q in FAMILIES.items():
        n_all,u = count(q); n_ce,_ = count(f"({q}) AND {CE}")
        counts[f] = (n_all, n_ce, u)
        tot = {}
        for g in groups(q, "authorships.countries"):
            code = str(g["key"]).rstrip("/").split("/")[-1].upper()
            r = region_of(code); tot[r] = tot.get(r,0) + g["count"]
        s = sum(tot.values()) or 1
        regions[f] = {r: tot.get(r,0)/s for r in list(REGIONS)+["Other"]}
        years[f] = {int(g["key"]): g["count"] for g in groups(q, "publication_year")}
        print(f"{f:26s} all={n_all:6d} CE={n_ce:6d}  originating-region share={sum(regions[f][r] for r in ORIGINATING):.0%}")

order = sorted(FAMILIES, key=lambda f: -counts[f][0])
prom_rank = {f:i+1 for i,f in enumerate(order)}
if not REPLOT:
  with open(_os.path.join(DATA_DIR, "S3_family_counts.csv"),"w",newline="",encoding="utf-8") as fh:
      w=csv.writer(fh); w.writerow(["family","records_2010_2026","records_CE_framed","prominence_rank","applicability_rank","date_run","query","url"])
      for f in order: w.writerow([f,counts[f][0],counts[f][1],prom_rank[f],APPLICABILITY[f],today,FAMILIES[f],counts[f][2]])
  with open(_os.path.join(DATA_DIR, "S3_family_regions.csv"),"w",newline="",encoding="utf-8") as fh:
      w=csv.writer(fh); cols=list(REGIONS)+["Other"]; w.writerow(["family"]+cols+["originating_share"])
      for f in order: w.writerow([f]+[f"{regions[f][r]:.3f}" for r in cols]+[f"{sum(regions[f][r] for r in ORIGINATING):.3f}"])
  with open(_os.path.join(DATA_DIR, "S3_family_years.csv"),"w",newline="",encoding="utf-8") as fh:
      w=csv.writer(fh); w.writerow(["family"]+list(range(2010,2027)))
      for f in order: w.writerow([f]+[years[f].get(y,0) for y in range(2010,2027)])

plt.rcParams.update({"font.family":"serif","font.size":8})
def save(fig,name):
    if DEMO: fig.text(0.5,0.5,"DEMO DATA",fontsize=40,color="red",alpha=0.25,ha="center",va="center",rotation=20)
    for ext,kw in (("tiff",{"dpi":600,"pil_kwargs":{"compression":"tiff_lzw"}}),("pdf",{}),("png",{"dpi":300})):
        fig.savefig(_os.path.join(FIG_DIR, f"{name}.{ext}"),**kw)
    plt.close(fig)

# Article Figure 3: (a) counts, (b) region heatmap
fig,(a,b)=plt.subplots(1,2,figsize=(7.2,2.8),gridspec_kw={"width_ratios":[1,1.5]})
y=np.arange(len(order))
a.barh(y,[counts[f][0] for f in order],color="0.6",label="All records")
a.barh(y,[counts[f][1] for f in order],color="0.25",label="CE-framed")
for yy,f in zip(y,order): a.text(counts[f][0]+0.015*max(counts[g][0] for g in order),yy,f"{counts[f][0]:,}",va="center",fontsize=6.5)
a.set_xlim(0,max(counts[f][0] for f in order)*1.18)
a.set_yticks(y,order); a.invert_yaxis(); a.set_xlabel("OpenAlex records, 2010–2026")
a.legend(frameon=False,fontsize=6.5,loc="lower right"); a.text(-0.55,1.03,"(a)",transform=a.transAxes,weight="bold")
cols=list(REGIONS)+["Other"]; M=np.array([[regions[f][r]*100 for r in cols] for f in order])
im=b.imshow(M,cmap="Greys",aspect="auto",vmin=0,vmax=max(60,M.max()))
SHORT={"EU, UK and EFTA":"EU/UK/EFTA","North America":"N. America","Oceania":"Oceania","East Asia":"E. Asia","South Asia":"S. Asia","Latin America":"Lat. America","Africa":"Africa","Middle East":"Mid. East","Other":"Other"}
b.set_xticks(range(len(cols)),[SHORT[c] for c in cols],fontsize=6.5,rotation=40,ha="right")
b.set_yticks(y,[]); 
for i in range(M.shape[0]):
    for j in range(M.shape[1]):
        b.text(j,i,f"{M[i,j]:.0f}",ha="center",va="center",fontsize=6,color="white" if M[i,j]>35 else "black")
b.set_title("Share of author-country affiliations (%)",fontsize=7.5)
b.text(-0.05,1.03,"(b)",transform=b.transAxes,weight="bold")
fig.tight_layout(); save(fig,"Figure_2_provenance")

# Article Figure 7: slope chart prominence rank vs applicability rank
fig,ax=plt.subplots(figsize=(5.6,3.0))
for f in FAMILIES:
    ax.plot([0,1],[prom_rank[f],APPLICABILITY[f]],"-o",color="0.2",lw=1,ms=4)
    ax.text(-0.04,prom_rank[f],f"{f} ({counts[f][0]:,})",ha="right",va="center",fontsize=7)
for r in sorted(set(APPLICABILITY.values())):
    lab={1:"Least obstructed",2:"Conditional",3.5:"Not currently assessable",5:"Low priority"}[r]
    ax.text(1.04,r,lab,ha="left",va="center",fontsize=7)
ax.set_xlim(-0.05,1.05); ax.set_ylim(5.6,0.4); ax.axis("off")
ax.text(-0.04,0.1,"Prominence rank\n(1 = most published)",ha="right",va="bottom",fontsize=7,weight="bold")
ax.text(1.04,0.1,"Verdict\n(1 = least obstructed)",ha="left",va="bottom",fontsize=7,weight="bold")
fig.subplots_adjust(left=0.36,right=0.62,top=0.83,bottom=0.05); save(fig,"Figure_6_inversion")

# Figure S1: trend (log scale so the smaller families are visible)
fig,ax=plt.subplots(figsize=(4.5,2.8))
for f,ls,mk in zip(order,["-","--",":","-.",(0,(5,1,1,1))],["","","","o","s"]):
    vals=[years[f].get(yy,0) for yy in range(2010,2027)]
    ax.plot(range(2010,2027),[v if v>0 else np.nan for v in vals],ls=ls,marker=mk,ms=2.5,color="0.2",lw=1,label=f)
ax.set_yscale("log"); ax.set_ylim(0.8,3000)
ax.axvspan(2025.5,2026.5,color="0.9",zorder=0); ax.text(2026,2000,"2026\npartial",fontsize=5.5,ha="center",va="top")
ax.set_xlim(2009.5,2026.5)
ax.set_xlabel("Publication year"); ax.set_ylabel("OpenAlex records (log scale)"); ax.legend(frameon=False,fontsize=6,ncol=2,loc="upper left")
fig.tight_layout(); save(fig,"Figure_S1_trend")

print("\nProminence order:", " > ".join(order))
top, bottom = order[0], order[-1]
claim = (top == "Whey valorization") and (bottom == "Thermal integration")
pr = np.array([prom_rank[f] for f in FAMILIES]); ap = np.array([APPLICABILITY[f] for f in FAMILIES])
rp = np.argsort(np.argsort(pr)); ra = np.argsort(np.argsort(ap))
rho = np.corrcoef(pr, ap)[0,1]   # ranks already; ties averaged in APPLICABILITY
print(f"Most published: {top}; least published: {bottom}")
print("Original claim holds (most published = whey, least published = thermal)" if claim
      else "Original claim (least published = thermal) does not hold; the text reports the measured order")
print(f"Rank correlation, prominence vs applicability: rho = {rho:.2f} (negative = inversion)")
