import json
import pandas as pd
from sqlmodel import Session, SQLModel, create_engine, select
from src.models import (
    Movie, Genre, Keyword, ProductionCompany, ProductionCountry, SpokenLanguage,
    MovieGenreLink, MovieKeywordLink, MovieProductionCompanyLink, MovieProductionCountryLink, MovieSpokenLanguageLink,
    Cast, Crew
)
import os

DB_PATH = os.environ.get("MOVIES_DB_PATH", "sqlite:///movies.db")
MOVIES_CSV = os.environ.get("MOVIES_CSV", "data/tmdb_5000_movies.csv")
CREDITS_CSV = os.environ.get("CREDITS_CSV", "data/tmdb_5000_credits.csv")

def parse_json_field(field):
    try:
        return json.loads(field.replace("'", '"')) if isinstance(field, str) and field else []
    except Exception:
        try:
            return json.loads(field) if isinstance(field, str) and field else []
        except Exception:
            return []

def main():
    engine = create_engine(DB_PATH)
    SQLModel.metadata.create_all(engine)

    movies_df = pd.read_csv(MOVIES_CSV)
    credits_df = pd.read_csv(CREDITS_CSV)

    with Session(engine) as session:
        # Lookup caches
        genre_cache = {}
        keyword_cache = {}
        company_cache = {}
        country_cache = {}
        language_cache = {}

        # First, insert all movies
        for _, row in movies_df.iterrows():
            movie = Movie(
                id=int(row['id']),
                title=row['title'],
                original_title=row.get('original_title'),
                overview=row.get('overview'),
                tagline=row.get('tagline'),
                status=row.get('status'),
                homepage=row.get('homepage'),
                release_date=row.get('release_date'),
                original_language=row.get('original_language'),
                budget=int(row['budget']) if not pd.isna(row['budget']) else None,
                revenue=int(row['revenue']) if not pd.isna(row['revenue']) else None,
                runtime=float(row['runtime']) if not pd.isna(row['runtime']) else None,
                popularity=float(row['popularity']) if not pd.isna(row['popularity']) else None,
                vote_average=float(row['vote_average']) if not pd.isna(row['vote_average']) else None,
                vote_count=int(row['vote_count']) if not pd.isna(row['vote_count']) else None,
            )
            session.add(movie)
            session.flush()  # Ensure movie.id is available
            # Genres
            for genre in parse_json_field(row.get('genres')):
                gid = int(genre['id'])
                if gid not in genre_cache:
                    genre_obj = Genre(id=gid, name=genre['name'])
                    session.merge(genre_obj)
                    genre_cache[gid] = genre_obj
                session.add(MovieGenreLink(movie_id=movie.id, genre_id=gid))
            # Keywords
            for keyword in parse_json_field(row.get('keywords')):
                kid = int(keyword['id'])
                if kid not in keyword_cache:
                    keyword_obj = Keyword(id=kid, name=keyword['name'])
                    session.merge(keyword_obj)
                    keyword_cache[kid] = keyword_obj
                session.add(MovieKeywordLink(movie_id=movie.id, keyword_id=kid))
            # Production Companies
            for company in parse_json_field(row.get('production_companies')):
                cid = int(company['id'])
                if cid not in company_cache:
                    company_obj = ProductionCompany(id=cid, name=company['name'])
                    session.merge(company_obj)
                    company_cache[cid] = company_obj
                session.add(MovieProductionCompanyLink(movie_id=movie.id, company_id=cid))
            # Production Countries
            for country in parse_json_field(row.get('production_countries')):
                # Use a synthetic int id since no id in country
                country_id = hash(country['iso_3166_1'] + country['name']) % (10**9)
                if country_id not in country_cache:
                    country_obj = ProductionCountry(id=country_id, iso_3166_1=country['iso_3166_1'], name=country['name'])
                    session.merge(country_obj)
                    country_cache[country_id] = country_obj
                session.add(MovieProductionCountryLink(movie_id=movie.id, country_id=country_id))
            # Spoken Languages
            for lang in parse_json_field(row.get('spoken_languages')):
                lang_id = hash(lang['iso_639_1'] + lang['name']) % (10**9)
                if lang_id not in language_cache:
                    lang_obj = SpokenLanguage(id=lang_id, iso_639_1=lang['iso_639_1'], name=lang['name'])
                    session.merge(lang_obj)
                    language_cache[lang_id] = lang_obj
                session.add(MovieSpokenLanguageLink(movie_id=movie.id, language_id=lang_id))
        session.commit()

        # Now, insert credits (cast and crew)
        for _, row in credits_df.iterrows():
            movie_id = int(row['movie_id'])
            # Cast
            for cast_member in parse_json_field(row.get('cast')):
                if not cast_member.get('credit_id'): continue
                session.add(Cast(
                    credit_id=cast_member['credit_id'],
                    movie_id=movie_id,
                    person_id=int(cast_member['id']),
                    cast_id=cast_member.get('cast_id'),
                    character=cast_member.get('character'),
                    gender=cast_member.get('gender'),
                    name=cast_member.get('name'),
                    order=cast_member.get('order'),
                ))
            # Crew
            for crew_member in parse_json_field(row.get('crew')):
                if not crew_member.get('credit_id'): continue
                session.add(Crew(
                    credit_id=crew_member['credit_id'],
                    movie_id=movie_id,
                    person_id=int(crew_member['id']),
                    department=crew_member.get('department'),
                    gender=crew_member.get('gender'),
                    job=crew_member.get('job'),
                    name=crew_member.get('name'),
                ))
        session.commit()

if __name__ == "__main__":
    main()
