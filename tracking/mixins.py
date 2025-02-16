from .base_mixins import BaseLoggingMixin
from .models import APIRequestLog

class LoggingMixins(BaseLoggingMixin):
        def handle_log(self):
            APIRequestLog.objects.create(**self.log)
