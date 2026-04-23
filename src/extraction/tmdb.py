import os
import requests
import polars as pl
from dotenv import load_dotenv
from loguru import logger

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"
GENRE_HORREUR_ID = 27


def fetch_movies(pages: int = 5) -> pl.DataFrame:
    logger.info(f"TMDB — début extraction ({pages} pages)")
    results = []

    for page in range(1, pages + 1):
        try:
            response = requests.get(
                f"{BASE_URL}/discover/movie",
                params={
                    "api_key": TMDB_API_KEY,
                    "with_genres": GENRE_HORREUR_ID,
                    "language": "fr-FR",
                    "page": page,
                },
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            results.extend(data.get("results", []))
            logger.info(f"TMDB — page {page}/{pages} OK ({len(data.get('results', []))} films)")

        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB — erreur page {page} : {e}")
            continue

    if not results:
        logger.warning("TMDB — aucun résultat récupéré")
        return pl.DataFrame()

    df = pl.DataFrame([
        {
            "titre": r.get("title", ""),
            "synopsis": r.get("overview", ""),
            "date_sortie": r.get("release_date", None),
            "note_moyenne": r.get("vote_average", None),
            "type": "film",
            "source": "tmdb",
        }
        for r in results
    ])

    logger.success(f"TMDB — {len(df)} films extraits")
    return df


if __name__ == "__main__":
    df = fetch_movies(pages=3)
    print(df.head(5))