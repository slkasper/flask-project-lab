DROP TABLE IF EXISTS housing;

-- usecols = ["Id", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "TotRmsAbvGrd", "Neighborhood", "SalePrice"]
-- NOT USING THIS!!! CREATING A PANDAS SOLUTION BECAUSE THE 1stFlr and 2ndFlr are causing issues in manual setup

    CREATE TABLE IF NOT EXISTS housing (
    Id serial PRIMARY KEY,
    TotalBsmtSF INTEGER,
    1stFlrSF INTEGER,
    2ndFlrSF INTEGER,
    TotRmsAbvGrd INTEGER,
    Neighborhood VARCHAR(255) NOT NULL,
    price INTEGER,
    --created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS housing_price_index ON housing (price);
