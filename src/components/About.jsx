import React from "react";
import "./PsychoSphere.css"; // Reużywamy wspólne style

const AboutUs = () => {
  return (
    <div
  className="about-flex-container"
  style={{
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    gap: "8rem",
    width: "100vw",
    minheight: "100vh",
    boxSizing: "border-box",
    padding: "8rem 0",
  }}
>
      <div style={{ flex: 1, maxWidth: "1200px" }}>
        <h1 style={{color:"white", textShadow: "2px 2px 0 #33006F, -2px -2px 0 #33006F, 2px -2px 0 #33006F, -2px 2px 0 #33006F"}}>O nas</h1>

        <div className="psych-section">
          <h2>Nasza misja</h2>
          <p>
            Neurodetective powstało z potrzeby stworzenia narzędzia, które
            realnie wspiera dialog między rodzicem a nauczycielem. Naszym celem
            jest usprawnienie komunikacji, aby każde dziecko mogło rozwijać się w
            bezpiecznym i wspierającym środowisku.
          </p>
          <p>Skontaktuj się z nami! info@psychodetective.pl</p>
        </div>

        <div className="psych-section">
          <h2>Dla kogo stworzyliśmy tę platformę?</h2>
          <p>
            Dla nauczycieli, którzy chcą szybciej reagować na potrzeby uczniów. Dla
            rodziców, którzy szukają zrozumienia i chcą być aktywną częścią procesu
            edukacyjnego. I przede wszystkim – dla dzieci.
          </p>
        </div>

        <div className="psych-section">
          <h2>Co nas napędza?</h2>
          <p>
            Ambicja, pasja do technologii edukacyjnej oraz chęć zbudowania
            mostu między dwoma światami: szkolnym i domowym. Wierzymy, że razem
            możemy tworzyć przyszłość edukacji bardziej empatyczną i skuteczną.
          </p>
        </div>
      </div>
      <div
        style={{
          flex: "0 0 680px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          paddingLeft: "2rem", // większy odstęp od tekstu
        }}
      >
        <div
          style={{
            background: "rgba(255,255,255,0.95)",
            borderRadius: "20px",
            boxShadow: "0 4px 32px rgba(51,0,111,0.12)",
            padding: "1.5rem",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            width: "100%",
            maxWidth: "680px",
          }}
        >
          <video
            src="https://storage.googleapis.com/psychological-app-a359c-frontend/movie/Neurodetective.mp4"
            controls
            style={{
              width: "100%",
              maxWidth: "680px",
              borderRadius: "10px",
              boxShadow: "0 2px 16px rgba(0,0,0,0.15)",
              background: "#fff"
            }}
          />
        </div>
      </div>
    </div>
  );
};

export default AboutUs;