#!/usr/bin/env python
# -*- coding: utf-8 -*-

# diemlib/mailhandler.py

"""
   These are specific functions to be used for handling mail
   This one uses sendgrid
"""


from sendgrid.helpers.mail import (
    Mail,
    Attachment,
    FileContent,
    FileName,
    FileType,
    Disposition,
    ContentId,
)
from sendgrid import SendGridAPIClient
import base64
from diemlib.main import *
from diemlib.util import get_random_string
import diemlib.config as config
import mimetypes


class mailhandler(object):
    def __init__(self):

        self.sg = SendGridAPIClient(config.api_key)

    def mail(self, **kwargs):

        message = Mail(
            from_email=kwargs.get("sender"),
            to_emails=kwargs.get("to"),
            subject=kwargs.get("subject"),
            html_content=kwargs.get("content"),
        )

        if "attachment" in kwargs:

            attachment_name = kwargs.get("attachment")

            if "attachment_data" in kwargs:
                data = kwargs.get("attachment_data")
                encoded = base64.b64encode(data).decode()

            mail_attachment = Attachment()
            mail_attachment.file_content = FileContent(encoded)
            mail_attachment.file_name = FileName(attachment_name)
            mail_attachment.disposition = Disposition("attachment")

            # create the content_id based on a random string
            content_id = get_random_string(8)
            mail_attachment.content_id = ContentId(content_id)

            mime_type = mimetypes.guess_type(attachment_name)

            mail_attachment.file_type = FileType(mime_type[0])

            message.attachment = mail_attachment

        self.sendMail(message)

    def sendMail(self, message):
        try:

            response = self.sg.send(message)
            out(f"mail successfully sent - response status: {response.status_code}")

        except Exception as e:
            error(e)