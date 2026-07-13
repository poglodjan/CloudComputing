import { Link, useParams } from "react-router-dom";
import { psychosphereArticles } from "../data/psychosphereArticles";
import "./psychosphere.css";

function ArticlePage() {
  const { slug } = useParams();

  const article = psychosphereArticles.find(
    (currentArticle) => currentArticle.slug === slug
  );

  const hasSubscription = false; // Replace with actual subscription check logic

  if (!article) {
    return (
      <main className="ps-article-page">
        <div className="ps-not-found">
          <span className="ps-not-found__number">404</span>
          <h1>Nie znaleziono artykułu</h1>
          <p>Wybrany artykuł nie istnieje albo został usunięty.</p>

          <Link to="/psychosphere" className="ps-primary-button">
            Wróć do PsychSphere
          </Link>
        </div>
      </main>
    );
  }

  const canReadArticle = !article.isPremium || hasSubscription;

  return (
    <main className="ps-article-page">
      <article className="ps-article">
        <Link to="/psychosphere" className="ps-back-link">
          ← Wróć do wszystkich artykułów
        </Link>

        <header className="ps-article__header">
          <span className="ps-article__category">
            {article.category}
          </span>

          {article.isPremium && (
            <span className="ps-article__premium">
              🔒 Artykuł Premium
            </span>
          )}

          <h1>{article.title}</h1>

          <p className="ps-article__excerpt">{article.excerpt}</p>

          <div className="ps-article__meta">
            <span>{article.publishedAt}</span>
            <span aria-hidden="true">•</span>
            <span>{article.readTime} czytania</span>
          </div>

          <div className="ps-card__tags">
            {article.tags.map((tag) => (
              <span key={tag} className="ps-card__tag">
                #{tag}
              </span>
            ))}
          </div>
        </header>

        <img
          src={article.image}
          alt=""
          className="ps-article__cover"
        />

        {canReadArticle ? (
          <div className="ps-article__body">
            {article.content.map((paragraph, index) => (
              <p key={`${article.id}-${index}`}>{paragraph}</p>
            ))}
          </div>
        ) : (
          <>
            <div className="ps-article__preview">
              <p>
                Ten artykuł jest częścią biblioteki PsychSphere Premium.
                Aktywna subskrypcja umożliwia dostęp do całej treści oraz
                pozostałych materiałów premium.
              </p>
            </div>

            <section className="ps-paywall">
              <div className="ps-paywall__icon" aria-hidden="true">
                🔒
              </div>

              <div className="ps-paywall__content">
                <span className="ps-paywall__label">
                  PsychSphere Premium
                </span>

                <h2>Pełna treść wymaga subskrypcji</h2>

                <p>
                  Uzyskaj dostęp do wszystkich artykułów premium,
                  materiałów specjalistycznych i nowych publikacji.
                </p>

                <div className="ps-paywall__actions">
                  <Link
                    to="/psychosphere/subscription"
                    className="ps-primary-button"
                    >
                    Zobacz dostępne plany
                  </Link>

                  <Link to="/login" className="ps-secondary-button">
                    Mam już konto
                  </Link>
                </div>
              </div>
            </section>
          </>
        )}
      </article>
    </main>
  );
}

export default ArticlePage;