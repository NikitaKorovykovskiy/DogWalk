from django.contrib import admin

from dw.models import Pet, User, WalkOrder, Walker


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "phone")
    fields = ("first_name", "last_name", "phone")

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass


@admin.register(Walker)
class WalkerAdmin(admin.ModelAdmin):
    pass


@admin.register(WalkOrder)
class WalkOrderAdmin(admin.ModelAdmin):
    list_display = ("walker", "pet", "user", "start_time")
    fields = ("user", "pet", "walker", "start_time", "end_time", "comment")

