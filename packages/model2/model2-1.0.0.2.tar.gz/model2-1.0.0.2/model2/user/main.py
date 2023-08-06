from db.db_op import userDao

class service():
    def _api_find(self, **params):
        if params:
            name = params.get("name")
            print("name======>>>>>", name)
        user = userDao()
        return user.find_user()