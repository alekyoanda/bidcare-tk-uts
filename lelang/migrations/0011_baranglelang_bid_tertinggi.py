# Generated by Django 4.1.2 on 2022-10-26 11:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lelang", "0010_komentar"),
    ]

    operations = [
        migrations.AddField(
            model_name="baranglelang",
            name="bid_tertinggi",
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
    ]
