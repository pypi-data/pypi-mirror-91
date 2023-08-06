from pytempmail.emailid import EmailID
from pytempmail.inbox import Inbox

class TempMail():
    def __init__(self):
        self.__email_id=EmailID()
        self.__inbox=Inbox()
    
    @property
    def email_id(self):
        return self.__email_id.email_id

    @property
    def inbox_size(self):
        return self.__inbox.getInboxSize
    
    def getMail(self, msg_num):
        try:
            mail=self.__inbox.getMail(msg_num)
            return mail
        except IndexError:
            raise IndexError

    def addMail(self, mail):
        self.__inbox.putMail(mail)

    def ext(self, l):
        self.__inbox.ext(l)

    @property
    def getInbox(self):
        return self.__inbox.getMail()
    
    def setEmailID(self, email_id):
        self.__email_id.setEmail(email_id)

    def resetInbox(self):
        self.__inbox.resetInbox()

    def resetEmail(self):
        self.__email_id.resetEmail()

    def __del__(self):
        del self.__email_id
        del self.__inbox