from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from pydantic import BaseModel, EmailStr

from typing import List

# class EmailSchema(BaseModel):
#     email: List[EmailStr]

conf = ConnectionConfig(
    MAIL_USERNAME="AazamCodes",
    MAIL_PASSWORD="mmqt haqf tluz lnxc",
    MAIL_FROM="aazam.codes@gmail.com",
    MAIL_PORT=465,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Aazam Mansuri",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

async def sendMail(emails: List[str]):
    message = MessageSchema(
        subject="Sending mail through fastapi",
        recipients=emails,
        body="<p>Thanks for using Fastapi-mail</p>",
        subtype=MessageType.html,
    )
    await FastMail(conf).send_message(message)
    print({"message": "email has been sent"})