# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'QuestionTextHistory'
        db.delete_table(u'questionnaire_questiontexthistory')


    def backwards(self, orm):
        # Adding model 'QuestionTextHistory'
        db.create_table(u'questionnaire_questiontexthistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Questionnaire'])),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', to=orm['questionnaire.Question'])),
            ('export_label', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('questionnaire', ['QuestionTextHistory'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.answer': {
            'Meta': {'object_name': 'Answer'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Country']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'null': 'True', 'to': "orm['questionnaire.Question']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Draft'", 'max_length': '15'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'})
        },
        'questionnaire.answergroup': {
            'Meta': {'object_name': 'AnswerGroup'},
            'answer': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'answergroup'", 'null': 'True', 'to': "orm['questionnaire.Answer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grouped_question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer_groups'", 'null': 'True', 'to': "orm['questionnaire.QuestionGroup']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'questionnaire.comment': {
            'Meta': {'object_name': 'Comment'},
            'answer_group': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comments'", 'symmetrical': 'False', 'to': "orm['questionnaire.AnswerGroup']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'questionnaire.country': {
            'Meta': {'object_name': 'Country'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'countries'", 'null': 'True', 'to': "orm['questionnaire.Region']"})
        },
        'questionnaire.dateanswer': {
            'Meta': {'object_name': 'DateAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        'questionnaire.multichoiceanswer': {
            'Meta': {'object_name': 'MultiChoiceAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answer'", 'null': 'True', 'to': "orm['questionnaire.QuestionOption']"})
        },
        'questionnaire.numericalanswer': {
            'Meta': {'object_name': 'NumericalAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '2'})
        },
        'questionnaire.organization': {
            'Meta': {'object_name': 'Organization'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'questionnaire.question': {
            'Meta': {'object_name': 'Question'},
            'UID': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6'}),
            'answer_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'export_label': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'is_primary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'questions'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'questionnaire.questiongroup': {
            'Meta': {'ordering': "('order',)", 'object_name': 'QuestionGroup'},
            'allow_multiples': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_all': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'grid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_group'", 'null': 'True', 'to': "orm['questionnaire.QuestionGroup']"}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'question_group'", 'symmetrical': 'False', 'to': "orm['questionnaire.Question']"}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'question_group'", 'to': "orm['questionnaire.SubSection']"})
        },
        'questionnaire.questiongrouporder': {
            'Meta': {'ordering': "('order',)", 'object_name': 'QuestionGroupOrder'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['questionnaire.Question']"}),
            'question_group': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'null': 'True', 'to': "orm['questionnaire.QuestionGroup']"})
        },
        'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'questionnaire'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'draft'", 'max_length': '100', u'no_check_for_status': 'True'}),
            'year': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'questionnaire.questionoption': {
            'Meta': {'ordering': "('modified',)", 'object_name': 'QuestionOption'},
            'UID': ('django.db.models.fields.CharField', [], {'max_length': '6', 'unique': 'True', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': "orm['questionnaire.Question']"}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'questionnaire.region': {
            'Meta': {'object_name': 'Region'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'regions'", 'null': 'True', 'to': "orm['questionnaire.Organization']"})
        },
        'questionnaire.section': {
            'Meta': {'ordering': "('order',)", 'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['questionnaire.Questionnaire']"}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'questionnaire.subsection': {
            'Meta': {'ordering': "('order',)", 'object_name': 'SubSection'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_sections'", 'null': 'True', 'to': "orm['questionnaire.Region']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_sections'", 'to': "orm['questionnaire.Section']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'questionnaire.supportdocument': {
            'Meta': {'object_name': 'SupportDocument'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Country']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'path': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'support_documents'", 'to': "orm['questionnaire.Questionnaire']"})
        },
        'questionnaire.textanswer': {
            'Meta': {'object_name': 'TextAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        'questionnaire.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Country']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Organization']", 'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Region']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'user_profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['questionnaire']