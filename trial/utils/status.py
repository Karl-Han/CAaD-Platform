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
INFO_CTRING = -8
INFO_NOT_MATCH = -9
INFO_NOT_EXIST = -10
INFO_LIMIT = -11
INFO_DB_ERR = -12
INFO_UNZIP_ERR = -13
INFO_UNKNOW = -14
INFO_OS_ERR = -15

INFO_STR = {
    INFO_HACKER: 'Hacker?110!',
    INFO_LOGIN: 'Please login!',
    INFO_TIMEOUT: 'Please login!',
    INFO_SAME: '%s with same %s exists!',  # add
    INFO_REFRESH: 'Please refresh!',
    INFO_CTRING: 'Creatting!',
    INFO_NOT_MATCH: '%s not match',
    INFO_CANTB_SAME: '%s can not be same!',
    INFO_CANTB_SELF: '%s can not be yourself!',
    INFO_NOT_EXIST: '%s not exist!',
    INFO_LIMIT: '%s limited %d!',
    INFO_DB_ERR: 'Database error!',
    INFO_UNZIP_ERR: 'Zip error!',
    INFO_UNKNOW: 'Something wrong!',
    INFO_OS_ERR: 'Os error!',
    SUCCESS: 'Success!',
    FAIL: 'Fail!',
    WA_PWD: 'Wrong password!',
    WA_PWD2: 'Wrong name or password!'
}

# models status and types
# user
SU_UNACT = 0
SU_NORMAL = 1
SU_BAN = 2
SU_CANCEL = 3

# course
SC_TBACT = 0
SC_UNSTART = 1
SC_RUNNING = 2
SC_CLOSED = 3

# courseMember
TCM_ADMIN = 0
TCM_TEACHER = 1
TCM_ASISTANT = 2
TCM_STUDENT = 3

# homework
SH_DRAFT = 0
SH_RUNNING = 1
SH_CLOSED = 2

# homeworkStatu
SHS_UD_IT = 1
SHS_DN_IT = 2*SH_RUNNING  # 2
SHS_UD_TO = 3
SHS_DN_TO = 2*SH_CLOSED   # 4

THS_UNCOMMENT = 0
THS_COMMENTED = 1

# docker
SDK_NONE = 0
SDK_CRTING = 1
SDK_FAIL = 2
SDK_RUNNING = 3
SDK_UPDATING = 4
SDK_DELING = 5



