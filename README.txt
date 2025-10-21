🧱 Projektiaikataulu-komponentin tekninen kuvaus
1. Yleiskuva

Tiedosto: frontend/src/Aikataulu.jsx
Teknologia: React (Vite build-järjestelmä, JavaScript ES6)
Komponentti: Aikataulu
Käyttötarkoitus:
Selainpohjainen käyttöliittymä rakennusprojektin toimitus- ja projektiaikataulun esittämiseen.

Komponentti laskee ja visualisoi viikkokohtaiset tapahtumat dynaamisesti käyttäjän antaman sopimuspäivän perusteella.

2. Tietovirta ja sovelluslogiikka
2.1 Käyttäjän syöte

Käyttäjä syöttää sopimuspäivän (sopimusPvm) päivämääräkenttään.
Painike “Näytä aikataulu” lähettää POST-pyynnön backendille.

const res = await fetch("http://127.0.0.1:5000/api/aikataulu", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ sopimus_pvm: sopimusPvm }),
});

2.2 Vastauksen käsittely

Backend palauttaa aikataulun listamuotoisena JSON-datana:

[
  { "pvm": "2026-01-12", "kalenteri_viikko": 3, "kuukausi": "tammi", "vaihe": "Luonnoskuvien tekeminen", "jakso": "Rakennuslupakuvien suunnittelu" },
  ...
]


Tämä data tallennetaan aikataulu-tilamuuttujaan ja käsitellään edelleen funktiossa laskeViikot.

3. Laskentalogiikka
3.1 Jakson ja projektiviikkojen numerointi

Funktio laskeViikot(data) lisää kaksi laskennallista kenttää:

jakson_viikko – kertoo, monesko viikko on menossa nykyisessä rakennusvaiheessa

projektiviikko – kertoo, monesko viikko on menossa koko projektissa

let laskuri = 0;
let edellinenJakso = "";
let projektiviikko = 0;

if (rivi.jakso !== edellinenJakso) laskuri = 1;
else laskuri += 1;
projektiviikko += 1;

3.2 Merkittävien vaiheiden uudelleennimeäminen

Projektin tietyt avainviikot korvataan selkeämmillä otsikoilla, jotka näkyvät korostettuna taulukossa.

if (projektiviikko === 6) vaihe = "Lupakuvien tekeminen ja lupakuvat valmiit";
else if (projektiviikko === 14) vaihe = "Rakennuslupa myönnetty";
else if (projektiviikko === 18) vaihe = "Rakennuslupa lainvoimainen";
else if (projektiviikko === 26) vaihe = "Talotoimitus";
else if (projektiviikko === 48) vaihe = "Lattiamateriaalin asennus, listoitus";
else if (projektiviikko === 51) vaihe = "Luovutus 1 krs. talot";
else if (projektiviikko === 56) vaihe = "Luovutus 2 ja 1,5 krs. talot";
else if (projektiviikko === 60) vaihe = "Luovutus paritalot";


Näitä vaiheita käytetään myöhemmin visuaaliseen korostukseen.

4. Käyttöliittymä ja visuaaliset komponentit
4.1 Rakenne

Logo (public/sievitalo_logo.png)

Otsikko: “Projektiaikataulu”

Päivämäärän valinta ja painike

Korttimainen taulukko aikataululle

Koko komponentti on keskitetty ja skaalautuva:

<div style={{
  padding: "20px",
  textAlign: "center",
  backgroundColor: "#f8f9fa",
  minHeight: "100vh",
}}>

4.2 Korttimainen taulukko

Kortti toteutetaan erillisellä <div>-säiliöllä, jossa on varjo ja pyöristetyt kulmat:

<div style={{
  width: "70%",
  margin: "30px auto",
  backgroundColor: "#fff",
  borderRadius: "12px",
  boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
  padding: "25px",
}}>


Tämä luo paperimaisen, keskitetyn “kortin” projektiaikataululle.

4.3 Taulukon asettelu

Taulukko on rakennettu tableLayout: "fixed" -asetuksella, joka varmistaa vakioidut sarakeleveydet:

<table style={{
  width: "100%",
  tableLayout: "fixed",
  borderCollapse: "collapse",
  fontSize: "15px",
}}>


Sarakkeiden leveydet määritellään otsikoissa (<th style={{ width: "10%" }}>).

4.4 Värikoodaus
Kuukausittainen väritys

Taustaväri määräytyy kuukauden mukaan (kuukaudenVari()):

Tammi → #e0f7fa  
Helmi → #f1f8e9  
Maalis → #fff3e0  
… jne.

Rakennusjaksojen väritys

Eri työvaiheet erotetaan selkeästi:

"Suunnittelun lähtötietojen hankkinen" → sininen  
"Rakennuslupakuvien suunnittelu" → keltainen  
"Rakennusluvan hakemus..." → vaalea oranssi  
"Rakentaminen" → vihreä

Merkittävien vaiheiden korostus

Merkittävät tapahtumat (esim. “Rakennuslupa myönnetty”) korostetaan paksulla reunaviivalla ja lihavoinnilla.

5. Tasaus ja typografia
Sarake	Tasaus	Perustelu
Päivämäärä	vasen	päivämäärätasainen esitys
Viikko (kalenteri)	vasen	selkeä luettavuus
Kuukausi	vasen	kuukauden nimi samaan linjaan
Jakso	vasen, lihavoitu	jakson nimi korostettuna
Vaihe	vasen	kuvaileva teksti
Jakson viikkomäärä	keskitetty	numeerinen tieto
Projektin viikko	keskitetty	numeerinen tieto
6. Ylläpidettävyys ja jatkokehitys

Värit ja sarakeleveyssuhteet ovat helposti muokattavissa suoraan komponentin style-määrityksissä.

Komponentti on eristetty, joten se voidaan upottaa mihin tahansa React-näkymään ilman riippuvuuksia.

Tulostus- tai PDF-vienti on helppo lisätä esimerkiksi kirjastolla react-to-print
.

7. Laajennusideoita
Toiminto	Kuvaus
Tulostettava PDF-näkymä	Tyylitelty versio ilman taustavärejä tulostusta varten
Hakutoiminto	Mahdollisuus suodattaa aikataulua jakson tai kuukauden mukaan
Interaktiiviset värit	Hover-efektit korostamaan aktiivista viikkoa
Backend-parametrit	Käyttäjän valittavat projektityypit (1krs / 2krs / paritalo)
Responsiivinen asettelu	Automaattinen sarakkeiden piilotus kapeilla näytöillä
8. Yhteenveto

Komponentti Aikataulu.jsx on moderni, komponenttipohjainen ja laajennettavissa oleva React-näkymä, joka yhdistää:

datalähtöisen ajankäsittelyn (viikko- ja jaksotason logiikka),

visuaalisesti selkeän korttipohjaisen esityksen,

ja joustavan rakenteen tulevaa kehitystä varten.

Se on tuotantovalmiin käyttöliittymän ydinrakennuspalikka aikataulutukseen ja projektiseurantaan.