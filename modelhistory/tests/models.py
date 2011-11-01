from django.db import models


class SimpleModel(models.Model):
    name = models.CharField(max_length=100, blank=True)
    real_name = models.CharField(max_length=100, blank=True)

    def __unicode__(self):
        return u"%s %s" % (self._meta.verbose_name, self.pk)


class ChoiceModel(models.Model):
    name = models.CharField(max_length=100)

    choices = (("value_1", "Verbose value 1"),
               ("value_2", "Verbose value 2"))
    choice = models.CharField(choices=choices, max_length=100)
    def __unicode__(self):
        return u"%s %s" % (self._meta.verbose_name, self.pk)


class ReleatedModel(models.Model):
    name = models.CharField(max_length=100)
    choice = models.ForeignKey('SimpleModel')

    def __unicode__(self):
        return u"%s %s" % (self._meta.verbose_name, self.pk)
