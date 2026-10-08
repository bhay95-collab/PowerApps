import re
def r(n): return f"Round({n} * UI, 0)"
# Power Apps font Size is in points (1pt = 1.33px). Designs were drawn in px, so convert.
FS={36:28,24:19,22:18,19:15,18:14,17:14,16:13,15:12,14:11,13:11}
def F(n): return FS.get(n,n)
HDR_FILL="RGBA(7, 95, 115, 1)"
def fv(v):
    return v if v.startswith('=') else '='+v
class N:
    def __init__(s,name,control,variant=None,props=None,children=None):
        s.name=name;s.control=control;s.variant=variant;s.props=props or {};s.children=children or []
def emit(n,ind):
    p=' '*ind
    out=[f"{p}- {n.name}:",f"{p}    Control: {n.control}"]
    if n.variant: out.append(f"{p}    Variant: {n.variant}")
    out.append(f"{p}    Properties:")
    for k in sorted(n.props):
        v=fv(str(n.props[k]))
        if '\n' in v or ': ' in v or ' #' in v:
            out.append(f"{p}      {k}: |-")
            for ln in v.split('\n'): out.append(f"{p}        {ln}")
        else: out.append(f"{p}      {k}: {v}")
    if n.children:
        out.append(f"{p}    Children:")
        for c in n.children: out+=emit(c,ind+6)
    return out
SBOX={'PaddingBottom':'5','PaddingLeft':'12','PaddingRight':'12','PaddingTop':'5','RadiusBottomLeft':'4','RadiusBottomRight':'4','RadiusTopLeft':'4','RadiusTopRight':'4'}
def rad(x): return {k:x for k in ('RadiusBottomLeft','RadiusBottomRight','RadiusTopLeft','RadiusTopRight')}
def lbl(name,text,x=None,y=None,w='Parent.Width',h=None,size=15,color='C_Ink',bold=False,wrap=False,align=None,visible=None,extra=None):
    p={'Color':color,'Font':'AppFont','Size':r(F(size)),'Text':text,'Width':w,'Height':h or r(round(size*1.7))}
    if bold:p['FontWeight']='FontWeight.Bold'
    if not wrap:p['Wrap']='false'
    if x is not None:p['X']=x
    if y is not None:p['Y']=y
    if align:p['Align']=align
    if visible:p['Visible']=visible
    if extra:p.update(extra)
    return N(name,'Label@2.5.1',props=p)
def ico(name,icon,x,y,size,color,filled=False):
    p={'Height':r(size),'Icon':f'"{icon}"','IconColor':color,'Width':r(size),'X':x,'Y':y}
    if filled:p['IconStyle']='IconStyle.Filled'
    return N(name,'ModernIcon@1.1.1',props=p)
def tbtn(name,onselect,x=None,y=None,w='Parent.Width',h='Parent.Height',display=None):
    p={'Align':'Align.Center','Appearance':'ButtonAppearance.Transparent','BorderStyle':'BorderStyle.None','FontWeight':'""','Height':h,'OnSelect':onselect,'Text':'""','VerticalAlign':'VerticalAlign.Middle','Width':w}
    p.update(SBOX)
    if x is not None:p['X']=x
    if y is not None:p['Y']=y
    if display:p['DisplayMode']=display
    return N(name,'ModernButton@1.0.0',props=p)
def box(name,x=None,y=None,w='Parent.Width',h=None,fill=None,border=None,radius=None,visible=None,auto=False,extra=None,children=None):
    p={'DropShadow':'DropShadow.None','Height':h,'Width':w}
    if fill:p['Fill']=fill
    if border:p['BorderColor']=border;p['BorderThickness']='1'
    if radius is not None:p.update(rad(radius))
    if x is not None:p['X']=x
    if y is not None:p['Y']=y
    if visible:p['Visible']=visible
    if extra:p.update(extra)
    return N(name,'GroupContainer@1.5.0','ManualLayout',p,children)
def inflow(name,h,w=None,minh=None,**kw):
    """child of an auto-layout vertical container"""
    e={'AlignInContainer':'AlignInContainer.SetByContainer','FillPortions':'0','LayoutMinHeight':minh or h}
    e.update(kw.pop('extra',{}))
    return box(name,h=h,w=w or f"PageW - {r(40)}",extra=e,**kw)
def vroot(name,children,fill='C_Bg'):
    p={'DropShadow':'DropShadow.None','Fill':fill,'Height':'Parent.Height','LayoutAlignItems':'LayoutAlignItems.Stretch','LayoutDirection':'LayoutDirection.Vertical','Width':'Parent.Width'}
    p.update(rad('0'))
    return N(name,'GroupContainer@1.5.0','AutoLayout',p,children)
def vbody(name,children,gap=12,top=15,bottom=10,scroll=False):
    p={'AlignInContainer':'AlignInContainer.SetByContainer','DropShadow':'DropShadow.None','LayoutAlignItems':'LayoutAlignItems.Stretch','LayoutDirection':'LayoutDirection.Vertical','LayoutGap':r(gap),'LayoutMinHeight':r(250),'PaddingBottom':r(bottom),'PaddingLeft':f"Gutter + {r(20)}",'PaddingRight':f"Gutter + {r(20)}",'PaddingTop':r(top),'Width':'App.Width'}
    p.update(rad('0'))
    if scroll:p['LayoutOverflowY']='LayoutOverflow.Scroll'
    return N(name,'GroupContainer@1.5.0','AutoLayout',p,children)
def header(sfx,title,sub,back,height=95):
    ch=[N(f'imgHdr_{sfx}','Image@2.2.3',props={'Height':'Parent.Height','Image':'HeaderImage','ImagePosition':'ImagePosition.Fill','Width':'Parent.Width'})]
    bp={'Align':'Align.Center','Appearance':'ButtonAppearance.Transparent','Color':'C_White','FontWeight':'""','Height':r(60),'Icon':'"ChevronLeft"','OnSelect':back,'Size':r(24),'Text':'""','VerticalAlign':'VerticalAlign.Middle','Width':r(60),'X':f"Gutter + {r(5)}",'Y':r(18)}
    bp.update(SBOX)
    ch.append(N(f'btnBack_{sfx}','ModernButton@1.0.0',props=bp))
    ch.append(lbl(f'lblHdrT_{sfx}',title,x=f"Gutter + {r(65)}",y=r(12),w=f"PageW - {r(85)}",h=r(42),size=24,color='C_White',bold=True))
    ch.append(lbl(f'lblHdrS_{sfx}',sub,x=f"Gutter + {r(65)}",y=r(53),w=f"PageW - {r(85)}",h=r(25),size=15,color='RGBA(255, 255, 255, 0.85)'))
    return inflow(f'conHdr_{sfx}',r(height),w='App.Width',fill=HDR_FILL,radius='0',children=ch,extra={'DropShadow':'DropShadow.None'})
def screen(name,props,children):
    out=["Screens:",f"  {name}:","    Properties:"]
    for k in sorted(props):
        v=fv(props[k])
        if '\n' in v:
            out.append(f"      {k}: |-")
            for ln in v.split('\n'): out.append(f"        {ln}")
        else: out.append(f"      {k}: {v}")
    out.append("    Children:")
    for c in children: out+=emit(c,6)
    return '\n'.join(out)+'\n'
