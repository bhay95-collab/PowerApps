# Layout simulator: evaluates the geometry formulas of a generated .pa.yaml and draws it as HTML
import yaml, re, sys, html, math

def load(path):
    t = open(path, encoding='utf-8').read()
    t = re.sub(r'(?m)^(\s*[\w.]+:) =$', r'\1 "="', t)
    d = yaml.safe_load(t)
    name = list(d['Screens'].keys())[0]
    return name, d['Screens'][name]

COL = {'C_Ink': '#0e1c2a', 'C_Ink2': '#3a5068', 'C_Muted': '#8c9bae', 'C_Bg': '#ebf2f8', 'C_Bg2': '#f4f9fc', 'C_Line': 'rgba(14,42,70,.12)',
       'C_White': '#fff', 'C_Accent': '#1a5a99', 'C_AccentDark': '#124070', 'C_AccentSoft': 'rgba(26,90,153,.10)', 'C_Good': '#0c7a52',
       'C_GoodBg': '#e8f6f0', 'C_Danger': '#b41a1a', 'C_DangerBg': '#fef2f2', 'C_Amber': '#b26900', 'C_AmberBg': '#fff6e5', 'C_Teal': '#009099'}

def color(expr, pick='last'):
    if expr is None:
        return None
    e = str(expr).lstrip('=')
    toks = re.findall(r'C_[A-Za-z0-9]+|RGBA\([^)]*\)', e)
    if not toks:
        return None
    t = toks[-1] if pick == 'last' else toks[0]
    if t.startswith('C_'):
        return COL.get(t, '#ccc')
    m = re.match(r'RGBA\(([^)]*)\)', t)
    r, g, b, a = [x.strip() for x in m.group(1).split(',')]
    return f'rgba({r},{g},{b},{a})'

class Ctx:
    def __init__(self, app_w, app_h):
        self.app_w, self.app_h = app_w, app_h

def ev(expr, env, default=None):
    if expr is None:
        return default
    s = str(expr).lstrip('=').strip()
    if s in ('', 'true', 'false'):
        return default
    s = re.sub(r'Parent\.TemplateWidth', 'PTW', s)
    s = re.sub(r'Parent\.TemplateHeight', 'PTH', s)
    s = re.sub(r'Parent\.Width', 'PW', s)
    s = re.sub(r'Parent\.Height', 'PH', s)
    s = re.sub(r'App\.Width', 'AW', s)
    s = re.sub(r'App\.Height', 'AH', s)
    s = re.sub(r'Self\.Height', 'SH', s)
    s = re.sub(r'Self\.Width', 'SWD', s)
    s = s.replace('Min(', 'min(').replace('Max(', 'max(')
    try:
        return float(eval(s, {'min': min, 'max': max, 'Round': lambda a, b=0: round(a, int(b)), 'If': lambda c, a, b=0: a if c else b}, env))
    except Exception:
        return default

def num(p, k, env, default=None):
    return ev(p.get(k), env, default)

class Node:
    pass

def layout(name, c, parent_env, out, x, y, w, h, depth, fw=None, fh=None):
    """x,y,w,h = actual (drawn) geometry. fw,fh = what Parent.Width / Parent.Height return for children (formula values)."""
    pass

def draw(name, ctrl, env_parent, geom, out, path, flags):
    """geom = (x, y, w, h) drawn in parent's coordinate space; returns nothing; appends div html"""
    p = ctrl.get('Properties', {})
    kind = ctrl['Control'].split('@')[0]
    x, y, w, h = geom
    # formula-world size for children = formula values (may differ from drawn)
    fw = ev(p.get('Width'), env_parent, w)
    fh = ev(p.get('Height'), env_parent, h)
    if ctrl.get('Variant') == 'AutoLayout' or kind in ('Label', 'Button', 'ModernIcon', 'Image', 'BarcodeReader') or True:
        pass
    # record mismatch between drawn width and formula width (only meaningful when parent is auto layout)
    if abs(fw - w) > 1.5 and ctrl.get('_inauto'):
        flags.append(f'{path}/{name}: drawn width {w:.0f} but Width formula = {fw:.0f}')
    env = dict(env_parent)
    env.update({'PW': fw, 'PH': fh})
    style = f'left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;height:{h:.1f}px;'
    inner = ''
    txt = ''
    cls = kind
    fill = color(p.get('Fill'), 'last') if kind in ('GroupContainer',) else None
    if kind == 'GroupContainer':
        if fill:
            style += f'background:{fill};'
        bc = color(p.get('BorderColor'), 'last')
        if bc and p.get('BorderStyle'):
            style += f'border:1px solid {bc};box-sizing:border-box;'
        rt = ev(p.get('RadiusTopLeft'), env, 0) or 0
        rb = ev(p.get('RadiusBottomLeft'), env, 0) or 0
        rtr = ev(p.get('RadiusTopRight'), env, 0) or 0
        rbr = ev(p.get('RadiusBottomRight'), env, 0) or 0
        style += f'border-radius:{rt}px {rtr}px {rbr}px {rb}px;overflow:hidden;'
        kids = ctrl.get('Children') or []
        if ctrl.get('Variant') == 'AutoLayout':
            kid_geoms = auto_layout(p, kids, env, w, h)
            for (kn, kc), g in zip(flat(kids), kid_geoms):
                kc['_inauto'] = True
                inner += draw(kn, kc, env, g, out, path + '/' + name, flags)
        else:
            for kn, kc in flat(kids):
                kc['_inauto'] = False
                kw = ev(kc['Properties'].get('Width'), env, 100)
                kh = ev(kc['Properties'].get('Height'), env, 30)
                e2 = dict(env); e2['SH'] = kh; e2['SWD'] = kw
                kx = ev(kc['Properties'].get('X'), e2, 0)
                ky = ev(kc['Properties'].get('Y'), e2, 0)
                inner += draw(kn, kc, env, (kx, ky, kw, kh), out, path + '/' + name, flags)
    elif kind == 'Gallery':
        horizontal = ctrl.get('Variant') == 'Horizontal'
        ts = ev(p.get('TemplateSize'), env, 70)
        tw, th = (ts, fh) if horizontal else (fw, ts)
        genv = dict(env)
        genv.update({'PTW': tw, 'PTH': th, 'PW': tw, 'PH': th})
        n = 4 if not horizontal else 6
        for i in range(n):
            ox, oy = (i * ts, 0) if horizontal else (0, i * ts)
            for kn, kc in flat(ctrl.get('Children') or []):
                kc['_inauto'] = False
                kx = ev(kc['Properties'].get('X'), genv, 0) + ox
                ky = ev(kc['Properties'].get('Y'), genv, 0) + oy
                kw = ev(kc['Properties'].get('Width'), genv, 100)
                kh = ev(kc['Properties'].get('Height'), genv, 30)
                inner += draw(f'{kn}', kc, genv, (kx, ky, kw, kh), out, path + '/' + name, flags)
        style += 'overflow:hidden;outline:1px dashed #c33;'
    else:
        size = (ev(p.get('Size'), env, 13) if kind in ('Label', 'Text', 'Button') else 13) * 4 / 3
        bold = 'Bold' in str(p.get('FontWeight', p.get('Weight', '')))
        c = color(p.get('Color') or p.get('FontColor'), 'last') or '#3a5068'
        al = str(p.get('Align', 'Left')).split('.')[-1].lower()
        txt = str(p.get('Text', '') or '')
        if kind == 'Label' or kind == 'Text':
            style += f'font-size:{size}px;color:{c};' + ('font-weight:700;' if bold else '') + f'text-align:{al};'
            va = str(p.get('VerticalAlign', 'Top')).split('.')[-1].lower()
            wrap = str(p.get('Wrap', 'true')) != '=false'
            if not wrap:
                style += 'white-space:nowrap;'
            style += 'overflow:hidden;line-height:1.15;'
            if va == 'middle':
                style += 'display:flex;align-items:center;' + ('justify-content:center;' if al == 'center' else ('justify-content:flex-end;' if al == 'right' else ''))
            inner = sample(txt, name)
        elif kind == 'Button':
            ico = p.get('Icon')
            c = color(p.get('FontColor'), 'last') or '#3a5068'
            style += f'font-size:{size}px;color:{c};font-weight:700;display:flex;align-items:center;justify-content:center;'
            t = str(p.get('Text', '') or '')
            inner = sample(t, name) if t not in ('=""', '=', '') else ''
            if ico and t in ('=""', '=', ''):
                inner = '‹' if 'Left' in str(ico) else '›'
            cl = 'btn'
        elif kind == 'ModernIcon':
            ic = color(p.get('IconColor'), 'last') or '#888'
            style += f'background:{ic};border-radius:50%;opacity:.55;'
        elif kind == 'Image':
            style += 'background:linear-gradient(90deg,#001d46,#075f73,#00838a);'
        elif kind.startswith('Classic/TextInput'):
            hint = str(p.get('HintText', '')).strip('="')
            style += f'font-size:{ev(p.get("Size"), env, 13)}px;color:#8c9bae;display:flex;align-items:center;padding-left:6px;'
            inner = html.escape(hint)
        elif kind.startswith('Classic/DropDown') or kind.startswith('Classic/ComboBox') or kind.startswith('Classic/DatePicker'):
            style += 'background:#fff;font-size:14px;color:#0e1c2a;display:flex;align-items:center;padding-left:8px;'
            inner = kind.split('/')[1].split('@')[0] + ' ▾'
        elif kind == 'BarcodeReader':
            style += 'background:rgba(255,255,255,.05);'
    vis = str(p.get('Visible', ''))
    hidden = vis.strip('=') == 'false' or name.startswith(('lblEmpty', 'lblNone', 'lblNoCal')) or name in HIDE
    if any(t in vis for t in HIDE_VIS) and not OVERLAY:
        hidden = True
    if name.startswith('conOverlay') and not OVERLAY:
        hidden = True
    if hidden:
        return ''
    return f'<div class="c {cls}" title="{html.escape(path + "/" + name)}" style="{style}">{inner}</div>'

def sample(expr, name):
    e = expr.strip()
    m = re.fullmatch(r'="((?:[^"]|"")*)"', e)
    if m:
        return html.escape(m.group(1).replace('""', '"'))
    if e in ('=', '', '=""'):
        return ''
    SAM={'lblstream_hm':'Internal Medicine & Emergency','lbldept_sel':'Emergency and Trauma Centre','lblloc_sel':'POD B Staff Station','lblasset_sel':'James Mayne Building · Ground · QH12745661','lblhello_hm':'Hi Alex  ·  Wednesday 30 September','lblinfot_aud':'Emergency and Trauma Centre','lblinfol_aud':'POD B Staff Station','lblinfoa_aud':'James Mayne Building · Ground · QH12745661','lblinfoacc_aud':'Log in with account: DTV-EDTC-POD-B','lblokr_dn':'Login Yes  ·  Print No  ·  Kit no list','lbloks_dn':'Emergency and Trauma Centre - POD B Staff Station','lblcount_sel':'30 DTVs','lblhdrs_sel':'Step 1 of 2  ·  Your stream','lblhdrs_dn':'Emergency and Trauma Centre','lblsubmit_aud':'Answer every question to submit','lblstartt_hm':'Start an Audit','lbladdphoto_aud':'Change Photo','lblempty_sel':'No DTVs in your stream match. Try All DTVs','lblstreams_hm':'Use All DTVs below, or contact Ben'}
    if name.lower() in SAM: return SAM[name.lower()]
    # dynamic formula: show a plausible sample
    n = name.lower()
    if 'count' in n or 'days' in n:
        return '12d'
    return 'Sample text'

def flat(kids):
    out = []
    for k in kids:
        for n, c in k.items():
            out.append((n, c))
    return out

def auto_layout(p, kids, env, w, h):
    vertical = 'Vertical' in str(p.get('LayoutDirection', 'Vertical'))
    pt = ev(p.get('PaddingTop'), env, 0); pr = ev(p.get('PaddingRight'), env, 0)
    pb = ev(p.get('PaddingBottom'), env, 0); pl = ev(p.get('PaddingLeft'), env, 0)
    gap = ev(p.get('LayoutGap'), env, 0)
    iw, ih = w - pl - pr, h - pt - pb
    items = flat(kids)
    sizes = []  # main-axis size (fixed) or None for flex; with portions and min
    for n, c in items:
        cp = c['Properties']
        vis = str(cp.get('Visible', '')).strip('=')
        portions = ev(cp.get('FillPortions'), env, 0) or 0
        if 'FillPortions' not in cp and ('Height' if vertical else 'Width') not in cp: portions = 1
        if vertical:
            fixedv = ev(cp.get('Height'), env, 40)
            minv = ev(cp.get('LayoutMinHeight'), env, 0) or 0
        else:
            fixedv = ev(cp.get('Width'), env, 80)
            minv = ev(cp.get('LayoutMinWidth'), env, 0) or 0
        sizes.append([fixedv, portions, minv, vis == 'false'])
    main = ih if vertical else iw
    n_vis = sum(1 for s in sizes if not s[3])
    used = sum(s[0] for s in sizes if s[1] == 0 and not s[3]) + gap * max(0, n_vis - 1)
    free = max(0, main - used)
    tot = sum(s[1] for s in sizes if s[1] > 0 and not s[3]) or 1
    geoms = []
    pos = pt if vertical else pl
    for (n, c), s in zip(items, sizes):
        if s[3]:
            geoms.append((0, 0, 0, 0)); continue
        size = max(s[2], free * s[1] / tot) if s[1] > 0 else s[0]
        if vertical:
            geoms.append((pl, pos, iw, size))
        else:
            geoms.append((pos, pt, size, ih))
        pos += size + gap
    return geoms

HIDE = set(['galResC_Fd', 'galSug_Au'])
OVERLAY = False
HIDE_VIS = ['ulTab = "Size"', 'ulTab = "Wards"', 'ulShowDetail']
CSS = '''body{margin:0;background:#888;font-family:"Segoe UI",Arial,sans-serif}
.phone{position:relative;background:#ebf2f8;overflow:hidden;margin:0 auto}
.c{position:absolute;box-sizing:border-box}
.Gallery{}
'''

def render(path, aw, ah, outpng, extra_screens=()):
    name, scr = load(path)
    flags = []
    import os
    if os.environ.get('TRAIN'):
        Wd = aw >= 820; UI = 1 if Wd else max(0.9, min(1.25, min(aw, ah * 0.55) / 390)); PageW = min(aw, 1280)
    else:
        Wd = False; UI = max(0.9, min(1.25, min(aw, ah * 0.55) / 390)); PageW = min(aw, 720)
    env = {'AW': aw, 'AH': ah, 'PW': aw, 'PH': ah, 'PTW': aw, 'PTH': 70, 'SH': 0, 'SWD': 0, 'UI': UI, 'PageW': PageW, 'Wide': Wd, 'GapPx': round(20 * UI), 'ListW': (min(525 * UI, (PageW - 3 * round(20 * UI)) * 0.4) if Wd else PageW - 2 * round(20 * UI)), 'DetailX': ((aw - PageW) / 2 + 2 * round(20 * UI) + (min(525 * UI, (PageW - 3 * round(20 * UI)) * 0.4)) if Wd else (aw - PageW) / 2 + round(20 * UI)), 'DetailW': (PageW - 3 * round(20 * UI) - min(525 * UI, (PageW - 3 * round(20 * UI)) * 0.4) if Wd else PageW - 2 * round(20 * UI)), 'Gutter': (aw - PageW) / 2, 'SheetW': min(aw, 600), 'SX': aw / 1366, 'SY': ah / 768, 'SF': max(0.75, min(1.4, min(aw / 1366, ah / 768))), 'SR': min(aw / 1366, ah / 768)}
    env['DashW'] = min(aw - round(48 * UI), 1400); env['DashX'] = (aw - env['DashW']) / 2; env['DashWide'] = aw >= 1000; env['DashGap'] = round(16 * UI)
    body = ''
    for kn, kc in flat(scr.get('Children') or []):
        kc['_inauto'] = False
        kx = ev(kc['Properties'].get('X'), env, 0); ky = ev(kc['Properties'].get('Y'), env, 0)
        kw = ev(kc['Properties'].get('Width'), env, aw); kh = ev(kc['Properties'].get('Height'), env, ah)
        body += draw(kn, kc, env, (kx, ky, kw, kh), None, name, flags)
    doc = f'<html><head><style>{CSS}</style></head><body><div class="phone" style="width:{aw}px;height:{ah}px">{body}</div></body></html>'
    open(outpng.replace('.png', '.html'), 'w').write(doc)
    return flags

if __name__ == '__main__':
    path, aw, ah, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4]
    if len(sys.argv) > 5 and sys.argv[5] == 'overlay':
        OVERLAY = True
    fl = render(path, aw, ah, out)
    print('\n'.join(fl[:40]) or 'no width mismatches')
