from django.contrib.auth.models import User, Permission, Group
from django.contrib.contenttypes.models import ContentType
from questionnaire.models import Region, UserProfile, Country


def create_user_with_no_permissions(username=None, country_name="Uganda", region_name="Afro"):
    username = username if username else "user"
    user = User.objects.create(username=username, email="user@mail.com")
    uganda = Country.objects.create(name=country_name)
    region = None
    if region_name:
        region = Region.objects.create(name=region_name)
    UserProfile.objects.create(user=user, country=uganda, region=region)
    user.set_password("pass")
    user.save()
    return user, uganda, region


def assign(permissions, user):
    auth_content = ContentType.objects.get_for_model(Permission)
    group = Group.objects.get_or_create(name="Group with %s permissions" % permissions)[0]
    permission, out = Permission.objects.get_or_create(codename=permissions, content_type=auth_content)
    group.permissions.add(permission)
    group.user_set.add(user)
    return user
