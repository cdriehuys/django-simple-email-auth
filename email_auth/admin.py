from django.contrib import admin

from email_auth import models


class EmailVerificationInline(admin.TabularInline):
    """
    Inline display for email verifications.
    """

    extra = 0
    fields = ("email", "token", "time_sent", "time_created", "time_updated")
    model = models.EmailVerification
    readonly_fields = fields

    # Disable adding new verification tokens through the inline since
    # the behavior is broken. We could not solve the issue of tokens
    # added through the inline not being persisted upon saving the
    # parent email address.
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(models.EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    """
    Admin for the ``EmailAddress`` model.
    """

    autocomplete_fields = ("user",)
    date_hierarchy = "time_created"
    fields = (
        "address",
        "user",
        "is_verified",
        "time_verified",
        "time_created",
        "time_updated",
    )
    inlines = (EmailVerificationInline,)
    list_display = (
        "address",
        "user",
        "is_verified",
        "time_verified",
        "time_created",
        "time_updated",
    )
    list_filter = ("is_verified",)
    readonly_fields = ("time_created", "time_updated")
    search_fields = ("address",)


@admin.register(models.EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """
    Admin for the ``EmailVerification`` model.
    """

    autocomplete_fields = ("email",)
    date_hierarchy = "time_created"
    fields = ("email", "token", "time_sent", "time_created", "time_updated")
    list_display = ("email", "time_sent", "time_created", "time_updated")
    readonly_fields = ("time_created", "time_sent", "time_updated", "token")
    search_fields = ("email__address", "token")


@admin.register(models.PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):
    """
    Admin for the ``PasswordReset`` model.
    """

    autocomplete_fields = ("email",)
    date_hierarchy = "time_created"
    fields = ("email", "token", "time_sent", "time_created", "time_updated")
    list_display = ("email", "time_sent", "time_created", "time_updated")
    readonly_fields = ("time_created", "time_sent", "time_updated", "token")
    search_fields = ("email__address", "token")
