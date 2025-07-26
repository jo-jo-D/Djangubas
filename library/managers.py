from django.db import models


class SoftDeleteManager(models.Manager):
    def get_queryset(self):
        """
        Переопределяем базовый QuerySet, чтобы по умолчанию
        исключать записи, помеченные как удаленные.
        """
        return super().get_queryset().filter(is_deleted=False)