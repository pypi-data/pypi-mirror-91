from db.db_op import userDao

class service():
    def _api_find(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = userDao()
        return user.find()

    def _api_add(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = userDao()
        user.add()
        return True