-- Supprimer ancienne version si elle existe
DROP FUNCTION IF EXISTS silver.final_clean_bronze();
DROP TABLE IF EXISTS silver.covid_cleaned_final;

-- Créer la version finale nettoyée et complétée
CREATE OR REPLACE FUNCTION silver.final_clean_bronze()
RETURNS void AS $$
BEGIN
 /*
        ==============================================
        FONCTION : silver.final_clean_bronze()
        ==============================================
        Objectif :
        - Générer une version propre et exploitable des données COVID-19
        - Préparer un jeu de données pour l’apprentissage automatique
        - Nettoyer la couche Silver et créer la table silver.covid_cleaned_final

        Raisons des choix :
        ---------------------
        1. Les colonnes marquées "❌ à exclure" ont été supprimées car :
           - Elles contenaient trop de valeurs nulles
           - Et leur importance pour la prédiction était faible
           → Cela évite du bruit et simplifie l’apprentissage

        2. Les colonnes marquées "⚠️ utile mais taux NULL élevé" ont été conservées, 
           mais leurs valeurs NULL ont été **remplacées artificiellement** avec des 
           valeurs aléatoires cohérentes (bornes réalistes) pour :
           - Éviter la perte d’information importante
           - Pouvoir continuer l’entraînement du modèle même sans vraie complétion
           Ce choix est justifié ici car c’est un **projet d’expérimentation pédagogique**
           et non une base de données utilisée en production réelle.

        3. Les colonnes "utiles" et "neutres" sont conservées telles quelles.

         Ce nettoyage permet de produire une base prête à l’usage pour du ML supervisé
           sans lignes manquantes ni colonnes inutiles.
    */

    -- Création d’une table finale à partir de silver.covid_cleaned
    CREATE TABLE silver.covid_cleaned_final AS
    SELECT
        -- Métadonnées essentielles
        iso_code,
        continent,
        country,
        date,

        -- ✅ Colonnes utiles
        total_cases,
        new_cases,
        total_deaths,
        new_deaths,
        total_tests,
        positive_rate,
        tests_per_case,
        population,
        median_age,
        aged_65_older,
        aged_70_older,
        gdp_per_capita,
        human_development_index,
        life_expectancy,
        excess_mortality,

        -- ⚠️ Colonnes utiles mais avec beaucoup de NULL —> complétion artificielle
        COALESCE(reproduction_rate, ROUND((RANDOM() * 0.4 + 0.8)::numeric, 2)) AS reproduction_rate,
        COALESCE(icu_patients, ROUND((RANDOM() * 50)::numeric)) AS icu_patients,
        COALESCE(hosp_patients, ROUND((RANDOM() * 100)::numeric)) AS hosp_patients,
        COALESCE(new_tests, ROUND((RANDOM() * 10000)::numeric)) AS new_tests,
        COALESCE(total_vaccinations, ROUND((RANDOM() * 1000000)::numeric)) AS total_vaccinations,
        COALESCE(people_vaccinated, ROUND((RANDOM() * 800000)::numeric)) AS people_vaccinated,
        COALESCE(people_fully_vaccinated, ROUND((RANDOM() * 700000)::numeric)) AS people_fully_vaccinated,
        COALESCE(total_boosters, ROUND((RANDOM() * 400000)::numeric)) AS total_boosters,
        COALESCE(stringency_index, ROUND((RANDOM() * 100)::numeric, 2)) AS stringency_index,

        -- 🔍 Colonnes neutres gardées sans modification
        hospital_beds_per_thousand,
        extreme_poverty,
        new_vaccinations_smoothed,
        new_vaccinations_smoothed_per_million,
        new_people_vaccinated_smoothed,
        new_people_vaccinated_smoothed_per_hundred,
        total_cases_per_million,
        new_cases_per_million,
        total_deaths_per_million,
        new_deaths_per_million

    FROM silver.covid_cleaned;

    RAISE NOTICE '✅ Table finale silver.covid_cleaned_final créée avec succès.';
END;
$$ LANGUAGE plpgsql;

-- Exécuter pour créer la table nettoyée finale
SELECT silver.final_clean_bronze();


-- checking de la nouvelle table
SELECT * FROM silver.covid_cleaned_final LIMIT 10;