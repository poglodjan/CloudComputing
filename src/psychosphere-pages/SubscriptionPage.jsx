import { Link } from "react-router-dom";
import "./psychosphere.css";

function SubscriptionPage() {
  return (
    <main className="ps-subscription-page">
      <section className="ps-subscription-box">
        <span className="ps-subscription-box__label">
          PsychoSphere Premium
        </span>

        <h1>Subskrypcje będą dostępne wkrótce</h1>

        <p>
          Pracujemy nad dostępem do artykułów premium. Obecnie zakup
          subskrypcji nie jest jeszcze dostępny.
        </p>

        <div className="ps-subscription-features">
          <div>✓ Dostęp do wszystkich artykułów premium</div>
          <div>✓ Nowe publikacje psychologiczne</div>
          <div>✓ Materiały dotyczące ADHD, autyzmu i emocji</div>
        </div>

        <Link to="/psychosphere" className="ps-primary-button">
          Wróć do artykułów
        </Link>
      </section>
    </main>
  );
}

export default SubscriptionPage;