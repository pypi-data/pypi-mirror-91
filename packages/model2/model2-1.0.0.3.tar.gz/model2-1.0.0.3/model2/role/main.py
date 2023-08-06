from db.db_op import roleDao

class service():
    def _api_find(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = roleDao()
        return user.find_user()

    def _api_add(self, **params):
        if params:
            for i in params:
                print("find params===>", i)

        user = roleDao()
        user.add()
        return True