from django.contrib import admin

from dw.models import Pet, User, WalkOrder, Walker


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    pass


@admin.register(Walker)
class WalkerAdmin(admin.ModelAdmin):
    pass


@admin.register(WalkOrder)
class WalkOrderAdmin(admin.ModelAdmin):
    pass

