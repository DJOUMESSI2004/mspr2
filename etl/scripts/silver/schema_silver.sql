/* * Script de création de la table silver.covid_cleaned
 * Ce script supprime la table si elle existe déjà et crée une nouvelle table vide
 * avec les colonnes nettoyées pour le traitement des données COVID-19.
 */

-- Supprimer la table si elle existe
DROP TABLE IF EXISTS silver.covid_cleaned;

-- Créer la table silver vide avec les colonnes nettoyées
CREATE TABLE silver.covid_cleaned (
    iso_code TEXT,
    continent TEXT,
    location TEXT,
    date DATE,

    total_cases DOUBLE PRECISION,
    new_cases DOUBLE PRECISION,
    total_deaths DOUBLE PRECISION,
    new_deaths DOUBLE PRECISION,
    reproduction_rate DOUBLE PRECISION,

    icu_patients DOUBLE PRECISION,
    hosp_patients DOUBLE PRECISION,
    weekly_icu_admissions DOUBLE PRECISION,
    weekly_hosp_admissions DOUBLE PRECISION,

    total_vaccinations DOUBLE PRECISION,
    people_vaccinated DOUBLE PRECISION,
    people_fully_vaccinated DOUBLE PRECISION,
    total_boosters DOUBLE PRECISION,
    new_vaccinations DOUBLE PRECISION,

    total_tests DOUBLE PRECISION,
    new_tests DOUBLE PRECISION,
    positive_rate DOUBLE PRECISION,
    tests_per_case DOUBLE PRECISION,

    stringency_index DOUBLE PRECISION,
    population_density DOUBLE PRECISION,
    median_age DOUBLE PRECISION,
    aged_65_older DOUBLE PRECISION,
    aged_70_older DOUBLE PRECISION,
    gdp_per_capita DOUBLE PRECISION,
    human_development_index DOUBLE PRECISION,
    population DOUBLE PRECISION,

    excess_mortality DOUBLE PRECISION
);
