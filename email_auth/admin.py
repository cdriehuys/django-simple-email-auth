from django.contrib import admin

from email_auth import models


@admin.register(models.EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    """
    Admin for the ``EmailAddress`` model.
    """

    autocomplete_fields = ("user",)
    date_hierarchy = "time_created"
    fields = (
        "address",
        "normalized_address",
        "user",
        "is_verified",
        "time_verified",
        "time_created",
        "time_updated",
    )
    list_display = (
        "address",
        "user",
        "is_verified",
        "time_verified",
        "time_created",
        "time_updated",
    )
    list_filter = ("is_verified",)
    readonly_fields = ("normalized_address", "time_created", "time_updated")
    search_fields = ("address", "normalized_address")
