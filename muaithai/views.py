from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
# from django.contrib.auth.forms import AuthenticationForm
from .models import Fighter_Details, Carousel
from .forms import Fighter_form, SignUpForm, LoginForm

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers


#AI imports
from django.http import JsonResponse
from openai import OpenAI
from django.conf import settings


# @cache_page(60 * 10)
def fighterCards_view(request):
    fighters = Fighter_Details.objects.all().order_by('p4p_rank')[:6]
    carousel = Carousel.objects.all()
    return render(request, 'muaithai/fighter_cards.html', {'carousel': carousel, 'fighters' : fighters} )

# class fighterCards_view(ListView):
#     model = Fighter_Details
#     template_name = "muaithai/fighter_cards.html"
#     context_object_name = 'fighters'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['carousel'] = Carousel.objects.all()  # Add extra context
#         return context



# def CreateFighter_view(request ):
#     if request.method=="POST":
#         form = Fighter_form(request.POST, request.FILES )
#         if form.is_valid():
#             form.save()
#             return redirect('readfighter')
#     else:
#         form = Fighter_form() 
#     return render(request, 'muaithai/fighter_register_form.html', {'form':form})


class CreateFighter_view(CreateView):
    model = Fighter_Details
    fields = ['Name', 'Weight_class', 'Age', 'Prof_record', 'Image', 'p4p_rank']
    success_url = reverse_lazy('readfighter')
    context_object_name = 'form'


# def ReadFighter_view(request):
#     fighterTable = Fighter_Details.objects.all()
#     return render(request, 'muaithai/fighterInfoTable.html', {'fighterTable':fighterTable})


# def ReadFighter_view(request):
#     # get distinct weight classes for dropdown
#     weight_classes = Fighter_Details.objects.values_list('Weight_class', flat=True).distinct()

#     # check if a filter is applied
#     selected_weight = request.GET.get('weight')
#     if selected_weight:
#         fighterTable = Fighter_Details.objects.filter(Weight_class=selected_weight)
#     else:
#         fighterTable = Fighter_Details.objects.all().order_by('p4p_rank')

#     return render(request, 'muaithai/fighterInfoTable.html', {
#         'fighterTable': fighterTable,
#         'weight_classes': weight_classes,
#         'selected_weight': selected_weight,
#     })


class ReadFighter_view(ListView):
    model = Fighter_Details
    template_name = 'muaithai/fighterInfoTable.html'
    context_object_name = 'fighterTable'
    paginate_by = 6   # optional: adds pagination automatically

    def get_queryset(self):
        # base queryset
        qs = Fighter_Details.objects.all().order_by('p4p_rank')

        # filter by weight if provided
        selected_weight = self.request.GET.get('weight')
        if selected_weight:
            qs = qs.filter(Weight_class=selected_weight)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # distinct weight classes for dropdown
        context['weight_classes'] = Fighter_Details.objects.values_list(
            'Weight_class', flat=True
        ).distinct()
        # keep track of selected filter
        context['selected_weight'] = self.request.GET.get('weight')
        return context



# def fighterDetailsView(request, pk):
#     fighterDetails = get_object_or_404(Fighter_Details, pk=pk)
#     return render(request, 'muaithai/detailspage.html', {'fighterDetails': fighterDetails})


class fighterDetailsView(DetailView):
    model = Fighter_Details
    template_name = 'muaithai/detailspage.html'
    context_object_name = 'fighterDetails'


# def UpdateFighter_view(request, pk):
#     fighter = get_object_or_404(Fighter_Details, pk=pk)
#     if request.method =='POST':
#         form = Fighter_form(request.POST, request.FILES, instance=fighter)
#         if form.is_valid():
#             form.save()
#             return redirect('readfighter')
#     else:
#         form = Fighter_form(instance=fighter)
#     return render(request, 'muaithai/fighter_register_form.html', {'form':form})


class UpdateFighter_view(UpdateView):
    model = Fighter_Details
    fields = ['Name', 'Weight_class', 'Age', 'Prof_record', 'Image', 'p4p_rank']
    template_name_suffix = '_form'
    context_object_name = 'form'
    success_url = reverse_lazy('readfighter')


# def deleteFighter_view(request, pk):
#     fighter = get_object_or_404(Fighter_Details, pk=pk)
#     if request.method == "POST":
#         fighter.delete()
#     return redirect('readfighter')


class deleteFighter_view(DeleteView):
    model = Fighter_Details
    success_url = reverse_lazy('readfighter')


# def auth_view(request):
#     return render(request, 'muaithai/auth.html')


def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto-login after signup
            return redirect("homepage")  # redirect to home
        else:
            print(form.errors)
    else:
        form = SignUpForm()
    lform = LoginForm()
    return render(request, "muaithai/auth.html", {"form": form, "lform": lform, "mode": "signup"})



def login_view(request):
    if request.method == "POST":
        lform = LoginForm(data=request.POST)   # use custom
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


def search_view(request):
    query = request.GET.get("q")
    fighters = Fighter_Details.objects.all()
    if query:
        fighters = fighters.filter(Name__icontains=query)  # case-insensitive match

    carousel = Carousel.objects.all()  # your carousel items

    context = {
        "fighters": fighters,
        "carousel": carousel,
    }
    return render(request, "muaithai/fighter_cards.html", context)


# OpenRouter endpoint
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=settings.OPENAI_API_KEY
)

def chatbot_page(request):
    return render(request, "muaithai/chatbot.html")

def chatbot_response(request):
    user_message = request.GET.get("message", "")

    if not user_message:
        return JsonResponse({"error": "No message provided"}, status=400)

    try:
        # ✅ Works same as OpenAI
        response = client.chat.completions.create(
            # model="gpt-3.5-turbo",  # or try "mistralai/mistral-7b-instruct" (free model)
            model="mistralai/mistral-7b-instruct",
            messages=[

                # {"role": "system", "content": "You are a friendly UFC assistant."},

                {"role": "system", "content": """
                You are a UFC fighters info providing assistant who:
                - Always replies with short, factual summaries.
                - Uses emojis to make responses friendly.
                - If you don't know something, politely say you're unsure, and reply something related info.
                - Include fighter stats only if available in the provided context.
                - Use casual fight fan language.
                - “You teach new fans about UFC rules and divisions in a simple and educational tone.”
                """},


                {"role": "user", "content": user_message}
            ]
        )

        bot_reply = response.choices[0].message.content
        return JsonResponse({"reply": bot_reply})

    except Exception as e:
        print("Chatbot error:", e)
        return JsonResponse({"error": str(e)}, status=500)
