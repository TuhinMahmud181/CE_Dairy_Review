# Author: Tuhin Mahmud
import os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA_DIR = _os.path.join(_ROOT, "data")       # CSV inputs and outputs
FIG_DIR = _os.path.join(_ROOT, "figures")     # figures are written here
_os.makedirs(FIG_DIR, exist_ok=True)
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, Wedge, Polygon, Ellipse, PathPatch
from matplotlib.path import Path
plt.rcParams['font.family']='DejaVu Sans'
fig,ax=plt.subplots(figsize=(10.3,6.3)); ax.set_xlim(0,106); ax.set_ylim(0,63); ax.axis('off'); ax.set_aspect('equal')
K='#333333'; STEEL='#c3c9cf'; STEELD='#8e979f'; BLUE='#4a90c2'; LBLUE='#bcdcf0'; GREEN='#6aa84f'; ORANGE='#e58a2b'; YEL='#f4c542'; RED='#c94f3d'; PINK='#f2b8b8'; CREAM='#fbf3dc'
def P(patch,z=3): patch.set_zorder(z); ax.add_patch(patch); return patch
# ---------------------------------------------------------------- pictograms
def cow(x,y,s=1.0,flip=False):
    d=-1 if flip else 1
    for lx in (-2.1,-1.3,1.2,2.0): P(Rectangle((x+d*lx*s-0.25*s,y-3.3*s),0.5*s,2.2*s,fc='white',ec=K,lw=0.8),2)
    for lx in (-2.1,-1.3,1.2,2.0): P(Rectangle((x+d*lx*s-0.25*s,y-3.3*s),0.5*s,0.4*s,fc=K,ec=K,lw=0.5),3)
    P(Ellipse((x-d*0.9*s,y-1.55*s),1.3*s,0.9*s,fc=PINK,ec=K,lw=0.7),2)
    body=P(Ellipse((x,y),6.0*s,3.2*s,fc='white',ec=K,lw=0.9),4)
    for (sx,sy,sw,sh) in ((-1.2,0.5,2.2,1.6),(1.1,-0.4,1.6,1.3),(-2.6,-0.6,1.1,1.0)):
        sp=P(Ellipse((x+d*sx*s,y+sy*s),sw*s,sh*s,fc=K,ec='none'),5); sp.set_clip_path(body)
    ax.plot([x-d*2.95*s,x-d*3.5*s,x-d*3.4*s],[y+0.4*s,y-0.6*s,y-1.7*s],color=K,lw=0.9,zorder=3)
    P(Ellipse((x+d*3.3*s,y+1.25*s),0.9*s,0.45*s,angle=d*30,fc='white',ec=K,lw=0.7),5)
    P(Ellipse((x+d*3.2*s,y+0.5*s),2.0*s,1.6*s,fc='white',ec=K,lw=0.9),6)
    P(Ellipse((x+d*3.95*s,y+0.15*s),0.9*s,0.8*s,fc=PINK,ec=K,lw=0.7),7)
    P(Circle((x+d*3.1*s,y+0.75*s),0.13*s,fc=K,ec=K),8)
def barn(x,y,s=1.0):
    P(Rectangle((x,y),8*s,5*s,fc=RED,ec=K,lw=0.9))
    P(Polygon([[x-0.5*s,y+5*s],[x+1.2*s,y+7.3*s],[x+4*s,y+8.6*s],[x+6.8*s,y+7.3*s],[x+8.5*s,y+5*s]],fc='#5a4a42',ec=K,lw=0.9))
    P(Rectangle((x+2.9*s,y),2.2*s,3.2*s,fc='white',ec=K,lw=0.8),4)
    ax.plot([x+2.9*s,x+5.1*s],[y,y+3.2*s],color=K,lw=0.7,zorder=5); ax.plot([x+2.9*s,x+5.1*s],[y+3.2*s,y],color=K,lw=0.7,zorder=5)
    P(Rectangle((x+3.3*s,y+5.6*s),1.4*s,1.2*s,fc='white',ec=K,lw=0.7),4)
def silo(x,y,s=1.0):
    P(Rectangle((x,y),2.8*s,8.5*s,fc=STEEL,ec=K,lw=0.9)); P(Wedge((x+1.4*s,y+8.5*s),1.4*s,0,180,fc=STEELD,ec=K,lw=0.9))
    for k in (2.2,4.4,6.6): ax.plot([x,x+2.8*s],[y+k*s,y+k*s],color=STEELD,lw=0.7,zorder=4)
def bottle(x,y,s=1.0):
    P(FancyBboxPatch((x,y),1.9*s,3.4*s,boxstyle='round,pad=0,rounding_size=%f'%(0.35*s),fc='white',ec=K,lw=0.9))
    P(Rectangle((x+0.55*s,y+3.4*s),0.8*s,0.9*s,fc='white',ec=K,lw=0.9)); P(Rectangle((x+0.45*s,y+4.3*s),1.0*s,0.45*s,fc=BLUE,ec=K,lw=0.8))
    P(Rectangle((x+0.12*s,y+1.0*s),1.66*s,1.2*s,fc=LBLUE,ec='none'),4)
def cheese(x,y,s=1.0):
    P(Polygon([[x,y],[x+4.2*s,y],[x+4.2*s,y+1.5*s],[x,y+1.5*s]],fc=YEL,ec=K,lw=0.9)); P(Polygon([[x,y+1.5*s],[x+4.2*s,y+1.5*s],[x+4.2*s,y+3.0*s]],fc='#f7d76a',ec=K,lw=0.9))
    for hx,hy,hr in ((0.9,0.7,0.3),(2.3,0.5,0.22),(3.3,0.95,0.3)): P(Circle((x+hx*s,y+hy*s),hr*s,fc='#d9a520',ec='none'),4)
def cup(x,y,s=1.0):
    P(Polygon([[x,y+2.6*s],[x+2.2*s,y+2.6*s],[x+1.8*s,y],[x+0.4*s,y]],fc='white',ec=K,lw=0.9)); P(Rectangle((x-0.15*s,y+2.6*s),2.5*s,0.35*s,fc=GREEN,ec=K,lw=0.8))
def pond(x,y,s=1.0):
    P(Wedge((x,y),5.2*s,180,360,fc='#9db7c7',ec=K,lw=0.9)); P(Ellipse((x,y),10.4*s,1.6*s,fc='#b9cfdb',ec=K,lw=0.9),4)
    P(Rectangle((x+3.0*s,y+3.2*s),5.0*s,1.3*s,fc=STEELD,ec=K,lw=0.9),5); P(Rectangle((x+2.3*s,y+2.2*s),1.3*s,2.3*s,fc=STEELD,ec=K,lw=0.9),5)
    for k,(dx,dy) in enumerate(((2.95,1.5),(2.95,0.7),(3.3,1.1),(2.6,1.0))): P(Ellipse((x+dx*s,y+dy*s),0.3*s,0.55*s,fc='#7fa3b8',ec='none'),6)
# equipment
def eq_whey(x,y):      # membrane vessel feeding a spray dryer, with a product sack
    P(FancyBboxPatch((x-6.2,y+0.6),4.6,1.5,boxstyle='round,pad=0,rounding_size=0.7',fc=STEEL,ec=K,lw=0.9)); P(FancyBboxPatch((x-6.2,y-1.6),4.6,1.5,boxstyle='round,pad=0,rounding_size=0.7',fc=STEEL,ec=K,lw=0.9))
    for yy in (y+1.35,y-0.85): ax.plot([x-5.6,x-2.2],[yy,yy],color=STEELD,lw=0.8,ls=(0,(2,1.2)),zorder=4)
    P(Rectangle((x-6.6,y-2.6),0.4,5.2,fc=STEELD,ec=K,lw=0.7),2); P(Rectangle((x-1.6,y-2.6),0.4,5.2,fc=STEELD,ec=K,lw=0.7),2)
    ax.plot([x-1.2,x+0.4,x+0.4],[y+1.35,y+1.35,y+2.6],color=K,lw=1.2,zorder=2)
    P(Rectangle((x+0.2,y-0.2),3.6,3.3,fc=STEEL,ec=K,lw=0.9)); P(Polygon([[x+0.2,y-0.2],[x+3.8,y-0.2],[x+2.3,y-2.6],[x+1.7,y-2.6]],fc=STEEL,ec=K,lw=0.9)); P(Wedge((x+2.0,y+3.1),1.8,0,180,fc=STEELD,ec=K,lw=0.9))
    for a in (-120,-100,-80,-60): ax.plot([x+2.0,x+2.0+1.5*np.cos(np.radians(a))],[y+2.7,y+2.7+1.5*np.sin(np.radians(a))],color='white',lw=0.8,zorder=4)
    P(FancyBboxPatch((x+4.6,y-2.6),2.2,2.9,boxstyle='round,pad=0,rounding_size=0.5',fc=CREAM,ec=K,lw=0.9)); ax.plot([x+5.0,x+6.4],[y-0.1,y-0.1],color=K,lw=0.6,zorder=4)
def eq_ad(x,y):        # digester with gas dome and flare
    P(Rectangle((x-5.2,y-2.6),7.2,3.4,fc=STEEL,ec=K,lw=0.9)); P(Wedge((x-1.6,y+0.8),3.6,0,180,fc=GREEN,ec=K,lw=0.9)).set_alpha(0.9)
    P(Rectangle((x-5.2,y-2.6),7.2,1.2,fc='#8a6f4d',ec=K,lw=0.7),4)
    for bx,by in ((-3.9,-0.7),(-2.2,-0.2),(-0.6,-0.8),(0.8,-0.3)): P(Circle((x+bx,y+by),0.28,fc='white',ec=STEELD,lw=0.6),5)
    ax.plot([x-1.6,x-1.6,x+4.6,x+4.6],[y+4.4,y+5.0,y+5.0,y+1.4],color=K,lw=1.3,zorder=2)
    P(Rectangle((x+4.25,y-2.6),0.7,4.0,fc=STEELD,ec=K,lw=0.8))
    flame(x+4.6,y+2.5,0.9)
def eq_membrane(x,y):  # rack of pressure vessels with pump
    P(Rectangle((x-5.6,y-2.6),0.45,5.6,fc=STEELD,ec=K,lw=0.7),2); P(Rectangle((x+3.2,y-2.6),0.45,5.6,fc=STEELD,ec=K,lw=0.7),2)
    for k,yy in enumerate((y+1.7,y-0.1,y-1.9)):
        P(FancyBboxPatch((x-5.0,yy-0.65),8.0,1.3,boxstyle='round,pad=0,rounding_size=0.6',fc='white',ec=K,lw=0.9)); P(Rectangle((x-4.2,yy-0.45),6.4,0.9,fc=LBLUE,ec='none'),4)
        for xx in np.linspace(x-3.8,x+1.8,6): ax.plot([xx,xx],[yy-0.45,yy+0.45],color=BLUE,lw=0.6,zorder=5)
    P(Circle((x+5.4,y-1.7),1.0,fc=STEEL,ec=K,lw=0.9)); P(Polygon([[x+5.0,y-2.2],[x+5.0,y-1.2],[x+6.0,y-1.7]],fc=K,ec=K),4)
    ax.plot([x+3.65,x+5.4,x+5.4],[y+1.7,y+1.7,y-0.7],color=K,lw=1.2,zorder=2)
def eq_cip(x,y):       # tank with spray ball and recovery loop
    P(FancyBboxPatch((x-4.6,y-2.0),4.4,5.0,boxstyle='round,pad=0,rounding_size=1.0',fc=STEEL,ec=K,lw=0.9)); 
    for lx in (-4.0,-0.8): P(Rectangle((x+lx-0.2,y-2.7),0.4,0.8,fc=STEELD,ec=K,lw=0.6),2)
    P(Circle((x-2.4,y+1.9),0.35,fc=K,ec=K),5)
    for a in (-150,-125,-100,-80,-55,-30): ax.plot([x-2.4,x-2.4+1.9*np.cos(np.radians(a))],[y+1.9,y+1.9+1.9*np.sin(np.radians(a))],color=BLUE,lw=0.8,zorder=4)
    P(Rectangle((x-4.5,y-1.9),4.2,1.1,fc='white',ec='none'),4)
    ax.plot([x-2.4,x-2.4,x+2.2,x+2.2],[y+3.0,y+3.8,y+3.8,y+1.0],color=K,lw=1.2,zorder=2); ax.plot([x-0.2,x+1.0],[y-1.3,y-1.3],color=K,lw=1.2,zorder=2)
    P(FancyBboxPatch((x+1.0,y-2.6),2.6,3.6,boxstyle='round,pad=0,rounding_size=0.5',fc='white',ec=K,lw=0.9)); P(Rectangle((x+1.1,y-2.5),2.4,2.0,fc=CREAM,ec='none'),4)
    P(Circle((x+4.9,y-1.7),0.9,fc=STEEL,ec=K,lw=0.9)); ax.plot([x+3.6,x+4.0],[y-1.7,y-1.7],color=K,lw=1.2,zorder=2)
def eq_heat(x,y):      # plate heat exchanger with hot and cold arrows
    P(Rectangle((x-4.6,y-2.4),0.7,5.0,fc=STEELD,ec=K,lw=0.9)); P(Rectangle((x+1.9,y-2.4),0.7,5.0,fc=STEELD,ec=K,lw=0.9))
    for k,xx in enumerate(np.linspace(x-3.7,x+1.5,11)): P(Rectangle((xx,y-2.0),0.34,4.2,fc=(RED if k%2==0 else BLUE),ec=K,lw=0.4)).set_alpha(0.85)
    ax.plot([x-4.6,x+2.6],[y+2.9,y+2.9],color=K,lw=1.0,zorder=2); ax.plot([x-4.6,x+2.6],[y-2.7,y-2.7],color=K,lw=1.0,zorder=2)
    for (x0,y0,x1,y1,c) in ((x-7.0,y+1.5,x-4.8,y+1.5,RED),(x+2.8,y+1.5,x+5.0,y+1.5,BLUE),(x+5.0,y-1.3,x+2.8,y-1.3,BLUE),(x-4.8,y-1.3,x-7.0,y-1.3,RED)):
        ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle='-|>',mutation_scale=9,lw=1.6,color=c,zorder=6))
# resources
def flame(x,y,s=1.0):
    t=np.linspace(0,2*np.pi,60); 
    def shape(k): return np.c_[x+k*s*0.75*np.sin(t)*(1-0.55*np.cos(t))/1.3, y+k*s*(0.9-1.25*np.cos(t)) - (1-k)*s*0.3]
    P(Polygon(shape(1.0),fc=ORANGE,ec=K,lw=0.7),6); P(Polygon(shape(0.55),fc=YEL,ec='none'),7)
def drop(x,y,s=1.0,c=BLUE):
    t=np.linspace(0,2*np.pi,60); P(Polygon(np.c_[x+s*1.25*np.sin(t)*(1-np.cos(t))/2*1.15, y+s*1.6*np.cos(t)-0.3*s],fc=c,ec=K,lw=0.8),6)
    P(Ellipse((x-0.4*s,y-1.0*s),0.3*s,0.7*s,angle=20,fc='white',ec='none',alpha=0.7),7)
def sack(x,y,s=1.0):
    P(FancyBboxPatch((x-1.5*s,y-1.9*s),3.0*s,3.4*s,boxstyle='round,pad=0,rounding_size=%f'%(0.6*s),fc=CREAM,ec=K,lw=0.9)); P(Polygon([[x-1.1*s,y+1.5*s],[x+1.1*s,y+1.5*s],[x+1.5*s,y+2.2*s],[x-1.5*s,y+2.2*s]],fc=CREAM,ec=K,lw=0.9))
    P(Rectangle((x-0.95*s,y-0.9*s),1.9*s,1.3*s,fc='white',ec=K,lw=0.6),5)
def churn(x,y,s=1.0):
    P(FancyBboxPatch((x-1.3*s,y-1.9*s),2.6*s,2.9*s,boxstyle='round,pad=0,rounding_size=%f'%(0.4*s),fc=STEEL,ec=K,lw=0.9)); P(Polygon([[x-1.3*s,y+1.0*s],[x+1.3*s,y+1.0*s],[x+0.7*s,y+1.8*s],[x-0.7*s,y+1.8*s]],fc=STEEL,ec=K,lw=0.9)); P(Rectangle((x-0.9*s,y+1.8*s),1.8*s,0.45*s,fc=STEELD,ec=K,lw=0.8))
    ax.plot([x-1.3*s,x+1.3*s],[y-0.9*s,y-0.9*s],color=STEELD,lw=0.8,zorder=5); P(Ellipse((x,y+0.15*s),1.5*s,0.9*s,fc='white',ec='none'),5)
def heat(x,y,s=1.0):
    yy=np.linspace(-1.9*s,1.9*s,50)
    for dx in (-1.0,0,1.0): ax.plot(x+dx*s+0.32*s*np.sin(yy/s*2.6),y+yy,color=RED,lw=2.2,solid_capstyle='round',zorder=6)
    for dx in (-1.0,0,1.0): P(Polygon([[x+dx*s-0.45*s+0.2*s,y+1.75*s],[x+dx*s+0.45*s+0.2*s,y+1.75*s],[x+dx*s+0.2*s,y+2.6*s]],fc=RED,ec='none'),6)
# ---------------------------------------------------------------- left: source
ax.text(11,61.2,'Dairy farming',ha='center',va='center',fontsize=10.5,fontweight='bold')
barn(2.6,50.6,0.85); silo(11.6,50.6,0.85); 
P(Ellipse((11,42.0),22,3.2,fc='#dcebd0',ec='none'),1)
cow(5.6,45.2,0.95); cow(16.2,44.4,0.95,flip=True)
ax.add_patch(FancyArrowPatch((11,39.9),(11,36.6),arrowstyle='-|>',mutation_scale=13,lw=1.8,color=K))
P(Circle((11,29.6),6.6,fc='#eef4fa',ec=BLUE,lw=1.4),1)
bottle(5.9,27.0,0.95); cup(8.7,26.9,0.9); cheese(11.6,27.0,0.9); 
ax.text(11,33.4,'milk · yoghurt · cheese',ha='center',va='center',fontsize=6.6,color='#555555')
ax.text(11,21.6,'Dairy processing',ha='center',va='center',fontsize=10.5,fontweight='bold')
ax.add_patch(FancyArrowPatch((11,20.0),(11,16.8),arrowstyle='-|>',mutation_scale=13,lw=1.8,color=K))
pond(8.6,11.0,0.9)
ax.text(11,3.4,'Side streams\nand wastewater',ha='center',va='center',fontsize=10.5,fontweight='bold',color=RED)
# ---------------------------------------------------------------- bus and rows
ys=[53.5,42.0,30.5,19.0,7.5]; BUS=23.5
ax.plot([17.6,BUS],[30.5,30.5],color=K,lw=1.3,zorder=1); ax.plot([15.6,BUS],[11.6,11.6],color=K,lw=1.3,zorder=1)
ax.plot([BUS,BUS],[ys[-1],ys[0]],color=K,lw=1.3,zorder=1)
rows=[('whey','Whey valorization','needs coagulated products\nand a buyer',eq_whey,sack,'Protein, lactose','food ingredients, feed, drinks'),
      ('effluent','Anaerobic digestion','needs strong, warm effluent\nand skilled operation',eq_ad,flame,'Biogas','process heat or electricity'),
      ('wastewater','Membrane water reuse','needs measured\nstream data',eq_membrane,drop,'Clean water','cleaning, cooling, boiler feed'),
      ('rinse water','Residual milk solids recovery','needs stream data\nfor each plant',eq_cip,churn,'Milk solids','product or feed'),
      ('waste heat','Heat integration','needs energy\nmetering',eq_heat,heat,'Recovered heat','lower fuel and electricity use')]
ax.text(46,61.2,'Recovery route',ha='center',va='center',fontsize=10.5,fontweight='bold',color=RED)
ax.text(89,61.2,'Recovered resource and use',ha='center',va='center',fontsize=10.5,fontweight='bold',color=RED)
SC={sack:1.15,flame:1.7,drop:1.45,churn:1.15,heat:1.0}
for (st,name,need,eq,res,rname,use),y in zip(rows,ys):
    ax.add_patch(FancyArrowPatch((BUS,y),(31.5,y),arrowstyle='-|>',mutation_scale=10,lw=1.3,color=K,zorder=1))
    ax.text(24.4,y+0.8,st,ha='left',va='bottom',fontsize=6.8,style='italic',color='#444444')
    eq(40.0,y)
    two=len(name)>24
    ax.text(49.0,y+1.5,name.replace(' solids recovery','\nsolids recovery') if two else name,ha='left',va='center',fontsize=9.2,fontweight='bold',linespacing=1.05)
    ax.text(49.0,y-2.6 if two else y-1.9,need,ha='left',va='center',fontsize=7.0,style='italic',color='#555555',linespacing=1.1)
    ax.add_patch(FancyArrowPatch((70.0,y),(75.0,y),arrowstyle='simple,head_width=9,head_length=7,tail_width=4',mutation_scale=1.6,fc=LBLUE,ec='none',zorder=1))
    res(79.0,y-(1.0 if res is flame else 0),SC[res])
    ax.text(83.0,y+1.1,rname,ha='left',va='center',fontsize=9.2,fontweight='bold')
    ax.text(83.0,y-1.3,use,ha='left',va='center',fontsize=7.6,color='#333333')
fig.savefig(_os.path.join(FIG_DIR, 'Figure_overview.png'),dpi=220,bbox_inches='tight',pad_inches=0.08,facecolor='white')
fig.savefig(_os.path.join(FIG_DIR, 'Figure_overview.pdf'),bbox_inches='tight',pad_inches=0.08)
fig.savefig(_os.path.join(FIG_DIR, 'Figure_overview.tiff'),dpi=600,bbox_inches='tight',pad_inches=0.08,pil_kwargs={'compression':'tiff_lzw'},facecolor='white')
from PIL import Image; print(Image.open(_os.path.join(FIG_DIR, 'Figure_overview.png')).size)
