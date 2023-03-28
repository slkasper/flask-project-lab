DROP TABLE IF EXISTS housing;
--  usecols = ["Id", "Neighborhood", "TotalBsmtSF", "1stFlrSF", "2ndFlrSF", "TotRmsAbvGrd",  "SalePrice"]
-- corrected =["id", "Neighborhood", "TotalBsmtSF", "firstFlrSF", "secondFlrSF", "TotRmsAbvGrd", "SalePrice"]

CREATE TABLE IF NOT EXISTS housing (
    id serial PRIMARY KEY,
    Neighborhood VARCHAR(255) NOT NULL,
    TotalBsmtSF INTEGER,
    firstFlrSF INTEGER,
    secondFlrSF INTEGER,
    TotRmsAbvGrd INTEGER,
    saleprice INTEGER
);

CREATE INDEX IF NOT EXISTS housing_price_index ON housing (price);
