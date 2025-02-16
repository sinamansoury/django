from datetime import datetime
from django.db import models
from django.conf import settings
from Account.models import User


class BaseAPIRequestLog(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    user_name_persistent = models.CharField(
        max_length=getattr(settings, 'USERNAME_PERSISTENT', 100),
        null=True,
        blank=True,
    )
    requested_at = models.DateTimeField(
        default=datetime.now,
        db_index=True,
    )
    response_ms = models.PositiveSmallIntegerField(default=0)
    path = models.CharField(
        max_length=getattr(settings, 'PATH_LENGTH', 100),
        db_index=True,
        help_text='path',
    )
    view= models.CharField(
        max_length=getattr(settings, "DRF_TRACKING_VIEW_LENGTH", 200),
        null=True,
        blank=True,
        db_index=True,
        help_text="method called by this endpoint",
    )
    view_method = models.CharField(
        max_length=getattr(settings, "DRF_TRACKING_VIEW_METHOD_LENGTH", 200),
        null=True,
        blank=True,
        db_index=True,
    )
    remote_addr = models.GenericIPAddressField(null=True, blank=True)
    host = models.URLField()
    method = models.CharField(max_length=10)
    user_agent = models.CharField(max_length=255, blank=True)
    query_params = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    response = models.TextField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    status_code = models.PositiveIntegerField(null=True, blank=True, db_index=True)

    class Meta:
        abstract = True
        verbose_name = "API Request Log"

    def __str__(self):
        return f"{self.method} {self.path}"
    