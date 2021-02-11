SUCCESS = 1
FAIL = 2
WA_PWD = 3
WA_PWD2 = 4

# info
INFO_HACKER = -1
INFO_LOGIN = -2
INFO_TIMEOUT = -3
INFO_SAME = -4
INFO_CANTB_SAME = -5
INFO_CANTB_SELF = -6
INFO_REFRESH = -7
INFO_NOT_MATCH = -8
INFO_NOT_EXIST = -9
INFO_LIMIT = -10
INFO_DB_ERR = -11
INFO_UNZIP_ERR = -12
INFO_UNKNOW = -13

INFO_STR = {
    INFO_HACKER: 'Hacker?110!',
    INFO_LOGIN: 'Please login!',
    INFO_TIMEOUT: 'Please login!',
    INFO_SAME: '%s with same %s exists!',  # add
    INFO_REFRESH: 'Please refresh!',
    INFO_NOT_MATCH: '%s not match',
    INFO_CANTB_SAME: '%s can not be same!',
    INFO_CANTB_SELF: '%s can not be yourself!',
    INFO_NOT_EXIST: '%s not exist!',
    INFO_LIMIT: '%s limited %d!',
    INFO_DB_ERR: 'Database error!',
    INFO_UNZIP_ERR: 'Zip error!',
    INFO_UNKNOW: 'Something wrong!',
    SUCCESS: 'Success!',
    FAIL: 'Fail!',
    WA_PWD: 'Wrong password!',
    WA_PWD2: 'Wrong name or password!'
}

