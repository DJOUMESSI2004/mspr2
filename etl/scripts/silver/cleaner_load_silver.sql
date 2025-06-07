ALTER TABLE silver.covid_cleaned
RENAME COLUMN location TO country;

DROP FUNCTION IF EXISTS silver.clean_bronze();

CREATE OR REPLACE FUNCTION silver.clean_bronze()
RETURNS void
LANGUAGE plpgsql
AS $$
BEGIN
    /*
        Script de nettoyage des données COVID-19 pour la couche Silver

        Cette fonction nettoie les données brutes de la couche Bronze et les insère dans la table Silver.
        Elle effectue les opérations suivantes :
        1. Filtre les lignes mal formées
        2. Supprime les lignes totalement vides
        3. Supprime les lignes absurdes (trop vides ou invalides)
        4. Supprime les doublons exacts
        5. Supprime les entrées agrégées (OWID_*)
        6. Supprime les anciennes données nettoyées si présentes
        7. Insère les données nettoyées dans silver.covid_cleaned
    */

    RAISE NOTICE '🚿 Nettoyage de la table silver.covid_cleaned...';
    TRUNCATE TABLE silver.covid_cleaned;

    RAISE NOTICE '🧼 Insertion des données nettoyées depuis bronze.covid_raw...';
    INSERT INTO silver.covid_cleaned (
        iso_code, continent, country, date,
        total_cases, new_cases, total_deaths, new_deaths,
        reproduction_rate, icu_patients, hosp_patients,
        total_tests, total_vaccinations,
        population, median_age, aged_65_older, aged_70_older,
        cardiovasc_death_rate, diabetes_prevalence, human_development_index,
        excess_mortality
    )
    SELECT
        iso_code, continent, location, date,
        total_cases, new_cases, total_deaths, new_deaths,
        reproduction_rate, icu_patients, hosp_patients,
        total_tests, total_vaccinations,
        population, median_age, aged_65_older, aged_70_older,
        cardiovasc_death_rate, diabetes_prevalence, human_development_index,
        excess_mortality
    FROM bronze.covid_raw
    WHERE
        iso_code IS NOT NULL
        AND location IS NOT NULL
        AND date IS NOT NULL
        AND iso_code NOT LIKE 'OWID_%'
        AND continent IS NOT NULL

        AND (
            total_cases IS NOT NULL OR
            new_cases IS NOT NULL OR
            total_deaths IS NOT NULL OR
            reproduction_rate IS NOT NULL OR
            total_tests IS NOT NULL OR
            total_vaccinations IS NOT NULL OR
            excess_mortality IS NOT NULL
        )

        AND NOT (
            COALESCE(total_cases, 0) = 0 AND
            COALESCE(new_cases, 0) = 0 AND
            COALESCE(total_deaths, 0) = 0
        )

        AND (iso_code, location, date) IN (
            SELECT iso_code, location, date
            FROM (
                SELECT iso_code, location, date,
                       ROW_NUMBER() OVER (PARTITION BY iso_code, location, date ORDER BY date) AS rn
                FROM bronze.covid_raw
            ) AS t
            WHERE t.rn = 1
        );

    RAISE NOTICE '✅ Données nettoyées insérées avec succès dans silver.covid_cleaned.';
END;
$$;

-- Définir le propriétaire si besoin
ALTER FUNCTION silver.clean_bronze() OWNER TO postgres;



-- utiliser la fonction pour nettoyer les données
SELECT silver.clean_bronze();

