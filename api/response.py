# -*- coding: utf-8 -*-  

__all__ = ["ApiError", "ApiSuccess"]

class ApiError:
    @staticmethod
    def check_param(param, type):
        if param is None:
            return ApiError.parameter_miss_error
        if not isinstance(param, type):
            return ApiError.parameter_type_error
        return
    
    parameter_miss_error = {'message':'parameter miss'}, 1001
    parameter_type_error = {'message':'parameter type error'}, 1002
    suppliers_service_errror = {'message':'suppliers service error'}, 1003
    wx_jscode2ses_error = {'message':'wx jscode2ses error'}, 1004

    user_exist_error = {'message':'user exist'}, 2001
    authorization_error = {'message':'Authorization error'}, 2002

class ApiSuccess:
    @staticmethod
    def success(data):
        return {'message':'成功', 'data':data}, 200