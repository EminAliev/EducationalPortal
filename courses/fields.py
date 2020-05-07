from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class SortField(models.PositiveIntegerField):
    """Сортировка(порядок) для содержимого курсов"""

    def __init__(self, fields=None, *args, **kwargs):
        self.fields = fields
        super(SortField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        """Сортировка объектов по порядку номеров"""
        if getattr(model_instance, self.attname) is None:
            try:
                queryset = self.model.objects.all()
                if self.fields:
                    # Фильтрация объектов с такими же значениями полей
                    q = {field: getattr(model_instance, field)
                         for field in self.fields}
                    queryset = queryset.filter(**q)
                # получаем объект с максимальным значением порядкового номера и результата фильтрации
                item = queryset.latest(self.attname)
                value = item.sort + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(SortField, self).pre_save(model_instance, add)
