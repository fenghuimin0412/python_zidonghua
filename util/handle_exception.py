from secsmart_autotest.lib.exceptions import SecsmartError


class DuplicateError(SecsmartError):
    """
    资产重复异常
    """
    pass


class AppNotExistError(SecsmartError):
    """
    资产应用不存在异常
    """
    pass


class UserNameOrPassWordError(SecsmartError):
    """
    用户名或密码错误异常
    """
    pass


class AppStatusError(SecsmartError):
    """
    应用状态错误
    """
    pass


class ParamError(SecsmartError):
    """
    接口参数异常
    """
    pass
