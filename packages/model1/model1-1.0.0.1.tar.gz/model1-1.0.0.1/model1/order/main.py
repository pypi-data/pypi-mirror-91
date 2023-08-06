from db.db_op import orderDao

class service():
    def _api_find(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = orderDao()
        return user.find_user()

    def _api_add(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = orderDao()
        user.add()
        return True