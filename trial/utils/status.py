SUCCESS = 1
FAIL = 2
WA_PWD = 3
WA_PWD2 = 4

# info
INFO_HACKER = -1
INFO_LOGIN = -2
INFO_TIMEOUT = -3
INFO_SAME_NAME = -4
INFO_REFRESH = -5
INFO_NOT_MATCH = -6
INFO_CANTB_SAME = -7
INFO_CANTB_YS = -8
INFO_DB_ERR = -9
INFO_UNKNOW = -10

INFO_STR = {
    INFO_HACKER: 'Hacker?110!',
    INFO_LOGIN: 'Please login!',
    INFO_TIMEOUT: 'Please login!',
    INFO_SAME_NAME: ' with same name exists!',  # add front
    INFO_REFRESH: 'Please refresh!',
    INFO_NOT_MATCH: ' not match',  # add
    INFO_CANTB_SAME: ' can not be same!',  # add,
    INFO_CANTB_YS: ' can not be yourself',  # add,
    INFO_DB_ERR: 'Database error!',
    INFO_UNKNOW: 'Something wrong!',
    SUCCESS: 'Success!',
    FAIL: 'Fail!',
    WA_PWD: 'Wrong password!',
    WA_PWD2: 'Wrong name or password!'
}

