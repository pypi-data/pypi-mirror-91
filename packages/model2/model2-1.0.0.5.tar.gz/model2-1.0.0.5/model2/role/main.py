from db.db_op import roleDao

from model2.common_utils import resp_result


class service(object):
    def _api_find(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))
                if(i == "request"):
                    print("request get name ===>>>>>", params[i].args.get("name"))

        user = roleDao()
        return resp_result(data=user.find())

    def _api_add(self, **params):
        if params:
            for i in params:
                print("find params===>key={0},value={1}".format(i, params[i]))
                if (i == "request"):
                    print("request get name ===>>>>>", params[i].form.get("name"))

        user = roleDao()
        user.add()
        return resp_result()

if __name__ == '__main__':
    ser = service()
    print(ser._api_find())
    print(ser._api_add())