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
    (2025, 44): "Asiakas kerää lähtötiedot suunnittelua varten",
    (2025, 45): "Asiakas kerää lähtötiedot suunnittelua varten",
    (2025, 46): "Luonnoskuvien tekeminen",
    (2025, 47): "Asiakas esittelee kuvat rakennusvalvontaan",
    (2025, 48): "Lupakuvien tekeminen",
    (2025, 49): "Lupakuvien tekeminen",
    (2026, 5): "RAKENNUSLUPA MYÖNNETTY",
    (2026, 7): "Sähköasemapiirros",
    (2026, 8): "(LVI-asemakuva tehdään 10 vk ennen talotoimitusta)",
    (2026, 9): "RAKENNUSLUPA LAINVOIMAINEN",
    (2026, 10): "LVI-suunnittelu, lopullinen kiintokalustesuunnittelu 5 viikkoa tästä eteen päin. 17–19 viikot elementtisuunnittelu",
    (2026, 11): "LVI-suunnittelu",
    (2026, 12): "Maansiirtotyöt alkaa",
    (2026, 13): "Tontti rakentamiskunnossa / paalukohteissa paalutus",
    (2026, 14): "Perustusten valu, sähkösuunnitelmien tekeminen",
    (2026, 16): "Aloituspalaveri. Salaojat, sadevesikaivot ja routasuojaus. Sisä- ja ulkopuoliset täytöt",
    (2026, 17): "Talotoimitus. (Sähkösuunnittelu / Sähköpistesuunnittelu)",
    (2026, 18): "Vesikattoasennus. Asiakas kommentoi sähkösuunnitelman",
    (2026, 19): "Sähkösuunnitelman tekeminen jatkuu",
    (2026, 20): "LVI-töiden aloitus / asiakas hyväksyy sähkösuunnitelman",
    (2026, 21): "Sisustusvalinnat ilmoitetaan toimittajalle",
    (2026, 22): "Lattiavalu",
    (2026, 23): "Vesimittarin asennus. Sähköjohdotus",
    (2026, 25): "Takka-asennus",
    (2026, 26): "Sisälevytykset tehty",
    (2026, 31): "Sisustusmateriaalin sisäänkanto (SISUSTAITSE LUOVUTUS)",
    (2026, 32): "Maalus / tapetointi alkaa. Kattoturvatuotteiden ja sadevesijärjestelmän toimitus/asennus",
    (2026, 33): "Laattojen vastaanotto. Laatoitus",
    (2026, 36): "Kiintokalustetoimitus / asennus. Kodinkoneiden vastaanotto",
    (2026, 38): "LVI- ja sähkökalustus / Laminaatti, listat, väliovet, vastaanotto. Välisiivous",
    (2026, 39): "Laminaattiasennus, listoitus",
    (2026, 40): "Luovutustarkastus",
    (2026, 42): "Luovutus. Loppusiivous. Talonäyttely HUOM! 2 ja 1,5 krs +5 viikkoa. Paritalo 1krs. +9 vk",
    (2026, 47): "Luovutus 2 tai 1,5 krs (+5 viikkoa)",
    (2026, 51): "Luovutus paritalo 1 krs (+9 viikkoa)",
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

    start_date = sopimus_pvm
    end_date = sopimus_pvm + timedelta(weeks=60)  # 60 viikkoa projektille
    current = start_date
    tulos = []

    while current <= end_date:
        # projektiviikko = montako viikkoa on kulunut projektin alusta
        projektiviikko = ((current - start_date).days // 7) + 1

        iso_year, iso_week, _ = current.isocalendar()
        month_name = current.strftime("%b").capitalize()
        vaihe = PHASES.get((iso_year, iso_week), "")
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
