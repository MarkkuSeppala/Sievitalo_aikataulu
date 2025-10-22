import React, { useState } from "react";

export default function Aikataulu() {
  const [sopimusPvm, setSopimusPvm] = useState("");
  const [aikataulu, setAikataulu] = useState([]);
  const [loading, setLoading] = useState(false);

  const haeAikataulu = async () => {
    if (!sopimusPvm) return;
    
    setLoading(true);
    try {
      const res = await fetch("https://sievitalo-backend.onrender.com/api/aikataulu", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sopimus_pvm: sopimusPvm }),
      });
      const data = await res.json();
      setAikataulu(data);
    } catch (error) {
      console.error("Virhe aikataulun haussa:", error);
    } finally {
      setLoading(false);
    }
  };

  const kuukaudenVari = (kuukausi) => {
    const colors = {
      Tammi: "#e0f7fa",
      Helmi: "#f1f8e9",
      Maalis: "#fff3e0",
      Huhti: "#e8eaf6",
      Touko: "#e0f2f1",
      Kesä: "#fffde7",
      Heinä: "#fce4ec",
      Elo: "#f3e5f5",
      Syys: "#ede7f6",
      Loka: "#e3f2fd",
      Marras: "#edeef0",
      Joulu: "#ffebee",
    };
    return colors[kuukausi] || "white";
  };

  const jaksonVari = (jakso) => {
    const colors = {
      "Suunnittelun lähtötietojen hankkiminen": "#bbdefb",
      "Rakennuslupakuvien suunnittelu": "#fff59d",
      "Rakennusluvan hakemus, käsittely ja päätös": "#ffe082",
      "Rakennusluvan valitusaika": "#ffcc80",
      "Maansiirtotyöt, elementtien valmistus ja talotoimitus": "#a5d6a7",
      Rakentaminen: "#81c784",
    };
    return colors[jakso] || "white";
  };

  const merkittavatVaiheet = [
    "Lupakuvien tekeminen ja lupakuvat valmiit",
    "Rakennuslupa myönnetty",
    "Rakennuslupa lainvoimainen",
    "Talotoimitus",
    "Luovutus 1 krs. talot",
    "Luovutus 2 ja 1,5 krs. talot",
    "Luovutus paritalot",
  ];

  const laskeViikot = (data) => {
    let laskuri = 0;
    let edellinenJakso = "";
    let projektiviikko = 0;
    return data.map((rivi) => {
      if (rivi.jakso !== edellinenJakso) {
        laskuri = 1;
        edellinenJakso = rivi.jakso;
      } else {
        laskuri += 1;
      }
      projektiviikko += 1;

      let vaihe = rivi.vaihe;

      if (projektiviikko === 6)
        vaihe = "Lupakuvien tekeminen ja lupakuvat valmiit";
      else if (projektiviikko === 14) vaihe = "Rakennuslupa myönnetty";
      else if (projektiviikko === 18) vaihe = "Rakennuslupa lainvoimainen";
      else if (projektiviikko === 26) vaihe = "Talotoimitus";
      else if (projektiviikko === 48)
        vaihe = "Lattiamateriaalin asennus, listoitus";
      else if (projektiviikko === 51) vaihe = "Luovutus 1 krs. talot";
      else if (projektiviikko === 56) vaihe = "Luovutus 2 ja 1,5 krs. talot";
      else if (projektiviikko === 60) vaihe = "Luovutus paritalot";

      return { ...rivi, jakson_viikko: laskuri, projektiviikko, vaihe };
    });
  };

  const aikatauluViikoilla = laskeViikot(aikataulu);

  // Tiimalasi-komponentti
  const Tiimalasi = () => (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '40px',
      backgroundColor: '#ffffff',
      borderRadius: '12px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
      margin: '30px auto',
      width: '300px'
    }}>
      <div style={{
        width: '50px',
        height: '50px',
        border: '4px solid #f3f3f3',
        borderTop: '4px solid #1976d2',
        borderRadius: '50%',
        animation: 'spin 1s linear infinite',
        marginBottom: '20px'
      }}></div>
      <p style={{
        fontSize: '18px',
        color: '#666',
        margin: 0,
        fontWeight: '500'
      }}>Ladataan aikataulua...</p>
    </div>
  );

  return (
    <div
      style={{
        padding: "20px",
        fontFamily: "Arial, sans-serif",
        textAlign: "center",
        backgroundColor: "#f8f9fa",
        minHeight: "100vh",
      }}
    >
      <style>
        {`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
        `}
      </style>
      <img
        src="/sievitalo_logo.png"
        alt="Sievitalo logo"
        style={{
          width: "900px",
          marginBottom: "10px",
        }}
      />
      <h2 style={{ marginBottom: "20px" }}>Viitteellinen projektiaikataulu</h2>

      <div style={{ marginBottom: "15px" }}>
        <label
          htmlFor="sopimusPvm"
          style={{
            display: "block",
            fontWeight: "bold",
            marginBottom: "6px",
            fontSize: "15px",
          }}
        >
          Sopimuspäivä
        </label>
        <input
          id="sopimusPvm"
          type="date"
          value={sopimusPvm}
          onChange={(e) => setSopimusPvm(e.target.value)}
          style={{
            padding: "6px",
            marginRight: "10px",
            fontSize: "16px",
            borderRadius: "5px",
            border: "1px solid #ccc",
          }}
        />
        <button
          onClick={haeAikataulu}
          disabled={loading}
          style={{
            padding: "6px 12px",
            backgroundColor: loading ? "#ccc" : "#1976d2",
            color: "white",
            border: "none",
            borderRadius: "5px",
            fontSize: "16px",
            cursor: loading ? "not-allowed" : "pointer",
            opacity: loading ? 0.6 : 1,
          }}
        >
          {loading ? "Ladataan..." : "Näytä aikataulu"}
        </button>
      </div>

      {loading && <Tiimalasi />}

      {!loading && aikatauluViikoilla.length > 0 && (
        <div
          style={{
            width: "70%",
            margin: "30px auto",
            backgroundColor: "#ffffff",
            borderRadius: "12px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.1)",
            padding: "25px",
          }}
        >
          <table
            style={{
              borderCollapse: "collapse",
              width: "100%",
              fontSize: "15px",
              border: "1px solid #ccc",
              tableLayout: "fixed",
            }}
          >
            <thead style={{ backgroundColor: "#f0f0f0" }}>
              <tr>
                <th style={{ ...thStyle, width: "4%" }}>Päivämäärä</th>
                <th style={{ ...thStyle, width: "3%" }}>
                  Viikko<br />(kalenteri)
                </th>
                <th style={{ ...thStyle, width: "4%" }}>Kuukausi</th>
                <th style={{ ...thStyle, width: "20%" }}>Jakso</th>
                <th style={{ ...thStyle, width: "20%" }}>Vaihe</th>
                <th style={{ ...thStyle, width: "4%" }}>
                  Jakson<br />viikkomäärä
                </th>
                <th style={{ ...thStyle, width: "4%" }}>
                  Projektin<br />viikko
                </th>
              </tr>
            </thead>

            <tbody>
              {aikatauluViikoilla.map((r, i) => {
                const kuukausi =
                  r.kuukausi.charAt(0).toUpperCase() + r.kuukausi.slice(1);
                const monthColor = kuukaudenVari(kuukausi);
                const jaksoColor = jaksonVari(r.jakso);

                const onMerkittava = merkittavatVaiheet.includes(r.vaihe);
                const korostusStyle = onMerkittava
                  ? {
                      borderTop: "2px solid #000",
                      borderBottom: "2px solid #000",
                      fontWeight: "bold",
                    }
                  : {};

                return (
                  <tr key={i}>
                    <td
                      style={{
                        ...tdStyle,
                        backgroundColor: monthColor,
                        textAlign: "left",
                      }}
                    >
                      {r.pvm}
                    </td>
                    <td
                      style={{
                        ...tdStyle,
                        backgroundColor: monthColor,
                        textAlign: "left",
                      }}
                    >
                      {r.kalenteri_viikko}
                    </td>
                    <td
                      style={{
                        ...tdStyle,
                        backgroundColor: monthColor,
                        textAlign: "left",
                      }}
                    >
                      {kuukausi}
                    </td>

                    <td
                      style={{
                        ...tdStyle,
                        backgroundColor: jaksoColor,
                        fontWeight: "bold",
                        textAlign: "left",
                      }}
                    >
                      {r.jakso}
                    </td>
                    <td
                      style={{
                        ...tdStyle,
                        backgroundColor: jaksoColor,
                        textAlign: "left",
                        ...korostusStyle,
                      }}
                    >
                      {r.vaihe}
                    </td>
                    <td
                      style={{
                        ...tdStyle,
                        backgroundColor: jaksoColor,
                        textAlign: "center",
                        fontWeight: "bold",
                      }}
                    >
                      {r.jakson_viikko}
                    </td>
                    <td
                      style={{
                        ...tdStyle,
                        backgroundColor: jaksoColor,
                        textAlign: "center",
                        fontWeight: "bold",
                      }}
                    >
                      {r.projektiviikko}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

const thStyle = {
  textAlign: "left",
  padding: "8px",
  borderBottom: "1px solid #ccc",
};

const tdStyle = {
  padding: "6px",
  borderBottom: "1px solid #eee",
};
