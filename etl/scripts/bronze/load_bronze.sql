/*
 * Script to load data into the Bronze layer of the COVID-19 data warehouse.
 * This script truncates the existing table and loads new data from a CSV file.
 * Ensure that the CSV file path is correctly set before running this script.
 */


DO $$
DECLARE
    start_time TIMESTAMP;
    end_time TIMESTAMP;
BEGIN
    RAISE NOTICE '================================================';
    RAISE NOTICE '💾 DÉMARRAGE : Chargement Bronze Layer';
    RAISE NOTICE '================================================';

    start_time := clock_timestamp();
    
    -- Étape 1 : Vider la table
    RAISE NOTICE '🧹 Troncature de la table : bronze.covid_data';
    TRUNCATE TABLE bronze.covid_data;

    -- Étape 2 : Chargement CSV
    RAISE NOTICE '📥 Chargement du fichier CSV vers la table bronze.covid_data';

    -- ⚠️ Remplace ce chemin par le chemin réel depuis le serveur PostgreSQL
    COPY bronze.covid_data
    FROM 'C:\Users\wamba\Desktop\python\mspr2\etl\datasets\model_covid19_data.csv'
    WITH (
        FORMAT csv,
        HEADER true,
        DELIMITER ',',
        NULL '',
        ENCODING 'UTF8'
    );

    end_time := clock_timestamp();
    RAISE NOTICE '✅ Chargement terminé en % secondes.', EXTRACT(SECOND FROM end_time - start_time);

EXCEPTION
    WHEN OTHERS THEN
        RAISE NOTICE '❌ ERREUR pendant le chargement Bronze Layer';
        RAISE NOTICE 'Fichier CSV chargé avec succès, CODE : %', SQLSTATE;
        RAISE NOTICE 'Message : %', SQLERRM;
END $$;

/*
Si le dataset n'est pas sur un serveur PostgreSQL, Utilisez la cmd suivante dans votre terminal pour charger le fichier CSV :
psql -U <username> -d model_covid19_data -c "\copy bronze.covid_data FROM 'C:\Users\wamba\Desktop\python\mspr2\etl\datasets\model_covid19_data.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', NULL '', ENCODING 'UTF8')"
Rassurez-vous de remplacer `<username>` par votre nom d'utilisateur PostgreSQL.
*/
