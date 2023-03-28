class Property:
    __table__ = 'housing'
    columns = ["id", "Neighborhood", "TotalBsmtSF", "firstFlrSF", "secondFlrSF", "TotRmsAbvGrd", "SalePrice"]

    def __init__(self, values):
        self.__dict__ = dict(zip(self.columns, values))
