import StringIO
import json
import os
import subprocess
from django.core.files import File
from django.test import Client
import time
from mock import patch
from questionnaire.models import Questionnaire, Section
from questionnaire.tests.base_test import BaseTest


class ExportSectionToPDFViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.login_user()

        self.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English",
                                                          description="From dropbox as given by Rouslan", year=2013)
        self.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)",
                                                order=1,
                                                questionnaire=self.questionnaire, name="Reported Cases")

    def test_get(self):
        meta ={'HTTP_REFERER': 'http://', 'HTTP_HOST': 'somehost'}

        mock_time = '123'
        with patch.object(time, 'time', return_value=mock_time):
            with patch.object(subprocess, 'Popen') as mock_popen:
                response = self.client.get("/export-section/", **meta)

        self.assertEqual(200, response.status_code)
        content = json.loads(response.content)
        self.assertEqual(1, len(content.keys()))
        self.assertEqual('filename', content.keys()[0])

        file_name = 'eJRF_export_%s.pdf' % mock_time
        export_file_name = 'export/' + file_name
        self.assertTrue(file_name, content['filename'])

        session_id = response.client.cookies['sessionid'].value
        url = (meta['HTTP_REFERER'] +'?printable=1')
        domain = meta['HTTP_HOST']
        phantomjs_script = 'questionnaire/static/js/export-section.js'
        command = ["phantomjs", phantomjs_script, url, export_file_name, session_id, domain, "&> /dev/null &"]

        mock_popen.assert_called_once_with(command)

    def test_login_required(self):
        self.assert_login_required('/export-section/')


class DownloadSectionPDFViewTest(BaseTest):
    def setUp(self):
        self.client = Client()
        self.user, self.country, self.region = self.create_user_with_no_permissions()
        self.login_user()

    def test_get(self):
        filename = "haha.pdf"
        os.system("echo 'haha' > export/%s" % filename)

        response = self.client.get('/export-section/%s' % filename)
        self.assertEqual('attachment; filename=%s' % filename, response.get('Content-Disposition'))
        self.assertFalse(os.path.isfile('export/'+filename))

    def test_login_required(self):
        self.assert_login_required('/export-section/hahaha.pdf')
