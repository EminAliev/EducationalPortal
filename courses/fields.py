from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class SortField(models.PositiveIntegerField):
    def __init__(self, fields=None, *args, **kwargs):
        self.fields = fields
        super(SortField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                queryset = self.model.objects.all()
                if self.fields:
                    q = {field: getattr(model_instance, field)
                         for field in self.fields}
                    queryset = queryset.filter(**q)
                item = queryset.latest(self.attname)
                value = item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(SortField, self).pre_save(model_instance, add)
