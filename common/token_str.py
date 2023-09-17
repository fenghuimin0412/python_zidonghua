from business.login.login_bus import LoginBusiness

token_sec = LoginBusiness().login(用户名="secadmin", 密码="Admin!123456").headers['Authorization']
token_sys = LoginBusiness().login(用户名="sysadmin", 密码="Admin!123456").headers['Authorization']
# print(token)


# def login(self, **kwargs):
#     login = Login()
#     if "用户名" in kwargs.keys():
#         login.username = kwargs["用户名"]
#     if "密码" in kwargs.keys():
#         PUBLIC_KEY = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAk8fEwBXx7pNAx7L6eUMwLDb7g2d04cCFakT07GRBnwBZGftkImKh86tRJHeIserYkvXEmQN3oPmr2J/r6Z7fco5yO5WS02sufOJ6PmAkAvE1efXZNZ042S41HNwz0CyTLcimJdSwR5PmOoDd88NZYmTiHorkW6bFzNLaIiMQUm+wtbDiDtObo/IvIGMRBZK9QhVu+8gl6UOkg+zRQtnnpOV6FoDGDCXLIdMgHZBN2dBSNpbsuFH4yebzC1Bd+podCcOMPBEub4QlIwWnfhRutdvZfXbOGX7fa1i4E95vJRP2CSE7h+3oW3paoRoqkqNlcQZQtYPzxY7W3Fvt1cl2kwIDAQAB"
#         password = gen_body(kwargs["密码"], PUBLIC_KEY)
#         login.password = password
#     # 返回的是respones
#     login_res = LoginInterface(login).response
# # 将Authorization存储在conf.ini中
# Authorization = login_res.headers['Authorization']
# ConfWrite().writeToINI(Authorization)