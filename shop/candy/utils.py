from datetime import datetime


class Utils:

    @staticmethod
    def session_data(request, order_id):
        request.session['order_id'] = order_id

    @staticmethod
    def check_time():
        time_now = datetime.now()
        time_ten_hour = time_now.replace(hour=22, minute=0, second=0, microsecond=0)
        time_eight_hour = time_now.replace(hour=8, minute=0, second=0, microsecond=0)
        return time_ten_hour > time_now > time_eight_hour
