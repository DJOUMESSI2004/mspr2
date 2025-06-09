-- ==============================================
-- Fonction pour créer les index sur les dimensions et la table de faits
-- ==============================================
DROP FUNCTION IF EXISTS gold.create_indexes();

CREATE OR REPLACE FUNCTION gold.create_indexes()
RETURNS void AS $$
BEGIN
    -- Index pour dim_country
    CREATE INDEX IF NOT EXISTS idx_dim_country_code_name ON gold.dim_country(iso_code, country);

    -- Index pour dim_date
    CREATE INDEX IF NOT EXISTS idx_dim_date_full_date ON gold.dim_date(full_date);

    -- Index pour dim_economic
    CREATE INDEX IF NOT EXISTS idx_dim_economic_country_id ON gold.dim_economic(country_id);

    -- Index pour dim_health
    CREATE INDEX IF NOT EXISTS idx_dim_health_country_id ON gold.dim_health(country_id);

    -- Index pour dim_vaccination
    CREATE INDEX IF NOT EXISTS idx_dim_vaccination_country_id ON gold.dim_vaccination(country_id);

    -- Index pour la table de faits pour lecture future
    CREATE INDEX IF NOT EXISTS idx_fact_metrics_country_date ON gold.fact_covid_metrics(country_id, date_id);

    RAISE NOTICE '✅ Index créés avec succès.';
END;
$$ LANGUAGE plpgsql;