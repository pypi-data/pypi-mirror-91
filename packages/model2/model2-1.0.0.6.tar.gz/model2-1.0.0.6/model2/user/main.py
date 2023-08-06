from db.db_op import userDao

from model2.common_utils import resp_result


class service():
    def _api_get(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = userDao()
        return resp_result(data=user.find())

    def _api_post(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))

        user = userDao()
        user.add()
        return resp_result()