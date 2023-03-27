from api.models.property import Property

#columns = ["id", "Neighborhood", "TotalBsmtSF", "firstFlrSF", "secondFlrSF", "TotRmsAbvGrd", "SalePrice"]

def test_init_property():
    property = Property(['1', 'My Neighborhood', 500, 500,
            450, 6, 350_000])
    assert property.SalePrice == 350_000