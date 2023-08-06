from db.db_op import goodsDao

class service():
    def _api_find(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = goodsDao()
        return user.find_user()

    def _api_add(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = goodsDao()
        user.add()
        return True