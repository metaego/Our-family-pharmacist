from django import forms
from datetime import datetime
from django.core.exceptions import ValidationError

class Survey1Form(forms.Form):
    # profile_name (profile model)
    name = forms.CharField(label="프로필명", widget=forms.TextInput, required=True)
    # profile_birth (profile model)
    birth = forms.DateField(label="생년월일", input_formats=["%Y-%m-%d"], widget=forms.DateInput(attrs={"placeholder": "2000-01-01"}), required=True)
    # survey_sex (survey model)   ## choicefield = (DB 저장값, 사용자에게 표시할 값)
    sex = forms.ChoiceField(label="성별", choices=[(None, "선택"), ("f", "여자"), ("m", "남자")], required=True)
    # survey_pregnancy_code (survey model)
    pregnancy = forms.ChoiceField(label="임신 상태", choices=[(None, "선택"), ("P3", "임신 중"), ("P2", "수유 중"), ("P1", "임신 계획 중"), ("P0", "해당 사항 없음")], required=True)
    # allergy_code_name (allergycode model)
    allergy = forms.MultipleChoiceField(label="알레르기 상태", widget=forms.CheckboxSelectMultiple, required=True,
                                        choices=[("AL00", "해당 사항 없음"), ("AL01", "게 또는 새우 등의 갑각류"), ("AL02", "옻"), ("AL03", "땅콩"), ("AL04", "프로폴리스"),
                                                 ("AL05", "대두 및 대두단백"), ("AL06", "에스트로겐, 대두 이소플라본"), ("AL07", "우유 및 유제품"), ("AL08", "소맥"), ("AL09", "호프"), 
                                                 ("AL10", "호박씨"), ("AL11", "홍삼"), ("AL12", "사상자"), ("AL13", "산수유"), ("AL14", "무화과"), 
                                                 ("AL15", "사과"), ("AL16", "국화과"), ("AL17", "난화"), ("AL18", "달맞이꽃종자유"), ("AL19", "석류"), 
                                                 ("AL20", "강황")])

    def clean_birth(self):
        # 만나이 계산
        profile_birth = str(self.cleaned_data['birth'])
        birth = datetime.strptime(profile_birth, '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - int(profile_birth[:4])
        if today.month < birth.month:
            age -= 1
        elif today.month == birth.month and today.day < birth.day:
            age -= 1
        if age < 6:
            raise ValidationError('만 6세 미만은 서비스 이용이 불가합니다.')
        return birth
    
    def age_group(self):
        # 만나이 계산
        profile_birth = str(self.cleaned_data['birth'])
        birth = datetime.strptime(profile_birth, '%Y-%m-%d').date()
        today = datetime.now().date()
        age = today.year - int(profile_birth[:4])
        if today.month < birth.month:
            age -= 1
        elif today.month == birth.month and today.day < birth.day:
            age -= 1
        if age >= 6:
            if age <=8:
                age_group = '6~8세'
            elif age <= 11:
                age_group = '9~11세'
            elif age <= 14:
                age_group = '12~14세'
            elif age <= 18:
                age_group = '15~18세'
            elif age <= 29:
                age_group = '20대'
            elif age <= 39:
                age_group = '30대'
            elif age <= 49:
                age_group = '40대'
            elif age <= 59:
                age_group = '50대'
            elif age <= 69:
                age_group = '60대'
            elif age <= 79:
                age_group = '70대'
            elif age >= 80:
                age_group = '80세 이상'
            return age_group

    def clean_pregnancy(self):
        if self.cleaned_data['sex'] == 'm':
            if self.cleaned_data['pregnancy'] == 'P0':
                return self.cleaned_data['pregnancy']
            else:
                raise ValidationError('임신 상태를 확인해 주세요.')
        else:
            return self.cleaned_data['pregnancy']
            
    def allergy_json(self):
        json_data = {}
        if self.cleaned_data.get('allergy'):
            json_data['ALLERGY'] = self.cleaned_data['allergy']
        return json_data
    
    def edit_save(self, profile_instance, survey_instance):
        profile_instance.profile_name = self.cleaned_data['name']
        profile_instance.profile_birth = self.cleaned_data['birth']
        profile_instance.save()
        survey_instance.survey_sex = self.cleaned_data['sex']
        survey_instance.survey_age_group = self.age_group()
        survey_instance.survey_pregnancy_code = self.clean_pregnancy()
        survey_instance.survey_allergy_code = self.allergy_json()
        survey_instance.save()



class Survey2Form(forms.Form):
    # function_code_name (functioncode model) 
    function_list = [(None, "선택"), ("HF01", "간"), ("HF02", "피로개선"), ("HF03", "뼈/관절"), ("HF04", "치아/구강"), ("HF05", "면역개선"), ("HF06", "노화/항산화"), 
                     ("HF07", "피부"), ("HF08", "눈"), ("HF09", "위/소화"), ("HF10", "장 건강"), ("HF11", "비뇨"), ("HF12", "요로"), 
                     ("HF13", "전립선"), ("HF14", "남성 건강"), ("HF15", "여성 갱년기"), ("HF16", "여성 건강"), ("HF17", "운동 능력"), ("HF18", "체지방 감소"), 
                     ("HF19", "스트레스/수면"), ("HF20", "두뇌 활동"), ("HF21", "어린이 성장"), ("HF22", "혈당"), ("HF23", "혈압"), ("HF24", "혈관/혈액순환"),
                     ("HF25", "임산/태아건강")]

    function1 = forms.ChoiceField(label="1순위", required=False, choices=function_list)
    function2 = forms.ChoiceField(label="2순위", required=False, choices=function_list)
    function3 = forms.ChoiceField(label="3순위", required=False, choices=function_list)
    function4 = forms.ChoiceField(label="4순위", required=False, choices=function_list)
    function5 = forms.ChoiceField(label="5순위", required=False, choices=function_list)

    def clean(self):
        cleaned_data = super().clean()
        survey_age_group = cleaned_data.get('survey_age_group')
        survey_sex = cleaned_data.get('survey_sex')
        survey_function_field = [cleaned_data.get('function1'),
                                 cleaned_data.get('function2'),
                                 cleaned_data.get('function3'),
                                 cleaned_data.get('function4'),
                                 cleaned_data.get('function5')]
        if not (survey_age_group == '6~8세' or survey_age_group == '9세~11세'):
            if ('HF21' in survey_function_field):
                self.add_error("function1", "어린이 성장 선택 불가 대상입니다.")
                self.add_error("function2", "어린이 성장 선택 불가 대상입니다.")
                self.add_error("function3", "어린이 성장 선택 불가 대상입니다.")
                self.add_error("function4", "어린이 성장 선택 불가 대상입니다.")
                self.add_error("function5", "어린이 성장 선택 불가 대상입니다.")
        if survey_sex == 'f' and ('HF13' in survey_function_field or 'HF14' in survey_function_field):
            self.add_error("function1", "전립선, 남성 건강 선택 불가 대상입니다.")
            self.add_error("function2", "전립선, 남성 건강 선택 불가 대상입니다.")
            self.add_error("function3", "전립선, 남성 건강 선택 불가 대상입니다.")
            self.add_error("function4", "전립선, 남성 건강 선택 불가 대상입니다.")
            self.add_error("function5", "전립선, 남성 건강 선택 불가 대상입니다.")
        if survey_sex == 'm' and ('HF15' in survey_function_field or 'HF16' in survey_function_field):
            self.add_error("function1", "여성 갱년기, 여성 건강 선택 불가 대상입니다.")
            self.add_error("function2", "여성 갱년기, 여성 건강 선택 불가 대상입니다.")
            self.add_error("function3", "여성 갱년기, 여성 건강 선택 불가 대상입니다.")
            self.add_error("function4", "여성 갱년기, 여성 건강 선택 불가 대상입니다.")
            self.add_error("function5", "여성 갱년기, 여성 건강 선택 불가 대상입니다.")
        return cleaned_data

    def function_json(self):
        json_data = {}
        if self.cleaned_data.get('function1'):
            json_data['1st'] = self.cleaned_data['function1']
        if self.cleaned_data.get('function2'):
            json_data['2nd'] = self.cleaned_data['function2']
        if self.cleaned_data.get('function3'):
            json_data['3rd'] = self.cleaned_data['function3']
        if self.cleaned_data.get('function4'):
            json_data['4th'] = self.cleaned_data['function4']
        if self.cleaned_data.get('function5'):
            json_data['5th'] = self.cleaned_data['function5']     
        if not json_data:
            json_data['1st'] = 'HF00'
        return json_data

    def edit_save(self, survey_instance):
        survey_instance.survey_function_code = self.function_json()
        survey_instance.save()



class Survey3Form(forms.Form):
    # survey_height (survey model)
    height = forms.DecimalField(label="키", required=False,
                                widget=forms.TextInput(attrs={"placeholder": "cm로 입력하세요"}))
    # survey_weight (survey model)
    weight = forms.DecimalField(label="몸무게", required=False,
                                widget=forms.TextInput(attrs={"placeholder": "kg로 입력하세요"}))
    # survey_smoke (survey model)
    smoke = forms.ChoiceField(label="흡연 상태", required=False, 
                              choices=[("S9", "선택"), ("S1", "흡연 중"), ("S0", "비흡연")])
    # survey_alcohol_code (survey model)
    alcohol = forms.ChoiceField(label="음주 상태", required=False, 
                                choices=[("A9", "선택"), ("A3", "주 4회 이상"), ("A2", "주 2~3회"), ("A1", "주 1회"), ("A0", "거의 마시지 않음")])
    # survey_alcohol_code (survey model)
    operation = forms.ChoiceField(label="수술 상태", required=False, 
                                choices=[("O9", "선택"), ("O3", "수술 전"), ("O2", "수술 후"), ("O1", "수술 이전"), ("O0", "해당 사항 없음")])

    # disease_code (diseasecode model)
    disease = forms.MultipleChoiceField(label="기저질환 상태 (최대 5개 선택)", widget=forms.CheckboxSelectMultiple, required=False, 
                                        choices=[("DI01", "위 및 장 관련 질환"), ("DI02", "간 관련 질환"), ("DI03", "심장/혈관 관련 질환"), ("DI04", "신장/콩팥 관련 질환"), ("DI05", "당뇨"), 
                                                ("DI06", "고혈압"), ("DI07", "고지혈증"), ("DI08", "혈액응고장애"), ("DI09", "갑상선 관련 질환"), ("DI10", "천식"), 
                                                ("DI11", "담당/쓸개 관련 질환"), ("DI12", "자가면역 및 면역 억제제 복용"), ("DI13", "신경 및 정신계 질환"), ("DI14", "암"), ("DI15", "단장증후군 및 유당불내증"), 
                                                ("DI16", "피부 광과민성"), ("DI17", "호르몬제(경구 피임약) 복용")])

    def clean_disease(self):
        disease_codes = self.cleaned_data['disease']
        if len(disease_codes) > 5:
            raise ValidationError(f'최대 선택 수를 초과하였습니다.')
        else:
            return disease_codes  
              
    def disease_json(self):
        json_data = {}
        if self.cleaned_data.get('disease'):
            json_data['DISEASE'] = self.cleaned_data['disease']
        if not json_data:
            json_data['DISEASE'] = 'DI00'
        return json_data

    def edit_save(self, survey_instance):
        survey_instance.survey_height = self.cleaned_data['height']
        survey_instance.survey_weight = self.cleaned_data['weight']
        survey_instance.survey_smoking_code = self.cleaned_data['smoke']
        survey_instance.survey_alcohol_code = self.cleaned_data['alcohol']
        survey_instance.survey_operation_code = self.cleaned_data['operation']
        survey_instance.survey_disease_code = self.disease_json()
        survey_instance.save()