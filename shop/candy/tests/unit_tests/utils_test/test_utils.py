from candy.utils import Utils
from unittest.mock import MagicMock, patch, call
from django.test import SimpleTestCase
from datetime import datetime
from freezegun import freeze_time


class UtilsTestCase(SimpleTestCase):

    def test_session_data(self):
        order_id_mock = MagicMock()
        request_mock = MagicMock(session={'order_id': ''})

        Utils.session_data(request_mock, order_id_mock)

        self.assertEqual(request_mock.session['order_id'], order_id_mock)

    @freeze_time("2022-01-01")
    @patch('candy.utils.datetime.now')
    def test_check_time_allow(self, datetime_now_patch):

        time_now_mock = MagicMock()
        datetime_now_patch.return_value = time_now_mock
        time_ten_hour_mock = MagicMock()
        time_eight_hour_mock = MagicMock()
        time_now_mock.replace.side_effect = [time_ten_hour_mock, time_eight_hour_mock]
        time_ten_hour_mock.__gt__.return_value = True
        time_now_mock.__gt__.return_value = True

        result = Utils.check_time()

        self.assertEqual(result, True)
        datetime_now_patch.assert_called_once_with()
        time_now_mock.replace.assert_has_calls([call(hour=22, minute=0, second=0, microsecond=0),
                                                call(hour=8, minute=0, second=0, microsecond=0)])
        time_ten_hour_mock.__gt__.assert_called_once_with(time_now_mock)
        time_now_mock.__gt__.assert_called_once_with(time_eight_hour_mock)

    @freeze_time("2022-01-01")
    @patch('candy.utils.datetime.now')
    def test_check_time_not_allow_1(self, datetime_now_patch):

        time_now_mock = MagicMock()
        datetime_now_patch.return_value = time_now_mock
        time_ten_hour_mock = MagicMock()
        time_eight_hour_mock = MagicMock()
        time_now_mock.replace.side_effect = [time_ten_hour_mock, time_eight_hour_mock]
        time_ten_hour_mock.__gt__.return_value = True
        time_now_mock.__gt__.return_value = False

        result = Utils.check_time()

        self.assertEqual(result, False)
        datetime_now_patch.assert_called_once_with()
        time_now_mock.replace.assert_has_calls([call(hour=22, minute=0, second=0, microsecond=0),
                                                call(hour=8, minute=0, second=0, microsecond=0)])
        time_ten_hour_mock.__gt__.assert_called_once_with(time_now_mock)
        time_now_mock.__gt__.assert_called_once_with(time_eight_hour_mock)

    @freeze_time("2022-01-01")
    @patch('candy.utils.datetime.now')
    def test_check_time_not_allow_2(self, datetime_now_patch):

        time_now_mock = MagicMock()
        datetime_now_patch.return_value = time_now_mock
        time_ten_hour_mock = MagicMock()
        time_eight_hour_mock = MagicMock()
        time_now_mock.replace.side_effect = [time_ten_hour_mock, time_eight_hour_mock]
        time_ten_hour_mock.__gt__.return_value = False
        time_now_mock.__gt__.return_value = True

        result = Utils.check_time()

        self.assertEqual(result, False)
        datetime_now_patch.assert_called_once_with()
        time_now_mock.replace.assert_has_calls([call(hour=22, minute=0, second=0, microsecond=0),
                                                call(hour=8, minute=0, second=0, microsecond=0)])
        time_ten_hour_mock.__gt__.assert_called_once_with(time_now_mock)

    @freeze_time("2022-01-01")
    @patch('candy.utils.datetime.now')
    def test_check_time_not_allow_3(self, datetime_now_patch):

        time_now_mock = MagicMock()
        datetime_now_patch.return_value = time_now_mock
        time_ten_hour_mock = MagicMock()
        time_eight_hour_mock = MagicMock()
        time_now_mock.replace.side_effect = [time_ten_hour_mock, time_eight_hour_mock]
        time_ten_hour_mock.__gt__.return_value = False
        time_now_mock.__gt__.return_value = False

        result = Utils.check_time()

        self.assertEqual(result, False)
        datetime_now_patch.assert_called_once_with()
        time_now_mock.replace.assert_has_calls([call(hour=22, minute=0, second=0, microsecond=0),
                                                call(hour=8, minute=0, second=0, microsecond=0)])
        time_ten_hour_mock.__gt__.assert_called_once_with(time_now_mock)
