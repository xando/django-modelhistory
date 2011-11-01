from django.db import models

from django.utils.text import get_text_list, capfirst
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

    def _form_fields_filter(self, form):
        # Rewrite this haskell code!
        return [field for field in form.fields.items() \
                if field[0] in form.changed_data and \
                field[0] not in ['DELETE']]

    def _discover_action(self, obj):
        if getattr(obj._state, "created", None) and obj.pk:
            action = History.ADDITION
        else:
            if obj.pk:
                action = History.CHANGE
            else:
                action = History.DELETION

        return action

    def _get_form_field_value(self, form, field_name):
        try:
            return getattr(form.instance, "get_%s_display" % field_name)()
        except AttributeError:
            return getattr(form.instance, field_name)

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

        message_parts = []

        if action == History.ADDITION:

            for field_name, field in self._form_fields_filter(form):
                message_parts.append(
                    "%s set to '%s'" %
                    (field.label, self._get_form_field_value(form, field_name))
                )

        elif action == History.CHANGE:

            for field_name, field in self._form_fields_filter(form):
                message_parts.append(
                    "%s changed to '%s'" %
                    (field.label, self._get_form_field_value(form, field_name))
                )

        if message_parts:
            message = "%s." % get_text_list(message_parts, "and")
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

    objects = HistoryManager()

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    time = models.DateTimeField(_('time'), auto_now=True)
    action = models.PositiveSmallIntegerField(_('action flag'), null=True)
    _message = models.TextField(_('change message'), blank=True)

    def get_message(self):
        message_parts = []
        if self.action == History.ADDITION:
            message_parts.append("%s created"
                                 % unicode(self.content_object))

        elif self.action == History.CHANGE:
            message_parts.append("%s changed"
                                 % unicode(self.content_object))

        if self._message:
            message_parts.append(self._message or None)

        message_parts = [capfirst(message) for message in message_parts]

        if len(message_parts) > 1:
            return ". ".join(message_parts)
        elif len(message_parts) == 1:
            return "%s." % message_parts[0]
        return ""

    def set_message(self, message):
        self._message = message

    message = property(get_message, set_message)

    def __repr__(self):
        return "<History: %s:%s:%s>" % (self.content_object,
                                        self.action,
                                        self.message)

