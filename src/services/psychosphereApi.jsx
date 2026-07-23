const API_URL =
  import.meta.env.VITE_API_URL || "https://psychosphere-backend-312700987588.europe-central2.run.app";

function formatDate(dateValue) {
  if (!dateValue) {
    return "";
  }

  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return "";
  }

  return new Intl.DateTimeFormat("pl-PL", {
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(date);
}

function splitContentIntoParagraphs(content) {
  if (!content || typeof content !== "string") {
    return [];
  }

  return content
    .split(/\n\s*\n/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);
}

/**
 * Zamienia nazwy pól Django na format używany w React.
 */
function normalizeArticle(article) {
  const categories = Array.isArray(article.categories)
    ? article.categories
    : [];

  const tags = Array.isArray(article.tags)
    ? article.tags.map((tag) => tag.name)
    : [];

  return {
    id: article.id,
    slug: article.slug,
    title: article.title,
    author: article.author || "Redakcja PsychSphere",
    excerpt: article.excerpt || "",
    content: splitContentIntoParagraphs(article.content),

    image:
      article.image_url ||
      "/static-images/article-default.jpg",

    categories,
    tags,

    isPremium: Boolean(article.is_premium),
    isFeatured: Boolean(article.is_featured),

    hasAccess:
      typeof article.has_access === "boolean"
        ? article.has_access
        : !article.is_premium,

    readTime: `${article.read_time_minutes || 5} min`,
    publishedAt: formatDate(article.published_at),
  };
}

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      Accept: "application/json",
      ...options.headers,
    },
  });

  if (!response.ok) {
    if (response.status === 404) {
      throw new Error("Nie znaleziono artykułu.");
    }

    throw new Error(
      `Błąd połączenia z API: ${response.status}`
    );
  }

  return response.json();
}

export async function getArticles() {
  const data = await request(
    "/api/psychosphere/articles/"
  );

  /*
   * Obsługuje zarówno zwykłą listę:
   * [...]
   *
   * jak i przyszłą paginację:
   * { results: [...] }
   */
  const articles = Array.isArray(data)
    ? data
    : data.results || [];

  return articles.map(normalizeArticle);
}

export async function getArticle(slug) {
  const data = await request(
    `/api/psychosphere/articles/${encodeURIComponent(slug)}/`
  );

  return normalizeArticle(data);
}