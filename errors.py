# -*- coding:utf-8 -*-
# author = 'paul'
# date = '2015-01-23 10:57:51'


class Error(Exception):
    since = '0.0.1'

    def __init__(self, error_code):
        self.error_code = error_code


class UnknownError(Error):
    def __init__(self):
        super(UnknownError, self).__init__(1)
        self.error_message = u'未知错误'


class ParamInvalidError(Error):
    def __init__(self, invalid_param=None):
        super(ParamInvalidError, self).__init__(2)
        if invalid_param is not None:
            self.error_message = 'Invalid param: %s' % invalid_param
        else:
            self.error_message = u'无效参数'


class InvalidSignature(Error):
    def __init__(self):
        super(InvalidSignature, self).__init__(3)
        self.error_message = u'无效签名'


class InvalidOperation(Error):
    def __init__(self, message=None):
        super(InvalidOperation, self).__init__(4)
        self.error_message = u'无效操作' if not message else message


class NotFoundError(Error):
    def __init__(self):
        super(NotFoundError, self).__init__(5)
        self.error_message = "No data found"


class AuthExpire(Error):
    def __init__(self):
        super(AuthExpire, self).__init__(10)
        self.error_message = u'授权信息超时，请重新登录'


class PermissionDeny(Error):
    def __init__(self):
        super(PermissionDeny, self).__init__(20)
        self.error_message = u'操作非法'


class OldVersion(Error):
    def __init__(self):
        super(OldVersion, self).__init__(30)
        self.error_message = u'客户端版本过旧，请及时更新'


class VerifyCodeInvalid(Error):
    def __init__(self):
        super(VerifyCodeInvalid, self).__init__(40)
        self.error_message = u'验证码非法'


class NotHaveEnoughMoney(Error):
    def __init__(self):
        super(NotHaveEnoughMoney, self).__init__(50)
        self.error_message = u'账户余额不足'


class AccountNotExist(Error):
    def __init__(self):
        super(AccountNotExist, self).__init__(60)
        self.error_message = u'账户不存在'

class AccountLocked(Error):
    def __init__(self):
        super(AccountLocked, self).__init__(61)
        self.error_message = u'账户已被锁定'

class AccountExist(Error):
    def __init__(self):
        super(AccountExist, self).__init__(70)
        self.error_message = u'账户已注册'

class CreateError(Error):
    def __init__(self):
        super(CreateError, self).__init__(100)
        self.error_message = u'添加数据失败'

class InvalidItemPrice(Error):
    def __init__(self):
        super(InvalidItemPrice, self).__init__(101)
        self.error_message = u'无效商品价格'

class WithdrawMoneyTooLow(Error):
    def __init__(self, min_money):
        super(WithdrawMoneyTooLow, self).__init__(102)
        self.error_message = u'提现金额不能少于%d元' % (min_money / 100)

class WithdrawCountOverflow(Error):
    def __init__(self):
        super(WithdrawCountOverflow, self).__init__(103)
        self.error_message = u'每日提现次数超过限制'

class ShopNameInvalid(Error):
    def __init__(self, message=None):
        super(ShopNameInvalid, self).__init__(104)
        self.error_message = u'无效店铺名称' if not message else message

class invalid_master_key(Error):
    def __init__(self):
        super(invalid_master_key, self).__init__('10000')
        self.error_message = "Invalid master key"

class duplicate_error(Error):
    def __init__(self, key, value):
        super(duplicate_error, self).__init__('11000')
        self.error_message = "Duplicate key %s value %s"%(key, value)

class invalid_app_id_or_app_secret(Error):
    def __init__(self):
        super(invalid_app_id_or_app_secret, self).__init__('12000')
        self.error_message = "Invalid app ID or app secret"

class invalid_access_token(Error):
    def __init__(self):
        super(invalid_access_token, self).__init__('13000')
        self.error_message = "Invalid access token"