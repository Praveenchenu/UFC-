from django.contrib import admin
from .models import Fighter_Details, Carousel

# Register your models here.
@admin.register(Fighter_Details)
class fighter_details_admin(admin.ModelAdmin):
    list_display = ('Name', 'Weight_class', 'Age', 'Prof_record')
    search_fields = ('Name','Weight_class' )


@admin.register(Carousel)
class carousel_admin(admin.ModelAdmin):
    list_display = ('title', 'description')
    search_fields = ('title',)

