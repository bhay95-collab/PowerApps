from dtvgen import *
import os
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','..','powerapps','dtv')+os.sep
W=f"PageW - {r(40)}"
LINE="RGBA(14, 42, 70, 0.22)"

# ------------------------------------------------------------------ HOME
hello='With({ n: User().FullName }, If("," in n, Trim(Last(Split(n, ",")).Value), First(Split(n, " ")).Value))'
hdr=inflow('conHdr_Hm',r(165),w='App.Width',fill=HDR_FILL,radius='0',children=[
  N('imgHdr_Hm','Image@2.2.3',props={'Height':'Parent.Height','Image':'HeaderImage','ImagePosition':'ImagePosition.Fill','Width':'Parent.Width'}),
  lbl('lblKicker_Hm','"ieMR DOWNTIME VIEWER AUDIT"',x=f"Gutter + {r(25)}",y=r(33),w=f"PageW - {r(50)}",h=r(23),size=14,color='RGBA(255, 255, 255, 0.8)',bold=True),
  lbl('lblTitle_Hm','"DTV Audit"',x=f"Gutter + {r(25)}",y=r(45),w=f"PageW - {r(50)}",h=r(70),size=36,color='C_White',bold=True),
  lbl('lblHello_Hm',f'"Hi " & {hello} & "  ·  " & Text(Today(), "dddd d mmmm")',x=f"Gutter + {r(25)}",y=r(110),w=f"PageW - {r(50)}",h=r(28),size=16,color='RGBA(255, 255, 255, 0.9)'),
])
hero=inflow('conStart_Hm',r(120),fill='C_Accent',radius=r(25),children=[
  box('conStartIc_Hm',x=r(20),y=r(32),w=r(56),h=r(56),fill='RGBA(255, 255, 255, 0.16)',radius=r(28),children=[ico('icoStart_Hm','CheckmarkCircle',r(11),r(11),34,'C_White',True)]),
  lbl('lblStartT_Hm','"Start an Audit"',x=r(92),y=r(32),w=f"Parent.Width - {r(108)}",h=r(32),size=24,color='C_White',bold=True),
  lbl('lblStartS_Hm','"Pick a DTV from your stream"',x=r(92),y=r(66),w=f"Parent.Width - {r(108)}",h=r(22),size=15,color='RGBA(255, 255, 255, 0.85)'),
  tbtn('btnStart_Hm','Set(varShowAll, IsBlank(varStream));\nNavigate(SelectDTV, ScreenTransition.Cover)'),
])
noStream='IsBlank(varStream)'
pct='Coalesce(varMyPct, 0)'
stream=inflow('conStream_Hm',f'Round(If({noStream}, 92, 112) * UI, 0)',fill=f'If({noStream}, C_AmberBg, C_White)',border=f'If({noStream}, RGBA(178, 105, 0, 0.35), C_Line)',radius=r(20),children=[
  lbl('lblStreamCap_Hm','"YOUR STREAM"',x=r(20),y=r(12),w=f"Parent.Width - {r(40)}",h=r(18),size=13,color=f'If({noStream}, C_Amber, C_Muted)',bold=True),
  lbl('lblStream_Hm',f'If({noStream}, "Not allocated to a stream", varStream)',x=r(20),y=r(32),w=f"Parent.Width - {r(40)}",h=r(28),size=19,color=f'If({noStream}, C_Amber, C_Ink)',bold=True,extra={'Size':f'If(Len(Coalesce(varStream, "")) > 26, {r(13)}, {r(15)})'}),
  lbl('lblStreamS_Hm','"Use All DTVs below, or contact Ben"',x=r(20),y=r(62),w=f"Parent.Width - {r(40)}",h=r(20),size=14,color='C_Amber',visible=noStream),
  lbl('lblProg_Hm','varMyDone & " of " & varMyDTVs & " audited"',x=r(20),y=r(62),w=f"Parent.Width - {r(40)}",h=r(20),size=14,color='C_Ink2',visible=f'!{noStream}'),
  box('conBarBg_Hm',x=r(20),y=r(88),w=f"Parent.Width - {r(40)}",h=r(8),fill='C_Line',radius=r(4),visible=f'!{noStream}',children=[
    box('conBarFg_Hm',w=f'Parent.Width * {pct}',h='Parent.Height',fill=f'If({pct} >= 1, RGBA(30, 122, 80, 1), C_Accent)',radius=r(4))]),
])
cap=inflow('capOther_Hm',r(23),w=W,children=None)
cap=lbl('capOther_Hm','"OTHER OPTIONS"',w=W,h=r(23),size=14,color='C_Muted',bold=True,extra={'AlignInContainer':'AlignInContainer.SetByContainer','LayoutMinHeight':r(23)})
apct='Coalesce(varAllPct, 0)'
tile=inflow('conTileAll',r(100),fill='C_White',border='C_Line',radius=r(20),children=[
  box('conTileIcAll',x=r(18),y=r(22),w=r(55),h=r(55),fill='C_AccentSoft',radius=r(28),children=[ico('icoTileAll','AppsList',r(13),r(13),30,'C_Accent',True)]),
  lbl('lblTileTAll','"All DTVs"',x=r(88),y=r(16),w=f"Parent.Width - {r(130)}",h=r(26),size=19,color='C_Ink',bold=True),
  lbl('lblTileSAll','varAllDone & " of " & varAllDTVs & " audited site-wide"',x=r(88),y=r(44),w=f"Parent.Width - {r(130)}",h=r(22),size=15,color='C_Muted'),
  box('conAllBarBg_Hm',x=r(88),y=r(74),w=f"Parent.Width - {r(130)}",h=r(8),fill='C_Line',radius=r(4),children=[
    box('conAllBarFg_Hm',w=f'Parent.Width * {apct}',h='Parent.Height',fill=f'If({apct} >= 1, RGBA(30, 122, 80, 1), C_Accent)',radius=r(4))]),
  ico('icoTileGoAll','ChevronRight',f"Parent.Width - {r(38)}",r(38),24,'C_Muted'),
  tbtn('btnTileAll','Set(varShowAll, true);\nNavigate(SelectDTV, ScreenTransition.Cover)'),
])
tileRe=inflow('conTileRe_Hm',r(90),fill='C_White',border='C_Line',radius=r(20),children=[
  box('conTileIcRe_Hm',x=r(18),y=r(18),w=r(55),h=r(55),fill='C_AmberBg',radius=r(28),children=[ico('icoTileRe_Hm','ArrowClockwise',r(13),r(13),30,'C_Amber',True)]),
  lbl('lblTileTRe_Hm','"Re-audit"',x=r(88),y=r(18),w=f"Parent.Width - {r(130)}",h=r(26),size=19,color='C_Ink',bold=True),
  lbl('lblTileSRe_Hm','"Re-check an audited DTV"',x=r(88),y=r(46),w=f"Parent.Width - {r(130)}",h=r(22),size=15,color='C_Muted'),
  ico('icoTileGoRe_Hm','ChevronRight',f"Parent.Width - {r(38)}",r(33),24,'C_Muted'),
  tbtn('btnTileRe_Hm','Navigate(ReAuditList, ScreenTransition.Cover)'),
])
tileDash=inflow('conTileDash_Hm',r(90),fill='C_White',border='C_Line',radius=r(20),children=[
  box('conTileIcDash_Hm',x=r(18),y=r(18),w=r(55),h=r(55),fill='C_AccentSoft',radius=r(28),children=[ico('icoTileDash_Hm','Eye',r(13),r(13),30,'C_Accent',True)]),
  lbl('lblTileTDash_Hm','"Dashboard"',x=r(88),y=r(18),w=f"Parent.Width - {r(130)}",h=r(26),size=19,color='C_Ink',bold=True),
  lbl('lblTileSDash_Hm','"Results and data extract"',x=r(88),y=r(46),w=f"Parent.Width - {r(130)}",h=r(22),size=15,color='C_Muted'),
  ico('icoTileGoDash_Hm','ChevronRight',f"Parent.Width - {r(38)}",r(33),24,'C_Muted'),
  tbtn('btnTileDash_Hm','Navigate(Dashboard, ScreenTransition.Cover)'),
])
endHm=inflow('conEnd_Hm',r(16),extra={'DropShadow':'DropShadow.None'})
body=vbody('conBody_Hm',[hero,stream,cap,tile,tileRe,tileDash,endHm],gap=15,top=20,bottom=30,scroll=True)
onv_hm='''Set(varStreamPick, Blank());
// back on Home: the next audit is a normal audit unless Re-audit is chosen
Set(varReaudit, false);
// audit progress: DTVs with an audit in the last month
Refresh(Audit_Results);
ClearCollect(
    colRecentAudits,
    Distinct(Filter(Audit_Results, Created >= DateAdd(Now(), -1, TimeUnit.Months)), Title)
);
ClearCollect(colAllTags, DTV_Register);
Set(varAllDTVs, CountRows(colAllTags));
Set(varAllDone, CountRows(Filter(colAllTags, Title in colRecentAudits.Value)));
Set(varMyDTVs, CountRows(Filter(colAllTags, !IsBlank(varStream) && (Stream = varStream || Stream = "All"))));
Set(varMyDone, CountRows(Filter(colAllTags, !IsBlank(varStream) && (Stream = varStream || Stream = "All") && Title in colRecentAudits.Value)));
// share done, worked out once (0 when the stream has no DTVs, so there is never a divide by zero)
Set(varMyPct, If(varMyDTVs > 0, varMyDone / varMyDTVs, 0));
Set(varAllPct, If(varAllDTVs > 0, varAllDone / varAllDTVs, 0))'''
open(OUT+'DTV_Home.pa.yaml','w').write(screen('Home',{'Fill':'C_Bg','OnVisible':onv_hm},[vroot('conRoot_Hm',[hdr,body])]))

# ------------------------------------------------------------------ SELECT DTV
count='CountRows(galDTV_Sel.AllItems)'
search=inflow('conSearch_Sel',r(60),border=LINE,fill='C_White',radius=r(15),children=[
  ico('icoSearch_Sel','Search',r(16),r(18),24,'C_Muted'),
  N('txtSearch_Sel','Classic/TextInput@2.3.2',props={'BorderStyle':'BorderStyle.None','Color':'C_Ink','Default':'""','DelayOutput':'true','Fill':'RGBA(0, 0, 0, 0)','Font':'AppFont','Height':'Parent.Height','HintText':'"Search DTVs"','Size':r(F(16)),'Width':f"Parent.Width - {r(54)}",'X':r(46)}),
])
segw=f"(PageW - {r(40)} - {r(10)}) / 2"
def seg(name,x,var,txt,onsel,sel):
    return box(f'con{name}_Sel',x=x,w=segw,h=r(50),fill=f'If({sel}, C_Accent, C_White)',border=f'If({sel}, C_Accent, C_Line)',radius=r(25),children=[
      N(f'btn{name}_Sel','ModernButton@1.0.0',props=dict({'Align':'Align.Center','Appearance':'ButtonAppearance.Transparent','Color':f'If({sel}, C_White, C_Ink2)','Font':'AppFont','FontWeight':'FontWeight.Bold','Height':'Parent.Height','OnSelect':onsel,'Size':r(F(16)),'Text':txt,'VerticalAlign':'VerticalAlign.Middle','Width':'Parent.Width'},**rad(r(25)),**{k:v for k,v in SBOX.items() if not k.startswith('Radius')})),
    ])
segs=inflow('conSeg_Sel',r(50),children=[
  seg('Mine',0,'varShowAll','"My Stream"','Set(varShowAll, false);\nSet(varStreamPick, Blank())','!varShowAll'),
  seg('All',f"{segw} + {r(10)}",'varShowAll','"All DTVs"','Set(varShowAll, true)','varShowAll'),
])
chipsel='If(ThisItem.Value = "All streams", IsBlank(varStreamPick), ThisItem.Value = varStreamPick)'
chip=box('conChip_Sel',x=1,y=r(3),w=f"Parent.TemplateWidth - {r(8)}",h=r(42),fill=f'If({chipsel}, C_AccentSoft, C_White)',border=f'If({chipsel}, C_Accent, C_Line)',radius=r(21),children=[
  lbl('lblChip_Sel','ThisItem.Value',w='Parent.Width',h=r(42),size=14,color=f'If({chipsel}, C_Accent, C_Ink2)',bold=True,align='Align.Center',extra={'VerticalAlign':'VerticalAlign.Middle'}),
  tbtn('btnChip_Sel','Set(varStreamPick, If(ThisItem.Value = "All streams", Blank(), ThisItem.Value))')])
chips=N('galChips_Sel','Gallery@2.15.0','Horizontal',{'AlignInContainer':'AlignInContainer.SetByContainer','FillPortions':'0','Height':r(48),'LayoutMinHeight':r(48),'ShowScrollbar':'false','TemplatePadding':'0','TemplateSize':r(235),'Visible':'varShowAll && CountRows(colStreamChips) > 1','Width':W,'Items':'colStreamChips'},[chip])
cnt=lbl('lblCount_Sel',f'{count} & If({count} = 1, " DTV", " DTVs") & " to audit"',w=W,h=r(22),size=14,color='C_Muted',bold=True,extra={'AlignInContainer':'AlignInContainer.SetByContainer','LayoutMinHeight':r(22)})
empty=lbl('lblEmpty_Sel','If(!IsBlank(Trim(txtSearch_Sel.Text)), "No DTVs match your search", If(varShowAll, "Every DTV has been audited in the last month", "Every DTV in your stream has been audited in the last month"))',w=W,h=r(50),size=15,color='C_Muted',align='Align.Center',wrap=True,visible=f'{count} = 0',extra={'AlignInContainer':'AlignInContainer.SetByContainer','LayoutMinHeight':r(50)})
items='''SortByColumns(
    Filter(
        DTV_Register,
        If(
            varShowAll,
            IsBlank(varStreamPick) || Stream = varStreamPick || Stream = "All",
            (!IsBlank(varStream) && Stream = varStream) || Stream = "All"
        )
        // audited in the last month: off the to-do list
        && !(Title in colRecentAudits.Value)
        && (
            IsBlank(Trim(txtSearch_Sel.Text))
            || Lower(Trim(txtSearch_Sel.Text)) in Lower(DisplayName)
            || Lower(Trim(txtSearch_Sel.Text)) in Lower(Department)
            || Lower(Trim(txtSearch_Sel.Text)) in Lower(DTVLocation)
            || Lower(Trim(txtSearch_Sel.Text)) in Lower(Title)
        )
    ),
    "field_2",
    SortOrder.Ascending
)'''
row=box('conRow_Sel',x=1,y=r(5),w=f"Parent.TemplateWidth - {r(10)}",h=r(84),fill='C_White',border='C_Line',radius=r(18),children=[
  lbl('lblDept_Sel','ThisItem.Department',x=r(16),y=r(10),w=f"Parent.Width - {r(56)}",h=r(24),size=17,color='C_Ink',bold=True),
  lbl('lblLoc_Sel','ThisItem.DTVLocation & "  ·  " & ThisItem.Title',x=r(16),y=r(35),w=f"Parent.Width - {r(56)}",h=r(20),size=14,color='C_Ink2'),
  lbl('lblAsset_Sel','ThisItem.Building & "  ·  " & ThisItem.Floor',x=r(16),y=r(56),w=f"Parent.Width - {r(56)}",h=r(20),size=13,color='C_Muted'),
  ico('icoGo_Sel','ChevronRight',f"Parent.Width - {r(36)}",r(30),24,'C_Muted'),
  tbtn('btnRow_Sel','Set(varReaudit, false);\nSet(varDTV, ThisItem);\nNavigate(Audit, ScreenTransition.Cover)'),
])
gal=N('galDTV_Sel','Gallery@2.15.0','Vertical',{'AlignInContainer':'AlignInContainer.SetByContainer','Items':items,'LayoutMinHeight':r(150),'TemplatePadding':'0','TemplateSize':r(94),'Width':W},[row])
psel='Or(And(ThisItem.Key = "MINE", !varShowAll), And(ThisItem.Key = "ALL", varShowAll, IsBlank(varStreamPick)), And(varShowAll, ThisItem.Key = varStreamPick))'
pill1=box('conPill_Sel',x=3,y=r(2),w=f"Parent.TemplateWidth - {r(6)}",h=r(48),fill=f'If({psel}, C_Accent, C_White)',border=f'If({psel}, C_Accent, C_Line)',radius=r(24),children=[
  lbl('lblPill_Sel','ThisItem.Label',x=r(4),w=f"Parent.Width - {r(8)}",h=r(48),size=14,color=f'If({psel}, C_White, C_Ink2)',bold=True,align='Align.Center',wrap=True,extra={'VerticalAlign':'VerticalAlign.Middle'}),
  tbtn('btnPill_Sel','Switch(\n    ThisItem.Key,\n    "MINE", Set(varShowAll, false); Set(varStreamPick, Blank()),\n    "ALL", Set(varShowAll, true); Set(varStreamPick, Blank()),\n    Set(varShowAll, true); Set(varStreamPick, ThisItem.Key)\n)')])
pills=N('galPills_Sel','Gallery@2.15.0','Horizontal',{'AlignInContainer':'AlignInContainer.SetByContainer','FillPortions':'0','Height':r(52),'LayoutMinHeight':r(52),'ShowScrollbar':'false','TemplatePadding':'0','TemplateSize':f"(PageW - {r(40)}) / Max(1, CountRows(colPills))",'Width':W,'Items':'colPills'},[pill1])
body=vbody('conBody_Sel',[search,pills,cnt,empty,gal],gap=12,top=15,bottom=10)
hdr=header('Sel','"Choose a DTV"','"Step 1 of 2  ·  " & If(varShowAll, Coalesce(varStreamPick, "All DTVs"), "Your stream")','Navigate(Home, ScreenTransition.UnCoverRight)')
onv_sel='''// filter pills: My Stream (if you have one), the other streams, then All
Clear(colPills);
If(!IsBlank(varStream), Collect(colPills, { Label: "My Stream", Key: "MINE" }));
ForAll(
    Filter(Distinct(DTV_Register, Stream), !IsBlank(Value) && Value <> "All" && Value <> Coalesce(varStream, "")) As s,
    Collect(colPills, { Label: Trim(First(Split(Substitute(s.Value, ",", "&"), "&")).Value), Key: s.Value })
);
Collect(colPills, { Label: "All", Key: "ALL" });
// DTVs audited in the last month (they drop off the to-do list)
Refresh(Audit_Results);
ClearCollect(
    colRecentAudits,
    Distinct(Filter(Audit_Results, Created >= DateAdd(Now(), -1, TimeUnit.Months)), Title)
)'''
open(OUT+'DTV_SelectDTV.pa.yaml','w').write(screen('SelectDTV',{'Fill':'C_Bg','OnVisible':onv_sel},[vroot('conRoot_Sel',[hdr,body])]))


# ------------------------------------------------------------------ RE-AUDIT LIST
cntR='CountRows(galRe_Re.AllItems)'
searchR=inflow('conSearch_Re',r(50),border=LINE,fill='C_White',radius=r(15),children=[
  ico('icoSearch_Re','Search',r(16),r(13),24,'C_Muted'),
  N('txtSearch_Re','Classic/TextInput@2.3.2',props={'BorderStyle':'BorderStyle.None','Color':'C_Ink','Default':'""','DelayOutput':'true','Fill':'RGBA(0, 0, 0, 0)','Font':'AppFont','Height':'Parent.Height','HintText':'"Search DTVs"','Size':r(F(16)),'Width':f"Parent.Width - {r(54)}",'X':r(46)}),
])
def segR(name,x,txt,onsel,sel):
    return box(f'con{name}_Re',x=x,w=segw,h=r(50),fill=f'If({sel}, C_Accent, C_White)',border=f'If({sel}, C_Accent, C_Line)',radius=r(25),children=[
      N(f'btn{name}_Re','ModernButton@1.0.0',props=dict({'Align':'Align.Center','Appearance':'ButtonAppearance.Transparent','Color':f'If({sel}, C_White, C_Ink2)','Font':'AppFont','FontWeight':'FontWeight.Bold','Height':'Parent.Height','OnSelect':onsel,'Size':r(F(16)),'Text':txt,'VerticalAlign':'VerticalAlign.Middle','Width':'Parent.Width'},**rad(r(25)),**{k:v for k,v in SBOX.items() if not k.startswith('Radius')})),
    ])
segsR=inflow('conSeg_Re',r(50),children=[
  segR('Follow','0','"Needs Follow-up"','Set(varReAll, false)','!varReAll'),
  segR('AllRe',f"{segw} + {r(10)}",'"All Audited"','Set(varReAll, true)','varReAll'),
])
cntRe=lbl('lblCount_Re',f'{cntR} & If({cntR} = 1, " DTV", " DTVs") & If(varReAll, " audited in the last month", " need follow-up")',w=W,h=r(22),size=14,color='C_Muted',bold=True,extra={'AlignInContainer':'AlignInContainer.SetByContainer','LayoutMinHeight':r(22)})
emptyRe=lbl('lblEmpty_Re','If(!IsBlank(Trim(txtSearch_Re.Text)), "No DTVs match your search", If(varReAll, "No DTVs have been audited in the last month", "Nothing needs follow-up. Every audited DTV passed."))',w=W,h=r(50),size=15,color='C_Muted',align='Align.Center',wrap=True,visible=f'{cntR} = 0',extra={'AlignInContainer':'AlignInContainer.SetByContainer','LayoutMinHeight':r(50)})
itemsR="""SortByColumns(
    Filter(
        colReaudit,
        (varReAll || NeedsFollowUp)
        && (
            IsBlank(Trim(txtSearch_Re.Text))
            || Lower(Trim(txtSearch_Re.Text)) in Lower(Department)
            || Lower(Trim(txtSearch_Re.Text)) in Lower(DTVLocation)
            || Lower(Trim(txtSearch_Re.Text)) in Lower(Title)
        )
    ),
    "NeedsFollowUp", SortOrder.Descending,
    "LastDate", SortOrder.Descending
)"""
rowR=box('conRow_Re',x=1,y=r(5),w=f"Parent.TemplateWidth - {r(10)}",h=r(84),fill='C_White',border='C_Line',radius=r(18),children=[
  box('conBar_Re',w=r(8),h='Parent.Height',fill='If(ThisItem.NeedsFollowUp, RGBA(176, 52, 40, 1), RGBA(30, 122, 80, 1))',extra={**{'RadiusTopLeft':r(18),'RadiusBottomLeft':r(18),'RadiusTopRight':'0','RadiusBottomRight':'0'}}),
  lbl('lblDept_Re','ThisItem.Department',x=r(22),y=r(10),w=f"Parent.Width - {r(62)}",h=r(24),size=17,color='C_Ink',bold=True),
  lbl('lblLoc_Re','ThisItem.DTVLocation & "  ·  " & ThisItem.Title',x=r(22),y=r(35),w=f"Parent.Width - {r(62)}",h=r(20),size=14,color='C_Ink2'),
  lbl('lblIssue_Re','If(ThisItem.NeedsFollowUp, ThisItem.Issue, "All clear") & "  ·  " & Text(ThisItem.LastDate, "d mmm") & If(ThisItem.WasReaudit, "  ·  re-audit", "")',x=r(22),y=r(56),w=f"Parent.Width - {r(62)}",h=r(20),size=13,color='If(ThisItem.NeedsFollowUp, RGBA(176, 52, 40, 1), RGBA(30, 122, 80, 1))',bold=True),
  ico('icoGo_Re','ChevronRight',f"Parent.Width - {r(36)}",r(30),24,'C_Muted'),
  tbtn('btnRow_Re','Set(varReaudit, true);\nSet(varPrevIssue, ThisItem.Issue);\nSet(varPrevDate, ThisItem.LastDate);\nSet(varPrevBy, ThisItem.LastBy);\nSet(varDTV, LookUp(DTV_Register, Title = ThisItem.Title));\nNavigate(Audit, ScreenTransition.Cover)'),
])
galR=N('galRe_Re','Gallery@2.15.0','Vertical',{'AlignInContainer':'AlignInContainer.SetByContainer','Items':itemsR,'LayoutMinHeight':r(150),'TemplatePadding':'0','TemplateSize':r(94),'Width':W},[rowR])
bodyR=vbody('conBody_Re',[searchR,segsR,cntRe,emptyRe,galR],gap=12,top=15,bottom=10)
hdrR=header('Re','"Re-audit"','"Pick a DTV audited in the last month"','Navigate(Home, ScreenTransition.UnCoverRight)')
onv_re="""// latest audit of each DTV in the last month (re-audits included)
Refresh(Audit_Results);
ClearCollect(
    colMonthAudits,
    SortByColumns(Filter(Audit_Results, Created >= DateAdd(Now(), -1, TimeUnit.Months)), "Created", SortOrder.Descending)
);
ClearCollect(colReg, DTV_Register);
ClearCollect(
    colReaudit,
    ForAll(
        Distinct(colMonthAudits, Title) As t,
        With(
            {
                a: LookUp(colMonthAudits, Title = t.Value),
                d: LookUp(colReg, Title = t.Value)
            },
            With(
                {
                    issue: If(
                        a.DTVFound.Value = "No",
                        "DTV not found",
                        Concat(
                            Filter(
                                Table(
                                    { p: If(a.LoginWorked.Value = "No", "Login", "") },
                                    { p: If(a.PatientListWorked.Value = "No", "Patient list", "") },
                                    { p: If(a.PrintWorked.Value = "No", "Print", "") },
                                    { p: If(a.FolderFound.Value = "No", "Kit not found", "") },
                                    { p: If(a.ContentsListInFolder.Value = "No", "No contents list", "") },
                                    { p: If(a.KitMatched.Value = "No", "Kit mismatch", "") }
                                ),
                                p <> ""
                            ),
                            p,
                            " · "
                        )
                    )
                },
                {
                    Title: t.Value,
                    Department: Coalesce(d.Department, a.DisplayName),
                    DTVLocation: Coalesce(d.DTVLocation, ""),
                    LastDate: a.Created,
                    LastBy: a.'Created By'.DisplayName,
                    Issue: issue,
                    NeedsFollowUp: !IsBlank(issue),
                    WasReaudit: !IsBlank(a.ReAudit)
                }
            )
        )
    )
);
Set(varReAll, false);
Reset(txtSearch_Re)"""
open(OUT+'DTV_ReAuditList.pa.yaml','w').write(screen('ReAuditList',{'Fill':'C_Bg','OnVisible':onv_re},[vroot('conRoot_Re',[hdrR,bodyR])]))

# ------------------------------------------------------------------ AUDIT
PADX=r(18); IW=f"Parent.Width - {r(36)}"
GREEN="RGBA(30, 122, 80, 1)"; RED="RGBA(176, 52, 40, 1)"
def yn(sfx,var,y):
    hw=f"Round((Parent.Width - {r(36)} - {r(12)}) / 2, 0)"
    def half(nm,val,col,x):
        return box(f'con{nm}_{sfx}',x=x,y=y,w=hw,h=r(48),fill=f'If({var} = "{val}", {col}, C_White)',border=f'If({var} = "{val}", {col}, C_Line)',radius=r(24),children=[
          N(f'btn{nm}_{sfx}','ModernButton@1.0.0',props=dict({'Align':'Align.Center','Appearance':'ButtonAppearance.Transparent','Color':f'If({var} = "{val}", C_White, C_Muted)','Font':'AppFont','FontWeight':'FontWeight.Bold','Height':'Parent.Height','OnSelect':f'Set({var}, "{val}")','Size':r(F(15)),'Text':f'"{val}"','VerticalAlign':'VerticalAlign.Middle','Width':'Parent.Width'},**rad(r(24)),**{k:v for k,v in SBOX.items() if not k.startswith('Radius')}))])
    return [half('Yes','Yes',GREEN,PADX),half('No','No',RED,f"{PADX} + {hw} + {r(12)}")]
def head(cap,q,sfx):
    return [lbl(f'cap_{sfx}',f'"{cap}"',x=PADX,y=r(14),w=IW,h=r(22),size=14,color='C_Muted',bold=True),
            lbl(f'q_{sfx}',f'"{q}"',x=PADX,y=r(38),w=IW,h=r(28),size=16,color='C_Ink',bold=True)]
def pill(sfx,k,var,val,y,vis):
    sel=f'{var} = "{val}"'
    return box(f'conR{k}_{sfx}',x=PADX,y=y,w=IW,h=r(44),fill=f'If({sel}, C_AccentSoft, C_White)',border=f'If({sel}, C_Accent, C_Line)',radius=r(22),visible=vis,children=[
      N(f'btnR{k}_{sfx}','ModernButton@1.0.0',props=dict({'Align':'Align.Center','Appearance':'ButtonAppearance.Transparent','Color':f'If({sel}, C_Accent, C_Muted)','Font':'AppFont','FontWeight':'FontWeight.Bold','Height':'Parent.Height','OnSelect':f'Set({var}, "{val}")','Size':r(F(14)),'Text':f'"{val}"','VerticalAlign':'VerticalAlign.Middle','Width':'Parent.Width'},**rad(r(22)),**{k2:v for k2,v in SBOX.items() if not k2.startswith('Radius')}))])
def tin(name,hint,y,h,vis=None):
    p={'BorderColor':'C_Line','BorderThickness':'1','Color':'C_Ink','Default':'""','FocusedBorderColor':'C_Accent','FocusedBorderThickness':'2','Font':'AppFont','Height':r(h),'HintText':f'"{hint}"','Mode':'TextMode.MultiLine','Size':r(F(15)),'Width':IW,'X':PADX,'Y':y}
    p.update(rad(r(12)))
    if vis:p['Visible']=vis
    return N(name,'Classic/TextInput@2.3.2',props=p)
def sub(text,y,name,vis):
    return lbl(name,f'"{text}"',x=PADX,y=y,w=IW,h=r(24),size=14,color='C_Muted',bold=True,visible=vis)
def card(name,h,children,vis=None):
    return inflow(name,f'Round(({h}) * UI, 0)',fill='C_White',border='C_Line',radius=r(20),children=children,visible=vis)

info=inflow('conInfo_Aud',r(122),fill='C_White',border='C_Line',radius=r(20),children=[
  lbl('lblInfoT_Aud','varDTV.Department',x=PADX,y=r(10),w=IW,h=r(30),size=19,color='C_Ink',bold=True),
  lbl('lblInfoL_Aud','varDTV.DTVLocation',x=PADX,y=r(42),w=IW,h=r(24),size=15,color='C_Muted'),
  lbl('lblInfoA_Aud','varDTV.Building & " · " & varDTV.Floor & " · " & varDTV.Title',x=PADX,y=r(68),w=IW,h=r(22),size=14,color='C_Muted'),
  lbl('lblInfoAcc_Aud','"Log in with account: " & varDTV.LoginAccount',x=PADX,y=r(92),w=IW,h=r(22),size=14,color='C_Accent',bold=True),
])
NO_L='varLogin = "No"'; YES_L='varLogin = "Yes"'; NO_P='varPrint = "No"'
FOUND='varFound <> "No"'
# ---- 1 DTV found
found=card('conFound_Aud','If(varFound = "No", 198, 140)',head('1  ·  DTV','Could you find the DTV?','Found')+yn('Found','varFound',r(74))+[
  box('conNotFound_Aud',x=PADX,y=r(136),w=IW,h=r(44),fill='C_AmberBg',border='RGBA(178, 105, 0, 0.35)',radius=r(16),visible='varFound = "No"',children=[
    lbl('lblNotFound_Aud','"Login, patient list and print are skipped"',x=r(12),w=f"Parent.Width - {r(24)}",h=r(44),size=14,color='C_Amber',bold=True,align='Align.Center',extra={'VerticalAlign':'VerticalAlign.Middle'})])])
# ---- 2 Login + patient list
login=card('conLogin_Aud',f'If({NO_L}, 422, If({YES_L}, 236, 140))',head('2  ·  LOGIN AND PATIENT LIST','Could you log in to the DTV?','Login')+yn('Login','varLogin',r(74))+[
  sub('Why not?',r(136),'lblWhy_LoginNo',NO_L),
  pill('LoginNo',1,'varLoginWhy','Password/Username is wrong',r(164),NO_L),
  pill('LoginNo',2,'varLoginWhy','Unable to access DTV',r(216),NO_L),
  pill('LoginNo',3,'varLoginWhy','Other',r(268),NO_L),
  tin('txtNotes_LoginNo','Notes (optional)',r(320),84,NO_L),
  lbl('lblPListQ_Aud','"Could you open the patient list?"',x=PADX,y=r(136),w=IW,h=r(28),size=16,color='C_Ink',bold=True,visible=YES_L)]
  +yn('PList','varPList',r(170)),vis=FOUND)
for c in login.children:
    if c.name in ('conYes_PList','conNo_PList'): c.props['Visible']=YES_L
# ---- 3 Print
prints=['Printer offline or not found','No printer set up on DTV','Sent to print nothing came out','Printed on wrong printer','Error message (auditor types it)','Other (type it)']
printc=head('3  ·  PRINT','Could you print from the DTV?','Print')+yn('Print','varPrint',r(74))+[sub('Why not?',r(136),'lblWhy_PrintNo',NO_P)]
for i,t in enumerate(prints): printc.append(pill('PrintNo',i+1,'varPrintWhy',t,r(164+52*i),NO_P))
printc.append(tin('txtNotes_PrintNo','Type the error message or details (optional)',r(476),84,NO_P))
printcard=card('conPrint_Aud',f'If({NO_P}, 578, 140)',printc,vis=FOUND)
# ---- 4 Kit and folder
FY='varFolder = "Yes"'; LY=f'{FY} && varList = "Yes"'; GAP=f'{LY} && varMatch = "No"'
kit=card('conKit_Aud','If(varFolder = "Yes", If(varList = "Yes", If(varMatch = "No", 578, 330), If(varList = "No", 304, 236)), If(varFolder = "No", 210, 140))',
  head('4  ·  KIT AND FOLDER','Yellow folder and kit found?','Kit')+yn('Folder','varFolder',r(74))+[
  box('conNoFolder_Aud',x=PADX,y=r(136),w=IW,h=r(56),fill='C_AmberBg',border='RGBA(178, 105, 0, 0.35)',radius=r(16),visible='varFolder = "No"',children=[
    lbl('lblNoFolder_Aud','"Kit not checked: folder and kit not found"',x=r(12),w=f"Parent.Width - {r(24)}",h=r(56),size=15,color='C_Amber',bold=True,align='Align.Center',wrap=True,extra={'VerticalAlign':'VerticalAlign.Middle'})]),
  lbl('lblListQ_Aud','"Contents list in the folder?"',x=PADX,y=r(136),w=IW,h=r(28),size=16,color='C_Ink',bold=True,visible=FY)]
  +yn('List','varList',r(170))+[
  box('conNoList_Aud',x=PADX,y=r(230),w=IW,h=r(56),fill='C_AmberBg',border='RGBA(178, 105, 0, 0.35)',radius=r(16),visible=f'{FY} && varList = "No"',children=[
    lbl('lblNoList_Aud','"Kit not checked: no contents list in the folder"',x=r(12),w=f"Parent.Width - {r(24)}",h=r(56),size=15,color='C_Amber',bold=True,align='Align.Center',wrap=True,extra={'VerticalAlign':'VerticalAlign.Middle'})]),
  lbl('lblMatchQ_Aud','"Kit matches the folder list?"',x=PADX,y=r(230),w=IW,h=r(28),size=16,color='C_Ink',bold=True,visible=LY)]
  +yn('Match','varMatch',r(264))
  +[sub('What was missing?',r(324),'lblMissing_Aud',GAP),tin('txtMissing_Aud','List missing items',r(352),84,GAP),
    sub('What was extra?',r(448),'lblExtra_Aud',GAP),tin('txtExtra_Aud','List extra items',r(476),84,GAP)])
for c in kit.children:
    if c.name in ('conYes_List','conNo_List'): c.props['Visible']=FY
    if c.name in ('conYes_Match','conNo_Match'): c.props['Visible']=LY
# ---- 5 Staff and education
EDU=['Downtime Escalation Pathway','Downtime Process','Downtime Coordinator',"Key's Location",'DMN Resourcing Page']
def edupill(k,val,y):
    v=val.replace('"','""')
    sel=f'"{v}" in colEdu.Value'
    return box(f'conEdu{k}_Aud',x=PADX,y=y,w=IW,h=r(44),fill=f'If({sel}, C_AccentSoft, C_White)',border=f'If({sel}, C_Accent, C_Line)',radius=r(22),children=[
      N(f'btnEdu{k}_Aud','ModernButton@1.0.0',props=dict({'Align':'Align.Center','Appearance':'ButtonAppearance.Transparent','Color':f'If({sel}, C_Accent, C_Muted)','Font':'AppFont','FontWeight':'FontWeight.Bold','Height':'Parent.Height','OnSelect':f'If({sel}, RemoveIf(colEdu, Value = "{v}"), Collect(colEdu, {{ Value: "{v}" }}))','Size':r(F(14)),'Text':f'If({sel}, "✓  ", "") & "{v}"','VerticalAlign':'VerticalAlign.Middle','Width':'Parent.Width'},**rad(r(22)),**{k2:x for k2,x in SBOX.items() if not k2.startswith('Radius')}))])
def tin1(name,hint,y):
    t=tin(name,hint,y,44); t.props['Mode']='TextMode.SingleLine'; return t
staff=card('conStaff_Aud','552',[
  lbl('cap_Staff','"5  ·  STAFF AND EDUCATION"',x=PADX,y=r(14),w=IW,h=r(22),size=14,color='C_Muted',bold=True),
  lbl('q_Staff','"Who did you speak to?"',x=PADX,y=r(38),w=IW,h=r(28),size=16,color='C_Ink',bold=True),
  tin1('txtSpoke_Aud','Name and role (optional)',r(70)),
  sub('Education given (tick any)',r(128),'lblEdu_Aud',None)]
  +[edupill(i+1,t,r(156+52*i)) for i,t in enumerate(EDU)]
  +[sub('Issues raised by staff',r(422),'lblIssues_Aud',None),
    tin('txtIssues_Aud','Anything the ward raised (optional)',r(450),84)])
TR="RGBA(0, 0, 0, 0)"
nophoto='IsBlank(addPhoto_Aud.Media)'
photo=card('conPhoto_Aud',f'If({nophoto}, 140, 262)',[
  lbl('cap_Photo','"6  ·  PHOTO (OPTIONAL)"',x=PADX,y=r(14),w=IW,h=r(22),size=14,color='C_Muted',bold=True),
  lbl('q_Photo','"Only if it helps show a problem"',x=PADX,y=r(38),w=IW,h=r(28),size=16,color='C_Ink',bold=True),
  box('conAddPhoto_Aud',x=PADX,y=r(74),w=IW,h=r(48),fill='C_White',border='C_Accent',radius=r(24),children=[
    lbl('lblAddPhoto_Aud',f'If({nophoto}, "Add Photo", "Change Photo")',w='Parent.Width',h=r(48),size=15,color='C_Accent',bold=True,align='Align.Center',extra={'VerticalAlign':'VerticalAlign.Middle'})]),
  N('imgPhoto_Aud','Image@2.2.3',props={'Height':r(110),'Image':'addPhoto_Aud.Media','ImagePosition':'ImagePosition.Fit','Visible':f'!{nophoto}','Width':r(110),'X':PADX,'Y':r(134)}),
  lbl('lblRemovePhoto_Aud','"Remove Photo"',x=f"{PADX} + {r(126)}",y=r(176),w=f"Parent.Width - {r(36)} - {r(126)}",h=r(26),size=15,color=RED,bold=True,visible=f'!{nophoto}'),
  tbtn('btnRemovePhoto_Aud','Reset(addPhoto_Aud)',x=f"{PADX} + {r(116)}",y=r(166),w=f"Parent.Width - {r(36)} - {r(116)}",h=r(46),display=None),
  N('addPhoto_Aud','AddMedia@2.2.1',props={'BorderColor':TR,'BorderStyle':'BorderStyle.None','BorderThickness':'0','Color':TR,'DisabledColor':TR,'DisabledFill':TR,'Fill':TR,'Font':'Font.\'Segoe UI\'','Height':r(48),'HoverBorderColor':TR,'HoverColor':TR,'HoverFill':TR,'PressedBorderColor':TR,'PressedColor':TR,'PressedFill':TR,'Size':r(F(15)),'Width':IW,'X':PADX,'Y':r(74)}),
])
notes=card('conNotes_Aud','148',[
  lbl('capNotes_Aud','"NOTES (OPTIONAL)"',x=PADX,y=r(14),w=IW,h=r(22),size=14,color='C_Muted',bold=True),
  tin('txtNotes_Aud','Anything else about this DTV or kit',r(40),90)])
# a scrolling container ignores its bottom padding at the end of the scroll, so add real space under the last card
spacer=inflow('conEnd_Aud',r(16),extra={'DropShadow':'DropShadow.None'})
prev=inflow('conPrev_Aud',r(76),fill='C_AmberBg',border='RGBA(178, 105, 0, 0.35)',radius=r(20),visible='varReaudit',children=[
  lbl('lblPrevCap_Aud','"RE-AUDIT  ·  LAST AUDIT " & Upper(Text(varPrevDate, "d mmm")) & "  ·  " & Upper(varPrevBy)',x=PADX,y=r(12),w=IW,h=r(20),size=13,color='C_Amber',bold=True),
  lbl('lblPrev_Aud','If(IsBlank(varPrevIssue), "Last audit was all clear", "Last time: " & varPrevIssue)',x=PADX,y=r(36),w=IW,h=r(28),size=16,color='C_Ink',bold=True),
])
body=vbody('conBody_Aud',[prev,info,found,login,printcard,kit,staff,photo,notes,spacer],gap=12,top=15,bottom=0,scroll=True)
READY='And(!IsBlank(varFound), varFound = "No" || And(!IsBlank(varLogin), (varLogin = "Yes" && !IsBlank(varPList)) || (varLogin = "No" && !IsBlank(varLoginWhy)), !IsBlank(varPrint), varPrint = "Yes" || !IsBlank(varPrintWhy)), !IsBlank(varFolder), varFolder = "No" || (!IsBlank(varList) && (varList = "No" || (!IsBlank(varMatch) && (varMatch = "Yes" || !IsBlank(Trim(txtMissing_Aud.Text)) || !IsBlank(Trim(txtExtra_Aud.Text)))))))'
ok='btnSubmit_Aud.DisplayMode = DisplayMode.Edit'
save='''With(
    {
        rec: Patch(
            Audit_Results,
            Defaults(Audit_Results),
            {
                Title: varDTV.Title,
                DisplayName: varDTV.DisplayName,
                Stream: varDTV.Stream,
                DTVFound: { Value: varFound },
                LoginWorked: If(varFound = "Yes", { Value: varLogin }, Blank()),
                LoginFailReason: If(varFound = "Yes" && varLogin = "No", { Value: varLoginWhy }, Blank()),
                LoginNotes: If(varFound = "Yes" && varLogin = "No", Trim(txtNotes_LoginNo.Text), Blank()),
                PatientListWorked: If(varFound = "Yes" && varLogin = "Yes", { Value: varPList }, Blank()),
                PrintWorked: If(varFound = "Yes", { Value: varPrint }, Blank()),
                PrintFailReason: If(varFound = "Yes" && varPrint = "No", { Value: varPrintWhy }, Blank()),
                PrintNotes: If(varFound = "Yes" && varPrint = "No", Trim(txtNotes_PrintNo.Text), Blank()),
                FolderFound: { Value: varFolder },
                ContentsListInFolder: If(varFolder = "Yes", { Value: varList }, Blank()),
                KitMatched: If(varFolder = "Yes" && varList = "Yes", { Value: varMatch }, Blank()),
                MissingItems: If(varFolder = "Yes" && varList = "Yes" && varMatch = "No", Trim(txtMissing_Aud.Text), Blank()),
                ExtraItems: If(varFolder = "Yes" && varList = "Yes" && varMatch = "No", Trim(txtExtra_Aud.Text), Blank()),
                SpokeTo: Trim(txtSpoke_Aud.Text),
                EducationGiven: ForAll(colEdu As e, { Value: e.Value }),
                IssuesRaised: Trim(txtIssues_Aud.Text),
                Notes: Trim(txtNotes_Aud.Text),
                ReAudit: If(varReaudit, "Yes", Blank())
            }
        )
    },
    If(
        IsEmpty(Errors(Audit_Results)),
        If(
            !IsBlank(addPhoto_Aud.Media),
            Patch(Audit_Results, rec, { AuditPhoto: imgPhoto_Aud.Image });
            If(
                !IsEmpty(Errors(Audit_Results, rec)),
                Notify("Audit saved, but the photo could not be attached.", NotificationType.Warning)
            )
        );
        // off the to-do list straight away
        Collect(colRecentAudits, { Value: varDTV.Title });
        Set(varLastAudit, rec);
        Set(varSaving, false);
        Navigate(Done, ScreenTransition.Cover),
        Set(varSaving, false);
        Notify("Could not save the audit. Check your connection and try again.", NotificationType.Error)
    )
)'''
submit=box('conSubmit_Aud',x=f"Gutter + {r(20)}",y=r(12),w=W,h=r(60),fill=f'If({ok}, C_Accent, RGBA(160, 174, 180, 1))',radius=r(28),children=[
  lbl('lblSubmit_Aud',f'If({ok}, "Submit Audit", "Answer every question to submit")',w='Parent.Width',h=r(60),size=19,color='C_White',bold=True,align='Align.Center',extra={'Size':f'If({ok}, {r(F(19))}, {r(F(15))})','VerticalAlign':'VerticalAlign.Middle'}),
  tbtn('btnSubmit_Aud','Set(varSaving, true);\n'+save,display=f'If({READY} && !varSaving, DisplayMode.Edit, DisplayMode.Disabled)'),
])
foot=inflow('conFoot_Aud',r(84),w='App.Width',fill='C_White',border='C_Line',radius='0',children=[submit])
hdr=header('Aud','If(varReaudit, "Re-audit", "Audit")','If(varReaudit, "Re-check this DTV", "Step 2 of 2")','If(varReaudit, Navigate(ReAuditList, ScreenTransition.UnCoverRight), Navigate(SelectDTV, ScreenTransition.UnCoverRight))')
onv='''Set(varFound, Blank());
Set(varLogin, Blank());
Set(varPList, Blank());
Set(varFolder, Blank());
Set(varLoginWhy, Blank());
Set(varPrint, Blank());
Set(varPrintWhy, Blank());
Set(varList, Blank());
Set(varMatch, Blank());
Set(varSaving, false);
Reset(txtNotes_LoginNo);
Reset(txtNotes_PrintNo);
Reset(txtMissing_Aud);
Reset(txtExtra_Aud);
Reset(txtNotes_Aud);
Reset(txtSpoke_Aud);
Reset(txtIssues_Aud);
Reset(addPhoto_Aud);
ClearCollect(colEdu, { Value: "" });
Clear(colEdu)'''
open(OUT+'DTV_Audit.pa.yaml','w').write(screen('Audit',{'Fill':'C_Bg','OnVisible':onv},[vroot('conRoot_Aud',[hdr,body,foot])]))

# ------------------------------------------------------------------ DONE
res='If(varLastAudit.DTVFound.Value = "No", "DTV not found", "Login " & varLastAudit.LoginWorked.Value & "  ·  Print " & varLastAudit.PrintWorked.Value) & "  ·  Kit " & If(varLastAudit.FolderFound.Value = "No", "not found", Coalesce(varLastAudit.KitMatched.Value, "no list"))'
okc=inflow('conOk_Dn',r(150),fill='C_White',border='C_Line',radius=r(20),children=[
  box('conOkIc_Dn',x=r(25),y=r(20),w=r(70),h=r(70),fill='C_AccentSoft',radius=r(35),children=[ico('icoOk_Dn','CheckmarkCircle',r(12),r(12),45,'C_Accent',True)]),
  lbl('lblOkT_Dn','"Thank You"',x=r(115),y=r(21),w=f"Parent.Width - {r(135)}",h=r(35),size=22,color='C_Ink',bold=True),
  lbl('lblOkS_Dn','varDTV.DisplayName',x=r(115),y=r(56),w=f"Parent.Width - {r(135)}",h=r(40),size=14,color='C_Muted',wrap=True),
  box('lnOk_Dn',x=r(25),y=r(104),w=f"Parent.Width - {r(50)}",h=1,fill='C_Line'),
  lbl('lblOkR_Dn',res,x=r(25),y=r(114),w=f"Parent.Width - {r(50)}",h=r(24),size=14,color='C_Ink2',bold=True),
])
nxt=inflow('conNext_Dn',r(100),fill='C_Accent',radius=r(25),children=[
  lbl('lblNextT_Dn','If(varReaudit, "Re-audit Another DTV", "Audit Another DTV")',x=r(25),y=r(22),w=f"Parent.Width - {r(40)}",h=r(35),size=22,color='C_White',bold=True),
  lbl('lblNextS_Dn','"Back to the list"',x=r(25),y=r(60),w=f"Parent.Width - {r(40)}",h=r(25),size=15,color='RGBA(255, 255, 255, 0.85)'),
  tbtn('btnNext_Dn','If(varReaudit, Navigate(ReAuditList, ScreenTransition.UnCoverRight), Navigate(SelectDTV, ScreenTransition.UnCoverRight))')])
home=inflow('conHome_Dn',r(80),fill='C_White',border='C_Line',radius=r(20),children=[
  lbl('lblHomeT_Dn','"Home"',x=r(25),w=f"Parent.Width - {r(80)}",h=r(80),size=19,color='C_Ink',bold=True,extra={'VerticalAlign':'VerticalAlign.Middle'}),
  ico('icoHomeGo_Dn','ChevronRight',f"Parent.Width - {r(45)}",r(25),30,'C_Muted'),
  tbtn('btnHome_Dn','Navigate(Home, ScreenTransition.UnCoverRight)')])
body=vbody('conBody_Dn',[okc,nxt,home],gap=12,top=18,bottom=30,scroll=True)
hdr=header('Dn','If(varReaudit, "Re-audit Saved", "Audit Saved")','varDTV.Department','Navigate(Home, ScreenTransition.UnCoverRight)')
open(OUT+'DTV_Done.pa.yaml','w').write(screen('Done',{'Fill':'C_Bg'},[vroot('conRoot_Dn',[hdr,body])]))
print('built')
