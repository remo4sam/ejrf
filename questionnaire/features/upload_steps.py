import os
from time import sleep
from django.core.files import File
from lettuce import world, step, after
from mock import mock_open, patch
from questionnaire.features.pages.uploads import UploadDocumentPage, DeleteDocumentPage
from questionnaire.models import SupportDocument


@step(u'And I click the upload support document link')
def and_i_click_the_upload_support_document_link(step):
    world.page.click_by_id('upload-file')

@step(u'Then I should see the upload form')
def then_i_should_see_the_upload_form(step):
    world.page = UploadDocumentPage(world.browser, world.questionnaire)
    world.page.validate_url()
    world.page.validate_upload_form({'Support document': 'path'})

@step(u'When I select a file to upload')
def when_i_select_a_file_to_upload(step):
    world.page.input_file(world.filename)

@step(u'And I click upload button')
def and_i_click_upload_button(step):
    world.page.click_by_id('upload-btn')

@step(u'Then I should see the file was uploaded successfully')
def then_i_should_see_the_file_was_uploaded_successfully(step):
    world.page.is_text_present(world.filename)
    world.page.is_text_present("File was uploaded successfully")

@step(u'And I have a pdf document')
def and_i_have_a_pdf_document(step):
    world.filename = 'sample_document.pdf'
    m = mock_open()
    with patch('__main__.open', m, create=True):
        with open(world.filename, 'w') as document:
            document.write("Some stuff")

@step(u'And I should be able to download the file')
def and_i_should_be_able_to_download_the_file(step):
    world.page.is_text_present(world.filename)

@step(u'And I have a zip file')
def and_i_have_a_zip_file(step):
    world.filename = 'sample_file.zip'
    m = mock_open()
    with patch('__main__.open', m, create=True):
        with open(world.filename, 'w') as document:
            document.write("Some stuff")

@step(u'Then I should see an error that the file type is not supported')
def then_i_should_see_an_error_that_the_file_type_is_not_supported(step):
    world.page.is_element_present_by_css('.error')
    world.page.is_text_present('file type is not an allowed')


@step(u'And I visit the attachments page')
def and_i_visit_the_attachments_page(step):
    world.page.click_by_id('id_attachments')

@step(u'And I have an attached file')
def and_i_have_an_attached_file(step):
    world.filename = 'sample_document.pdf'
    m = mock_open()
    with patch('__main__.open', m, create=True):
        with open(world.filename, 'w') as document:
            document.write("Some stuff")
            document = open(world.filename, 'rb')
            world.document = SupportDocument.objects.create(path=File(document), country=world.uganda,
                                                            questionnaire=world.questionnaire)

@step(u'And I click delete button next to that file')
def and_i_click_delete_button_next_to_that_file(step):
    world.page.click_by_css('.glyphicon-trash')
    sleep(3)

@step(u'Then I should see a warning dialog')
def then_i_should_see_a_warning_dialog(step):
    world.page = DeleteDocumentPage(world.browser, world.document)
    world.page.is_text_present("Are you sure you want to delete this document?")

@step(u'When I click confirm')
def when_i_click_confirm(step):
    world.page.click_by_id('confirm-delete-document-%s' % world.document.id)

@step(u'Then I should see that file was deleted')
def then_i_should_see_that_file_was_deleted(step):
    world.page.is_text_present(os.path.basename(world.document.path.url), status=False)
    world.page.is_text_present("Attachment was deleted successfully")

@step(u'And I clean up the files')
def and_i_clean_up_the_files(step):
    os.system("rm -rf %s" % world.filename)