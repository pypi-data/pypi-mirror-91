from typing import List, Type
from io import StringIO

from django.test import SimpleTestCase, override_settings  # type: ignore

import sms
from sms import send_sms
from sms.backends import dummy, locmem
from sms.backends.base import BaseSmsBackend
from sms.message import Message


class SmsTests(SimpleTestCase):

    def test_dummy_backend(self) -> None:
        """
        Make sure that dummy backends return correct number of sent text
        messages.
        """
        connection = dummy.SmsBackend()
        message = Message()
        self.assertEqual(
            connection.send_messages([message, message, message]),
            3
        )

    def test_backend_arg(self) -> None:
        """Test backend argument of mail.get_connection()."""
        self.assertIsInstance(
            sms.get_connection('sms.backends.dummy.SmsBackend'),
            dummy.SmsBackend
        )

    def test_custom_backend(self) -> None:
        """Test cutoms backend defined in this suite."""
        connection = sms.get_connection('tests.custombackend.SmsBackend')
        self.assertTrue(hasattr(connection, 'test_outbox'))
        message = Message('Content', '0600000000', ['0600000000'])
        connection.send_messages([message])  # type: ignore
        self.assertEqual(len(connection.test_outbox), 1)  # type: ignore

    @override_settings(SMS_BACKEND='sms.backends.locmem.SmsBackend')
    def test_send_sms(self) -> None:
        """
        Test send_sms with the to specified as a string to remain compatibility
        with django-sms<=0.0.4.
        """
        send_sms('Content', '0600000000', '0600000000')
        self.assertEqual(len(sms.outbox), 1)  # type: ignore
        self.assertIsInstance(sms.outbox[0].to, list)  # type: ignore


class LocmemBackendTests(SimpleTestCase):
    sms_backend: str = 'sms.backends.locmem.SmsBackend'

    def flush_mailbox(self) -> None:
        sms.outbox = []  # type: ignore

    def tearDown(self) -> None:
        super().tearDown()
        self.flush_mailbox()

    def test_locmem_shared_messages(self) -> None:
        """
        Make sure that the locmem backend populates the outbox.
        """
        connections: List[Type[BaseSmsBackend]] = [
            locmem.SmsBackend(),  # type: ignore
            locmem.SmsBackend()  # type: ignore
        ]
        message = Message('Content', '0600000000', ['0600000000'])
        for connection in connections:
            connection.send_messages([message])  # type: ignore
        self.assertEqual(len(sms.outbox), 2)  # type: ignore


class ConsoleBackendTests(SimpleTestCase):
    sms_backend: str = 'sms.backends.console.SmsBackend'

    def test_console_stream_kwarg(self) -> None:
        """
        The console backend can be pointed at an arbitrary stream.
        """
        stream = StringIO()
        connection = sms.get_connection(
            'sms.backends.console.SmsBackend',
            stream=stream
        )
        message = Message('Content', '0600000000', ['0600000000'])
        connection.send_messages([message])  # type: ignore
        messages = stream.getvalue().split('\n' + ('-' * 79) + '\n')
        self.assertIn('from: ', messages[0])
