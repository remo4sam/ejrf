# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Comment'
        db.create_table(u'questionnaire_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('questionnaire', ['Comment'])

        # Adding M2M table for field answer on 'Comment'
        db.create_table(u'questionnaire_comment_answer', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('comment', models.ForeignKey(orm['questionnaire.comment'], null=False)),
            ('answer', models.ForeignKey(orm['questionnaire.answer'], null=False))
        ))
        db.create_unique(u'questionnaire_comment_answer', ['comment_id', 'answer_id'])

        # Adding model 'QuestionOption'
        db.create_table(u'questionnaire_questionoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Question'])),
        ))
        db.send_create_signal('questionnaire', ['QuestionOption'])

        # Adding model 'Answer'
        db.create_table(u'questionnaire_answer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Question'], null=True)),
            ('country', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Country'], null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Draft', max_length=15)),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1, null=True)),
        ))
        db.send_create_signal('questionnaire', ['Answer'])

        # Adding model 'AnswerGroup'
        db.create_table(u'questionnaire_answergroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.Answer'], null=True)),
            ('grouped_question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionGroup'], null=True)),
            ('row', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal('questionnaire', ['AnswerGroup'])

        # Adding model 'TextAnswer'
        db.create_table(u'questionnaire_textanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
        ))
        db.send_create_signal('questionnaire', ['TextAnswer'])

        # Adding model 'MultiChoiceAnswer'
        db.create_table(u'questionnaire_multichoiceanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.QuestionOption'])),
        ))
        db.send_create_signal('questionnaire', ['MultiChoiceAnswer'])

        # Adding model 'QuestionGroup'
        db.create_table(u'questionnaire_questiongroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('subsection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['questionnaire.SubSection'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('questionnaire', ['QuestionGroup'])

        # Adding M2M table for field question on 'QuestionGroup'
        db.create_table(u'questionnaire_questiongroup_question', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questiongroup', models.ForeignKey(orm['questionnaire.questiongroup'], null=False)),
            ('question', models.ForeignKey(orm['questionnaire.question'], null=False))
        ))
        db.create_unique(u'questionnaire_questiongroup_question', ['questiongroup_id', 'question_id'])

        # Adding model 'NumericalAnswer'
        db.create_table(u'questionnaire_numericalanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
        ))
        db.send_create_signal('questionnaire', ['NumericalAnswer'])

        # Adding model 'DateAnswer'
        db.create_table(u'questionnaire_dateanswer', (
            (u'answer_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['questionnaire.Answer'], unique=True, primary_key=True)),
            ('response', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('questionnaire', ['DateAnswer'])


        # Changing field 'Question.answer_type'
        db.alter_column(u'questionnaire_question', 'answer_type', self.gf('django.db.models.fields.CharField')(max_length=20))
        # Adding field 'Section.name'
        db.add_column(u'questionnaire_section', 'name',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Comment'
        db.delete_table(u'questionnaire_comment')

        # Removing M2M table for field answer on 'Comment'
        db.delete_table('questionnaire_comment_answer')

        # Deleting model 'QuestionOption'
        db.delete_table(u'questionnaire_questionoption')

        # Deleting model 'Answer'
        db.delete_table(u'questionnaire_answer')

        # Deleting model 'AnswerGroup'
        db.delete_table(u'questionnaire_answergroup')

        # Deleting model 'TextAnswer'
        db.delete_table(u'questionnaire_textanswer')

        # Deleting model 'MultiChoiceAnswer'
        db.delete_table(u'questionnaire_multichoiceanswer')

        # Deleting model 'QuestionGroup'
        db.delete_table(u'questionnaire_questiongroup')

        # Removing M2M table for field question on 'QuestionGroup'
        db.delete_table('questionnaire_questiongroup_question')

        # Deleting model 'NumericalAnswer'
        db.delete_table(u'questionnaire_numericalanswer')

        # Deleting model 'DateAnswer'
        db.delete_table(u'questionnaire_dateanswer')


        # Changing field 'Question.answer_type'
        db.alter_column(u'questionnaire_question', 'answer_type', self.gf('django.db.models.fields.CharField')(max_length=10))
        # Deleting field 'Section.name'
        db.delete_column(u'questionnaire_section', 'name')


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
            'country': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Country']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Question']", 'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Draft'", 'max_length': '15'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1', 'null': 'True'})
        },
        'questionnaire.answergroup': {
            'Meta': {'object_name': 'AnswerGroup'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Answer']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grouped_question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionGroup']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'row': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'questionnaire.comment': {
            'Meta': {'object_name': 'Comment'},
            'answer': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'comments'", 'symmetrical': 'False', 'to': "orm['questionnaire.Answer']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        'questionnaire.country': {
            'Meta': {'object_name': 'Country'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'regions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'countries'", 'null': 'True', 'to': "orm['questionnaire.Region']"})
        },
        'questionnaire.dateanswer': {
            'Meta': {'object_name': 'DateAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.DateField', [], {})
        },
        'questionnaire.multichoiceanswer': {
            'Meta': {'object_name': 'MultiChoiceAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.QuestionOption']"})
        },
        'questionnaire.numericalanswer': {
            'Meta': {'object_name': 'NumericalAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'questionnaire.questiongroup': {
            'Meta': {'object_name': 'QuestionGroup'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questionnaire.Question']", 'symmetrical': 'False'}),
            'subsection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.SubSection']"})
        },
        'questionnaire.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'questionnaire.questionoption': {
            'Meta': {'object_name': 'QuestionOption'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questionnaire.Question']"}),
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
            'Meta': {'object_name': 'Section'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sections'", 'to': "orm['questionnaire.Questionnaire']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'questionnaire.subsection': {
            'Meta': {'object_name': 'SubSection'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sub_sections'", 'to': "orm['questionnaire.Section']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'questionnaire.textanswer': {
            'Meta': {'object_name': 'TextAnswer', '_ormbases': ['questionnaire.Answer']},
            u'answer_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['questionnaire.Answer']", 'unique': 'True', 'primary_key': 'True'}),
            'response': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        }
    }

    complete_apps = ['questionnaire']