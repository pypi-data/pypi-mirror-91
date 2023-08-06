class Mail():
    def __init__(self, from_id, sender_name, date_time, subject, msg, attach=0):
        self.__from_id=from_id
        self.__msg=msg
        self.__attach=attach
        self.__sender_name=sender_name
        self.__date_time=date_time
        self.__subject=subject

    @property
    def from_id(self):
        return self.__from_id

    @property
    def msg(self):
        return self.__msg

    @property
    def sender_name(self):
        return self.__sender_name
    
    @property
    def date_time(self):
        return self.__date_time

    @property
    def subject(self):
        return self.__subject

    def _checkAttachment(self):
        if (self.__attach==0):
            return False

    @property
    def attachment(self):
        return self.__attach

    def __del__(self):
        del self.__from_id
        del self.__msg
        del self.__attach