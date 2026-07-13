import { useMemo, useState } from "react";
import ArticleCard from "../components/psychosphere/ArticleCard";
import { psychosphereArticles } from "../data/psychosphereArticles";
import "./psychosphere.css";

function normalizeText(value) {
  return value
    .toLocaleLowerCase("pl-PL")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "");
}

function PsychoSpherePage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [activeCategory, setActiveCategory] = useState("Wszystkie");
  const [activeTag, setActiveTag] = useState("");

  const categories = useMemo(() => {
    const uniqueCategories = psychosphereArticles.map(
      (article) => article.category
    );

    return ["Wszystkie", ...new Set(uniqueCategories)];
  }, []);

  const tags = useMemo(() => {
    const uniqueTags = psychosphereArticles.flatMap(
      (article) => article.tags
    );

    return [...new Set(uniqueTags)].sort((firstTag, secondTag) =>
      firstTag.localeCompare(secondTag, "pl")
    );
  }, []);

  const filteredArticles = useMemo(() => {
    const normalizedQuery = normalizeText(searchQuery.trim());

    return psychosphereArticles.filter((article) => {
      const searchableText = normalizeText(
        [
          article.title,
          article.excerpt,
          article.category,
          ...article.tags,
        ].join(" ")
      );

      const matchesSearch =
        normalizedQuery === "" ||
        searchableText.includes(normalizedQuery);

      const matchesCategory =
        activeCategory === "Wszystkie" ||
        article.category === activeCategory;

      const matchesTag =
        activeTag === "" || article.tags.includes(activeTag);

      return matchesSearch && matchesCategory && matchesTag;
    });
  }, [searchQuery, activeCategory, activeTag]);

  const hasActiveFilters =
    searchQuery !== "" ||
    activeCategory !== "Wszystkie" ||
    activeTag !== "";

  function clearFilters() {
    setSearchQuery("");
    setActiveCategory("Wszystkie");
    setActiveTag("");
  }

  function handleTagClick(tag) {
    setActiveTag((currentTag) => (currentTag === tag ? "" : tag));
  }

  return (
    <main className="ps-page">
      <section className="ps-hero">
        <div className="ps-hero__content">
          <span className="ps-hero__eyebrow">PsychSphere</span>

          <h1>Wiedza psychologiczna podana w przystępny sposób</h1>

          <p>
            Artykuły przygotowane z myślą o osobach, które chcą lepiej
            rozumieć emocje, relacje, neuroróżnorodność i zdrowie
            psychiczne.
          </p>
        </div>
      </section>

      <section className="ps-content">
        <div className="ps-search-panel">
          <label htmlFor="psychosphere-search" className="ps-search-label">
            Przeszukaj artykuły
          </label>

          <div className="ps-search-wrapper">
            <span className="ps-search-icon" aria-hidden="true">
              🔎
            </span>

            <input
              id="psychosphere-search"
              type="search"
              value={searchQuery}
              onChange={(event) => setSearchQuery(event.target.value)}
              placeholder="Wpisz np. ADHD, emocje, stres..."
              className="ps-search-input"
            />
          </div>

          <div className="ps-filter-section">
            <span className="ps-filter-title">Kategorie</span>

            <div className="ps-filter-list">
              {categories.map((category) => (
                <button
                  key={category}
                  type="button"
                  onClick={() => setActiveCategory(category)}
                  className={
                    activeCategory === category
                      ? "ps-filter-button ps-filter-button--active"
                      : "ps-filter-button"
                  }
                >
                  {category}
                </button>
              ))}
            </div>
          </div>

          <div className="ps-filter-section">
            <span className="ps-filter-title">Popularne tagi</span>

            <div className="ps-tag-list">
              {tags.map((tag) => (
                <button
                  key={tag}
                  type="button"
                  onClick={() => handleTagClick(tag)}
                  className={
                    activeTag === tag
                      ? "ps-tag-button ps-tag-button--active"
                      : "ps-tag-button"
                  }
                >
                  #{tag}
                </button>
              ))}
            </div>
          </div>
        </div>

        <div className="ps-results-header">
          <div>
            <span className="ps-results-label">Biblioteka PsychSphere</span>

            <h2>
              {filteredArticles.length === 1
                ? "Znaleziono 1 artykuł"
                : `Znaleziono ${filteredArticles.length} artykułów`}
            </h2>
          </div>

          {hasActiveFilters && (
            <button
              type="button"
              onClick={clearFilters}
              className="ps-clear-button"
            >
              Wyczyść filtry
            </button>
          )}
        </div>

        {filteredArticles.length > 0 ? (
          <div className="ps-articles-list">
            {filteredArticles.map((article) => (
              <ArticleCard key={article.id} article={article} />
            ))}
          </div>
        ) : (
          <div className="ps-empty-state">
            <span className="ps-empty-state__icon" aria-hidden="true">
              🔍
            </span>

            <h2>Nie znaleziono artykułów</h2>

            <p>
              Spróbuj wpisać inne słowo albo wyczyść wybrane filtry.
            </p>

            <button
              type="button"
              onClick={clearFilters}
              className="ps-primary-button"
            >
              Pokaż wszystkie artykuły
            </button>
          </div>
        )}
      </section>
    </main>
  );
  useEffect(() => {
  fetchArticles();
}, []);
}

export default PsychoSpherePage;