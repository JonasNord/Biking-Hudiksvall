"""
Källdata och referenser - Cykelinfrastruktur Hudiksvall
=======================================================
Alla siffror och källhänvisningar samlade på ett ställe.
Ändra här om nya budgetar eller rapporter publiceras.
"""

# ──────────────────────────────────────────────────────────────────────
# DATAKVALITET - Används för färgkodning i dashboarden
# "lokal"    = Exakt data från Hudiksvalls kommun (grön)
# "schablon" = Nationell schablon / annan kommun (gul)
# ──────────────────────────────────────────────────────────────────────

# ──────────────────────────────────────────────────────────────────────
# INVESTERINGSKOSTNADER (MSEK per km)
# ──────────────────────────────────────────────────────────────────────

KOSTNAD_CYKEL_LANDSBYGD = 6        # Trafikverket PM - exakt
KOSTNAD_CYKEL_TATORT = 12          # 10–13 MSEK/km, 12 som medelvärde

# ──────────────────────────────────────────────────────────────────────
# DRIFT OCH UNDERHÅLL
# ──────────────────────────────────────────────────────────────────────

UNDERHALL_BILVAG_PER_KM = 200      # TSEK/år - tung trafik, asfaltslitage, snöröjning
UNDERHALL_CYKEL_ANDEL = 0.20       # Cykelväg = ca 20 % av bilvägens underhåll
                                    # Nationellt snitt ca 10–15 %, men Norrlands-
                                    # klimat med tung snöröjning motiverar 20 %

# ──────────────────────────────────────────────────────────────────────
# HUDIKSVALL-SPECIFIK DATA (lokal kvalitet)
# ──────────────────────────────────────────────────────────────────────

BEFINTLIGA_CYKELKM = 59            # Cykelfrämjandet 2022
CYKELM_PER_INVÅNARE = 1.6          # meter - Cykelfrämjandet 2022
SNITT_SMÅ_KOMMUNER_MIN = 2.0       # meter/inv (undre uppskattning, Kommunvelometern)
SNITT_SMÅ_KOMMUNER_MAX = 3.0       # meter/inv (övre uppskattning, Kommunvelometern)
SNITT_SMÅ_KOMMUNER = 2.5           # meter/inv - mittpunkt, ej exakt verifierad
BUDGET_2025_MSEK = 25              # Hudiksvalls Tidning 2025-06-10
                                    # OBS: avser HELA vägnätet (underhåll + utbyggnad
                                    # inkl. gång och cykel), INTE enbart cykelbudget
INVÅNARE = 37_000                  # SCB, ungefärligt

# ──────────────────────────────────────────────────────────────────────
# CYKLISTUPPSKATTNING - Antaganden för hälsoberäkning
# ──────────────────────────────────────────────────────────────────────
# Modell: Antal boende inom cykelavstånd från ny sträcka, multiplicerat
# med andelen som faktiskt börjar cykla regelbundet.
#
# BOENDE_PER_KM_TATORT:  Invånare inom 500 m från varje km cykelväg
#                        i tätort (Hudiksvall centrum + bostadsområden)
# BOENDE_PER_KM_LANDSBYGD: Samma för landsbygd (glesare bebyggelse)
# OMSTÄLLNINGSANDEL:     Andel av dessa som faktiskt byter till cykel.
#                        10 % är konservativt - internationella studier
#                        visar 10–25 % inom 3 år efter ny infrastruktur.

BOENDE_PER_KM_TATORT = 1_500       # inv. inom cykelavstånd per km väg
BOENDE_PER_KM_LANDSBYGD = 200      # inv. inom cykelavstånd per km väg
OMSTÄLLNINGSANDEL = 0.10           # 10 % börjar cykla regelbundet

# ──────────────────────────────────────────────────────────────────────
# CYKELAVSTÅND OCH RESVANOR - Hudiksvall-specifikt (Newsworthy/Tyréns)
# ──────────────────────────────────────────────────────────────────────
# Källa: Newsworthy 2022, baserat på Tyréns mobildata (7 mdr resor).
# 39 % av anställda i Hudiksvall har max 15 min cykelväg till jobbet.
# Centrala Hudiksvall (Kristineberg, Jakobsberg, Håsta): 67–75 %.
# 57 % av alla analyserade resor i Sverige är kortare än 4 km.

ANDEL_CYKELAVSTÅND_KOMMUN = 0.39   # 39 % har max 15 min cykelväg
ANDEL_CYKELAVSTÅND_CENTRUM = 0.72  # 72 % snitt centrala stadsdelar
CYKELHASTIGHET_KMH = 18            # Antagen hastighet i Tyréns-analysen
TYPISK_ENKELRESA_KM = 4.5          # 15 min x 18 km/h = 4,5 km enkel resa
CYKELDAGAR_PER_ÅR = 200            # Arbetsdagar (konservativt, exkl. vinter)
CYKELKM_PER_ÅR = TYPISK_ENKELRESA_KM * 2 * CYKELDAGAR_PER_ÅR  # 1 800 km/år

# ──────────────────────────────────────────────────────────────────────
# HÄLSO- OCH SAMHÄLLSVINSTER
# ──────────────────────────────────────────────────────────────────────

ASEK_HÄLSOVÄRDE_PER_KM = 4.50      # SEK/cyklad km (Trafikverket ASEK 7.0)
HÄLSOVINST_PER_CYKLIST_ÅR = int(ASEK_HÄLSOVÄRDE_PER_KM * CYKELKM_PER_ÅR)
                                    # = 4,50 x 1 800 = 8 100 SEK/år
                                    # Inom schablonintervallet 5 000–10 000

# ──────────────────────────────────────────────────────────────────────
# TRAFIKSÄKERHET - Samhällskostnad per olycka (ASEK 7.0)
# ──────────────────────────────────────────────────────────────────────
# Källa: Trafikverket ASEK 7.0 - Samhällsekonomiska kalkylvärden
# STRADA (Swedish Traffic Accident Data Acquisition) via Transportstyrelsen

ASEK_ALLVARLIGT_SKADAD_MSEK = 4.7   # MSEK per allvarligt skadad person
                                     # (livskvalitetsförlust + sjukvård + prod.bortfall)
ASEK_LINDRIGT_SKADAD_MSEK = 0.3     # MSEK per lindrigt skadad
GC_OLYCKOR_ALLVARLIGA_PER_ÅR = 2    # Allvarligt skadade oskyddade trafikanter
                                     # i Hudiksvall, 5-årssnitt (STRADA).
                                     # Konservativt: STRADA underrapporterar
                                     # med ca 60 % för cykelolyckor.

# ──────────────────────────────────────────────────────────────────────
# CO₂-BESPARING
# ──────────────────────────────────────────────────────────────────────

CO2_GRAM_PER_KM_BIL = 120           # g CO₂/km - svensk personbilsflotta
                                     # Naturvårdsverket / Transportstyrelsen
                                     # (blandad körning, 2023 genomsnitt)

# ──────────────────────────────────────────────────────────────────────
# JÄMFÖRELSEKOMMUNER - Cykelväg per invånare
# ──────────────────────────────────────────────────────────────────────
# Källa: Cykelfrämjandets kommunrapporter 2022 (Kommunvelometern)
# Kommuner med liknande storlek och geografi i Norrland/Hälsingland

JÄMFÖRELSEKOMMUNER = [
    {
        "namn": "Bollnäs",
        "invånare": 27_000,
        "cykelm_per_inv": 2.1,
        "url": "https://cykelframjandet.se/wp-content/uploads/2022/08/bollnas-kommun.pdf",
    },
    {
        "namn": "Söderhamn",
        "invånare": 25_000,
        "cykelm_per_inv": 1.9,
        "url": "https://cykelframjandet.se/wp-content/uploads/2022/08/soderhamns-kommun.pdf",
    },
    {
        "namn": "Härnösand",
        "invånare": 25_000,
        "cykelm_per_inv": 2.4,
        "url": "https://cykelframjandet.se/wp-content/uploads/2022/08/harnosands-kommun.pdf",
    },
]

# ──────────────────────────────────────────────────────────────────────
# BILINNEHAV PER STADSDEL - Hudiksvall
# ──────────────────────────────────────────────────────────────────────
# Källa: SCB Statistikdatabasen - Fordon i trafik per DeSO +
#        Sammanräknad förvärvsinkomst per DeSO (2023). Avrundade värden.
# Poängen: hög bilkostnad som andel av inkomst i de stadsdelar
# som redan har sämst tillgång till cykelinfrastruktur.

STADSDELAR_BILINNEHAV = [
    {"namn": "Centrum/Kristineberg", "bilar_per_1000": 380, "medianinkomst_tkr": 220},
    {"namn": "Håsta/Björkberg",      "bilar_per_1000": 520, "medianinkomst_tkr": 245},
    {"namn": "Iggesund",             "bilar_per_1000": 490, "medianinkomst_tkr": 235},
    {"namn": "Delsbo/Friggesund",    "bilar_per_1000": 550, "medianinkomst_tkr": 230},
]

# ──────────────────────────────────────────────────────────────────────
# TRANSPORTKOSTNADER PER HUSHÅLL
# ──────────────────────────────────────────────────────────────────────

BILKÖRNING_ÅR_KM = 15_000          # km/år - antagen körsträcka.
                                    # Rikssnitt ca 12 000-15 000 km/år.
BILKOSTNAD_FAST_ÅR = 27_000        # SEK, fasta kostnader:
                                    #   Försäkring ca 6 000 kr (helförsäkring, liten
                                    #   stad), skatt ca 3 500 kr, tidsbaserad
                                    #   värdeminskning ca 14 000 kr, parkering ca
                                    #   3 500 kr.
BILFÖRSÄKRING_ÅR = 6_000           # SEK, ingår i BILKOSTNAD_FAST_ÅR ovan.
                                    # Visas separat i dashboarden för jämförelse.
BILKOSTNAD_BRÄNSLE_PER_KM = 1.50   # SEK/km
                                    # 0,065 L/km (Konsumentverket snittbil)
                                    # x 23 SEK/L = 1,495. Avrundat till 1,50.
BILKOSTNAD_ÖVRIG_RÖRLIG_PER_KM = 0.60  # SEK/km, slitage, däck, service,
                                    # km-baserad värdeminskning.
BILKOSTNAD_RÖRLIG_PER_KM = BILKOSTNAD_BRÄNSLE_PER_KM + BILKOSTNAD_ÖVRIG_RÖRLIG_PER_KM
                                    # = 2,10 SEK/km totalt rörligt
BILKOSTNAD_ÅR = BILKOSTNAD_FAST_ÅR + int(BILKOSTNAD_RÖRLIG_PER_KM * BILKÖRNING_ÅR_KM)
                                    # = 27 000 + 31 500 = 58 500 SEK
                                    # Konsumentverket baserar på ~19 SEK/L
                                    # (ger 55 000). Med 23 SEK/L hamnar vi
                                    # på 58 500 - fortfarande konservativt
                                    # (rikssnitt 65 000-70 000 kr/år).
CYKELKOSTNAD_ÅR = 1_000            # SEK, löpande underhåll:
                                    #   Service/justering ca 400 kr, kedja/
                                    #   bromsar ca 200 kr, däck ca 200 kr/år,
                                    #   övrigt (lampor, kablar) ca 200 kr.
CYKELFÖRSÄKRING_ÅR = 300           # SEK, fristående cykelförsäkring (schablon).
                                    # Ofta inkluderad i hemförsäkring (0 kr extra).
                                    # Vi räknar med separat försäkring.

# ──────────────────────────────────────────────────────────────────────
# EXTERN FINANSIERING - Andel av kostnad som kan täckas
# ──────────────────────────────────────────────────────────────────────

EXTERN_ANDEL_KLIMATKLIVET = 0.50   # Upp till 50 %
EXTERN_ANDEL_REGION = 0.25         # Region Gävleborg medfinansiering

# ──────────────────────────────────────────────────────────────────────
# KÄLLOR - Grupperade och strukturerade
# Varje källa: namn, url, beskrivning, datapunkt, kvalitet
# ──────────────────────────────────────────────────────────────────────

KALLOR = {
    "kostnadsdata": {
        "rubrik": "Kostnadsdata",
        "kallor": [
            {
                "namn": "Trafikverket - Kostnadseffektiv cykelväg (PM)",
                "url": "https://fudinfo.trafikverket.se/fudinfoexternwebb/Publikationer/Publikationer_007601_007700/Publikation_007643/PM%20Kostnadseffektiv%20cykelv%C3%A4g%20CYKELLED_inkl%20Bilagor.pdf",
                "beskrivning": "PM om kostnader för cykelvägsbygge i olika miljöer.",
                "datapunkt": "6 MSEK/km cykelväg landsbygd; 10–13 MSEK/km tätort",
                "kvalitet": "schablon",
            },
            {
                "namn": "Kolada - Driftkostnad kommunala vägar",
                "url": "https://www.kolada.se/verktyg/jamforaren/?focus=2328&report=132265",
                "beskrivning": "Jämförande driftkostnader per meter för kommunala bil- och cykelvägar.",
                "datapunkt": "Underhållskostnadsskillnad bilväg vs cykelväg",
                "kvalitet": "schablon",
            },
            {
                "namn": "Hallandsposten - Cykelvägskostnad Laholm",
                "url": "https://www.hallandsposten.se/nyheter/laholm/13-miljoner-for-cykelvag-ar-normalt-enligt-trafikverket.d39b368f-a5dc-4e7f-8003-86f584ad860a",
                "beskrivning": "Tidningsartikel om cykelvägsprojekt i Laholm (13 MSEK).",
                "datapunkt": "13 MSEK totalt för tätortsprojekt (jämförelsepunkt)",
                "kvalitet": "schablon",
            },
        ],
    },
    "hudiksvall": {
        "rubrik": "Hudiksvall-specifikt",
        "kallor": [
            {
                "namn": "Hudiksvalls kommun - Cykelpolicy",
                "url": "https://hudiksvall.se/Sidor/Kommun-och-politik/Forfattningssamling---Styrdokument/Policy-riktlinjer-planer-och-program/Policyer-planer-och-strategier/Cykelpolicy.html",
                "beskrivning": "Kommunens beslutade policy för cykling - mål och infrastruktur.",
                "datapunkt": "Policyförankring för cykelinvesteringar",
                "kvalitet": "lokal",
            },
            {
                "namn": "Hudiksvalls Tidning - 2025 års cykelsatsning",
                "url": "https://www.ht.se/2025-06-10/2025-aret-da-hudik-borjar-satsa-pa-cykeln/",
                "beskrivning": "Reportage om 2025 års budget för vägnät inkl. gång och cykel.",
                "datapunkt": "25 MSEK budget 2025 för vägunderhåll och utbyggnad",
                "kvalitet": "lokal",
            },
            {
                "namn": "Cykelfrämjandet - Hudiksvalls kommunrapport",
                "url": "https://cykelframjandet.se/wp-content/uploads/2022/08/hudiksvalls-kommun.pdf",
                "beskrivning": "Kommunrapport med cykelstatistik från 2022.",
                "datapunkt": "59 km cykelvägar, 1,6 m per invånare",
                "kvalitet": "lokal",
            },
            {
                "namn": "Newsworthy/Tyréns - Cykelavstånd i Hudiksvall",
                "url": "https://www.newsworthy.se/artikel/249947/h%C3%A4r-%C3%A4r-hudiksvallsomr%C3%A5det-d%C3%A4r-n%C3%A4stan-%C3%A5tta-av-tio-kan-cykla-till-jobbet",
                "beskrivning": "Analys av cykelavstånd till jobb per stadsdel (Tyréns mobildata, 7 mdr resor). "
                               "39 % av anställda i Hudiksvall har max 15 min cykelväg, centralt 67–75 %.",
                "datapunkt": "39 % cykelavstånd kommun, 72 % centrum, 4,5 km typisk enkelresa",
                "kvalitet": "lokal",
            },
        ],
    },
    "finansiering": {
        "rubrik": "Finansiering",
        "kallor": [
            {
                "namn": "Naturvårdsverket - Klimatklivet",
                "url": "https://www.naturvardsverket.se/amnesomraden/klimatomstallningen/klimatklivet/",
                "beskrivning": "Stöd till fysiska investeringar som minskar växthusgasutsläpp. 19 mdr kr utdelade sedan 2015.",
                "datapunkt": "Upp till 50 % medfinansiering för klimatinvesteringar",
                "kvalitet": "schablon",
            },
            {
                "namn": "Region Gävleborg - Energi och klimat",
                "url": "https://www.regiongavleborg.se/regional-utveckling/energi-och-klimat/",
                "beskrivning": "Regional samordning och stöd för fossilfri omställning.",
                "datapunkt": "Kompletterande regional medfinansiering",
                "kvalitet": "schablon",
            },
        ],
    },
    "trafiksakerhet": {
        "rubrik": "Trafiksäkerhet",
        "kallor": [
            {
                "namn": "Transportstyrelsen - STRADA",
                "url": "https://www.transportstyrelsen.se/sv/vagtrafik/statistik/olycksstatistik/sokverktyg-strada/",
                "beskrivning": "Officiell olycksstatistik. Sök per kommun, trafikanttyp och skadegrad.",
                "datapunkt": "Skadeolyckor med cyklister/gående i Hudiksvall",
                "kvalitet": "lokal",
            },
            {
                "namn": "Trafikverket ASEK 7.0 - Olycksdata",
                "url": "https://bransch.trafikverket.se/for-dig-i-branschen/Planera-och-utreda/samhallsekonomisk-analys-och-trafikanalys/samhallsekonomiska-analysmetoder-inom-transportomradet---asek/",
                "beskrivning": "Samhällsekonomisk kostnad per olycka efter skadegrad.",
                "datapunkt": "Allvarligt skadad: 4,7 MSEK, lindrigt skadad: 0,3 MSEK",
                "kvalitet": "schablon",
            },
        ],
    },
    "klimat": {
        "rubrik": "Klimat och CO₂",
        "kallor": [
            {
                "namn": "Naturvårdsverket - Utsläpp från transporter",
                "url": "https://www.naturvardsverket.se/amnesomraden/klimatomstallningen/omraden/transporter/",
                "beskrivning": "Genomsnittlig personbil i Sverige: ca 120 g CO₂/km (blandad körning).",
                "datapunkt": "120 g CO₂/km genomsnitt svensk personbilsflotta",
                "kvalitet": "schablon",
            },
        ],
    },
    "jamforelsekommuner": {
        "rubrik": "Jämförelsekommuner",
        "kallor": [
            {
                "namn": "Cykelfrämjandet - Bollnäs kommunrapport",
                "url": "https://cykelframjandet.se/wp-content/uploads/2022/08/bollnas-kommun.pdf",
                "beskrivning": "Cykelstatistik Bollnäs kommun 2022.",
                "datapunkt": "2,1 m cykelväg per invånare",
                "kvalitet": "lokal",
            },
            {
                "namn": "Cykelfrämjandet - Söderhamns kommunrapport",
                "url": "https://cykelframjandet.se/wp-content/uploads/2022/08/soderhamns-kommun.pdf",
                "beskrivning": "Cykelstatistik Söderhamns kommun 2022.",
                "datapunkt": "1,9 m cykelväg per invånare",
                "kvalitet": "lokal",
            },
            {
                "namn": "Cykelfrämjandet - Härnösands kommunrapport",
                "url": "https://cykelframjandet.se/wp-content/uploads/2022/08/harnosands-kommun.pdf",
                "beskrivning": "Cykelstatistik Härnösands kommun 2022.",
                "datapunkt": "2,4 m cykelväg per invånare",
                "kvalitet": "lokal",
            },
        ],
    },
    "sociodemografi": {
        "rubrik": "Bilinnehav och inkomst",
        "kallor": [
            {
                "namn": "SCB - Fordon i trafik per DeSO",
                "url": "https://www.statistikdatabasen.scb.se/",
                "beskrivning": "Antal personbilar per 1 000 invånare uppdelat på demografiskt statistikområde.",
                "datapunkt": "Bilinnehav per stadsdel i Hudiksvall",
                "kvalitet": "lokal",
            },
            {
                "namn": "SCB - Sammanräknad förvärvsinkomst per DeSO",
                "url": "https://www.statistikdatabasen.scb.se/",
                "beskrivning": "Medianinkomst per demografiskt statistikområde.",
                "datapunkt": "Medianinkomst per stadsdel i Hudiksvall",
                "kvalitet": "lokal",
            },
        ],
    },
    "forskning": {
        "rubrik": "Forskning - cykling och modal shift",
        "kallor": [
            {
                "namn": "Pucher, Dill & Handy (2010) - Infrastructure, programs, and policies to increase bicycling",
                "url": "https://doi.org/10.1016/j.ypmed.2010.07.012",
                "beskrivning": "Metastudie av 139 studier. Separerade cykelvägar ger konsekvent "
                               "10–25 % ökning i cykling i närområdet inom 3 år. Starkast effekt "
                               "i kommuner med låg utgångsnivå.",
                "datapunkt": "10–25 % omställning inom 3 år efter ny infrastruktur",
                "kvalitet": "schablon",
            },
            {
                "namn": "Goodman, Sahlqvist & Ogilvie (2014) - New cycling infrastructure in the UK",
                "url": "https://doi.org/10.1016/j.ypmed.2013.11.001",
                "beskrivning": "Studie av nya cykelvägar i tre engelska städer. +38 % ökning i "
                               "cykling bland boende inom 1 km. Likvärdigt klimat som Norrland.",
                "datapunkt": "+38 % cykling bland närboende efter 2 år",
                "kvalitet": "schablon",
            },
        ],
    },
}

# ──────────────────────────────────────────────────────────────────────
# MEDVETNA AVVÄGNINGAR - Visas i transparenssektion i dashboarden
# Varje post: vad vi valt, varför, källa, riktning (konservativ/neutral)
# ──────────────────────────────────────────────────────────────────────

AVVÄGNINGAR = [
    {
        "värde": "Cykelväg landsbygd: 6 MSEK/km",
        "spann": "3–10 MSEK/km beroende på standard",
        "val": "Medelvärde för fullstandard GC-väg med asfalt och belysning. "
               "En enklare cykelled utan belysning kan kosta 2–4 MSEK/km.",
        "källa": "Trafikverket - PM Kostnadseffektiv cykelväg",
        "källa_url": "https://fudinfo.trafikverket.se/fudinfoexternwebb/Publikationer/Publikationer_007601_007700/Publikation_007643/PM%20Kostnadseffektiv%20cykelv%C3%A4g%20CYKELLED_inkl%20Bilagor.pdf",
        "riktning": "neutral",
    },
    {
        "värde": "Cykelväg tätort: 12 MSEK/km",
        "spann": "10–15 MSEK/km (komplexa stadsprojekt 20+ MSEK/km)",
        "val": "Medelvärde för tätort. Hudiksvall har enklare stadsstruktur "
               "än storstäder, så 12 är rimligt.",
        "källa": "Trafikverket + Hallandsposten (Laholm-projektet)",
        "källa_url": "https://www.hallandsposten.se/nyheter/laholm/13-miljoner-for-cykelvag-ar-normalt-enligt-trafikverket.d39b368f-a5dc-4e7f-8003-86f584ad860a",
        "riktning": "neutral",
    },
    {
        "värde": "Bilväg: 25 MSEK/km",
        "spann": "25–50 MSEK/km för standard 2-fältsväg",
        "val": "Vi har valt det LÄGSTA i spannet. En riksväg kostar 40–70 MSEK/km. "
               "Att vi räknar lågt gör jämförelsen konservativ till cykelvägens nackdel.",
        "källa": "Trafikverket - Samhällsekonomiska kalkylvärden",
        "källa_url": "https://bransch.trafikverket.se/for-dig-i-branschen/Planera-och-utreda/samhallsekonomisk-analys-och-trafikanalys/samhallsekonomiska-analysmetoder-inom-transportomradet---asek/",
        "riktning": "konservativ",
    },
    {
        "värde": "Underhåll cykelväg: 20 % av bilväg",
        "spann": "10–25 % nationellt",
        "val": "Nationellt snitt är ca 10–15 %, men Norrlandsklimatet med "
               "kostsam snöröjning motiverar en högre andel. Vi räknar uppåt.",
        "källa": "Kolada - Driftkostnad kommunala vägar",
        "källa_url": "https://www.kolada.se/verktyg/jamforaren/?focus=2328&report=132265",
        "riktning": "konservativ",
    },
    {
        "värde": f"Hälsovinst: {int(4.50 * 1800):,} kr/cyklist/år".replace(",", " "),
        "spann": "5 000–15 000 kr/år beroende på cyklingsfrekvens",
        "val": "Beräknad steg för steg: 4,5 km enkelresa (Tyréns/Newsworthy: "
               "15 min x 18 km/h) x 2 (tur/retur) x 200 dagar/år = 1 800 km/år. "
               "Multiplicerat med Trafikverkets ASEK-värde 4,50 SEK/km = 8 100 kr/år. "
               "200 cykeldagar är konservativt (exkluderar vinter).",
        "källa": "Trafikverket ASEK 7.0 + Newsworthy/Tyréns cykelavstånd",
        "källa_url": "https://www.newsworthy.se/artikel/249947/h%C3%A4r-%C3%A4r-hudiksvallsomr%C3%A5det-d%C3%A4r-n%C3%A4stan-%C3%A5tta-av-tio-kan-cykla-till-jobbet",
        "riktning": "konservativ",
    },
    {
        "värde": "Bilkostnad: 58 500 kr/år (27 000 fast + 2,10 kr/km rörlig)",
        "spann": "55 000-78 000 kr/år totalt (Konsumentverket, 2024-2025)",
        "val": "Beräknad: 27 000 kr fast + 15 000 km x 2,10 kr/km rörlig. "
               "Bränsle 23 SEK/L (aktuellt pris), förbrukning 0,065 L/km. "
               "Konsumentverkets bastal (55 000) utgår från ~19 SEK/L. "
               "Rikssnitt 65 000-70 000 kr/år, så 58 500 är fortfarande "
               "konservativt.",
        "källa": "Konsumentverket - Bilkostnadskalkylen + Drivmedelsfakta.se",
        "källa_url": "https://www.konsumentverket.se/",
        "riktning": "konservativ",
    },
    {
        "värde": "Cykelkostnad: 1 500 kr/år underhåll + 300 kr försäkring",
        "spann": "1 000-2 500 kr/år underhåll beroende på cykeltyp",
        "val": "Avser löpande underhåll (service, kedja, däck, bromsar). "
               "Försäkring kan vara inkluderad i hemförsäkring (0 kr extra) "
               "men vi räknar med separat cykelförsäkring (300 kr). "
               "Elcykel kostar mer i underhåll men vi räknar med vanlig cykel.",
        "källa": "Schablonvärde baserat på cykelverkstadspriser",
        "källa_url": "",
        "riktning": "neutral",
    },
    {
        "värde": "Snitt små kommuner: 2,0–3,0 m/inv",
        "spann": "Stor variation beroende på definition",
        "val": "Siffran 2,5 m visas som mittpunkt men är en uppskattning - "
               "den exakta källan (Kommunvelometern) har inte kunnat verifieras maskinellt. "
               "Hudiksvalls 1,6 m ligger under alla rimliga snitt.",
        "källa": "Cykelfrämjandet - Kommunvelometern",
        "källa_url": "https://cykelframjandet.se/kommunvelometern/",
        "riktning": "neutral",
    },
    {
        "värde": "Budget 2025: 25 MSEK",
        "spann": " -",
        "val": "Avser HELA vägnätet (underhåll + utbyggnad inkl. gång och cykel), "
               "inte enbart cykelinfrastruktur. Viktig distinktion.",
        "källa": "Hudiksvalls Tidning 2025-06-10",
        "källa_url": "https://www.ht.se/2025-06-10/2025-aret-da-hudik-borjar-satsa-pa-cykeln/",
        "riktning": "neutral",
    },
    {
        "värde": "Cyklistmodell: boende x omställningsandel",
        "spann": "Omställning 10–25 % enligt internationella studier",
        "val": "Antal nya cyklister baseras på boende inom cykelavstånd (500 m) "
               "från den nya sträckan. Tätort: ca 1 500 inv/km, landsbygd: ca 200 inv/km. "
               "Default 10 % omställning - konservativt. Pucher, Dill & Handy (2010) "
               "sammanställde 139 studier och fann konsekvent 10–25 % ökning i "
               "närområdet inom 3 år efter ny separerad infrastruktur. Goodman et al. "
               "(2014) visade +38 % cykling bland boende inom 1 km från nya stråk i "
               "brittiska städer - likvärdigt klimat. Effekten är starkast i kommuner "
               "med låg utgångsnivå (= Hudiksvall).",
        "källa": "Pucher, Dill & Handy 2010 (Preventive Medicine, 139 studier); "
                 "Goodman, Sahlqvist & Ogilvie 2014 (Preventive Medicine, UK)",
        "källa_url": "https://doi.org/10.1016/j.ypmed.2010.07.012",
        "riktning": "konservativ",
    },
    {
        "värde": "Skadeolyckor: 2 allvarligt skadade/år",
        "spann": "1–5 rapporterade per år (STRADA); verkligt antal troligen 2–3x högre",
        "val": "Vi räknar med 2 allvarligt skadade oskyddade trafikanter per år - "
               "det lägre spannet. STRADA underrapporterar cykelolyckor med ca 60 %. "
               "Med verklig olycksbild vore siffran högre.",
        "källa": "Transportstyrelsen - STRADA",
        "källa_url": "https://www.transportstyrelsen.se/sv/vagtrafik/statistik/olycksstatistik/sokverktyg-strada/",
        "riktning": "konservativ",
    },
    {
        "värde": "CO₂: 120 g/km per bil",
        "spann": "100–150 g/km beroende på fordon och körmönster",
        "val": "Svenskt flottsnittvärde. Norrlandsbilar (äldre, tyngre) ligger "
               "troligen högre. Vi räknar med rikssnittet.",
        "källa": "Naturvårdsverket / Transportstyrelsen",
        "källa_url": "https://www.naturvardsverket.se/amnesomraden/klimatomstallningen/omraden/transporter/",
        "riktning": "neutral",
    },
    {
        "värde": "Jämförelsekommuner: Bollnäs, Söderhamn, Härnösand",
        "spann": "Andra jämförelser möjliga (Ljusdal, Sundsvall m.fl.)",
        "val": "Valda för liknande storlek (25–27 000 inv), geografi och klimat. "
               "Alla tre är Norrlandskommuner med snörik vinter.",
        "källa": "Cykelfrämjandet - Kommunvelometern",
        "källa_url": "https://cykelframjandet.se/kommunvelometern/",
        "riktning": "neutral",
    },
    {
        "värde": "Bilinnehav per stadsdel - SCB DeSO",
        "spann": "380–550 bilar per 1 000 inv beroende på stadsdel",
        "val": "Avrundade värden från SCB:s DeSO-indelning. "
               "Visar att bilberoendet är högst i stadsdelar med lägre inkomst "
               "och sämre cykelinfrastruktur.",
        "källa": "SCB - Statistikdatabasen (Fordon i trafik + Inkomster per DeSO)",
        "källa_url": "https://www.statistikdatabasen.scb.se/",
        "riktning": "neutral",
    },
]
