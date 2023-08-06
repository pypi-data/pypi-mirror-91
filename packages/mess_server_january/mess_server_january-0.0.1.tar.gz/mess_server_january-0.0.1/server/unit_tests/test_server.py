"""Unit-тесты сервера"""

import sys
import os
import unittest
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from server import process_client_report


class TestServer(unittest.TestCase):
    """
    В сервере только 1 функция для тестирования
    """
    err_dict = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    ok_dict = {RESPONSE: 200}

    def test_no_action(self):
        """Ошибка, если нет действия"""
        self.assertEqual(process_client_report(
            {TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_wrong_action(self):
        """Ошибка, если неизвестное действие"""
        self.assertEqual(process_client_report(
            {ACTION: 'Wrong', TIME: '1.1', USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_time(self):
        """Ошибка, если  запрос не содержит штампа времени"""
        self.assertEqual(process_client_report(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Guest'}}), self.err_dict)

    def test_no_user(self):
        """Ошибка - нет пользователя"""
        self.assertEqual(process_client_report(
            {ACTION: PRESENCE, TIME: '1.1'}), self.err_dict)

    def test_unknown_user(self):
        """Ошибка - не Guest"""
        self.assertEqual(process_client_report(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest2'}}), self.err_dict)

    def test_ok_check(self):
        """Корректный запрос"""
        self.assertEqual(process_client_report(
            {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}}), self.ok_dict)


if __name__ == '__main__':
    unittest.main()
