from rest_framework.exceptions import NotFound
from rest_framework.pagination import CursorPagination


class DefaultCursorPagination(CursorPagination):
    page_size = 6
    ordering = 'id'

    # allowed_ordering_fields = ['created_at', 'task__title', 'deadline']
    # def get_ordering(self, request, queryset, view):
    #     ordering_param = request.query_params('ordering')
    #     if not ordering_param:
    #         return self.ordering
    #
    #     fields = ordering_param.split(',')
    #     validated_fields = []
    #     for field in fields:
    #         cleaned_field = field.lstrip()
    #         if cleaned_field in self.allowed_ordering_fields:
    #             validated_fields.append(field)
    #         else:
    #             raise NotFound(f"Field '{field}'is not allowed for ordering.")
    #
    #     return validated_fields or [self.ordering]
