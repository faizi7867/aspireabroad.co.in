# mbbs_visa/resend_backend.py
from typing import Iterable
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail import EmailMessage
from django.conf import settings
import resend

class ResendBackend(BaseEmailBackend):
    """
    Django EmailBackend that delivers emails via Resend API.
    Expects:
      - settings.RESEND_API_KEY
      - settings.DEFAULT_FROM_EMAIL (optional; falls back to onboarding@resend.dev)
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        api_key = getattr(settings, "RESEND_API_KEY", None)
        if not api_key:
            raise ValueError("RESEND_API_KEY is not set in settings.")
        resend.api_key = api_key
        self.default_from = getattr(settings, "DEFAULT_FROM_EMAIL", "onboarding@resend.dev")

    def send_messages(self, email_messages: Iterable[EmailMessage]):
        if not email_messages:
            return 0

        sent_count = 0
        for msg in email_messages:
            try:
                from_email = msg.from_email or self.default_from
                # Compose HTML/text: Resend accepts either html or text; prefer html if body looks HTML-ish
                html = None
                text = None
                if getattr(msg, "content_subtype", "") == "html":
                    html = msg.body
                else:
                    # If there are alternatives, pick the html alternative if present
                    alt_html = next((b for (b, ct) in getattr(msg, "alternatives", []) if ct == "text/html"), None)
                    if alt_html:
                        html = alt_html
                        text = msg.body or None
                    else:
                        text = msg.body

                # Resend expects a list of recipients
                to_list = list(msg.to or [])
                cc_list = list(msg.cc or [])
                bcc_list = list(msg.bcc or [])
                all_recipients = to_list + cc_list + bcc_list

                payload = {
                    "from": from_email,
                    "to": all_recipients,
                    "subject": msg.subject or "",
                }
                if html:
                    payload["html"] = html
                if text and not html:
                    payload["text"] = text

                # Attachments (optional): convert Django attachments to Resend format
                # Each attachment is a (filename, content, mimetype)
                attachments = []
                for att in getattr(msg, "attachments", []):
                    if isinstance(att, tuple) and len(att) in (2, 3):
                        filename = att[0]
                        content = att[1]
                        mimetype = att[2] if len(att) == 3 else "application/octet-stream"
                        # Resend expects base64 content
                        import base64
                        b64 = base64.b64encode(content if isinstance(content, (bytes, bytearray)) else str(content).encode()).decode()
                        attachments.append({
                            "filename": filename,
                            "content": b64,
                            "path": None,
                            "type": mimetype,
                        })
                if attachments:
                    payload["attachments"] = attachments

                resend.Emails.send(payload)
                sent_count += 1
            except Exception:
                if not self.fail_silently:
                    raise
                # else skip and continue
        return sent_count
