from django import forms
from users.models import Profile



class ProfileInfo(forms.Form):
    nickname = forms.CharField(widget=forms.TextInput, required=True)
    birth = forms.DateField(required=True)   # '$y/%d/%m'
    sex = forms.ChoiceField(choices=[("f", "여자"), ("m", "남자")], required=True)
    pregnancy = forms.ChoiceField(choices=[("P3", "임신 중"), ("P2", "수유 중"), ("P1", "임신 계획 중"), ("P0", "해당 사항 없음")], required=True)
    allergy = forms.CharField(widget=forms.TextInput, required=True)
    # function
    height = forms.DecimalField(max_digits=4, 
                                decimal_places=2, 
                                widget=forms.TextInput(attrs={"placeholder": "cm"}),
                                required=False)
    weight = forms.DecimalField(max_digits=4, 
                                decimal_places=2, 
                                widget=forms.TextInput(attrs={"placeholder": "kg"}),
                                required=False)
    smoke = forms.ChoiceField(choices=[("y", "흡연 중"), ("n", "비흡연")], required=False)
    disease = forms.CharField(widget=forms.TextInput, required=False)
    alcohol = forms.ChoiceField(choices=[("A3", "주 4회 이상"), ("A2", "주 2~3회"), ("A1", "주 1회"), ("A0", "거의 마시지 않음")], required=False)

    class Meta:
        model = Profile
        fields = '__all__'


class Survey1Form(forms.Form):
    # profile_name (profile model)
    nickname = forms.CharField(label="프로필명", widget=forms.TextInput, required=True)
    # profile_birth (profile model)
    birth = forms.DateField(label="생년월일", input_formats=["%Y-%m-%d"], widget=forms.DateInput(attrs={"placeholder": "2000-01-01"}), required=True)
    # birth = forms.DateField(label="생년월일", widget=forms.DateInput(format='%Y-%m-%d', attrs={"type":"date",}), required=True)
    # survey_sex (survey model)   ## choicefield = (DB 저장값, 사용자에게 표시할 값)
    sex = forms.ChoiceField(label="성별", choices=[("f", "여자"), ("m", "남자")], required=True)
    # survey_pregnancy_code (survey model)
    pregnancy = forms.ChoiceField(label="임신 상태", choices=[("P3", "임신 중"), ("P2", "수유 중"), ("P1", "임신 계획 중"), ("P0", "해당 사항 없음")], required=True)
    # allergy_code_name (allergycode model)
    allergy = forms.MultipleChoiceField(label="알레르기 상태", widget=forms.CheckboxSelectMultiple, required=True,
                                        choices=[("AL00", "해당 사항 없음"), ("AL01", "게 또는 새우 등의 갑각류"), ("AL02", "옻"), ("AL03", "땅콩"), ("AL04", "프로폴리스"),
                                                 ("AL05", "대두 및 대두단백"), ("AL06", "에스트로겐, 대두 이소플라본"), ("AL07", "우유 및 유제품"), ("AL08", "소맥"), ("AL09", "호프"), 
                                                 ("AL10", "호박씨"), ("AL11", "홍삼"), ("AL12", "사상자"), ("AL13", "산수유"), ("AL14", "무화과"), 
                                                 ("AL15", "사과"), ("AL16", "국화과"), ("AL17", "난화"), ("AL18", "달맞이꽃종자유"), ("AL19", "석류"), 
                                                 ("AL20", "강황")])


class Survey2Form(forms.Form):
    # function_code_name (functioncode model) 
    function = forms.MultipleChoiceField(label="최대 5개 선택", widget=forms.CheckboxSelectMultiple,
                                         choices=[("HF01", "간"), ("HF02", "피로개선"), ("HF03", "뼈/관절"), ("HF04", "치아/구강"), ("HF05", "면역개선"), ("HF06", "노화/항산화"), 
                                                  ("HF07", "피부"), ("HF08", "눈"), ("HF09", "위/소화"), ("HF10", "장 건강"), ("HF11", "비뇨"), ("HF12", "요로"), 
                                                  ("HF13", "전립선"), ("HF14", "남성 건강"), ("HF15", "여성 갱년기"), ("HF16", "여성 건강"), ("HF17", "운동 능력"), ("HF18", "체지방 감소"), 
                                                  ("HF19", "스트레스/수면"), ("HF20", "두뇌 활동"), ("HF21", "어린이 성장"), ("HF22", "혈당"), ("HF23", "혈압"), ("HF24", "혈관/혈액순환"),
                                                  ("HF25", "임산/태아건강")])
    

class Survey3Form(forms.Form):
    # survey_height (survey model)
    height = forms.DecimalField(label="키", max_digits=4, decimal_places=2, required=False,
                                widget=forms.TextInput(attrs={"placeholder": "cm로 입력하세요"}))
    # survey_weight (survey model)
    weight = forms.DecimalField(label="몸무게", max_digits=4, decimal_places=2, required=False,
                                widget=forms.TextInput(attrs={"placeholder": "kg로 입력하세요"}))
    # survey_smoke (survey model)
    smoke = forms.ChoiceField(label="흡연 상태", required=False,
                              choices=[("y", "흡연 중"), ("n", "비흡연")])
    # disease_code (diseasecode model)
    disease = forms.MultipleChoiceField(label="기저질환 상태", widget=forms.CheckboxSelectMultiple, required=False, 
                              choices=[("DI01", "위 및 장 관련 질환"), ("DI02", "간 관련 질환"), ("DI03", "심장/혈관 관련 질환"), ("DI04", "신장/콩팥 관련 질환"), ("DI05", "당뇨"), 
                                       ("DI06", "고혈압"), ("DI07", "고지혈증"), ("DI08", "혈액응고장애"), ("DI09", "갑상선 관련 질환"), ("DI10", "천식"), 
                                       ("DI11", "담당/쓸개 관련 질환"), ("DI12", "자가면역 및 면역 억제제 복용"), ("DI13", "신경 및 정신계 질환"), ("DI14", "암"), ("DI15", "단장증후군 및 유당불내증"), 
                                       ("DI16", "피부 광과민성"), ("DI17", "호르몬제(경구 피임약) 복용"), ])
    # survey_alcohol_code (survey model)
    alcohol = forms.ChoiceField(label="음주 상태", 
                                choices=[("A3", "주 4회 이상"), ("A2", "주 2~3회"), ("A1", "주 1회"), ("A0", "거의 마시지 않음")], 
                                required=False)