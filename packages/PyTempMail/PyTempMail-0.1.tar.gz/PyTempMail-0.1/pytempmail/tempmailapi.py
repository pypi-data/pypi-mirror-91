from selenium.common.exceptions import NoSuchElementException
from pytempmail.tempmail import TempMail
import pytempmail.consts as consts
from time import sleep
from pytempmail.mail import Mail
import logging
from threading import Thread
from pytempmail.timer import Clock
from pytempmail.excep import TimerException, MailNumOutOfRange

class TempMailAPI():
    __URL=consts.URL

    def __open(self):
        self.__driver.get(TempMailAPI.__URL)
        logging.info("opened site")
        self.__getEmail(self.timeout, self.sleep_time)
        self.getInbox()

    @property
    def email_id(self):
        return self.__temp_mail.email_id

    def getSS(self, ss_path):
        logging.info("taking screenshot")
        self.__driver.save_screenshot(ss_path)
        logging.info("took screenshot")

    @staticmethod
    def _find_links(driver, starts_with=''):
        elems = driver.find_elements_by_tag_name('a')
        links=[]
        for elem in elems:
            if (starts_with!=''):
                try:
                    if (elem.get_attribute("href").startswith(starts_with)):
                        links.append(elem.get_attribute("href"))
                except AttributeError:
                    pass
            else:
                try:
                    links.append(elem.get_attribute("href"))
                except AttributeError:
                    pass
        links=list(set(links))
        return links

    @staticmethod
    def _find_by_xpath(driver, xpath):
        try:
            elem=driver.find_element_by_xpath(xpath)
            return elem
        except NoSuchElementException:
            raise NoSuchElementException

    def checkMail(self, mail_num=-1):
        try:
            self.__driver.get(self.__temp_mail.getMail(mail_num))
            mail=self.__parseMail()
            self.__driver.back()
            return mail
        except IndexError:
            raise MailNumOutOfRange("Mail Number out of range")
    
    @staticmethod
    def _is_blank(s):
        out=bool(s and s.strip())
        return (not out)

    def __getEmail(self, timeout, sleep_time, starts_with="Loading"):
        logging.info("Getting email")
        logging.info("staring timer process")
        clock=Clock()
        clock_thread=Thread(target=clock.run, args=(timeout,))
        clock_thread.start()
        email=TempMailAPI._find_by_xpath(self.__driver, consts.email_selector) .get_attribute('value')
        while (email.startswith(starts_with) or email.startswith("Loading") or TempMailAPI._is_blank(email)):
            if (clock_thread.is_alive()==False):
                logging.info("Could not finish in given timeout")
                raise TimerException("Couldn't finish task in given timeout")
            logging.info("dont found email")
            sleep(sleep_time)
            logging.info("trying again for email")
            email=TempMailAPI._find_by_xpath(self.__driver, consts.email_selector).get_attribute('value')
        logging.debug(email)
        logging.info("Found email")
        logging.info("closing timer process")
        clock.terminate()
        logging.info("associating email with object")
        self.__temp_mail.setEmailID(email)
        logging.info("associated email with object")

    def __init__(self, driver_obj, session=0, timeout=20, sleep_time=1):
        logging.info("creating api object")
        self.__driver=driver_obj
        self.timeout=timeout
        self.sleep_time=sleep_time
        if (session != 0):
            self.__driver.session_id=session
        self.__temp_mail=TempMail()
        self.__open()
        logging.info("Created api object")

    def refresh(self):
        TempMailAPI._find_by_xpath(self.__driver, consts.refresh_button_selector).click()
        self.getInbox()
    
    def delEmail(self):
        TempMailAPI._find_by_xpath(self.__driver, consts.delete_email).click()
        self.__temp_mail.resetInbox()
        self.__getEmail(self.timeout, self.sleep_time, starts_with=self.__temp_mail.email_id)
        self.__temp_mail.resetEmail()

    @property
    def session_id(self):
        return (self.__driver.session_id)

    @property
    def inbox_size(self):
        return (self.__temp_mail.inbox_size)

    def getInbox(self):
        mail_links=TempMailAPI._find_links(self.__driver, 'https://temp-mail.org/en/view')
        self.__temp_mail.ext(mail_links)

    def __parseMail(self):
        sender_name=TempMailAPI._find_by_xpath(self.__driver, consts.sender_name).get_attribute("textContent")
        date_time=TempMailAPI._find_by_xpath(self.__driver, consts.mail_date_time).get_attribute("textContent")
        sender_email=TempMailAPI._find_by_xpath(self.__driver, consts.sender_email).get_attribute("textContent")
        subject=TempMailAPI._find_by_xpath(self.__driver, consts.mail_subject).get_attribute("textContent")
        text=TempMailAPI._find_by_xpath(self.__driver, consts.mail_text).get_attribute("textContent")
        #attach=TempMailAPI._find_by_xpath(self.__driver, consts.mail_attach).click()
        return Mail(sender_email, sender_name, date_time, subject, text)
    
    def __del__(self):
        del self.__driver
        del self.__temp_mail