import React from "react";
import "./PsychoSphere.css";
import "./About.css";

import photo1 from '../assets/photos/Ewa.png';
import photo2 from '../assets/photos/Marta.png';
import photo3 from '../assets/photos/Janek.png';
import photo4 from '../assets/photos/Paula.png';

const AboutUs = () => {
  return (
    // Główny kontener strony (układa elementy pionowo)
    <div style={{ width: "100%", padding: "8rem 2rem", boxSizing: "border-box" }}>
      
      {/* Kontener dla układu poziomego: Tekst po lewej, Wideo po prawej */}
      <div
        className="about-flex-container"
        style={{
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          gap: "8rem",
          maxWidth: "1480px", // Zapobiega rozciąganiu na ogromnych ekranach
          margin: "0 auto",   // Centruje kontener na środku strony
        }}
      >
        {/* LEWA KOLUMNA - TEKSTY */}
        <div style={{ flex: 1, maxWidth: "600px" }}>
          {/* <h1 style={{ color: "white", textShadow: "2px 2px 0 #33006F, -2px -2px 0 #33006F, 2px -2px 0 #33006F, -2px 2px 0 #33006F" }}>
            O nas
          </h1> */}

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

        {/* PRAWA KOLUMNA - WIDEO */}
        <div
          style={{
            flex: "0 0 680px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
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
            }}
          >
            <video
              src="https://storage.googleapis.com/psychological-app-a359c-frontend/movie/Neurodetective.mp4"
              controls
              style={{
                width: "100%",
                borderRadius: "10px",
                boxShadow: "0 2px 16px rgba(0,0,0,0.15)",
                background: "#fff"
              }}
            />
          </div>
        </div>
      </div>

      {/* SEKCJA ZESPOŁU - POZA KONTENEREM FLEX, WIĘC SPADA NA DÓŁ */}
      <div className="psych-section">
      <section className="team-section">
        <h2 className="team-title">Nasz Zespół</h2>
        
        <div className="team-grid">
          <div className="team-member">
            <img src={photo4} alt="Paula" className="team-photo" />
            <p className="team-name">Paula</p>
            <p className="team-role">Full Stack Developer</p>
          </div>

          <div className="team-member">
            <img src={photo3} alt="Janek" className="team-photo" />
            <p className="team-name">Janek</p>
            <p className="team-role">Full Stack Developer</p>
          </div>

          <div className="team-member">
            <img src={photo1} alt="Ewa" className="team-photo" />
            <p className="team-name">Ewa</p>
            <p className="team-role">Psychology specialist</p>
          </div>

          <div className="team-member">
            <img src={photo2} alt="Marta" className="team-photo" />
            <p className="team-name">Marta</p>
            <p className="team-role">Psychology specialist</p>      
          </div>
        </div>
      </section>
      </div>
      
    </div>
  );
};

export default AboutUs;