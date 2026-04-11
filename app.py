"""
Cykelinfrastruktur Dashboard - Hudiksvalls kommun
==================================================
Streamlit-app som visar att investeringar i cykelvägar är ekonomiskt
försvarbara jämfört med bilvägar. Byggd för politiska diskussioner.

Starta:  streamlit run app.py

Alla grundsiffror och källhänvisningar finns i kalldata.py -
ändra där om nya budgetar eller rapporter publiceras.
"""

import streamlit as st
import plotly.graph_objects as go

from kalldata import (
    KOSTNAD_CYKEL_LANDSBYGD, KOSTNAD_CYKEL_TATORT,
    UNDERHALL_BILVAG_PER_KM, UNDERHALL_CYKEL_ANDEL,
    BEFINTLIGA_CYKELKM, CYKELM_PER_INVÅNARE, SNITT_SMÅ_KOMMUNER,
    SNITT_SMÅ_KOMMUNER_MIN, SNITT_SMÅ_KOMMUNER_MAX,
    BUDGET_2025_MSEK, INVÅNARE,
    BOENDE_PER_KM_TATORT, BOENDE_PER_KM_LANDSBYGD, OMSTÄLLNINGSANDEL,
    ANDEL_CYKELAVSTÅND_KOMMUN, ANDEL_CYKELAVSTÅND_CENTRUM,
    TYPISK_ENKELRESA_KM, CYKELDAGAR_PER_ÅR, CYKELKM_PER_ÅR,
    ASEK_HÄLSOVÄRDE_PER_KM, HÄLSOVINST_PER_CYKLIST_ÅR,
    ASEK_ALLVARLIGT_SKADAD_MSEK, ASEK_LINDRIGT_SKADAD_MSEK,
    GC_OLYCKOR_ALLVARLIGA_PER_ÅR,
    CO2_GRAM_PER_KM_BIL,
    JÄMFÖRELSEKOMMUNER, STADSDELAR_BILINNEHAV,
    BILKOSTNAD_ÅR, BILKÖRNING_ÅR_KM, BILKOSTNAD_FAST_ÅR, BILFÖRSÄKRING_ÅR,
    BILKOSTNAD_BRÄNSLE_PER_KM, BILKOSTNAD_ÖVRIG_RÖRLIG_PER_KM,
    BILKOSTNAD_RÖRLIG_PER_KM, CYKELKOSTNAD_ÅR, CYKELFÖRSÄKRING_ÅR,
    EXTERN_ANDEL_KLIMATKLIVET, EXTERN_ANDEL_REGION,
    KALLOR, AVVÄGNINGAR,
)

# ──────────────────────────────────────────────────────────────────────
# HJÄLPFUNKTIONER
# ──────────────────────────────────────────────────────────────────────

# Datakvalitets-badge: 🟢 = exakt lokal data, 🟡 = nationell schablon
KVALITET_IKON = {"lokal": "🟢", "schablon": "🟡"}
KVALITET_ETIKETT = {"lokal": "Lokal data", "schablon": "Nationell schablon"}


def kvalitets_badge(kvalitet: str) -> str:
    """Returnerar en färgkodad badge-sträng för datakvalitet."""
    ikon = KVALITET_IKON.get(kvalitet, "⚪")
    text = KVALITET_ETIKETT.get(kvalitet, "Okänd")
    return f"{ikon} {text}"


def rendera_kallor_sidebar():
    """Renderar expanderbar källsektion i sidomenyn."""
    st.sidebar.markdown("---")
    st.sidebar.header("Källor och fördjupning")
    st.sidebar.markdown(
        f"{KVALITET_IKON['lokal']} = Lokal data (Hudiksvall)&emsp;"
        f"{KVALITET_IKON['schablon']} = Nationell schablon"
    )

    for grupp in KALLOR.values():
        with st.sidebar.expander(grupp["rubrik"]):
            for k in grupp["kallor"]:
                badge = kvalitets_badge(k["kvalitet"])
                st.markdown(
                    f"**[{k['namn']}]({k['url']})** {badge}  \n"
                    f"{k['beskrivning']}  \n"
                    f"*Datapunkt:* {k['datapunkt']}",
                )


# ──────────────────────────────────────────────────────────────────────
# APP-CONFIG
# ──────────────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Cykelinfrastruktur Hudiksvall",
    page_icon="🚲",
    layout="wide",
)

st.title("🚲 Cykelinfrastruktur - Hudiksvalls kommun")
st.markdown(
    "**Varför det kostar mer att *inte* investera i cykelvägar.**  \n"
    "Använd reglagen i sidopanelen för att utforska olika scenarier."
)

# ──────────────────────────────────────────────────────────────────────
# SIDOPANEL - Interaktiva kontroller
# ──────────────────────────────────────────────────────────────────────

st.sidebar.header("Scenarier")

ny_cykel_km = st.sidebar.slider(
    "Ny cykelvägslängd (km)", min_value=1, max_value=15, value=2, step=1
)

plats = st.sidebar.radio("Var byggs cykelvägen?", ["Tätort", "Landsbygd"])

# Cyklistberäkning - kopplad till sträckan, inte en lös procent
boende_per_km = BOENDE_PER_KM_TATORT if plats == "Tätort" else BOENDE_PER_KM_LANDSBYGD
potentiella = ny_cykel_km * boende_per_km
beräknade_cyklister = int(potentiella * OMSTÄLLNINGSANDEL)

omställning_pct = st.sidebar.slider(
    "Omställningsandel - andel boende längs sträckan som börjar cykla (%)",
    min_value=5, max_value=25, value=int(OMSTÄLLNINGSANDEL * 100), step=5,
)
nya_cyklister = int(potentiella * omställning_pct / 100)

st.sidebar.caption(
    f"Ca {potentiella:,} boende inom cykelavstånd från {ny_cykel_km} km "
    f"({plats.lower()}). Med {omställning_pct} % omställning "
    f"= **{nya_cyklister:,} nya cyklister**.".replace(",", " ")
)

tidshorisont = st.sidebar.slider(
    "Tidshorisont (år)", min_value=5, max_value=30, value=10, step=5
)

# Extern finansiering - opt-in, inte standard
st.sidebar.markdown("---")
st.sidebar.subheader("Extern finansiering")
st.sidebar.caption(
    "Grundkalkylen utgår från att kommunen betalar allt själv. "
    "Aktivera för att se vad extern medfinansiering kan ge."
)
visa_extern = st.sidebar.checkbox("Inkludera extern finansiering", value=False)

if visa_extern:
    andel_klimatklivet = st.sidebar.slider(
        "Klimatklivet (%)", min_value=0, max_value=50,
        value=int(EXTERN_ANDEL_KLIMATKLIVET * 100), step=5,
    ) / 100
    andel_region = st.sidebar.slider(
        "Region Gävleborg (%)", min_value=0, max_value=30,
        value=int(EXTERN_ANDEL_REGION * 100), step=5,
    ) / 100
else:
    andel_klimatklivet = 0.0
    andel_region = 0.0

# Rendera källor i sidomenyn (under kontrollerna)
rendera_kallor_sidebar()

# ──────────────────────────────────────────────────────────────────────
# BERÄKNINGAR
# ──────────────────────────────────────────────────────────────────────

kostnad_per_km = KOSTNAD_CYKEL_TATORT if plats == "Tätort" else KOSTNAD_CYKEL_LANDSBYGD

investering_cykel = ny_cykel_km * kostnad_per_km       # MSEK

underhall_cykel_ar = ny_cykel_km * UNDERHALL_BILVAG_PER_KM * UNDERHALL_CYKEL_ANDEL / 1_000  # MSEK

# Extern finansiering (0 % som standard - kommunen betalar allt)
extern_klimatklivet = investering_cykel * andel_klimatklivet
extern_region = investering_cykel * andel_region
kommunens_kostnad = investering_cykel - extern_klimatklivet - extern_region

# Hälsovinster (nya_cyklister beräknas i sidopanelen, kopplat till sträckan)
hälsovinst_år = nya_cyklister * HÄLSOVINST_PER_CYKLIST_ÅR / 1_000_000  # MSEK
hälsovinst_total = hälsovinst_år * tidshorisont

# Break-even: när hämtar hälsovinsterna hem investeringen?
netto_årlig_vinst = hälsovinst_år - underhall_cykel_ar
breakeven_år = kommunens_kostnad / netto_årlig_vinst if netto_årlig_vinst > 0 else float("inf")

# Budgetkontext - hur stor del av årsbudgeten?
andel_av_budget = investering_cykel / BUDGET_2025_MSEK
budgetår_behov = investering_cykel / BUDGET_2025_MSEK  # Antal hela årsbudgetar

# Trafiksäkerhet - samhällsbesparing från undvikna olyckor
undvikna_allvarliga_år = GC_OLYCKOR_ALLVARLIGA_PER_ÅR * 0.5  # 50 % reduktion konservativt
besparing_olyckor_år = undvikna_allvarliga_år * ASEK_ALLVARLIGT_SKADAD_MSEK  # MSEK

# CO₂-besparing
co2_ton_per_år = nya_cyklister * CYKELKM_PER_ÅR * CO2_GRAM_PER_KM_BIL / 1_000_000
bilar_motsvarande = co2_ton_per_år / (15_000 * CO2_GRAM_PER_KM_BIL / 1_000_000)  # ~15 000 km/år per bil

# ──────────────────────────────────────────────────────────────────────
# LAYOUT - Nyckeltal överst
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")

kol1, kol2, kol3, kol4 = st.columns(4)
kol1.metric("Investering cykelväg", f"{investering_cykel:.0f} MSEK")
if visa_extern:
    kol2.metric("Kommunens nettokostnad", f"{kommunens_kostnad:.1f} MSEK",
                delta=f"-{extern_klimatklivet + extern_region:.1f} MSEK extern",
                delta_color="inverse")
else:
    kol2.metric("Kommunen betalar", f"{investering_cykel:.0f} MSEK",
                delta="100 % kommunalt - utan önsketänkande",
                delta_color="off")
kol3.metric("Hälsovinst per år", f"{hälsovinst_år:.1f} MSEK",
            delta=f"{nya_cyklister:,} nya cyklister".replace(",", " "))
kol4.metric(
    "Break-even",
    f"ca {breakeven_år:.0f} år" if netto_årlig_vinst > 0 else " -",
    delta="enbart hälsovinster" if netto_årlig_vinst > 0 else "",
)

# Budgetkontext - så att ingen tror att vi ignorerar verkligheten
if andel_av_budget > 1:
    st.warning(
        f"**Budgetperspektiv:** Investeringen ({investering_cykel:.0f} MSEK) motsvarar "
        f"**{andel_av_budget:.1f}x hela årsbudgeten** för vägnätet ({BUDGET_2025_MSEK} MSEK, 2025). "
        f"Det innebär att projektet sannolikt sprids över flera år eller kräver särskild anslag. "
        f"OBS: 25 MSEK avser hela vägnätet inkl. underhåll - inte enbart cykel."
    )
else:
    st.info(
        f"**Budgetperspektiv:** Investeringen ({investering_cykel:.0f} MSEK) motsvarar "
        f"**{andel_av_budget:.0%} av årsbudgeten** för vägnätet ({BUDGET_2025_MSEK} MSEK, 2025). "
        f"OBS: 25 MSEK avser hela vägnätet inkl. underhåll - inte enbart cykel."
    )

# ──────────────────────────────────────────────────────────────────────
# 1. INVESTERA ELLER GÖRA INGENTING?
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("1. Investera eller göra ingenting?")
st.markdown(
    f"Frågan är inte om vi har råd att bygga cykelväg. "
    f"Frågan är om vi har råd att **låta bli**.  \n"
    f"Diagrammet visar ackumulerade kostnader över **{tidshorisont} år** "
    f"för de två alternativen."
)

# Ackumulerade serier - diagrammet sträcker sig alltid förbi break-even
diagram_år = tidshorisont
if netto_årlig_vinst > 0 and breakeven_år < float("inf"):
    diagram_år = max(tidshorisont, int(breakeven_år) + 3)
år_lista_1 = list(range(0, diagram_år + 1))

# INVESTERA: Engångskostnad år 0, sedan underhåll per år
kum_investera = [kommunens_kostnad + underhall_cykel_ar * år for år in år_lista_1]

# GÖRA INGENTING: Ingen investering, men varje år som går utan cykelväg
# förlorar samhället hälsovinster (uteblivna besparingar i sjukvård)
# och hushåll fortsätter betala för bilberoende.
kum_ingenting = [hälsovinst_år * år for år in år_lista_1]

fig_val = go.Figure()

fig_val.add_trace(go.Scatter(
    x=år_lista_1, y=kum_investera,
    mode="lines+markers", name="Investera i cykelväg (kommunens kostnad)",
    line=dict(color="#3498db", width=3),
))

fig_val.add_trace(go.Scatter(
    x=år_lista_1, y=kum_ingenting,
    mode="lines+markers", name="Göra ingenting (förlorade samhällsvinster)",
    line=dict(color="#e74c3c", width=3, dash="dash"),
    fill="tozeroy", fillcolor="rgba(231,76,60,0.08)",
))

# Markera break-even i diagrammet
if netto_årlig_vinst > 0 and breakeven_år < float("inf"):
    breakeven_y = kommunens_kostnad + underhall_cykel_ar * breakeven_år
    fig_val.add_trace(go.Scatter(
        x=[breakeven_år], y=[breakeven_y],
        mode="markers+text",
        marker=dict(size=14, color="#f39c12", symbol="diamond"),
        text=[f"Break-even: år {breakeven_år:.0f}"],
        textposition="top center",
        name="Break-even",
    ))

fig_val.update_layout(
    xaxis_title="År efter beslut",
    yaxis_title="MSEK (ackumulerat)",
    height=450,
    margin=dict(t=30),
    legend=dict(orientation="h", y=-0.15),
)

st.plotly_chart(fig_val, width="stretch")

# Förklarande text beroende på break-even
if netto_årlig_vinst > 0 and breakeven_år < float("inf"):
    st.success(
        f"**Investeringen hämtar hem sig på ca {breakeven_år:.0f} år** enbart genom "
        f"hälsovinster ({hälsovinst_år:.2f} MSEK/år). "
        f"Efter det kostar varje år *utan* cykelväg mer än ett år *med*."
    )
else:
    st.info(
        "Med nuvarande antaganden nås inte break-even. "
        "Prova en högre omställningsandel i sidomenyn."
    )

# Kompletterande budgetperspektiv
st.markdown(
    f"**Underhåll i perspektiv:** Cykelvägens underhåll kostar "
    f"**{underhall_cykel_ar:.2f} MSEK/år** - det är "
    f"**{underhall_cykel_ar / BUDGET_2025_MSEK:.1%} av kommunens "
    f"årliga vägbudget** ({BUDGET_2025_MSEK} MSEK).  \n"
    f"{kvalitets_badge('schablon')} Hälsovinster ({hälsovinst_år:.2f} MSEK/år) "
    f"tillfaller främst regionens sjukvårdsbudget, men en friskare befolkning "
    f"minskar även kommunens kostnader för hemtjänst och sociala insatser."
)

# ──────────────────────────────────────────────────────────────────────
# 2. FINANSIERINGSKALKYL
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("2. Finansieringskalkyl")

if visa_extern:
    st.markdown(
        "Med extern medfinansiering kan kommunens andel minska avsevärt.  \n"
        f"{kvalitets_badge('schablon')} Finansieringsandelar baserade på Klimatklivets och regionens generella villkor."
    )

    fig_finans = go.Figure(go.Pie(
        labels=["Kommunen", f"Klimatklivet ({int(andel_klimatklivet*100)} %)",
                f"Region Gävleborg ({int(andel_region*100)} %)"],
        values=[kommunens_kostnad, extern_klimatklivet, extern_region],
        marker_colors=["#3498db", "#2ecc71", "#f39c12"],
        hole=0.45,
        textinfo="label+value",
        texttemplate="%{label}<br>%{value:.1f} MSEK",
    ))

    fig_finans.update_layout(
        height=380,
        margin=dict(t=20, b=20),
        annotations=[dict(text=f"{kommunens_kostnad:.1f}<br>MSEK", x=0.5, y=0.5,
                           font_size=18, showarrow=False)],
    )

    st.plotly_chart(fig_finans, width="stretch")

    st.success(
        f"**Med extern finansiering: {kommunens_kostnad:.1f} MSEK** "
        f"(av {investering_cykel:.0f} MSEK total investering).  \n"
        f"Hälsovinsten på **{hälsovinst_total:.1f} MSEK** över {tidshorisont} år "
        f"kan dessutom räknas av mot kostnaden."
    )
else:
    st.markdown(
        "**Grundkalkylen: kommunen betalar allt själv.** "
        "Ingen extern finansiering inräknad - detta är vad det kostar om vi inte "
        "söker ett enda bidrag."
    )

    fig_finans = go.Figure(go.Bar(
        x=["Investering (100 % kommunalt)", f"Underhåll ({tidshorisont} år)"],
        y=[investering_cykel, underhall_cykel_ar * tidshorisont],
        marker_color=["#3498db", "#2980b9"],
        text=[f"{investering_cykel:.0f} MSEK",
              f"{underhall_cykel_ar * tidshorisont:.1f} MSEK"],
        textposition="outside",
    ))

    fig_finans.update_layout(
        yaxis_title="Miljoner kronor (MSEK)",
        height=380,
        margin=dict(t=30),
    )

    st.plotly_chart(fig_finans, width="stretch")

    st.info(
        f"**Med 100 % kommunal finansiering: {investering_cykel:.0f} MSEK investering "
        f"+ {underhall_cykel_ar * tidshorisont:.1f} MSEK underhåll på {tidshorisont} år.**  \n"
        f"Aktivera *extern finansiering* i sidomenyn för att se hur kostnaden "
        f"kan sänkas med Klimatklivet och Region Gävleborg."
    )

# ──────────────────────────────────────────────────────────────────────
# 3. HÄLSOKALKYL
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("3. Hälsokalkyl - Minskade sjukvårdskostnader")
st.markdown(
    f"Beräkningen utgår från att **{potentiella:,} invånare** bor inom cykelavstånd "
    f"(500 m) från den nya sträckan, och att **{omställning_pct} %** av dem "
    f"({nya_cyklister:,} personer) börjar cykla regelbundet.".replace(",", " ")
)

# Visa beräkningskedjan transparent
with st.expander("Så räknar vi - steg för steg"):
    st.markdown(f"""
| Steg | Antagande | Källa |
|------|-----------|-------|
| Typisk enkelresa | **{TYPISK_ENKELRESA_KM} km** (15 min x {int(18)} km/h) | [Newsworthy/Tyréns 2022](https://www.newsworthy.se/artikel/249947/h%C3%A4r-%C3%A4r-hudiksvallsomr%C3%A5det-d%C3%A4r-n%C3%A4stan-%C3%A5tta-av-tio-kan-cykla-till-jobbet) |
| Tur/retur per dag | **{TYPISK_ENKELRESA_KM * 2} km** | - |
| Cykeldagar per år | **{CYKELDAGAR_PER_ÅR}** (konservativt, exkl. vinterhalvåret) | Antagande |
| Cykelkilometer per år | **{CYKELKM_PER_ÅR:,.0f} km** | Beräknat |
| Hälsovärde per km | **{ASEK_HÄLSOVÄRDE_PER_KM:.2f} SEK** | [Trafikverket ASEK 7.0](https://bransch.trafikverket.se/for-dig-i-branschen/Planera-och-utreda/samhallsekonomisk-analys-och-trafikanalys/samhallsekonomiska-analysmetoder-inom-transportomradet---asek/) |
| **Hälsovinst per cyklist/år** | **{HÄLSOVINST_PER_CYKLIST_ÅR:,} kr** | Beräknat |
""".replace(",", " "))
    st.caption(
        f"Hudiksvall-kontext: 39 % av anställda har max 15 min cykelväg till jobbet. "
        f"I centrala stadsdelar (Kristineberg, Jakobsberg, Håsta) är andelen 67–75 %."
    )

år_lista = list(range(1, tidshorisont + 1))
kum_hälsa = [hälsovinst_år * i for i in år_lista]
kum_komm = [kommunens_kostnad] * tidshorisont

fig_hälsa = go.Figure()
fig_hälsa.add_trace(go.Scatter(
    x=år_lista, y=kum_hälsa,
    mode="lines+markers", name="Kumulativ hälsovinst",
    line=dict(color="#2ecc71", width=3),
    fill="tozeroy", fillcolor="rgba(46,204,113,0.15)",
))
fig_hälsa.add_trace(go.Scatter(
    x=år_lista, y=kum_komm,
    mode="lines", name="Kommunens nettokostnad",
    line=dict(color="#e74c3c", width=2, dash="dash"),
))

fig_hälsa.update_layout(
    xaxis_title="År efter investering",
    yaxis_title="MSEK",
    height=380,
    margin=dict(t=30),
    legend=dict(orientation="h", y=-0.18),
)

st.plotly_chart(fig_hälsa, width="stretch")

if hälsovinst_år > 0:
    payback = kommunens_kostnad / hälsovinst_år
    st.info(
        f"**Återbetalningstid enbart via hälsovinster: ca {payback:.1f} år.**  \n"
        f"Med {nya_cyklister:,} nya cyklister à {HÄLSOVINST_PER_CYKLIST_ÅR:,} kr/år "
        f"= **{hälsovinst_år:.1f} MSEK per år** i minskade sjukvårdskostnader.".replace(",", " ")
    )

# ──────────────────────────────────────────────────────────────────────
# 4. TRAFIKSÄKERHET - Undvikna olyckor
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("4. Trafiksäkerhet - Undvikna olyckor")
st.markdown(
    f"**GC-olycka** = olycka med gående eller cyklist (*oskyddad trafikant*) "
    f"inblandad - typiskt kollision med motorfordon, singelolycka på grund av "
    f"dålig vägyta, eller konflikt i korsning utan separerad cykelbana.  \n\n"
    f"Separerad cykelinfrastruktur minskar dessa olyckor. "
    f"Varje undviken allvarlig skada sparar "
    f"samhället **{ASEK_ALLVARLIGT_SKADAD_MSEK} MSEK** - sjukvård, rehabilitering, "
    f"produktionsbortfall och livskvalitetsförlust (ASEK 7.0).  \n"
    f"{kvalitets_badge('lokal')} Olycksdata från STRADA (Transportstyrelsen) - "
    f"den nationella databasen dit polis och akutsjukvård rapporterar trafikskador.  \n"
    f"{kvalitets_badge('schablon')} Samhällskostnad per olycka från Trafikverkets ASEK 7.0."
)

kol_s1, kol_s2, kol_s3 = st.columns(3)
kol_s1.metric(
    "Allvarliga GC-olyckor/år",
    f"{GC_OLYCKOR_ALLVARLIGA_PER_ÅR}",
    delta="gång/cykel - STRADA 5-årssnitt",
    delta_color="off",
)
kol_s2.metric(
    "Antagen reduktion",
    f"{undvikna_allvarliga_år:.0f} undvikna/år",
    delta="50 % - konservativt",
    delta_color="off",
)
kol_s3.metric(
    "Samhällsbesparing",
    f"{besparing_olyckor_år:.1f} MSEK/år",
    delta=f"{ASEK_ALLVARLIGT_SKADAD_MSEK} MSEK per allvarlig skada",
    delta_color="off",
)

if besparing_olyckor_år > 0:
    breakeven_med_olyckor = kommunens_kostnad / (netto_årlig_vinst + besparing_olyckor_år) \
        if (netto_årlig_vinst + besparing_olyckor_år) > 0 else float("inf")
    st.success(
        f"**En enda undviken allvarlig olycka per år sparar {ASEK_ALLVARLIGT_SKADAD_MSEK} MSEK** "
        f" - det motsvarar {ASEK_ALLVARLIGT_SKADAD_MSEK / investering_cykel:.0%} av hela investeringen.  \n"
        f"Med hälsovinster + olycksbesparing kombinerat: break-even på "
        f"**ca {breakeven_med_olyckor:.0f} år**."
    )

st.caption(
    "STRADA underrapporterar cykelolyckor med ca 60 %. "
    "Den verkliga olycksbilden är troligen betydligt värre än vad som "
    "registreras. Vår beräkning bygger på rapporterade olyckor."
)

# ──────────────────────────────────────────────────────────────────────
# 5. KLIMAT - CO₂-besparing
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("5. Klimatvinst - CO₂-besparing")
st.markdown(
    f"Varje bilresa som ersätts med cykling minskar utsläppen. "
    f"En genomsnittlig personbil i Sverige släpper ut "
    f"**{CO2_GRAM_PER_KM_BIL} g CO₂/km**.  \n"
    f"{kvalitets_badge('schablon')} Utsläppsfaktor: Naturvårdsverket, svenskt flottsnittvärde."
)

kol_c1, kol_c2 = st.columns(2)
kol_c1.metric(
    "CO₂-besparing per år",
    f"{co2_ton_per_år:.1f} ton",
    delta=f"{nya_cyklister:,} cyklister x {CYKELKM_PER_ÅR:,} km/år".replace(",", " "),
)
kol_c2.metric(
    "Motsvarar",
    f"{bilar_motsvarande:.0f} bilar borta",
    delta="som kör 15 000 km/år",
    delta_color="off",
)

co2_over_time = co2_ton_per_år * tidshorisont
st.info(
    f"**{co2_over_time:.0f} ton CO₂** på {tidshorisont} år.  \n"
    f"Det här stärker en ansökan till **Klimatklivet** - som kan ge "
    f"upp till 50 % medfinansiering för investeringar som minskar utsläpp."
)

# ──────────────────────────────────────────────────────────────────────
# 6. HUDIKSVALL-GAPET - Meter cykelväg per invånare
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("6. Hudiksvall vs grannkommunerna - Cykelväg per invånare")
st.markdown(
    f"{kvalitets_badge('lokal')} Befintliga 59 km och 1,6 m/inv. från Cykelfrämjandets kommunrapport 2022.  \n"
    f"{kvalitets_badge('lokal')} Jämförelsekommuner: "
    + ", ".join(f"[{k['namn']}]({k['url']})" for k in JÄMFÖRELSEKOMMUNER)
    + " - alla från Cykelfrämjandet 2022."
)

nuvarande = CYKELM_PER_INVÅNARE
efter_inv = (BEFINTLIGA_CYKELKM + ny_cykel_km) * 1_000 / INVÅNARE

# Bygg stapeldiagram med Hudiksvall + jämförelsekommuner
gap_namn = ["Hudiksvall idag", "Efter investering"]
gap_värden = [nuvarande, efter_inv]
gap_färger = ["#e74c3c", "#2ecc71"]
gap_text = [f"{nuvarande:.1f} m", f"{efter_inv:.1f} m"]

for k in JÄMFÖRELSEKOMMUNER:
    gap_namn.append(k["namn"])
    gap_värden.append(k["cykelm_per_inv"])
    gap_färger.append("#3498db")
    gap_text.append(f"{k['cykelm_per_inv']:.1f} m")

gap_namn.append(f"Snitt ({SNITT_SMÅ_KOMMUNER_MIN}–{SNITT_SMÅ_KOMMUNER_MAX})")
gap_värden.append(SNITT_SMÅ_KOMMUNER)
gap_färger.append("#95a5a6")
gap_text.append(f"{SNITT_SMÅ_KOMMUNER:.1f} m")

fig_gap = go.Figure()

fig_gap.add_trace(go.Bar(
    x=gap_namn, y=gap_värden,
    marker_color=gap_färger,
    text=gap_text,
    textposition="outside",
))

fig_gap.update_layout(
    yaxis_title="Meter cykelväg per invånare",
    height=420,
    margin=dict(t=30),
)

st.plotly_chart(fig_gap, width="stretch")

gap = SNITT_SMÅ_KOMMUNER - nuvarande
sämsta_jmf = min(k["cykelm_per_inv"] for k in JÄMFÖRELSEKOMMUNER)
if efter_inv >= SNITT_SMÅ_KOMMUNER:
    st.success(
        f"Med {ny_cykel_km} km ny cykelväg når Hudiksvall **{efter_inv:.1f} meter per invånare** "
        f" - över snittet på {SNITT_SMÅ_KOMMUNER} m!"
    )
elif efter_inv >= sämsta_jmf:
    st.info(
        f"Med {ny_cykel_km} km ny cykelväg når Hudiksvall **{efter_inv:.1f} m/invånare** "
        f" - i paritet med grannkommunerna men fortfarande "
        f"{SNITT_SMÅ_KOMMUNER - efter_inv:.1f} m under snittet."
    )
else:
    st.warning(
        f"Hudiksvall ligger **{gap:.1f} meter under snittet** och under samtliga "
        f"jämförelsekommuner. Investering på {ny_cykel_km} km tar oss till "
        f"{efter_inv:.1f} m/invånare - fortfarande {SNITT_SMÅ_KOMMUNER - efter_inv:.1f} m kvar."
    )

# ──────────────────────────────────────────────────────────────────────
# 7. KLASSPERSPEKTIV - Transportkostnader
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("7. Rättviseperspektivet - Transportkostnader per hushåll")

st.markdown(
    "Cykelinfrastruktur handlar inte om samma sak för alla.  \n"
    "- **Hushåll med god ekonomi:** Möjlighet att slippa *andrabilen* - "
    "en ren besparing.  \n"
    "- **Hushåll med små marginaler:** Tillgång till mobilitet som idag "
    "kräver en bil de knappt har råd med - eller helt saknar.  \n\n"
    f"{kvalitets_badge('schablon')} Bilkostnad baserad på Konsumentverkets genomsnitt "
    f"(fast + rörlig uppdelning)."
)

# Beräkna tredje alternativet: bil + cykelpendling
# Personen äger fortfarande bilen men sparar rörliga km-kostnader
# genom att cykla till/från jobb istället för att köra.
sparade_bilkm = CYKELKM_PER_ÅR  # km som ersätts av cykel
sparad_bränsle = sparade_bilkm * BILKOSTNAD_BRÄNSLE_PER_KM
sparad_övrig_rörlig = sparade_bilkm * BILKOSTNAD_ÖVRIG_RÖRLIG_PER_KM
minskad_rörlig = sparad_bränsle + sparad_övrig_rörlig
cykel_total_år = CYKELKOSTNAD_ÅR + CYKELFÖRSÄKRING_ÅR
kombikostnad_år = BILKOSTNAD_ÅR - minskad_rörlig + cykel_total_år
bränsle_år_bil = BILKÖRNING_ÅR_KM * BILKOSTNAD_BRÄNSLE_PER_KM

kol_a, kol_b, kol_c = st.columns(3)
with kol_a:
    st.metric("Enbart bil", f"{BILKOSTNAD_ÅR:,} kr/år".replace(",", " "))
    st.caption(
        f"Bränsle: {bränsle_år_bil:,.0f} kr "
        f"({BILKOSTNAD_BRÄNSLE_PER_KM:.2f} kr/km x "
        f"{BILKÖRNING_ÅR_KM:,} km). "
        f"Försäkring: {BILFÖRSÄKRING_ÅR:,} kr.".replace(",", " ")
    )
with kol_b:
    st.metric(
        "Bil + cykelpendling",
        f"{kombikostnad_år:,.0f} kr/år".replace(",", " "),
        delta=f"-{BILKOSTNAD_ÅR - kombikostnad_år:,.0f} kr/år".replace(",", " "),
        delta_color="inverse",
    )
    st.caption(
        f"Sparar {sparade_bilkm:,} km bilkörning/år: "
        f"bränsle -{sparad_bränsle:,.0f} kr, "
        f"slitage -{sparad_övrig_rörlig:,.0f} kr. "
        f"Cykel +{cykel_total_år:,} kr (underhåll + försäkring).".replace(",", " ")
    )
with kol_c:
    st.metric(
        "Enbart cykel",
        f"{cykel_total_år:,} kr/år".replace(",", " "),
        delta=f"-{BILKOSTNAD_ÅR - cykel_total_år:,} kr/år".replace(",", " "),
        delta_color="inverse",
    )
    st.caption(
        f"Underhåll {CYKELKOSTNAD_ÅR:,} kr + "
        f"försäkring {CYKELFÖRSÄKRING_ÅR:,} kr. "
        f"Förutsätter att hushållet kan klara sig utan bil.".replace(",", " ")
    )

# Dubbelframing - två kolumner med varsitt perspektiv
st.markdown("")
kol_välstånd, kol_rättvisa = st.columns(2)
with kol_välstånd:
    st.markdown(
        "**Hushåll med två bilar**  \n"
        f"Att ersätta andrabilen med cykel sparar "
        f"**{BILKOSTNAD_ÅR:,} kr/år** - samma som en semesterresa. "
        f"Med cykelpendling och bil kvar för helger: "
        f"minus **{BILKOSTNAD_ÅR - kombikostnad_år:,.0f} kr/år** "
        f"i rörliga kostnader.".replace(",", " ")
    )
with kol_rättvisa:
    st.markdown(
        "**Hushåll utan bil**  \n"
        "Idag betyder avsaknad av bil ofta begränsad tillgång till "
        "jobb, vård och fritid. Cykelinfrastruktur ger *reell mobilitet* "
        f"för **{CYKELKOSTNAD_ÅR:,} kr/år** istället för "
        f"{BILKOSTNAD_ÅR:,} kr - skillnaden avgör om pengarna "
        f"räcker till hyran.".replace(",", " ")
    )

with st.expander("Så räknar vi - fast vs rörlig bilkostnad"):
    st.markdown(f"""
| Post | Belopp | Typ |
|------|--------|-----|
| Försäkring (helförsäkring) | **{BILFÖRSÄKRING_ÅR:,} kr/år** | Fast |
| Skatt, parkering, tidsbaserad värdeminskning | **{BILKOSTNAD_FAST_ÅR - BILFÖRSÄKRING_ÅR:,} kr/år** | Fast |
| Bränsle (0,065 L/km x ~19 SEK/L) | **{BILKOSTNAD_BRÄNSLE_PER_KM:.2f} kr/km** (~{bränsle_år_bil:,.0f} kr/år) | Rörligt |
| Slitage, däck, service, km-värdeminskning | **{BILKOSTNAD_ÖVRIG_RÖRLIG_PER_KM:.2f} kr/km** | Rörligt |
| **Rörligt totalt** | **{BILKOSTNAD_RÖRLIG_PER_KM:.2f} kr/km** | Bränsle + övrigt |
| | | |
| **Cykelpendling ersätter** | **{sparade_bilkm:,} km/år** | {TYPISK_ENKELRESA_KM} km x 2 x {CYKELDAGAR_PER_ÅR} dagar |
| Sparad bränsle | **{sparad_bränsle:,.0f} kr/år** | {sparade_bilkm:,} km x {BILKOSTNAD_BRÄNSLE_PER_KM:.2f} kr |
| Sparat slitage m.m. | **{sparad_övrig_rörlig:,.0f} kr/år** | {sparade_bilkm:,} km x {BILKOSTNAD_ÖVRIG_RÖRLIG_PER_KM:.2f} kr |
| Cykelunderhåll tillkommer | **{CYKELKOSTNAD_ÅR:,} kr/år** | Service, kedja, däck, bromsar |
| Cykelförsäkring tillkommer | **{CYKELFÖRSÄKRING_ÅR:,} kr/år** | Fristående (ofta 0 kr om hemförsäkring finns) |
| **Netto: Bil + cykelpendling** | **{kombikostnad_år:,.0f} kr/år** | Bilen kvar, men {minskad_rörlig:,.0f} kr billigare |
""".replace(",", " "))
    st.caption(
        "Källa: Konsumentverkets bilkostnadskalkyl. "
        "Bränsleförbrukning: 0,065 L/km (Konsumentverket snittbil). "
        "Bensinpris: ~19 SEK/L (Drivmedelsfakta.se 2024/2025). "
        "Cykelpendlingsavstånd: Newsworthy/Tyréns Hudiksvall-data."
    )

besparing_hushall = (BILKOSTNAD_ÅR - cykel_total_år) * nya_cyklister
besparing_kombi = (BILKOSTNAD_ÅR - kombikostnad_år) * nya_cyklister
st.info(
    f"Om **{nya_cyklister:,} boende** längs den nya sträckan cykelpendlar "
    f"men behåller bilen frigörs **{besparing_kombi / 1_000_000:.2f} MSEK per år** "
    f"i hushållens ekonomi.  \n"
    f"Kan de dessutom bli av med bilen helt: "
    f"**{besparing_hushall / 1_000_000:.1f} MSEK per år**.".replace(",", " ")
)

# ──────────────────────────────────────────────────────────────────────
# 8. SAMMANFATTNING & ARGUMENT
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("Sammanfattning - Fem skäl att investera nu")

if netto_årlig_vinst > 0:
    kostnad_rad = (
        f"Investeringen ({kommunens_kostnad:.1f} MSEK) hämtar hem sig på "
        f"ca {breakeven_år:.0f} år enbart via hälsovinster"
    )
else:
    kostnad_rad = f"Investeringen kostar {kommunens_kostnad:.1f} MSEK"

if visa_extern:
    finansrad = f"Kommunen betalar {kommunens_kostnad:.1f} av {investering_cykel:.0f} MSEK (resten extern finansiering)"
else:
    finansrad = f"Kommunen betalar {investering_cykel:.0f} MSEK - helt utan bidrag. Med extern finansiering kan det bli {investering_cykel * (1 - EXTERN_ANDEL_KLIMATKLIVET - EXTERN_ANDEL_REGION):.1f} MSEK"

st.markdown(f"""
| Argument | Siffra |
|----------|--------|
| **Det kostar mer att *inte* investera** | {kostnad_rad} |
| **Varje undviken olycka sparar miljoner** | En allvarlig skada kostar samhället {ASEK_ALLVARLIGT_SKADAD_MSEK} MSEK - separerad cykelväg räddar liv |
| **Klimatvinsten stärker finansieringen** | {co2_ton_per_år:.0f} ton CO₂/år mindre - grund för Klimatklivet-ansökan |
| **Det är en rättvisefråga** | Varje cyklist sparar {BILKOSTNAD_ÅR - CYKELKOSTNAD_ÅR:,} kr/år jämfört med bilberoende |
| **Seriös kalkyl utan önsketänkande** | {finansrad} |
""".replace(",", " "))

# ──────────────────────────────────────────────────────────────────────
# 9. TRANSPARENS - Medvetna avvägningar
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("Så har vi räknat - medvetna avvägningar")
st.markdown(
    "Alla kalkyler bygger på val. Nedan redovisar vi varje val, "
    "vilka alternativ som fanns, och åt vilket håll vi har lutat oss.  \n"
    "**Konservativ** = vi har medvetet valt den siffra som gör cykelvägens "
    "fördelar *mindre*. Ingen ska kunna säga att vi räknat med önsketänkande."
)

RIKTNING_IKON = {"konservativ": "🔵", "neutral": "⚪"}

for a in AVVÄGNINGAR:
    ikon = RIKTNING_IKON.get(a["riktning"], "⚪")
    with st.expander(f"{ikon} {a['värde']}"):
        st.markdown(f"**Rimligt spann:** {a['spann']}")
        st.markdown(f"**Vårt val:** {a['val']}")
        if a["källa_url"]:
            st.markdown(f"**Källa:** [{a['källa']}]({a['källa_url']})")
        else:
            st.markdown(f"**Källa:** {a['källa']}")
        if a["riktning"] == "konservativ":
            st.success("Vi har medvetet valt den försiktigare siffran.")

st.markdown(
    f"\n{RIKTNING_IKON['konservativ']} = Konservativt val (till cykelvägens nackdel)&emsp;"
    f"{RIKTNING_IKON['neutral']} = Neutralt medelvärde"
)

# ──────────────────────────────────────────────────────────────────────
# 10. KÄLLÖVERSIKT I SIDFOTEN
# ──────────────────────────────────────────────────────────────────────

st.markdown("---")
st.header("Källor och fördjupning")
st.markdown(
    f"{KVALITET_IKON['lokal']} **Lokal data** - siffror direkt från Hudiksvalls kommun eller kommunrapporter  \n"
    f"{KVALITET_IKON['schablon']} **Nationell schablon** - generella värden från Trafikverket, Konsumentverket eller andra kommuner"
)

for grupp in KALLOR.values():
    st.subheader(grupp["rubrik"])
    for k in grupp["kallor"]:
        badge = kvalitets_badge(k["kvalitet"])
        st.markdown(
            f"- **[{k['namn']}]({k['url']})** {badge}  \n"
            f"  {k['beskrivning']}  \n"
            f"  *Datapunkt:* {k['datapunkt']}"
        )

st.caption(
    "Schablonvärden baserade på Trafikverkets, Konsumentverkets och SCB:s generella data. "
    "Exakta siffror kan variera beroende på lokala förutsättningar. "
    "Alla grundsiffror och källor finns samlade i filen kalldata.py för enkel uppdatering."
)
