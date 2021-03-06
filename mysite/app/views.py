# made by yasunaga kyohei
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView

from app.forms import SignUpForm
from app.models import ImageChoice


class SignUpView(CreateView):
    """View for sign up.

    Author:
        Kyohei Yasunaga
        Masato Umakoshi
    """
    def post(self, request, *args, **kwargs):
        """
        Basic function: Yasunaga
        Image choice: Umakoshi
        """

        form_data = request.POST
        user_img = form_data.get("user_img", "1")

        choice2img_path = {
            str(i): f'img/user_icon_{i}.png' for i in range(1, 6)
        }
        url_path = choice2img_path[user_img]

        form = SignUpForm(data=form_data)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username,
                                email=email,
                                password=password)
            img_choice = ImageChoice(user=user, url_path=url_path)
            img_choice.save()
            login(request, user)
            return redirect("/")
        return render(request, "app/signup.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        return render(request, "app/signup.html", {"form": form})

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())
