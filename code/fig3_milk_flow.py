# Author: Tuhin Mahmud
"""Figure 4 of the article - national milk channels in Bangladesh and where coagulation-derived whey arises.
Shares: UNIDO (2019) [9]: 15% household, 80% informal trade, 5% formal industrial collection.
Sweetmeat channel ~50-55% of national milk: RVO (2023) [10] ~55%, UNIDO [9] ~half; drawn at 52.5%
and assumed to lie within informal trade. The split of industrial milk between fluid and
coagulated products is not measured: drawn schematically and labelled as such."""
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.path.join(_ROOT, "data")       # CSV inputs and outputs
FIG_DIR = _os.path.join(_ROOT, "figures")     # figures are written here
_os.makedirs(FIG_DIR, exist_ok=True)
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch, Rectangle
plt.rcParams.update({"font.family":"serif","font.size":8})
fig,ax=plt.subplots(figsize=(7.2,3.9)); ax.set_xlim(0,10.4); ax.set_ylim(-3,126); ax.axis("off")
def band(x0,y0,x1,y1,h0,h1,c,a=0.55):
    xm=(x0+x1)/2
    v=[(x0,y0),(xm,y0),(xm,y1),(x1,y1),(x1,y1+h1),(xm,y1+h1),(xm,y0+h0),(x0,y0+h0),(x0,y0)]
    k=[Path.MOVETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.LINETO,Path.CURVE4,Path.CURVE4,Path.CURVE4,Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(v,k),fc=c,ec="none",alpha=a))
W=0.14
def node(x,y,h): ax.add_patch(Rectangle((x,y),W,h,fc="0.15",ec="none"))
L,M,D="0.72","0.50","0.30"
x1,x2,x3=1.5,4.6,7.4
# sources (bottom->top): household 0-15, informal 15-95, industrial 95-100
node(x1,0,100); ax.text(x1-0.12,50,"National milk\nproduction\n(100%)",ha="right",va="center")
yh,yi,yd=0,20,112          # destination bottoms in column 2
node(x2,yh,15); node(x2,yi,80); node(x2,yd,5)
band(x1+W,0,x2,yh,15,15,L); band(x1+W,15,x2,yi,80,80,L); band(x1+W,95,x2,yd,5,5,M)
bb=dict(fc="white",ec="none",pad=1.2,alpha=0.9)
ax.text(x2+W+0.08,yh+7.5,"Household consumption 15%",va="center")
ax.text(x2-0.08,yi+40,"Informal\ntrade\n80%",ha="right",va="center",bbox=bb)
ax.text(x2-0.08,yd+2.5,"Formal industrial\ncollection 5%",ha="right",va="center",bbox=bb)
# column 3
S=52.5; O=80-S
ys,yo=yi,yi+S+4
node(x3,ys,S); node(x3,yo,O)
band(x2+W,yi,x3,ys,S,S,D,0.5); band(x2+W,yi+S,x3,yo,O,O,L)
yf,yc=yd+6.0,yd-1.5        # industrial split (schematic 4.2 / 0.8)
node(x3,yf,4.2); node(x3,yc,0.8)
band(x2+W,yd+0.8,x3,yf,4.2,4.2,M); band(x2+W,yd,x3,yc,0.8,0.8,D,0.9)
tx=x3+W+0.12
ax.text(tx,ys+S/2+7,"Sweetmeat channel ~50–55%",va="center",weight="bold")
ax.text(tx,ys+S/2-5,"chhana (coagulated): whey generated\nin aggregate, dispersed across\nartisanal producers",va="center")
ax.text(tx,yo+O/2,"Other informal\n(liquid milk, ghee, yoghurt)",va="center")
ax.text(tx,yf+2.1,"Fluid, UHT, fermented, powder",va="center")
ax.text(tx,yc-2.0,"Coagulated (e.g. mozzarella): whey at plant\n(minor; share unmeasured, width schematic)",va="center")
fig.tight_layout()
for ext,kw in (("tiff",{"dpi":600,"pil_kwargs":{"compression":"tiff_lzw"}}),("pdf",{}),("png",{"dpi":300})):
    fig.savefig(_os.path.join(FIG_DIR, f"Figure_3_milk_flow.{ext}"),**kw)
