class EmailID():
    def __init__(self, email_id=''):
        self.__email_id=email_id
    
    @property
    def email_id(self):
        return self.__email_id

    def setEmail(self, email_id):
        self.__email_id=email_id

    def resetEmail(self):
        self.__email_id=''

    def __del__(self):
        del self.__email_id