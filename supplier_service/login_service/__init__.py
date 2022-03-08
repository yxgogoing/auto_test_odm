# from supplier_service.login_service.api.login_service.user_info import user
#
# def get_auth():
#     from supplier_service.login_service.api.login_service.login_api import Login
#     login_api_obj = Login().send_request()
#     return_data = login_api_obj.resp.data
#     return return_data.tokenHead + ' ' + return_data.token


# from supplier_service.login_service.api.login_service.user_info import user
from supplier_service.login_service.api.login_service.user_info import UserInfo
user = UserInfo(mobile='13430212979', password='chaowen666').login()



# return_data = user.resp.data


# print(user.resp.data)

# def get_auth():
#     from supplier_service.login_service.api.login_service.login_api import Login
#     login_api_obj =
#     return_data = login_api_obj.resp.data
#     return return_data.tokenHead + ' ' + return_data.token
# auth_token = get_auth()  #避免重复调用
# # print(auth_token)