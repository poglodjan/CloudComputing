import { Link } from "react-router-dom";

function ArticleCard({ article }) {
  return (
    <Link
      to={`/psychosphere/articles/${article.slug}`}
      className={`ps-card ${article.isPremium ? "ps-card--premium" : ""}`}
      aria-label={`Otwórz artykuł: ${article.title}`}
    >
      {article.isPremium && (
        <div className="ps-card__ribbon">
          <span>Artykuł premium</span>
        </div>
      )}

      <div className="ps-card__image-container">
        <img
          src={article.image}
          alt=""
          className="ps-card__image"
          loading="lazy"
        />

        <span className="ps-card__category">{article.category}</span>
      </div>

      <div className="ps-card__content">
        <div className="ps-card__meta">
          <span>{article.publishedAt}</span>
          <span aria-hidden="true">•</span>
          <span>{article.readTime} czytania</span>
        </div>

        <h2 className="ps-card__title">{article.title}</h2>

        <p className="ps-card__excerpt">{article.excerpt}</p>

        <div className="ps-card__tags">
          {article.tags.map((tag) => (
            <span key={tag} className="ps-card__tag">
              #{tag}
            </span>
          ))}
        </div>
      </div>
    </Link>
  );
}

export default ArticleCard;