from django import forms
from users.models import Profile


# class ProfileView(forms.Form):
#     class Meta:
#         model = Profile
#         fields = ["profile_name"]


class ProfileInfo(forms.Form):
    nickname = forms.CharField(widget=forms.TextInput, required=True)
    birth = forms.DateField(required=True)   # '$y/%d/%m'
    sex = forms.ChoiceField(choices=[("f", "여자"), ("m", "남자")], required=True)
    pregnancy = forms.ChoiceField(choices=[("P3", "임신 중"), ("P2", "수유 중"), ("P1", "임신 계획 중"), ("P0", "해당 사항 없음")], required=True)
    allergy = forms.CharField(widget=forms.TextInput, required=True)
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
    nickname = forms.CharField(widget=forms.TextInput, required=True)
    birth = forms.DateField(widget=forms.DateInput(format='%Y/%d/%m', attrs={"type":"date",}), required=True)
    # choicefield = (DB 저장값, 사용자에게 표시할 값)
    sex = forms.ChoiceField(choices=[("f", "여자"), ("m", "남자")], required=True)
    pregnancy = forms.ChoiceField(choices=[("P3", "임신 중"), ("P2", "수유 중"), ("P1", "임신 계획 중"), ("P0", "해당 사항 없음")], required=True)
    # 알레르기 >> 선택 방법 미확정
    allergy = forms.CharField(widget=forms.TextInput, required=True)

class Survey2Form(forms.Form):
    # 건강고민 >> 카테고리 미확정
    pass

class Survey3Form(forms.Form):
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