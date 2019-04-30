# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AcAd(models.Model):
    admin = models.ForeignKey('Administrators', models.DO_NOTHING, primary_key=True)
    academic = models.ForeignKey('Academics', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'Ac_Ad'
        unique_together = (('admin', 'academic'),)


class Academics(models.Model):
    academic_id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    encripted_pwd = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Academics'


class Administrators(models.Model):
    admin_id = models.CharField(primary_key=True, max_length=255)
    position = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    encripted_pwd = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'Administrators'


class Assignments(models.Model):
    assignment_id = models.CharField(primary_key=True, max_length=255)
    module_id = models.CharField(max_length=255, blank=True, null=True)
    academic_id = models.CharField(max_length=255, blank=True, null=True)
    registration_date = models.DateTimeField(blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    assignment_format = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    percentage = models.CharField(max_length=255, blank=True, null=True)
    realease_date = models.DateTimeField(blank=True, null=True)
    submission_date = models.DateTimeField(blank=True, null=True)
    cw_marks_format = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Assignments'


class Modules(models.Model):
    module_id = models.CharField(primary_key=True, max_length=255)
    module_code = models.CharField(max_length=255, blank=True, null=True)
    academic_id = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    students = models.IntegerField(blank=True, null=True)
    credits = models.IntegerField(blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Modules'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class CmdbUserinfor(models.Model):
    user = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'cmdb_userinfor'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
