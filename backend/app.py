from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_cors import CORS
import locale

try:
    locale.setlocale(locale.LC_TIME, "fi_FI.UTF-8")
except:
    pass

app = Flask(__name__)
CORS(app)


PHASES = {
    1: "Asiakas kerää lähtötiedot suunnittelua varten",
    2: "Asiakas kerää lähtötiedot suunnittelua varten",
    3: "Lupakuvien tekeminen",
    4: "Lupakuvien tekeminen, 1. kalustesuunnittelu",
    5: "Lupakuvien tekeminen, asiakas esittelee luonnokset rakennusvalvonnalle",
    6: "Lupakuvien tekeminen ja lupakuvat valmiit",
    14: "Rakennuslupa myönnetty",
    18: "Rakennuslupa lainvoimainen",
    19: "(LVI-asemakuva tehdään 10 vk ennen talotoimitusta)",
    20: "RAKENNUSLUPA LAINVOIMAINEN",
    21: "LVI-suunnittelu, lopullinen kiintokalustesuunnittelu 5 viikkoa tästä eteenpäin. 17–19 viikot elementtisuunnittelu",
    22: "LVI-suunnittelu",
    23: "Maansiirtotyöt alkaa",
    24: "Tontti rakentamiskunnossa / paalukohteissa paalutus",
    25: "Perustusten valu, sähkösuunnitelmien tekeminen",
    26: "Talotoimitus",
    27: "Aloituspalaveri. Salaojat, sadevesikaivot ja routasuojaus. Sisä- ja ulkopuoliset täytöt",
    28: "Talotoimitus. (Sähkösuunnittelu / Sähköpistesuunnittelu)",
    29: "Vesikattoasennus. Asiakas kommentoi sähkösuunnitelman",
    30: "Sähkösuunnitelman tekeminen jatkuu",
    31: "LVI-töiden aloitus / asiakas hyväksyy sähkösuunnitelman",
    32: "Sisustusvalinnat ilmoitetaan toimittajalle",
    33: "Lattiavalu",
    34: "Vesimittarin asennus. Sähköjohdotus",
    36: "Takka-asennus",
    37: "Sisälevytykset tehty",
    42: "Sisustusmateriaalin sisäänkanto (SISUSTAITSE LUOVUTUS)",
    43: "Maalus / tapetointi alkaa. Kattoturvatuotteiden ja sadevesijärjestelmän toimitus/asennus",
    44: "Laattojen vastaanotto. Laatoitus",
    47: "Kiintokalustetoimitus / asennus. Kodinkoneiden vastaanotto",
    48: "Lattiamateriaalin asennus, listoitus",
    49: "LVI- ja sähkökalustus / Laminaatti, listat, väliovet, vastaanotto. Välisiivous",
    50: "Laminaattiasennus, listoitus",
    51: "Luovutus 1 krs. talot",
    56: "Luovutus 2 ja 1,5 krs. talot",
    60: "Luovutus paritalot",
}


def laske_jakso(projektiviikko):
    if 1 <= projektiviikko <= 2:
        return "Suunnittelun lähtötietojen hankkinen"
    elif 3 <= projektiviikko <= 6:
        return "Rakennuslupakuvien suunnittelu"
    elif 7 <= projektiviikko <= 14:
        return "Rakennusluvan hakemus, käsittely ja päätös"
    elif 15 <= projektiviikko <= 18:
        return "Rakennusluvan valitusaika"
    elif 19 <= projektiviikko <= 26:
        return "Maansiirtotyöt, elementtien valmistus ja talotoimitus"
    elif projektiviikko >= 27:
        return "Rakentaminen"
    else:
        return ""



@app.route("/api/aikataulu", methods=["POST"])
def aikataulu():
    data = request.get_json()
    sopimus_pvm_str = data.get("sopimus_pvm")

    try:
        sopimus_pvm = datetime.strptime(sopimus_pvm_str, "%Y-%m-%d")
    except Exception:
        return jsonify({"error": "Virheellinen päivämäärä"}), 400

   # Selvitetään sopimuspäivä
    try:
        sopimus_pvm = datetime.strptime(sopimus_pvm_str, "%Y-%m-%d")
    except Exception:
        return jsonify({"error": "Virheellinen päivämäärä"}), 400

    # 🔹 Siirrytään seuraavaan maanantaihin
    # weekday(): ma=0, ti=1, ..., su=6
    paivia_lisatty = (7 - sopimus_pvm.weekday()) % 7
    if paivia_lisatty == 0:
        paivia_lisatty = 7  # jos sopimus on maanantai, siirrytään seuraavaan viikkoon

    projektin_alku = sopimus_pvm + timedelta(days=paivia_lisatty)

    # 🔹 Käytetään projektin_alkua varsinaisena alkupäivänä
    start_date = projektin_alku
    end_date = projektin_alku + timedelta(weeks=60)
    current = start_date
    tulos = []

    while current <= end_date:
        # projektiviikko = montako viikkoa on kulunut projektin alusta
        projektiviikko = ((current - start_date).days // 7) + 1

        iso_year, iso_week, _ = current.isocalendar()
        month_name = current.strftime("%b").capitalize()
        vaihe = PHASES.get(projektiviikko, "")
        jakso = laske_jakso(projektiviikko)

        tulos.append({
            "pvm": current.strftime("%d.%m.%Y"),
            "kalenteri_viikko": iso_week,
            "kuukausi": month_name,
            "vaihe": vaihe,
            "jakso": jakso
        })

        current += timedelta(weeks=1)

    return jsonify(tulos)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
