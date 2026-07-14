import { useEffect, useState } from "react";
import {
  Link,
  useParams,
} from "react-router-dom";

import { getArticle } from "../services/psychosphereApi";

import "./psychosphere.css";

function ArticlePage() {
  const { slug } = useParams();

  const [article, setArticle] = useState(null);
  const [isLoading, setIsLoading] =
    useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    let ignoreResult = false;

    async function loadArticle() {
      try {
        setIsLoading(true);
        setError("");

        const loadedArticle =
          await getArticle(slug);

        if (!ignoreResult) {
          setArticle(loadedArticle);
        }
      } catch (requestError) {
        console.error(requestError);

        if (!ignoreResult) {
          setError(
            requestError.message ||
              "Nie udało się pobrać artykułu."
          );
        }
      } finally {
        if (!ignoreResult) {
          setIsLoading(false);
        }
      }
    }

    loadArticle();

    return () => {
      ignoreResult = true;
    };
  }, [slug]);

  if (isLoading) {
    return (
      <main className="ps-article-page">
        <div className="ps-not-found">
          <span className="ps-not-found__number">
            …
          </span>

          <h1>Ładowanie artykułu</h1>

          <p>
            Pobieramy treść z PsychSphere.
          </p>
        </div>
      </main>
    );
  }

  if (error || !article) {
    return (
      <main className="ps-article-page">
        <div className="ps-not-found">
          <span className="ps-not-found__number">
            404
          </span>

          <h1>Nie znaleziono artykułu</h1>

          <p>
            {error ||
              "Wybrany artykuł nie istnieje albo został usunięty."}
          </p>

          <Link
            to="/psychosphere"
            className="ps-primary-button"
          >
            Wróć do PsychSphere
          </Link>
        </div>
      </main>
    );
  }

  return (
    <main className="ps-article-page">
      <article className="ps-article">
        <Link
          to="/psychosphere"
          className="ps-back-link"
        >
          ← Wróć do wszystkich artykułów
        </Link>

        <header className="ps-article__header">
          <div>
            {article.categories.map(
              (category) => (
                <span
                  key={
                    category.id ||
                    category.slug
                  }
                  className="ps-article__category"
                >
                  {category.name}
                </span>
              )
            )}

            {article.isPremium && (
              <span className="ps-article__premium">
                🔒 Artykuł Premium
              </span>
            )}
          </div>

          <h1>{article.title}</h1>

          <p className="ps-article__excerpt">
            {article.excerpt}
          </p>

          <div className="ps-article__meta">
            <span>
              Autor: {article.author}
            </span>

            <span aria-hidden="true">•</span>

            <span>{article.publishedAt}</span>

            <span aria-hidden="true">•</span>

            <span>
              {article.readTime} czytania
            </span>
          </div>

          <div className="ps-card__tags">
            {article.tags.map((tag) => (
              <span
                key={tag}
                className="ps-card__tag"
              >
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

        {article.hasAccess ? (
          <div className="ps-article__body">
            {article.content.map(
              (paragraph, index) => (
                <p
                  key={`${article.id}-${index}`}
                >
                  {paragraph}
                </p>
              )
            )}
          </div>
        ) : (
          <>
            <div className="ps-article__preview">
              <p>
                Ten artykuł jest częścią biblioteki
                PsychSphere Premium. Aktywna subskrypcja
                umożliwia dostęp do całej treści.
              </p>
            </div>

            <section className="ps-paywall">
              <div
                className="ps-paywall__icon"
                aria-hidden="true"
              >
                🔒
              </div>

              <div className="ps-paywall__content">
                <span className="ps-paywall__label">
                  PsychSphere Premium
                </span>

                <h2>
                  Pełna treść wymaga subskrypcji
                </h2>

                <p>
                  Uzyskaj dostęp do wszystkich
                  artykułów premium i materiałów
                  specjalistycznych.
                </p>

                <div className="ps-paywall__actions">
                  <Link
                    to="/psychosphere/subscription"
                    className="ps-primary-button"
                  >
                    Dowiedz się więcej
                  </Link>

                  <Link
                    to="/login"
                    className="ps-secondary-button"
                  >
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