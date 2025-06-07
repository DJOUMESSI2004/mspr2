/*
    Script de nettoyage des données COVID-19 pour la couche Silver

    Ce script nettoie les données brutes de la couche Bronze et les insère dans la table Silver.
    Il effectue les opérations suivantes :
    1. Filtre les lignes mal formées
    2. Supprime les lignes totalement vides
    3. Supprime les lignes absurdes (trop vides ou invalides)
    4. Supprime les doublons exacts
    5. Insère les données nettoyées dans la table Silver `silver.covid_cleaned`
    6. Supprime les anciennes données nettoyées si présentes
*/

-- Supprimer les anciennes données nettoyées si présentes
TRUNCATE TABLE silver.covid_cleaned;

-- Insérer les données nettoyées à partir de bronze
INSERT INTO silver.covid_cleaned (
    iso_code, continent, location, date,
    total_cases, new_cases, total_deaths, new_deaths,
    reproduction_rate, icu_patients, hosp_patients,
    total_tests, total_vaccinations,
    population, median_age, aged_65_older, aged_70_older,
    cardiovasc_death_rate, diabetes_prevalence, human_development_index,
    excess_mortality
)
SELECT
    -- Valeurs brutes sélectionnées
    iso_code, continent, location, date,
    total_cases, new_cases, total_deaths, new_deaths,
    reproduction_rate, icu_patients, hosp_patients,
    total_tests, total_vaccinations,
    population, median_age, aged_65_older, aged_70_older,
    cardiovasc_death_rate, diabetes_prevalence, human_development_index,
    excess_mortality
FROM bronze.covid_raw
WHERE
    -- 🧱 1. Filtrer les lignes mal formées
    iso_code IS NOT NULL
    AND location IS NOT NULL
    AND date IS NOT NULL

    -- 🧼 2. Supprimer les lignes totalement vides
    AND (
        total_cases IS NOT NULL OR
        new_cases IS NOT NULL OR
        total_deaths IS NOT NULL OR
        reproduction_rate IS NOT NULL OR
        total_tests IS NOT NULL OR
        total_vaccinations IS NOT NULL OR
        excess_mortality IS NOT NULL
    )

    -- 🛑 3. Supprimer les lignes absurdes (trop vides ou invalides)
    AND NOT (
        COALESCE(total_cases, 0) = 0 AND
        COALESCE(new_cases, 0) = 0 AND
        COALESCE(total_deaths, 0) = 0
    )

    -- 🧹 4. Supprimer les doublons exacts
    AND (iso_code, location, date) IN (
        SELECT iso_code, location, date
        FROM (
            SELECT iso_code, location, date,
                   ROW_NUMBER() OVER (PARTITION BY iso_code, location, date ORDER BY date) AS rn
            FROM bronze.covid_raw
        ) AS t
        WHERE t.rn = 1
    );
