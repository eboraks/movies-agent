from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

class MovieGenreLink(SQLModel, table=True):
    __tablename__ = "movie_genre_link"
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    genre_id: int = Field(foreign_key="genre.id", primary_key=True)

class MovieKeywordLink(SQLModel, table=True):
    __tablename__ = "movie_keyword_link"
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    keyword_id: int = Field(foreign_key="keyword.id", primary_key=True)

class MovieProductionCompanyLink(SQLModel, table=True):
    __tablename__ = "movie_production_company_link"
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    company_id: int = Field(foreign_key="production_company.id", primary_key=True)

class MovieProductionCountryLink(SQLModel, table=True):
    __tablename__ = "movie_production_country_link"
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    country_id: int = Field(foreign_key="production_country.id", primary_key=True)

class MovieSpokenLanguageLink(SQLModel, table=True):
    __tablename__ = "movie_spoken_language_link"
    movie_id: int = Field(foreign_key="movie.id", primary_key=True)
    language_id: int = Field(foreign_key="spoken_language.id", primary_key=True)

class Genre(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    movies: List["Movie"] = Relationship(back_populates="genres", link_model=MovieGenreLink)

class Keyword(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    movies: List["Movie"] = Relationship(back_populates="keywords", link_model=MovieKeywordLink)

class ProductionCompany(SQLModel, table=True):
    __tablename__ = "production_company"
    id: int = Field(primary_key=True)
    name: str
    movies: List["Movie"] = Relationship(back_populates="production_companies", link_model=MovieProductionCompanyLink)

class ProductionCountry(SQLModel, table=True):
    __tablename__ = "production_country"
    id: int = Field(primary_key=True)
    iso_3166_1: str
    name: str
    movies: List["Movie"] = Relationship(back_populates="production_countries", link_model=MovieProductionCountryLink)

class SpokenLanguage(SQLModel, table=True):
    __tablename__ = "spoken_language"
    id: int = Field(primary_key=True)
    iso_639_1: str
    name: str
    movies: List["Movie"] = Relationship(back_populates="spoken_languages", link_model=MovieSpokenLanguageLink)

class Movie(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    original_title: Optional[str]
    overview: Optional[str]
    tagline: Optional[str]
    status: Optional[str]
    homepage: Optional[str]
    release_date: Optional[str]
    original_language: Optional[str]
    budget: Optional[int]
    revenue: Optional[int]
    runtime: Optional[float]
    popularity: Optional[float]
    vote_average: Optional[float]
    vote_count: Optional[int]
    genres: List[Genre] = Relationship(back_populates="movies", link_model=MovieGenreLink)
    keywords: List[Keyword] = Relationship(back_populates="movies", link_model=MovieKeywordLink)
    production_companies: List[ProductionCompany] = Relationship(back_populates="movies", link_model=MovieProductionCompanyLink)
    production_countries: List[ProductionCountry] = Relationship(back_populates="movies", link_model=MovieProductionCountryLink)
    spoken_languages: List[SpokenLanguage] = Relationship(back_populates="movies", link_model=MovieSpokenLanguageLink)
    cast: List["Cast"] = Relationship(back_populates="movie")
    crew: List["Crew"] = Relationship(back_populates="movie")

class Cast(SQLModel, table=True):
    credit_id: str = Field(primary_key=True, max_length=255)
    movie_id: int = Field(foreign_key="movie.id")
    person_id: int
    cast_id: Optional[int]
    character: Optional[str]
    gender: Optional[int]
    name: Optional[str]
    order: Optional[int]
    movie: Optional[Movie] = Relationship(back_populates="cast")

class Crew(SQLModel, table=True):
    credit_id: str = Field(primary_key=True, max_length=255)
    movie_id: int = Field(foreign_key="movie.id")
    person_id: int
    department: Optional[str]
    gender: Optional[int]
    job: Optional[str]
    name: Optional[str]
    movie: Optional[Movie] = Relationship(back_populates="crew")
