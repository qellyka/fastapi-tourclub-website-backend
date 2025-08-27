from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

from core.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER="templates/email",
)


async def send_email(subject: str, recipients: list[str], body: str):
    message = MessageSchema(
        subject=subject,
        recipients=recipients,
        body=body,
        subtype="plain",
    )
    fm = FastMail(conf)
    await fm.send_message(message)


async def send_verification_email(email: str, verify_link: str):
    message = MessageSchema(
        subject="Подтверждение вашей почты",
        recipients=[email],
        template_body={"verify_link": verify_link},
        subtype="html",
    )
    fm = FastMail(conf)
    await fm.send_message(message, template_name="verify_email_updated.html")
