from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import EmailField
from django.shortcuts import render, redirect


def user_login(request: "HttpRequest") -> "HttpResponse":
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                form.add_error(None, "Invalid email address or password")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()
    return render(request, "users/login.html", {"form": form})


class LoginForm(AuthenticationForm):
    username = EmailField()

    def clean_password(self) -> str:
        password = self.cleaned_data.get("password")
        try:
            validate_password(password)
        except ValidationError as e:
            for error in e:
                self.add_error("password", error)

        return password

    def add_error(self, field: str, error: str) -> None:
        if field:
            self.errors[field] = self.error_class([error])
        else:
            self.errors["non_field_errors"] = self.error_class([error])
