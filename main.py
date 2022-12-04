import requests
from bs4 import BeautifulSoup
import lxml
import smtplib
from credential import password,sender,receiver
from email.message import  EmailMessage
import ssl
email_password=password
URL="https://www.amazon.com/Instant-Pot-Duo-Evo-Plus/dp/B07W55DDFB/ref=sr_1_1?qid=1597662463"
smptp_provider="smtp.gmail.com"

headers={
"Accept-Language" : "en-GB,en-US;q=0.9,en;q=0.8",
"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

response=requests.get(url=URL,headers=headers)
content=response.text

soup=BeautifulSoup(content,"lxml")
# print(soup.prettify())

price_finding=soup.find(name="span",class_="a-offscreen")
item_price=float(price_finding.getText().split("$")[1])
product_title=soup.find(name="span",id="productTitle")
product_title=product_title.getText().split(",")[0]
print(item_price)


BUY_PRICE = 300

if item_price< BUY_PRICE:
    message = f"{product_title} item is available today for only:  {item_price} $ \n Item link on Amazon: \n {URL}"

subject="Amazon Track Pricer. Important price update"


em=EmailMessage()
em["From"]=sender
em["To"]=receiver
em["subject"]=subject
em.set_content(message)

context=ssl.create_default_context()
with smtplib.SMTP_SSL(smptp_provider,465,context=context) as smtp:
    smtp.login(sender, email_password)
    smtp.sendmail(sender,receiver,em.as_string())