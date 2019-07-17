from django.db import models


class DMS(models.Model):
    DMSES = (
        ('NetDocuments', 'NetDocuments'),
        ('iManage', 'iManage'))
    dms_name = models.CharField(max_length=1000, default='iManage',
                                   choices=DMSES)
    dms_settings = models.CharField(max_length=1024)
