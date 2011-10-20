from django.db import models

from django.utils.text import get_text_list
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def callback(sender, instance, created, **kwargs):
    instance._state.created = created


class HistoryManager(models.Manager):

    def _discover_action(self, obj):
        if getattr(obj._state, "created", None) and obj.pk:
            action = History.ADDITION
        else:
            if obj.pk:
                action = History.CHANGE
            else:
                action = History.DELETION

        return action

    def log(self, message):
        return History.objects.create(message=message)

    def log_object(self, obj, message=""):
        action = self._discover_action(obj)

        return History.objects.create(content_object=obj,
                                      message=message,
                                      action=action)

    def log_form(self, form):
        obj = form.instance

        action = self._discover_action(obj)

        if action == History.CHANGE:
            message_parts = []

            for field_name in filter(lambda x: x is not "DELETE", form.changed_data):
                try:
                    value = getattr(form.instance, "get_%s_display" % field_name)()
                except AttributeError:
                    value = getattr(form.instance, field_name)

                message_parts.append("%s to '%s'" %
                                     (field_name, value))

            message = "changed %s" % get_text_list(message_parts, "and")
        else:
            message = ""

        return History.objects.create(content_object=obj,
                                      message=message,
                                      action=action)

    def log_formset(self, formset):
        history_objects = []
        for form in formset.forms:
            history_objects.append(self.log_form(form))

        return history_objects

    def log_inlineformset(self, inlineformset):
        history_objects = self.log_formset(inlineformset)
        message_parts = [element.message for element in history_objects]
        if any(message_parts):
            message = get_text_list(message_parts, "and")
        else:
            message = ""

        obj = inlineformset.instance
        history_objects.insert(0, self.log_object(obj, message))

        return history_objects


class History(models.Model):
    ADDITION = 1
    CHANGE = 2
    DELETION = 3

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    time = models.DateTimeField(_('time'), auto_now=True)
    message = models.TextField(_('change message'), blank=True)
    action = models.PositiveSmallIntegerField(_('action flag'), null=True)

    objects = HistoryManager()

    def __repr__(self):
        return "<History: %s:%s:%s>" % (self.content_object,
                                        self.action,
                                        self.message)




