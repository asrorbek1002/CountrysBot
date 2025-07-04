# Generated by Django 5.1.5 on 2025-06-13 16:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Bot", "0010_guide_status"),
    ]

    operations = [
        migrations.CreateModel(
            name="Appeal",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "message_id",
                    models.BigIntegerField(
                        blank=True, null=True, verbose_name="Murojaat xabar ID"
                    ),
                ),
                ("message", models.TextField(verbose_name="Murojaat matni")),
                ("status", models.BooleanField(default=False, verbose_name="Holat")),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Yaratilgan sana"
                    ),
                ),
                (
                    "admin",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="admin_appeals",
                        to="Bot.telegramuser",
                        verbose_name="Admin",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Bot.telegramuser",
                        verbose_name="Foydalanuvchi",
                    ),
                ),
            ],
            options={
                "verbose_name": "Appeal",
                "verbose_name_plural": "Appeals",
            },
        ),
    ]
