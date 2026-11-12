# Author: Tuhin Mahmud
"""Draws Figure 2 of the article (the transfer filter). Conceptual diagram; no data.
Outputs Figure_1_transfer_filter.(tiff|pdf|png) next to this script."""
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.path.join(_ROOT, "data")       # CSV inputs and outputs
FIG_DIR = _os.path.join(_ROOT, "figures")     # figures are written here
_os.makedirs(FIG_DIR, exist_ok=True)
import os
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
plt.rcParams.update({"font.family": "serif", "font.size": 7})

fig, ax = plt.subplots(figsize=(7.2, 3.4))
ax.set_xlim(0, 100); ax.set_ylim(0, 50); ax.axis("off")

fams = ["Whey valorization", "Anaerobic digestion", "Membrane reclamation",
        "Residual solids recovery", "Heat integration"]
ys = [40, 32, 24, 16, 8]
filters = [(33, "Product-mix\ncompatibility"), (51, "Capital and\noperational\nfeasibility"),
           (69, "Informational\nprecondition")]
# where each family is held (x of the filter it stops at, or None if it passes); label
stop = {"Whey valorization": (33, "Low priority"),
        "Anaerobic digestion": (51, "Conditional"),
        "Membrane reclamation": (69, "Not currently assessable"),
        "Residual solids recovery": (69, "Not currently assessable"),
        "Heat integration": (None, "Least obstructed")}

def box(x, y, w, h, text, fc="white", lw=0.8, fs=7, weight="normal"):
    ax.add_patch(FancyBboxPatch((x, y - h/2), w, h, boxstyle="round,pad=0.4,rounding_size=1",
                                fc=fc, ec="0.2", lw=lw))
    ax.text(x + w/2, y, text, ha="center", va="center", fontsize=fs, weight=weight)

ax.text(11, 47.5, "CE intervention set\n(as recommended)", ha="center", va="bottom", fontsize=7, weight="bold")
ax.text(88, 47.5, "Verdict for industrial\ndairy processing", ha="center", va="bottom", fontsize=7, weight="bold")

# filters
for x, lab in filters:
    ax.add_patch(plt.Rectangle((x - 1.6, 3), 3.2, 41, fc="0.82", ec="0.35", lw=0.6, hatch="////"))
    ax.text(x, 1.8, lab, ha="center", va="top", fontsize=6.5)
# bracket showing coupling
ax.annotate("", xy=(67, 45.5), xytext=(35, 45.5),
            arrowprops=dict(arrowstyle="<->", lw=0.6, color="0.3"))
ax.text(51, 46.3, "coupled: a sector short of one precondition\nis usually short of several", ha="center",
        va="bottom", fontsize=5.8, style="normal", color="0.25")

for f, y in zip(fams, ys):
    box(1, y, 20, 5, f)
    xs, verdict = stop[f]
    xend = (xs - 1.8) if xs else 79
    ax.annotate("", xy=(xend, y), xytext=(21.6, y),
                arrowprops=dict(arrowstyle="-|>", lw=1.0, color="0.15", mutation_scale=7))
    if xs:
        ax.plot([xs - 1.6, xs + 1.6], [y, y], color="0.15", lw=2.2)   # blocked at filter
        ax.plot([xs + 1.8, 79], [y, y], ls=(0, (2, 2)), color="0.6", lw=0.7)
    fc = "0.25" if verdict == "Least obstructed" else ("0.6" if verdict == "Conditional" else "white")
    tc = "white" if verdict == "Least obstructed" else "black"
    ax.add_patch(FancyBboxPatch((80, y - 2.5), 17, 5, boxstyle="round,pad=0.4,rounding_size=1",
                                fc=fc, ec="0.2", lw=0.8))
    ax.text(88.5, y, verdict, ha="center", va="center", fontsize=6.5, color=tc)

fig.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.12)
for ext, kw in (("tiff", {"dpi": 600, "pil_kwargs": {"compression": "tiff_lzw"}}), ("pdf", {}), ("png", {"dpi": 300})):
    fig.savefig(_os.path.join(FIG_DIR, f"Figure_1_transfer_filter.{ext}"), **kw)
print("Figure 2 (transfer filter) written")
