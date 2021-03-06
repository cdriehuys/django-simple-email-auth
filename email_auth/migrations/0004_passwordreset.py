# Generated by Django 2.2.2 on 2019-09-18 18:42

from django.db import migrations, models
import django.db.models.deletion
import email_auth.models


class Migration(migrations.Migration):

    dependencies = [("email_auth", "0003_rm_emailaddress_normalizedaddress")]

    operations = [
        migrations.CreateModel(
            name="PasswordReset",
            fields=[
                (
                    "time_created",
                    models.DateTimeField(
                        auto_now_add=True,
                        help_text="The time that the instance was created.",
                        verbose_name="creation time",
                    ),
                ),
                (
                    "time_sent",
                    models.DateTimeField(
                        blank=True,
                        help_text="The time that the token was emailed out.",
                        null=True,
                        verbose_name="sent time",
                    ),
                ),
                (
                    "time_updated",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="The time of the last update to the instance.",
                        verbose_name="last update time",
                    ),
                ),
                (
                    "token",
                    models.CharField(
                        default=email_auth.models.generate_token,
                        help_text="The random token identifying the password reset.",
                        max_length=64,
                        primary_key=True,
                        serialize=False,
                        verbose_name="token",
                    ),
                ),
                (
                    "email",
                    models.ForeignKey(
                        help_text="The email address that the reset token is sent to.",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="password_resets",
                        related_query_name="password_reset",
                        to="email_auth.EmailAddress",
                        verbose_name="email",
                    ),
                ),
            ],
            options={
                "verbose_name": "password reset",
                "verbose_name_plural": "password resets",
                "ordering": ("time_created",),
            },
        )
    ]
