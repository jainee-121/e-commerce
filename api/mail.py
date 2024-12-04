
from fastapi import BackgroundTasks, FastAPI
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import BaseModel, EmailStr, SecretStr
from starlette.responses import JSONResponse



conf = ConnectionConfig(
    MAIL_USERNAME ="jainee1215.ahm@gmail.com",
    MAIL_PASSWORD = SecretStr("xjwv pubi guak bsey"),
    MAIL_FROM = "jainee1215.ahm@gmail.com",
    MAIL_PORT = 465,
    MAIL_SERVER = "smtp.gmail.com",
    MAIL_STARTTLS = False,
    MAIL_SSL_TLS = True,
    USE_CREDENTIALS = True,
    VALIDATE_CERTS = True
)


html = """
<p>You have succesfully registered</p> 
"""

async def simple_send(email: str) -> JSONResponse:

    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=[email],
        body=html,
        subtype=MessageType.html)

    fm = FastMail(conf)
    await fm.send_message(message)
    return JSONResponse(status_code=200, content={"message": "email has been sent"})