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
from django.db import models
# from django.utils import timezone
# decimalfield 음수 허용 불가, 리뷰 제한을 위한 MinValueValidator 임포트
from django.core.validators import MinValueValidator, MaxValueValidator



class User(models.Model):
    custom_user_id = models.AutoField(primary_key=True)
    custom_user_email = models.CharField(unique=True, max_length=50)
    custom_user_password = models.TextField()
    custom_user_role = models.CharField(max_length=20)
    custom_user_status = models.CharField(max_length=10)
    custom_created_at = models.DateTimeField(auto_now_add=True)
    custom_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    cumstom_deleted_at = models.DateTimeField(blank=True, null=True)
    custom_last_login = models.DateTimeField(auto_now=True, blank=True, null=True)


    class Meta:
        
        db_table = 'user'



class Profile(models.Model):
    profile_id = models.AutoField(primary_key=True)
    custom_user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='custom_user_id')
    profile_name = models.CharField(max_length=20)
    profile_birth = models.DateField()
    profile_status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        
        db_table = 'profile'



class AllergyCode(models.Model):
    allergy_code = models.CharField(primary_key=True, max_length=20)
    allergy_code_name = models.CharField(max_length=50)
    allergy_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)


    class Meta:
        
        db_table = 'allergy_code'



class DiseaseCode(models.Model):
    disease_code = models.CharField(primary_key=True, max_length=20)
    disease_code_name = models.CharField(max_length=50)
    disease_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)


    class Meta:
        
        db_table = 'disease_code'



class FunctionCode(models.Model):
    function_code = models.CharField(primary_key=True, max_length=20)
    function_code_name = models.CharField(max_length=50)
    function_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)


    class Meta:
        
        db_table = 'function_code'



class ComCodeGrp(models.Model):
    com_code_grp = models.CharField(primary_key=True, max_length=10)
    com_code_grp_name = models.CharField(max_length=10)
    com_code_grp_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)


    class Meta:
        
        db_table = 'com_code_grp'



class ComCode(models.Model):
    com_code = models.CharField(primary_key=True, max_length=10)
    com_code_grp = models.ForeignKey(ComCodeGrp, on_delete=models.CASCADE, db_column='com_code_grp')
    com_code_name = models.CharField(max_length=50)
    com_code_desc = models.CharField(max_length=500, blank=True, null=True)
    use_yn = models.CharField(max_length=1)


    class Meta:
        
        db_table = 'com_code'
    


class Ingredient(models.Model):
    ingredient_id = models.AutoField(primary_key=True)
    ingredient_name = models.CharField(max_length=100)
    ingredient_limit_high = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True, validators=[MinValueValidator(0)])
    ingredient_limit_low = models.DecimalField(max_digits=15, decimal_places=10, blank=True, null=True, validators=[MinValueValidator(0)])
    ingredient_unit = models.CharField(max_length=10, blank=True, null=True)
    ingredient_function_content = models.TextField(blank=True, null=True)
    ingredient_caution = models.TextField(blank=True, null=True)
    ingredient_type = models.CharField(max_length=10, blank=True, null=True)

    
    class Meta:
        
        db_table = 'ingredient'



class IngredientFunction(models.Model):
    ingredient_function_id = models.AutoField(primary_key=True)
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_column='ingredient_id')
    function_code = models.ForeignKey(FunctionCode, on_delete=models.CASCADE, db_column='function_code')


    class Meta:
        
        db_table = 'ingredient_function'



class Survey(models.Model):
    survey_id = models.BigAutoField(primary_key=True)
    custom_user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='custom_user_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id')
    survey_age_group = models.CharField(max_length=20)
    survey_sex = models.CharField(max_length=1)
    survey_pregnancy_code = models.CharField(max_length=10)
    survey_operation_code = models.CharField(max_length=10, blank=True, null=True)
    survey_alcohol_code = models.CharField(max_length=10, blank=True, null=True)
    survey_smoke = models.CharField(max_length=1, blank=True, null=True)
    survey_height = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0)])
    survey_weight = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        
        db_table = 'survey'



class SurveyAllergy(models.Model):
    survey_allergy_id = models.BigAutoField(primary_key=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    allergy_code = models.ForeignKey(AllergyCode, on_delete=models.CASCADE, db_column='allergy_code')

    class Meta:
        
        db_table = 'survey_allergy'


class SurveyDisease(models.Model):
    survey_disease_id = models.BigAutoField(primary_key=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    disease_code = models.ForeignKey(DiseaseCode, on_delete=models.CASCADE, db_column='disease_code')


    class Meta:
        
        db_table = 'survey_disease'



class SurveyFunction(models.Model):
    survey_function_id = models.BigAutoField(primary_key=True)
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    function_code = models.ForeignKey(FunctionCode, on_delete=models.CASCADE, db_column='function_code')
    # function_code가 '해당 없음'일 경우 survey_function_rank를 null로 주기로 결정해서 모델 스키마 재 정의(2024.04.26)
    # survey_function_rank = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    survey_function_rank = models.IntegerField(null=True)

    class Meta:
        
        db_table = 'survey_function'



class Product(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    product_company = models.CharField(max_length=50)
    product_instruction = models.TextField(blank=True, null=True)
    product_function_content = models.TextField(blank=True, null=True)
    product_caution = models.TextField(blank=True, null=True)
    product_serving = models.TextField(blank=True, null=True)
    product_dispos = models.CharField(max_length=20, blank=True, null=True)
    product_storage_method = models.TextField(blank=True, null=True)
    product_image = models.TextField(blank=True, null=True)
    product_rating_avg = models.DecimalField(max_digits=3, decimal_places=2, validators=[MinValueValidator(0), MaxValueValidator(5)])
    product_rating_cnt = models.PositiveIntegerField()

    class Meta:
        
        db_table = 'product'



class ProductFunction(models.Model):
    product_function_id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    function_code = models.ForeignKey(FunctionCode,  on_delete=models.CASCADE, db_column='function_code')

    class Meta:
        
        db_table = 'product_function'



class ProductIngredient(models.Model):
    product_ingredient_id = models.BigAutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    ingredient_id = models.ForeignKey(Ingredient,  on_delete=models.CASCADE, db_column='ingredient_id')


    class Meta:
        
        db_table = 'product_ingredient'



class ProductReview(models.Model):
    product_review_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id') 
    product_review_rating = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
    product_review_content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        
        db_table = 'product_review'



class ProductLike(models.Model):
    product_like_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id') 
    custom_user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='custom_user_id')
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(blank=True, null=True)


    class Meta:
        
        db_table = 'product_like'



class ProductLog(models.Model):
    product_log_id = models.AutoField(primary_key=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id')
    visited_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    leaved_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    product_log_duration = models.PositiveIntegerField(blank=True, null=True)


    class Meta:
        
        db_table = 'product_log'



class Recommendation(models.Model):
    recommendation_id = models.BigAutoField(primary_key=True)
    custom_user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='custom_user_id', related_name='recommendations_user')
    survey_id = models.ForeignKey(Survey, on_delete=models.CASCADE, db_column='survey_id')
    created_at = models.DateTimeField(auto_now_add=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, db_column='profile_id')
    

# related_name='recommendations'이 설정하면
# User 모델에서 Recommendation 모델로 역참조할 때 recommendations라는 속성을 사용할 수 있음
# user.recommendations와 같이 사용하여 사용자와 관련된 모든 추천을 가져올 수 있음
    class Meta:
        
        db_table = 'recommendation'



class RecommendationIngredient(models.Model):
    recommendation_ingredient_id = models.BigAutoField(primary_key=True)
    recommendation_id = models.ForeignKey(Recommendation,  on_delete=models.CASCADE, db_column='recommendation_id')
    ingredient_id = models.ForeignKey(Ingredient, on_delete=models.CASCADE, db_column='ingredient_id')

    class Meta:
        
        db_table = 'recommendation_ingredient'



class RecommendationProduct(models.Model):
    recommendation_product_id = models.BigAutoField(primary_key=True)
    recommendation_id = models.ForeignKey(Recommendation, on_delete=models.CASCADE, db_column='recommendation_id')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product_id')


    class Meta:
        
        db_table = 'recommendation_product'
