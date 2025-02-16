import ipaddress
import traceback
from django.urls import resolve
from django.utils.timezone import now


class BaseLoggingMixin:
    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        self.log['errors'] = traceback.format_exc()
        return response

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        self.log = {
            'requested_at': now()
        }
        self.log.update({
            'remote_addr': self._get_ip_address(request),
            'view': self._get_view_name(request),
            'view_method': self._get_view_method(request),
            'path': request.path,
            'host': request.get_host(),
            'method': request.method,
            'user': self._get_user(request),
            'user_name_persistent':request.user.get_username() if request.user.is_authenticated else 'anonymous',
            'response_ms': self._get_response_ms(),
            'status_code': response.status_code,
        })
        self.handle_log()
        return response


    def handle_log(self):
        raise NotImplementedError

    def _get_ip_address(self, request):
        """Get the remote IP address the request was generated from."""
        ipaddr = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ipaddr:
            ipaddr = ipaddr.split(",")[0]
        else:
            ipaddr = request.META.get("REMOTE_ADDR", "").split(",")[0]

        possibles = (ipaddr.lstrip("[").split("]")[0], ipaddr.split(":")[0])

        for addr in possibles:
            try:
                return str(ipaddress.ip_address(addr))
            except ValueError:
                pass

        return ipaddr

    def _get_view_name(self, request):
        try:
            view_match = resolve(request.path_info)
            view = view_match.func

            if hasattr(view, 'view_class'):
                view = view.view_class
            module_name = view.__module__
            class_name = view.__name__
            return f"{module_name}.{class_name}"

        except Exception as e:
            return None

    def _get_view_method(self, request):
        method = request.method
        return method

    def _get_user(self, request):
        user = request.user
        if user.is_anonymous:
            return None
        return user

    def _get_response_ms(self):
        response_timedelta = now() - self.log['requested_at']
        response_ms = int(response_timedelta.total_seconds() * 1000)
        return max(response_ms, 0)

