import logging
import traceback
from typing import List

from moodle_dl.downloader.task import Task
from moodle_dl.notifications.notification_service import NotificationService
from moodle_dl.notifications.telegram.telegram_formater import TelegramFormater as TF
from moodle_dl.notifications.telegram.telegram_shooter import TelegramShooter
from moodle_dl.types import Course


class TelegramService(NotificationService):
    def _is_configured(self) -> bool:
        # Checks if the sending of Telegram messages has been configured.
        try:
            self.config.get_property('telegram')
            return True
        except ValueError:
            logging.debug('Telegram-Notifications not configured, skipping.')
            return False

    def _send_messages(self, messages: List[str]):
        """
        Sends an message
        """
        if not self._is_configured() or messages is None or len(messages) == 0:
            return

        telegram_cfg = self.config.get_property('telegram')

        logging.info('Sending Notification via Telegram...')

        telegram_shooter = TelegramShooter(telegram_cfg['token'], telegram_cfg['chat_id'])

        for message_content in messages:
            try:
                telegram_shooter.send(message_content)
            except BaseException as e:
                logging.error('While sending notification:\n%s', traceback.format_exc(), extra={'exception': e})
                raise e  # to be properly notified via Sentry

    def notify_about_changes_in_moodle(self, changes: List[Course]) -> None:
        """
        Sends out a notification about the downloaded changes.
        @param changes: A list of changed courses with changed files.
        """
        if not self._is_configured():
            return

        messages = TF.create_full_moodle_diff_messages(changes)

        self._send_messages(messages)

    def notify_about_error(self, error_description: str):
        """
        Sends out an error message if configured to do so.
        @param error_description: The error object.
        """
        if not self._is_configured():
            return

        telegram_cfg = self.config.get_property('telegram')

        if not telegram_cfg.get('send_error_msg', True):
            return
        messages = TF.create_full_error_messages(error_description)

        self._send_messages(messages)

    def notify_about_failed_downloads(self, failed_downloads: List[Task]):
        """
        Sends out an message about failed download if configured to send out error messages.
        @param failed_downloads: A list of failed Tasks.
        """
        if not self._is_configured():
            return

        telegram_cfg = self.config.get_property('telegram')

        if not telegram_cfg.get('send_error_msg', True):
            return
        messages = TF.create_full_failed_downloads_messages(failed_downloads)

        self._send_messages(messages)
