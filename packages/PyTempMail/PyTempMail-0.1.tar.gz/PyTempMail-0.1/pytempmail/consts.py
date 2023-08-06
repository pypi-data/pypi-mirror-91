from os import getcwd, name

URL="https://temp-mail.org/en/"

delete_email='//*[@id="click-to-delete"]'
email_selector='//*[@id="mail"]'
refresh_button_selector='//*[@id="click-to-refresh"]'
sender_name='/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/p[1]'
mail_date_time='/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div[2]/div[2]'
sender_email='/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[2]/div[1]/div[1]/p[2]'
mail_subject='/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[2]/div[2]/h4'
mail_text='/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[2]/div[3]/div'
mail_attach='/html/body/main/div[1]/div/div[3]/div[2]/div/div[1]/div/div[1]/div[2]/div/div/ul/li[2]/a/img'