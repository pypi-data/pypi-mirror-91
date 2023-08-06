from ctypes import CDLL, c_char_p
import os
import pwd

def _get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

class UserOkay(object):
    """
        Initialize this object with username and password strings.
        If username and password are None then return None. For security
        reason make to delete the password variable after you instanciate
        this object.
    """
    def __init__(self, username=None, password=None):
        if not username or not password:
            return None

        user = c_char_p()
        passwd = c_char_p()
        user.value = str.encode(username)
        passwd.value = str.encode(password)
        self.username = user
        self.password = passwd

    def login(self):
        """
            Using OpenBSD's auth_userokay(3) from libc BSD Auth api. auth_userokay(3)
            deletes the password from memory for security reasons. Be sure to
            instanciate this class every after self.login() call if you need to login
            again. If calling process is not owned by root return None. root privilege 
            is required by BSD Auth.
        """
        if _get_username() != 'root':
            return None

        sofile = '/usr/lib/libc.so*'
        authstyle = c_char_p()
        authstyle.value = str.encode('passwd')
        authtype = c_char_p()
        authtype.value = str.encode('auth-python')
        auth = CDLL(sofile)
        ret = auth.auth_userokay(self.username, authstyle, authtype, self.password)
        if ret != 0:
            return True
        else:
            return False

    def destroypw(self):
        """ 
            Delete password stored in memory in case self.login() is not called.
        """
        self.password.value = None
