import polars as pl
from loguru import logger

RAW_PATH = "data/raw/kaggle/horror_movies.csv"

COLONNES_UTILES = [
    "id",
    "title",
    "overview",
    "release_date",
    "vote_average",
    "genre_names",
    "original_language",
    "runtime",
    "status",
]


def fetch_movies() -> pl.DataFrame:
    logger.info(f"Kaggle — lecture du fichier {RAW_PATH}")

    try:
        df = pl.read_csv(RAW_PATH, infer_schema_length=1000)
    except Exception as e:
        logger.error(f"Kaggle — erreur lecture CSV : {e}")
        return pl.DataFrame()

    # Garder uniquement les colonnes utiles
    df = df.select(COLONNES_UTILES)

    # Renommer pour correspondre à notre modèle
    df = df.rename(
        {
            "title": "titre",
            "overview": "synopsis",
            "vote_average": "note_moyenne",
        }
    )

    # Ajouter les colonnes type et source
    df = df.with_columns(
        [
            pl.lit("film").alias("type"),
            pl.lit("kaggle").alias("source"),
        ]
    )

    # Filtrer les lignes sans titre
    df = df.filter(pl.col("titre").is_not_null() & (pl.col("titre") != ""))

    logger.success(f"Kaggle — {len(df)} films chargés")
    return df


if __name__ == "__main__":
    df = fetch_movies()
    print(df.shape)
    print(df.head(5))
