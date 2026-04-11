# Cykelinfrastruktur Dashboard - Hudiksvalls kommun

## Syfte

Lokalt Streamlit-dashboard som visar att investeringar i cykelvägar i Hudiksvall är ekonomiskt försvarbara. Byggt för att använda i politiska diskussioner med kostnadsmedvetna, skeptiska partikollegor (S). Grundkalkylen utgår från 100 % kommunal finansiering - ingen "önsketänkande-vinkel" med bidrag som inte är beviljade.

## Filer

- `app.py` - Streamlit-dashboard
- `kalldata.py` - Alla siffror, källor och medvetna avvägningar samlade på ett ställe (ändra här om nya budgetar beslutas)
- `requirements.txt` - streamlit, plotly, pandas

## Starta

```bash
pip install -r requirements.txt
python -m streamlit run app.py
```

Öppnas på http://localhost:8501

## Sektioner i dashboarden

1. **Investera eller göra ingenting?** - Kumulativ kostnadsjämförelse: kommunens investeringskostnad vs förlorade samhällsvinster av att inte bygga. Visar break-even-punkt (default ~10 år). Diagrammet sträcker sig alltid förbi break-even.
2. **Finansieringskalkyl** - Default: 100 % kommunalt. Extern finansiering (Klimatklivet, Region Gävleborg) är opt-in via checkbox.
3. **Hälsokalkyl** - Transparent beräkningskedja: 4,5 km enkelresa (Newsworthy/Tyréns Hudiksvall-data) x 2 x 200 dagar x 4,50 SEK/km (Trafikverket ASEK) = 8 100 kr/cyklist/år. Expanderbar "Så räknar vi"-tabell med klickbara källor per steg.
4. **Hudiksvall-gapet** - 1,6 m cykelväg/invånare vs snitt 2,0–3,0 m för små kommuner.
5. **Rättviseperspektivet** - Bilkostnad 55 000 kr/år vs cykel 3 000 kr/år. Klassfråga.
6. **Sammanfattning** - Tre argument i tabellform.
7. **Så har vi räknat** - 10 expanderbara avvägningar med spann, motivering och klickbar källa. 5 markerade som medvetet konservativa (🔵) till cykelvägens nackdel.
8. **Källor och fördjupning** - 11 källhänvisningar grupperade: Kostnadsdata, Hudiksvall-specifikt, Finansiering, Kompletterande.

## Sidopanel

Sliders för cykelvägslängd (1–15 km, default 2), plats (tätort/landsbygd), omställningsandel (5–25 %, default 10 %), tidshorisont (5–30 år, default 10). Expanderbara källsektioner. Datakvalitets-badges: 🟢 lokal data, 🟡 nationell schablon.

## Datamodell

**Cyklistmodell:** Antal nya cyklister = boende inom cykelavstånd (1 500/km tätort, 200/km landsbygd) x omställningsandel. Kopplat till sträckan, inte en lös procent av hela kommunens befolkning.

**Hälsovinst:** Beräknad steg för steg - 4,5 km enkelresa x 2 x 200 dagar = 1 800 km/år x 4,50 SEK/km (ASEK) = 8 100 kr/cyklist/år.

**Budgetvarning:** Visas automatiskt om investeringen överstiger årsbudgeten (25 MSEK avser hela vägnätet, inte enbart cykel).

## Ändra siffror

Alla grundvärden finns i `kalldata.py` med kommentarer. Ändra där om nya budgetar, rapporter eller policyförändringar publiceras.

## Retorisk linje

"Vi har räknat konservativt, med kommunens egna pengar, utan bidragsönsketänkande. Ändå lönsamt. Varje år vi väntar kostar mer."
