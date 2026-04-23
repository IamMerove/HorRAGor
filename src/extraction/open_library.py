import requests
import polars as pl
from loguru import logger

BASE_URL = "https://openlibrary.org/search.json"


def fetch_books(pages: int = 5) -> pl.DataFrame:
    logger.info(f"Open Library — début extraction ({pages} pages)")
    results = []

    for page in range(1, pages + 1):
        try:
            response = requests.get(
                BASE_URL,
                params={
                    "subject": "horror",
                    "fields": "key,title,author_name,first_publish_year,ratings_average,number_of_pages_median",
                    "page": page,
                    "limit": 100,
                },
                timeout=15,
            )
            response.raise_for_status()
            data = response.json()
            docs = data.get("docs", [])
            results.extend(docs)
            logger.info(f"Open Library — page {page}/{pages} OK ({len(docs)} livres)")

        except requests.exceptions.RequestException as e:
            logger.error(f"Open Library — erreur page {page} : {e}")
            continue

    if not results:
        logger.warning("Open Library — aucun résultat")
        return pl.DataFrame()

    df = pl.DataFrame([
        {
            "titre": r.get("title", ""),
            "synopsis": None,
            "date_sortie": str(r["first_publish_year"]) if r.get("first_publish_year") else None,
            "note_moyenne": round(r["ratings_average"], 1) if r.get("ratings_average") else None,
            "auteur": r["author_name"][0] if r.get("author_name") else None,
            "type": "livre",
            "source": "open_library",
        }
        for r in results
    ])

    logger.success(f"Open Library — {len(df)} livres extraits")
    return df


if __name__ == "__main__":
    df = fetch_books(pages=2)
    print(df.shape)
    print(df.head(5))