from tempfile import NamedTemporaryFile
import webbrowser

from django.core.mail.backends.console import EmailBackend as EmailBackendBase


class BrowserEmailBackend(EmailBackendBase):
    def send_messages(self, email_messages):
        html_messages = []
        for message in email_messages:
            html_messages.extend([
                message
                for message, mime_type in message.alternatives
                if mime_type == 'text/html'
            ])

        file_names = []
        for message in html_messages:
            on_disk = NamedTemporaryFile(delete=False, suffix='.html')
            on_disk.write(message.encode('utf-8'))
            file_names.append(on_disk.name)

        for name in file_names:
            webbrowser.open_new_tab('file://' + name)
