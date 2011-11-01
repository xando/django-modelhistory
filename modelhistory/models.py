from django.db import models
from django import forms


from django.utils.text import get_text_list, capfirst
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _, ugettext
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save)
def callback(sender, instance, created, **kwargs):
    instance._state.created = created


class HistoryManager(models.Manager):

    def __call__(self, obj, *args, **kwargs):

        if isinstance(obj, forms.models.BaseInlineFormSet):
            return self.inlineformset(obj, *args, **kwargs)

        if isinstance(obj, forms.models.BaseModelFormSet):
            return self.formset(obj, *args, **kwargs)

        if isinstance(obj, forms.ModelForm):
            return self.form(obj, *args, **kwargs)

        if isinstance(obj, models.Model):
            return self.obj(obj, *args, **kwargs)

        if isinstance(obj, basestring):
            return self.log(obj, *args, **kwargs)

        raise TypeError("History for type %s is unsupported." % type(obj))

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

    def obj(self, obj, message=""):
        action = self._discover_action(obj)

        return History.objects.create(content_object=obj,
                                      message=message,
                                      action=action)

    def form(self, form):
        obj = form.instance

        action = self._discover_action(obj)

        message_parts = []

        if action == History.ADDITION:

            for field_name, field in self._form_fields_filter(form):
                message_parts.append(_("%(attribute)s set to '%(value)s'") % {
                    "attribute": field.label,
                    "value": self._get_form_field_value(form, field_name)
                })

        elif action == History.CHANGE:

            for field_name, field in self._form_fields_filter(form):
                message_parts.append(_("%(attribute)s changed to '%(value)s'") % {
                    "attribute": field.label,
                    "value": self._get_form_field_value(form, field_name)
                })

        if message_parts:
            message = u"%s." % get_text_list(message_parts, _(u"and"))
        else:
            message = ""

        return History.objects.create(content_object=obj,
                                      message=message,
                                      action=action)

    def formset(self, formset):
        history_objects = []
        for form in formset.forms:
            history_objects.append(self.form(form))

        return history_objects

    def inlineformset(self, inlineformset):
        history_objects = self.formset(inlineformset)
        message_parts = [element.message for element in history_objects]
        if any(message_parts):
            message = unicode(get_text_list(message_parts, last_word=_(u'and')))
        else:
            message = ""

        obj = inlineformset.instance
        history_objects.insert(0, self.obj(obj, message))

        return history_objects


class History(models.Model):
    ADDITION = 1
    CHANGE = 2
    DELETION = 3

    objects = models.Manager()
    log = HistoryManager()

    content_type = models.ForeignKey(ContentType, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    time = models.DateTimeField(_('time'), auto_now=True)
    action = models.PositiveSmallIntegerField(_('action flag'), null=True)
    _message = models.TextField(_('change message'), blank=True)

    def get_message(self):
        return self._message

    def set_message(self, message):
        self._message = message

    message = property(get_message, set_message)

    def __repr__(self):
        return "<History: %s:%s:%s>" % (self.content_object,
                                        self.action,
                                        self.message)

