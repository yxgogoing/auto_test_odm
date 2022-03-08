def get_auth():
    from supplier_service.order_service.api.login_service.sp_login_api import spLogin
    login_api_obj = spLogin().send_request()
    return_data = login_api_obj.resp.data
    return return_data.tokenHead + ' ' + return_data.token


auth_token = get_auth()
print(auth_token)
