from django.test import TestCase
from django.forms.models import modelformset_factory, inlineformset_factory

from modelhistory.models import History

from .models import SimpleModel, ReleatedModel
from .forms import SimpleModelForm


class TestObjectLogs(TestCase):

    def test_message(self):
        message = "message"
        obj = SimpleModel.objects.create(name="test")

        log = History.log.obj(obj, message)
        self.assertEqual(log.message, message)

        log = History.log(obj, message)
        self.assertEqual(log.message, message)


    def test_create(self):
        obj = SimpleModel.objects.create(name="test")

        log = History.log.obj(obj)
        self.assertEqual(log.action, History.ADDITION)

        log = History.log(obj)
        self.assertEqual(log.action, History.ADDITION)


    def test_update(self):
        obj = SimpleModel.objects.create(name="test")

        obj.name = "test2"
        obj.save()

        log = History.log.obj(obj)

        self.assertEqual(log.action, History.CHANGE)


    def test_delete(self):
        obj = SimpleModel.objects.create(name="test")
        obj.delete()

        log = History.log.obj(obj)

        self.assertEqual(log.action, History.DELETION)


class TestFormLogs(TestCase):

    def test_create(self):
        form = SimpleModelForm({"name": "test"})

        self.assertTrue(form.is_valid())
        form.save()

        log = History.log.form(form)
        self.assertEqual(log.action, History.ADDITION)

        log = History.log(form)
        self.assertEqual(log.action, History.ADDITION)

    def test_update(self):
        obj = SimpleModel.objects.create(name="test")
        form = SimpleModelForm({"name": "test2"}, instance=obj)

        self.assertTrue(form.is_valid())
        form.save()

        log = History.log.form(form)
        self.assertEqual(log.action, History.CHANGE)


class TestFormSetLogs(TestCase):

    def test_create(self):
        SimpleModelFormSet = modelformset_factory(SimpleModel,
                                                  extra=2)

        data = {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-0-name': u'test 1',
            'form-1-name': u'test 2',
            }

        formset = SimpleModelFormSet(data)
        self.assertTrue(formset.is_valid())
        formset.save()

        log = History.log.formset(formset)

        self.assertEqual(len(log), 2)
        self.assertTrue(all([element.action == History.ADDITION for element in log]))

        log = History.log(formset)

        self.assertEqual(len(log), 2)
        self.assertTrue(all([element.action == History.ADDITION for element in log]))

    def test_update(self):
        SimpleModelFormSet = modelformset_factory(SimpleModel,
                                                  extra=0)

        simple_model_0 = SimpleModel.objects.create(name="test 0")
        simple_model_1 = SimpleModel.objects.create(name="test 1")

        data = {
            'form-TOTAL_FORMS': u'2',
            'form-INITIAL_FORMS': u'2',
            'form-0-id': str(simple_model_0.id),
            'form-0-name': u'new test 0',
            'form-1-id': str(simple_model_1.id),
            'form-1-name': u'new test 1',
            }

        formset = SimpleModelFormSet(data, queryset=SimpleModel.objects.all())

        self.assertTrue(formset.is_valid())
        formset.save()

        log = History.log.formset(formset)

        self.assertEqual(len(log), 2)
        self.assertTrue(all([element.action == History.CHANGE for element in log]))

    def test_delete(self):
        SimpleModelFormSet = modelformset_factory(SimpleModel,
                                                  extra=0,
                                                  can_delete=True)

        simple_model_0 = SimpleModel.objects.create(name="test 0")
        simple_model_1 = SimpleModel.objects.create(name="test 1")

        data = {
            'form-TOTAL_FORMS': 2,
            'form-INITIAL_FORMS': 0,
            'form-0-id': str(simple_model_0.id),
            'form-0-name': u'test 0',
            'form-0-DELETE': u'on',
            'form-1-id': str(simple_model_1.id),
            'form-1-name': u'test 1',
            'form-1-DELETE': u'on',
            }

        formset = SimpleModelFormSet(data, queryset=SimpleModel.objects.all())

        self.assertTrue(formset.is_valid())
        formset.save()

        log = History.log.formset(formset)

        self.assertEqual(len(log), 2)
        self.assertTrue(all([element.action == History.DELETION for element in log]))


class TestInlineFormSetLogs(TestCase):

    def test_create(self):
        ReleatedModelFormSet = inlineformset_factory(SimpleModel,
                                                     ReleatedModel,
                                                     extra=2)

        obj = SimpleModel.objects.create(name="test")

        data = {
            'releatedmodel_set-TOTAL_FORMS': u'2',
            'releatedmodel_set-INITIAL_FORMS': u'0',
            'releatedmodel_set-MAX_NUM_FORMS': u'',
            'releatedmodel_set-0-name': u'test 0',
            'releatedmodel_set-1-name': u'test 1'
            }

        formset = ReleatedModelFormSet(data, instance=obj)
        self.assertTrue(formset.is_valid())
        formset.save()

        log = History.log.inlineformset(formset)

        self.assertEqual(len(log), 3)
        self.assertEqual(log[0].content_object, obj)
        self.assertTrue(all([element.action == History.ADDITION for element in log[1:]]))

        log = History.log(formset)

        self.assertEqual(len(log), 3)
        self.assertEqual(log[0].content_object, obj)
        self.assertTrue(all([element.action == History.ADDITION for element in log[1:]]))


    def test_edit(self):
        ReleatedModelFormSet = inlineformset_factory(SimpleModel,
                                                     ReleatedModel,
                                                     extra=0)

        obj = SimpleModel.objects.create(name="test")
        related_object_0 = ReleatedModel.objects.create(name="test 0", choice=obj)
        related_object_1 = ReleatedModel.objects.create(name="test 0", choice=obj)

        data = {
            'releatedmodel_set-TOTAL_FORMS': u'2',
            'releatedmodel_set-INITIAL_FORMS': u'2',
            'releatedmodel_set-MAX_NUM_FORMS': u'',
            'releatedmodel_set-0-id': str(related_object_0.pk),
            'releatedmodel_set-0-name': u'new test 0',
            'releatedmodel_set-1-id': str(related_object_1.pk),
            'releatedmodel_set-1-name': u'new test 1'
            }

        formset = ReleatedModelFormSet(data, instance=obj)
        self.assertTrue(formset.is_valid())
        formset.save()

        log = History.log.inlineformset(formset)

        self.assertEqual(len(log), 3)
        self.assertEqual(log[0].content_object, obj)
        self.assertTrue(all([element.action == History.CHANGE for element in log[1:]]))

    def test_delete(self):
        ReleatedModelFormSet = inlineformset_factory(SimpleModel,
                                                     ReleatedModel,
                                                     extra=0)

        obj = SimpleModel.objects.create(name="test")
        related_object_0 = ReleatedModel.objects.create(name="test 0", choice=obj)
        related_object_1 = ReleatedModel.objects.create(name="test 0", choice=obj)

        data = {
            'releatedmodel_set-TOTAL_FORMS': u'2',
            'releatedmodel_set-INITIAL_FORMS': u'2',
            'releatedmodel_set-MAX_NUM_FORMS': u'',
            'releatedmodel_set-0-id': str(related_object_0.pk),
            'releatedmodel_set-0-name': u'test 0',
            'releatedmodel_set-0-DELETE': u'on',
            'releatedmodel_set-1-id': str(related_object_1.pk),
            'releatedmodel_set-1-name': u'test 1',
            'releatedmodel_set-1-DELETE': u'on',
            }

        formset = ReleatedModelFormSet(data, instance=obj)
        self.assertTrue(formset.is_valid())
        formset.save()

        log = History.log.inlineformset(formset)

        self.assertEqual(len(log), 3)
        self.assertEqual(log[0].content_object, obj)
        self.assertTrue(all([element.action == History.DELETION for element in log[1:]]))


class TestFormLogsMessage(TestCase):

    def setUp(self):
        pass

    def test_create(self):
        form = SimpleModelForm({"name": "test",
                                "real_name": "test"})

        self.assertTrue(form.is_valid())
        form.save()

        log = History.log.form(form)

        self.assertEqual(u"Name set to 'test' and Real name set to 'test'.", log.message)

    def test_update(self):
        obj = SimpleModel.objects.create(name="test")
        form = SimpleModelForm({"name": "test2",
                                "real_name": "test2"}, instance=obj)

        self.assertTrue(form.is_valid())
        form.save()

        log = History.log.form(form)

        self.assertEqual(u"Name changed to 'test2' and Real name changed to 'test2'.", log.message)


