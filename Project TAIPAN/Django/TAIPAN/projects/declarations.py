from django.db import models

status_control = {
    "CURRENT": "C",
    "ARCHIVED": "X",
}


class Detail(models.Model):
    status_control = models.CharField(max_length=1)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(null=True, blank=True)

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=4000)

    class Meta:
        abstract = True
