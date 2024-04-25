# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models


class AllergyInfo(models.Model):
    allergy_code = models.CharField(primary_key=True, max_length=20)
    allergy_code_name = models.CharField(max_length=50)
    allergy_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'allergy_info'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
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
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class ComCode(models.Model):
    com_code = models.CharField(primary_key=True, max_length=10)
    com_code_grp = models.ForeignKey('ComCodeGrp', models.DO_NOTHING, db_column='com_code_grp')
    com_code_name = models.CharField(max_length=50)
    com_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'com_code'
        unique_together = (('com_code', 'com_code_grp'),)


class ComCodeGrp(models.Model):
    com_code_grp = models.CharField(primary_key=True, max_length=10)
    com_code_grp_name = models.CharField(max_length=10)
    com_code_grp_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'com_code_grp'


class DiseaseCode(models.Model):
    disease_code = models.CharField(primary_key=True, max_length=20)
    disease_code_name = models.CharField(max_length=50)
    disease_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'disease_code'


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
    id = models.BigAutoField(primary_key=True)
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


class FunctionCode(models.Model):
    function_code = models.CharField(primary_key=True, max_length=20)
    function_code_name = models.CharField(max_length=50)
    function_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)

    class Meta:
        managed = False
        db_table = 'function_code'


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=100)
    ingredient_limit_high = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    ingredient_limit_low = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True)
    ingredient_unit = models.CharField(max_length=10, blank=True, null=True)
    ingredient_function_content = models.TextField(blank=True, null=True)
    ingredient_caution = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingredient'


class IngredientFunction(models.Model):
    ingredient_function_id = models.AutoField(primary_key=True)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)
    function_code = models.ForeignKey(FunctionCode, models.DO_NOTHING, db_column='function_code')

    class Meta:
        managed = False
        db_table = 'ingredient_function'


class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_company = models.CharField(max_length=50)
    product_instruction = models.TextField(blank=True, null=True)
    product_function_content = models.TextField(blank=True, null=True)
    product_caution = models.TextField(blank=True, null=True)
    product_serving = models.TextField(blank=True, null=True)
    product_image = models.TextField(blank=True, null=True)
    product_rating_avg = models.DecimalField(max_digits=3, decimal_places=2)
    product_rating_cnt = models.PositiveIntegerField()
    product_dispos = models.CharField(max_length=20, blank=True, null=True)
    product_storage_method = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductFunction(models.Model):
    product_function_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    function_code = models.ForeignKey(FunctionCode, models.DO_NOTHING, db_column='function_code')

    class Meta:
        managed = False
        db_table = 'product_function'


class ProductIngredient(models.Model):
    product_ingredient_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'product_ingredient'


class ProductLog(models.Model):
    product_log_id = models.PositiveIntegerField(primary_key=True)
    product_id = models.BigIntegerField(unique=True)
    profile = models.OneToOneField('Profile', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    visited_at = models.DateTimeField(blank=True, null=True)
    leaved_at = models.DateTimeField(blank=True, null=True)
    product_log_duration = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_log'


class ProductReview(models.Model):
    product_review_id = models.AutoField(primary_key=True)
    profile = models.ForeignKey('Profile', models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    product_review_rating = models.IntegerField(unique=True)
    product_review_content = models.CharField(max_length=200)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_review'


class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    profile_name = models.CharField(max_length=20)
    profile_birth = models.DateField()
    profile_status = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'profile'


class Recommendation(models.Model):
    recommendation_id = models.BigAutoField(primary_key=True)
    survey = models.ForeignKey('Survey', models.DO_NOTHING)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'recommendation'


class RecommendationIngredient(models.Model):
    recommendation_ingredient_id = models.BigAutoField(primary_key=True)
    recommendation = models.ForeignKey(Recommendation, models.DO_NOTHING)
    ingredient = models.ForeignKey(Ingredient, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recommendation_ingredient'


class RecommendationProduct(models.Model):
    recommendation_product_id = models.BigAutoField(primary_key=True)
    recommendation = models.ForeignKey(Recommendation, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recommendation_product'


class Survey(models.Model):
    survey_id = models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING)
    survey_age_group = models.CharField(max_length=20)
    survey_sex = models.CharField(max_length=1)
    survey_pregnancy_code = models.CharField(max_length=10)
    survey_operation_code = models.CharField(max_length=10, blank=True, null=True)
    survey_alcohol_code = models.CharField(max_length=10, blank=True, null=True)
    survey_smoke = models.CharField(max_length=1, blank=True, null=True)
    survey_height = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    survey_weight = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'survey'


class SurveyAllergy(models.Model):
    survey_allergy_id = models.BigAutoField(primary_key=True)
    survey = models.ForeignKey(Survey, models.DO_NOTHING)
    allergy_code = models.ForeignKey(AllergyInfo, models.DO_NOTHING, db_column='allergy_code')

    class Meta:
        managed = False
        db_table = 'survey_allergy'


class SurveyDisease(models.Model):
    survey_disease_id = models.BigAutoField(primary_key=True)
    survey = models.ForeignKey(Survey, models.DO_NOTHING)
    disease_code = models.ForeignKey(DiseaseCode, models.DO_NOTHING, db_column='disease_code')

    class Meta:
        managed = False
        db_table = 'survey_disease'


class SurveyFunction(models.Model):
    survey_function_id = models.BigAutoField(primary_key=True)
    survey = models.ForeignKey(Survey, models.DO_NOTHING)
    function_code = models.ForeignKey(FunctionCode, models.DO_NOTHING, db_column='function_code')

    class Meta:
        managed = False
        db_table = 'survey_function'


class User(AbstractUser):
    user_id = models.PositiveIntegerField(primary_key=True)
    user_email = models.CharField(unique=True, max_length=50)
    user_password = models.CharField(max_length=50)
    user_role = models.CharField(max_length=20)
    user_status = models.CharField(max_length=10)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField(blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user'
