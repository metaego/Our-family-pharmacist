# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models
# from django.utils import timezone
# decimalfield 음수 허용 불가, 리뷰 제한을 위한 MinValueValidator 임포트
from django.core.validators import MinValueValidator, MaxValueValidator



# ComCodeGrp class 위치를 현 위치로 이동
class ComCodeGrp(models.Model):
    com_code_grp = models.CharField(primary_key=True, max_length=20)
    com_code_grp_name = models.CharField(max_length=50)
    com_code_grp_desc = models.CharField(max_length=500, blank=True)
    use_yn = models.CharField(max_length=1)


    class Meta:
        managed = True
        db_table = 'com_code_grp'



# ComCode class 위치를 현 위치로 이동
class ComCode(models.Model):
    com_code = models.CharField(primary_key=True, max_length=20)
    com_code_grp = models.ForeignKey(ComCodeGrp, on_delete=models.CASCADE, db_column='com_code_grp')
    com_code_name = models.CharField(max_length=50)
    com_code_desc = models.CharField(max_length=500, blank=True)
    use_yn = models.CharField(max_length=1)


    class Meta:
        managed = True
        db_table = 'com_code'
    


# Ingredient class 위치를 현 위치로 이동
class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_grp_name = models.CharField(max_length=100) # 신규 추가
    ingredient_name = models.CharField(max_length=100)
    ingredient_auth_num = models.CharField(max_length=100, blank=True, null=True)   # 신규 추가(2024.07.04)
    ingredient_recom_name = models.CharField(max_length=100, blank=True, null=True) # 신규 추가(2024.07.04)
    ingredient_limit_high = models.TextField(blank=True, null=True)
    ingredient_limit_low = models.TextField(blank=True, null=True)
    ingredient_unit = models.CharField(max_length=10, blank=True, null=True)
    ingredient_type = models.CharField(max_length=10, blank=True, null=True)
    ingredient_function_content = models.TextField(blank=True, null=True)
    ingredient_caution_content = models.TextField(blank=True, null=True)
    ingredient_function_code = models.JSONField(blank=True, null=True) 
    ingredient_caution_code = models.JSONField(blank=True, null=True)

    
    class Meta:
        managed = True
        db_table = 'ingredient'



# IngredientComCode class 위치를 현 위치로 이동
class IngredientComCode(models.Model):
    ingredient_com_code_id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_column='ingredient_id')
    com_code_grp = models.ForeignKey(ComCodeGrp, on_delete=models.CASCADE, db_column='com_code_grp')
    com_code = models.ForeignKey(ComCode, on_delete=models.CASCADE, db_column='com_code')


    class Meta:
        managed = True
        db_table = 'ingredient_com_code'



# # AllergyCode class 위치를 현 위치로 이동
# class AllergyCode(models.Model):
#     allergy_code = models.CharField(primary_key=True, max_length=20)
#     allergy_code_name = models.CharField(max_length=50)
#     allergy_code_desc = models.CharField(max_length=500, blank=True, null=True)
#     use_yn = models.CharField(max_length=1)


#     class Meta:
#         managed = True
#         db_table = 'allergy_code'



# # DiseaseCode class 위치를 현 위치로 이동
# class DiseaseCode(models.Model):
#     disease_code = models.CharField(primary_key=True, max_length=20)
#     disease_code_name = models.CharField(max_length=50)
#     disease_code_desc = models.CharField(max_length=500, blank=True, null=True)
#     use_yn = models.CharField(max_length=1)


#     class Meta:
#         managed = True
#         db_table = 'disease_code'



# # FunctionCode class 위치를 현 위치로 이동
# class FunctionCode(models.Model):
#     function_code = models.CharField(primary_key=True, max_length=20)
#     function_code_name = models.CharField(max_length=50)
#     function_code_desc = models.CharField(max_length=500, blank=True, null=True)
#     use_yn = models.CharField(max_length=1)


#     class Meta:
#         managed = True
#         db_table = 'function_code'



# AbstractUser 자동 생성 필드 매칭 후 (24.06.12)
class User(AbstractUser):
    user_id = models.BigAutoField(primary_key=True)
    # user_email = models.EmailField(unique=True, max_length=50)
    # user_password = models.CharField(max_length=50)
    # user_role = models.CharField(max_length=20, default='user')
    # user_status = models.CharField(max_length=10, default='active')
    # user_created_at = models.DateTimeField(auto_now_add=True)
    user_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    user_deleted_at = models.DateTimeField(blank=True, null=True)
    # user_last_login = models.DateTimeField(auto_now=True)
    first_name = None
    last_name = None

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    class Meta:
        managed = True
        db_table = 'user'
        


# AbstractUser 자동 생성 필드 매칭 이전 (24.06.12)
# User class 위치를 현 위치로 이동
# class User(AbstractUser):
#     user_id = models.BigAutoField(primary_key=True)
#     user_email = models.EmailField(unique=True, max_length=50)
#     user_password = models.CharField(max_length=50)
#     user_role = models.CharField(max_length=20, default='user')
#     user_status = models.CharField(max_length=10, default='active')
#     user_created_at = models.DateTimeField(auto_now_add=True)
#     user_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
#     user_deleted_at = models.DateTimeField(blank=True, null=True)
#     user_last_login = models.DateTimeField(auto_now=True)


#     class Meta:
#         managed = True
#         db_table = 'user'



class Profile(models.Model):
    profile_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    profile_name = models.CharField(max_length=20)
    profile_birth = models.DateField()
    profile_status = models.CharField(max_length=10, default='active')
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    profile_deleted_at = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'profile'



# Survey class 위치를 현 위치로 이동
class Survey(models.Model):
    survey_id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id')
    survey_sex = models.CharField(max_length=1)
    survey_age_group = models.CharField(max_length=20)
    survey_pregnancy_code = models.CharField(max_length=10)
    survey_operation_code = models.CharField(max_length=10, blank=True)
    survey_alcohol_code = models.CharField(max_length=10, blank=True)
    survey_smoking_code = models.CharField(max_length=10, blank=True)
    survey_allergy_code = models.JSONField()
    survey_disease_code = models.JSONField(blank=True, null=True)
    survey_function_code = models.JSONField(blank=True, null=True)
    survey_height = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0)])
    survey_weight = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0)])
    survey_created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        managed = True
        db_table = 'survey'



# 신규생성(2024.06.11)
class SurveyComCode(models.Model):
    survey_com_code_id = models.BigAutoField(primary_key=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    com_code_grp = models.ForeignKey(ComCodeGrp, on_delete=models.CASCADE, db_column='com_code_grp')
    com_code = models.ForeignKey(ComCode, on_delete=models.CASCADE, db_column='com_code')
    survey_com_code_rank = models.PositiveSmallIntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'survey_com_code'



# 신규생성(2024.06.10) → SurveyComCode 테이블로 병합(06.11)
# class SurveyCaution(models.Model):
#     # 해당 테이블은 survey 테이블의 survey_allergy_code, survey_disease_code 필드의 json 데이터 정합성을 위해 생성한 테이블
#     survey_caution_id = models.BigAutoField(primary_key=True)
#     survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
#     com_code_grp = models.ForeignKey(ComCodeGrp, on_delete=models.CASCADE)
#     com_code = models.ForeignKey(ComCode, on_delete=models.CASCADE)


#     class Meta:
#         managed = True
#         db_table = 'survey_caution'



# 신규생성(2024.06.10) → SurveyComCode 테이블로 병합(06.11)
# class SurveyFunction(models.Model):
#     # 해당 테이블은 survey 테이블의 survey_function_code 필드의 json 데이터 정합성을 위해 생성한 테이블
#     survey_function_id = models.BigAutoField(primary_key=True, unique=True)
#     survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
#     com_code_grp = models.ForeignKey(ComCodeGrp, on_delete=models.CASCADE)
#     com_code = models.ForeignKey(ComCode, on_delete=models.CASCADE)
#     survey_function_rank = models.PositiveSmallIntegerField()


#     class Meta:
#         managed = True
#         db_table = 'survey_function'



# # SurveyAllergy class 위치를 현 위치로 이동
# class SurveyAllergy(models.Model):
#     survey_allergy_id = models.BigAutoField(primary_key=True)
#     survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
#     allergy_code = models.ForeignKey(AllergyCode, on_delete=models.CASCADE, db_column='allergy_code')

#     class Meta:
#         managed = True
#         db_table = 'survey_allergy'



# # SurveyDisease class 위치를 현 위치로 이동
# class SurveyDisease(models.Model):
#     survey_disease_id = models.BigAutoField(primary_key=True)
#     survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
#     disease_code = models.ForeignKey(DiseaseCode, on_delete=models.CASCADE, db_column='disease_code')


#     class Meta:
#         managed = True
#         db_table = 'survey_disease'



# # SurveyFunction class 위치를 현 위치로 이동
# class SurveyFunction(models.Model):
#     survey_function_id = models.BigAutoField(primary_key=True)
#     survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
#     function_code = models.ForeignKey(FunctionCode, on_delete=models.CASCADE, db_column='function_code')
#     # function_code가 '해당 없음'일 경우 survey_function_rank를 null로 주기로 결정해서 모델 스키마 재 정의(2024.04.26)
#     # survey_function_rank = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
#     # survey_function_rank = models.IntegerField(null=True)

#     class Meta:
#         managed = True
#         db_table = 'survey_function'



class Product(models.Model):
    product_id = models.BigIntegerField(primary_key=True)
    product_name = models.TextField()
    product_company = models.CharField(max_length=100)
    product_instruction = models.TextField(blank=True, null=True)
    product_image = models.TextField(blank=True, null=True)
    product_storage_method = models.TextField(blank=True, null=True)
    product_dispos = models.CharField(max_length=20, blank=True, null=True)
    product_serving = models.TextField(blank=True, null=True)
    product_function_content = models.TextField(blank=True, null=True)
    product_caution_content = models.TextField(blank=True, null=True) 
    product_function_code = models.JSONField(blank=True, null=True) 
    product_caution_code = models.JSONField(blank=True, null=True) 
    product_ingredient_id = models.JSONField(blank=True, null=True)
    product_rating_avg = models.DecimalField(max_digits=3, decimal_places=2, default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    product_rating_cnt = models.PositiveIntegerField(default=0)
    
    class Meta:
        managed = True
        db_table = 'product'



class ProductIngredient(models.Model):
    product_ingredient_id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_column='ingredient_id')


    class Meta:
        managed = True
        db_table = 'product_ingredient'



class ProductComCode(models.Model):
    product_com_code_id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    com_code_grp = models.ForeignKey(ComCodeGrp, on_delete=models.CASCADE, db_column='com_code_grp')
    com_code = models.ForeignKey(ComCode, on_delete=models.CASCADE, db_column='com_code')


    class Meta:
        managed = True
        db_table = 'product_com_code'



class ProductReview(models.Model):
    product_review_id = models.AutoField(primary_key=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id') 
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    product_review_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0)
    product_review_content = models.CharField(max_length=200, blank=True, null=True)
    product_review_created_at = models.DateTimeField(auto_now_add=True)
    product_review_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    product_review_deleted_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'product_review'



class ProductLike(models.Model):
    product_like_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id') 
    product_like_page = models.CharField(max_length=50, blank=True, null=True)  
    product_like_created_at = models.DateTimeField(auto_now_add=True)
    product_like_deleted_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'product_like'



# class 이름 변경: ProductLog → product_view
class ProductView(models.Model):
    product_view_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id')
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    product_view_visited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    product_view_leaved_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    product_view_duration = models.PositiveIntegerField(blank=True, null=True)


    class Meta:
        managed = True
        db_table = 'product_view'



# class 이름 변경: Recommendation → Recom
class Recom(models.Model):
    recom_id = models.BigAutoField(primary_key=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user_id', related_name='recom_users')
    recom_created_at = models.DateTimeField(auto_now_add=True)
    # related_name='recommendations'이 설정하면
    # User 모델에서 Recommendation 모델로 역참조할 때 recommendations라는 속성을 사용할 수 있음
    # user.recommendations와 같이 사용하여 사용자와 관련된 모든 추천을 가져올 수 있음


    class Meta:
        managed = True
        db_table = 'recom'



# class 이름 변경: RecommendationIngredient → RecomIngredient
class RecomIngredient(models.Model):
    recom_ingredient_id = models.BigAutoField(primary_key=True)
    recom_id = models.ForeignKey(Recom, on_delete=models.CASCADE, db_column='recom_id')
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_column='ingredient_id')


    class Meta:
        managed = True
        db_table = 'recom_ingredient'



# class 이름 변경: RecommendationProduct → RecomSurveyProduct
class RecomSurveyProduct(models.Model):
    recom_survey_product_id = models.BigAutoField(primary_key=True)
    recom_id = models.ForeignKey(Recom, on_delete=models.CASCADE, db_column='recom_id')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')


    class Meta:
        managed = True
        db_table = 'recom_survey_product'



# class 신규 추가
class RecomSexAgeProduct(models.Model):
    recom_sex_age_product_id = models.BigAutoField(primary_key=True)
    recom_id = models.ForeignKey(Recom, on_delete=models.CASCADE, db_column='recom_id')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')


    class Meta:
        managed = True
        db_table = 'recom_sex_age_product'