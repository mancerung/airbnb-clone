from django import forms
from . import models


class LoginForm(forms.Form):

    # email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Email"}))
    email = forms.CharField(widget=forms.CharField(attrs={"placeholder": "Email"}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )

    # clean_a + clean_b 합해서 clean으로 통합할수 있음.
    # 대신 return self.cleaned_data와 self.add_error(raise 대신)가 필요함
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        try:
            # user = models.User.objects.get(email=email)
            user = models.User.objects.get(username=email)
            if user.check_password(password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("email", forms.ValidationError("User does not exist"))


# ModelForm : 모델에 연결된 Form. form을 만들면 어떤 Model을 만들고 싶어하는지 안다.
# 특정 필드들을 Unique하게 만드는데 편리. user = super().save(commit=False)가 핵심
class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Name"}),
        }

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Confirm Password"})
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        try:
            models.User.objects.get(email=email)
            raise forms.ValidationError(
                "That email is already taken", code="existing_user"
            )
        except models.User.DoesNotExist:
            return email

    # clean_password로 하면 password1값을 불러오지 못함. 필드순서랑 상관있다.
    def clean_password1(self):
        password = self.cleaned_data.get("password")
        password1 = self.cleaned_data.get("password1")
        if password != password1:
            raise forms.ValidationError("Password confirmation does not match")
        else:
            return password

    def save(self, *args, **kwargs):
        # commit=False 뜻 : object는 생성하지만 DB에는 반영하지 않는다.
        user = super().save(commit=False)
        # 이메일과 비밀번호 추가 셋팅해서 DB에 저장
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        user.username = email
        user.set_password(password)
        user.save()