# Generated by Django 5.1.5 on 2025-06-13 02:18

import django_summernote.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Bot", "0007_alter_guide_content"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guide",
            name="content",
            field=django_summernote.fields.SummernoteTextField(),
        ),
    ]
