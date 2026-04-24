"""
Email sender service — wraps aiosmtplib for async email delivery.

Configured via GMAIL_SENDER / GMAIL_APP_PASSWORD env vars.
Falls back to console print in dev/test when no credentials are set.
"""
import os
import asyncio
from email.message import EmailMessage
from typing import Optional

from library.dddpy.shared.logging.logging import Logger


logger = Logger("EmailSender")


def _build_email_message(
    to: str,
    subject: str,
    html_body: str,
    sender: Optional[str] = None,
) -> EmailMessage:
    msg = EmailMessage()
    msg["From"] = sender or os.environ.get("GMAIL_SENDER", "noreply@condo.local")
    msg["To"] = to
    msg["Subject"] = subject
    msg["Content-Type"] = "text/html; charset=utf-8"
    msg.set_content(html_body)
    return msg


async def _send_via_smtp(
    message: EmailMessage,
    host: str = "smtp.gmail.com",
    port: int = 465,
    use_tls: bool = True,
) -> None:
    import aiosmtplib

    sender_email = os.environ.get("GMAIL_SENDER")
    app_password = os.environ.get("GMAIL_APP_PASSWORD")

    if not sender_email or not app_password:
        logger.warning("GMAIL_SENDER / GMAIL_APP_PASSWORD not set — email not sent")
        return

    logger.info(f"Sending email via SMTP: to={message['To']}, subject={message['Subject']}")
    await aiosmtplib.send(
        message,
        hostname=host,
        port=port,
        username=sender_email,
        password=app_password,
        use_tls=use_tls,
    )
    logger.info(f"Email sent: to={message['To']}")


class EmailService:

    # ──────────────────────────────────────────────────────────────────
    # Password reset
    # ──────────────────────────────────────────────────────────────────

    async def send_password_reset_email(
        self,
        to_email: str,
        reset_link: str,
        expiry_hours: int = 1,
    ) -> bool:
        subject = "Restablece tu contraseña — Condo Admin"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
          <h2>Restablece tu contraseña</h2>
          <p>Recibimos una solicitud para restablecer la contraseña de tu cuenta.</p>
          <p>Haz clic en el siguiente enlace para crear una nueva contraseña:</p>
          <p style="margin: 24px 0;">
            <a href="{reset_link}"
               style="background:#2563eb; color:#fff; padding:12px 24px;
                      border-radius:4px; text-decoration:none; font-weight:bold;">
              Restablecer contraseña
            </a>
          </p>
          <p>Este enlace expira en <strong>{expiry_hours} hora{'s' if expiry_hours != 1 else ''}</strong>.</p>
          <p>Si no solicitaste este cambio, ignora este correo. Tu contraseña no será modificada.</p>
          <hr style="margin-top:32px; border:none; border-top:1px solid #eee;">
          <p style="color:#888; font-size:12px;">
            Condo Admin — Capsule Corporation<br>
            Este correo fue enviado a {to_email}
          </p>
        </body>
        </html>
        """
        try:
            msg = _build_email_message(to_email, subject, html)
            await _send_via_smtp(msg)
            return True
        except Exception as e:
            logger.error(f"Failed to send password reset email: {e}")
            # In dev: print to console
            print(f"[DEV EMAIL] To: {to_email}\nSubject: {subject}\nLink: {reset_link}")
            return False

    # ──────────────────────────────────────────────────────────────────
    # Email verification
    # ──────────────────────────────────────────────────────────────────

    async def send_verification_email(
        self,
        to_email: str,
        verify_link: str,
    ) -> bool:
        subject = "Verifica tu correo electrónico — Condo Admin"
        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; padding: 20px;">
          <h2>Verifica tu correo electrónico</h2>
          <p>Gracias por registrarte. Por favor verifica tu correo haciendo clic en el siguiente enlace:</p>
          <p style="margin: 24px 0;">
            <a href="{verify_link}"
               style="background:#16a34a; color:#fff; padding:12px 24px;
                      border-radius:4px; text-decoration:none; font-weight:bold;">
              Verificar mi correo
            </a>
          </p>
          <p>Este enlace expira en <strong>24 horas</strong>.</p>
          <p>Si no creaste una cuenta, ignora este correo.</p>
          <hr style="margin-top:32px; border:none; border-top:1px solid #eee;">
          <p style="color:#888; font-size:12px;">
            Condo Admin — Capsule Corporation<br>
            Este correo fue enviado a {to_email}
          </p>
        </body>
        </html>
        """
        try:
            msg = _build_email_message(to_email, subject, html)
            await _send_via_smtp(msg)
            return True
        except Exception as e:
            logger.error(f"Failed to send verification email: {e}")
            print(f"[DEV EMAIL] To: {to_email}\nSubject: {subject}\nLink: {verify_link}")
            return False

    # ──────────────────────────────────────────────────────────────────
    # Sync wrapper (for use in sync context)
    # ──────────────────────────────────────────────────────────────────

    def send_password_reset_email_sync(self, to_email: str, reset_link: str, expiry_hours: int = 1) -> bool:
        """Sync wrapper — runs async send in a new event loop."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(
            self.send_password_reset_email(to_email, reset_link, expiry_hours)
        )

    def send_verification_email_sync(self, to_email: str, verify_link: str) -> bool:
        """Sync wrapper — runs async send in a new event loop."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(
            self.send_verification_email(to_email, verify_link)
        )
