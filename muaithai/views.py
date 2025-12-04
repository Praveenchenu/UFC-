from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.conf import settings
from openai import OpenAI

from .models import Fighter_Details, Carousel
from .forms import Fighter_form, SignUpForm, LoginForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Fighter Cards
def fighter_cards_view(request):
    fighters = Fighter_Details.objects.all().order_by('p4p_rank')[:6]
    carousel = Carousel.objects.all()
    return render(request, 'muaithai/fighter_cards.html', {'carousel': carousel, 'fighters': fighters})


# CRUD: Fighters
class CreateFighterView(CreateView):
    model = Fighter_Details
    fields = ['Name', 'Weight_class', 'Age', 'Prof_record', 'Image', 'p4p_rank']
    template_name = 'muaithai/fighter_register_form.html'
    success_url = reverse_lazy('readfighter')


class ReadFighterView(ListView):
    model = Fighter_Details
    template_name = 'muaithai/fighterInfoTable.html'
    context_object_name = 'fighterTable'
    paginate_by = 6

    def get_queryset(self):
        qs = Fighter_Details.objects.all().order_by('p4p_rank')
        selected_weight = self.request.GET.get('weight')
        if selected_weight:
            qs = qs.filter(Weight_class=selected_weight)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['weight_classes'] = Fighter_Details.objects.values_list('Weight_class', flat=True).distinct()
        context['selected_weight'] = self.request.GET.get('weight')
        return context


class FighterDetailsView(DetailView):
    model = Fighter_Details
    template_name = 'muaithai/detailspage.html'
    context_object_name = 'fighterDetails'


class UpdateFighterView(UpdateView):
    model = Fighter_Details
    fields = ['Name', 'Weight_class', 'Age', 'Prof_record', 'Image', 'p4p_rank']
    template_name = 'muaithai/fighter_register_form.html'
    success_url = reverse_lazy('readfighter')


class DeleteFighterView(DeleteView):
    model = Fighter_Details
    success_url = reverse_lazy('readfighter')


# Authentication
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("homepage")
    else:
        form = SignUpForm()
    lform = LoginForm()
    return render(request, "muaithai/auth.html", {"form": form, "lform": lform, "mode": "signup"})


def login_view(request):
    if request.method == "POST":
        lform = LoginForm(data=request.POST)
        if lform.is_valid():
            user = lform.get_user()
            login(request, user)
            return redirect("homepage")
    else:
        lform = LoginForm()
    form = SignUpForm()
    return render(request, "muaithai/auth.html", {"lform": lform, "form": form, "mode": "login"})


def logout_view(request):
    logout(request)
    return redirect("homepage")


# Search
def search_view(request):
    query = request.GET.get("q")
    fighters = Fighter_Details.objects.all()
    if query:
        fighters = fighters.filter(Name__icontains=query)
    carousel = Carousel.objects.all()
    return render(request, "muaithai/fighter_cards.html", {"fighters": fighters, "carousel": carousel})


# Chatbot
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=settings.OPENAI_API_KEY)


def chatbot_page(request):
    return render(request, "muaithai/chatbot.html")


def chatbot_response(request):
    user_message = request.GET.get("message", "")
    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)
    try:
        response = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct",
            messages=[
                {"role": "system", "content": """
                    You are a UFC fighters info providing assistant who:
                    - Always replies with short, factual summaries.
                    - Uses emojis to make responses friendly.
                    - If you don't know something, politely say you're unsure, and reply with related info.
                    - Include fighter stats only if available.
                    - Teach new fans about UFC rules and divisions in simple language.
                """},
                {"role": "user", "content": user_message}
            ]
        )
        bot_reply = response.choices[0].message["content"]
        return JsonResponse({"reply": bot_reply})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
