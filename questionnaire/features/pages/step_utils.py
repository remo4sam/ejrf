from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from questionnaire.models import Region, UserProfile, Country, Organization, Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionGroupOrder, AnswerGroup


def create_user_with_no_permissions(username=None, country_name="Uganda", region_name="Afro", password="pass"):
    username = username if username else "user"
    user = User.objects.create(username=username, email="user@mail.com")
    uganda = Country.objects.create(name=country_name)
    region = None
    if region_name:
        region = Region.objects.create(name=region_name)
        region.countries.add(uganda)
    UserProfile.objects.create(user=user, country=uganda, region=region)
    user.set_password(password)
    user.save()
    return user, uganda, region


def create_global_admin_with_no_permissions(username=None, org_name="unicef"):
    username = username if username else "user"
    user = User.objects.create(username=username, email="user@mail.com")
    organization = None
    if org_name:
        organization = Organization.objects.create(name=org_name)

    UserProfile.objects.create(user=user, organization=organization)
    user.set_password("pass")
    user.save()
    return user


def create_regional_admin_with_no_permissions(username=None, org_name="unicef", region_name="Afro"):
    username = username if username else "user"
    user = User.objects.create(username=username, email="user@mail.com")
    organization = None
    if org_name:
        organization = Organization.objects.create(name=org_name)

    region = None
    if region_name:
        region = Region.objects.create(name=region_name)

    UserProfile.objects.create(user=user, organization=organization, region=region)
    user.set_password("pass")
    user.save()
    return user, region


def assign(permissions, user):
    auth_content = ContentType.objects.get_for_model(Permission)
    group = Group.objects.get_or_create(name="Group with %s permissions" % permissions)[0]
    permission, out = Permission.objects.get_or_create(codename=permissions, content_type=auth_content)
    group.permissions.add(permission)
    group.user_set.add(user)
    return user


def create_regional_questionnaire_with_one_question(region):
    regional_questionnaire = Questionnaire.objects.create(name="JRF Regional", description="Regional Questionnaire",
                                                          status=Questionnaire.PUBLISHED, region=region)
    section = Section.objects.create(order=1, title="Section Title", description="Section Description",
                                     questionnaire=regional_questionnaire, name="Cover page")
    subsection = SubSection.objects.create(order=1, section=section, title='Subsection Title')
    question1 = Question.objects.create(text='Name of person in Ministry of Health', UID='C0001',
                                        answer_type='Text')
    parent = QuestionGroup.objects.create(subsection=subsection, order=1)
    parent.question.add(question1)
    QuestionGroupOrder.objects.create(question=question1, question_group=parent, order=1)
    answer_group = AnswerGroup.objects.create(grouped_question=parent, row=1)

    return regional_questionnaire, question1, answer_group