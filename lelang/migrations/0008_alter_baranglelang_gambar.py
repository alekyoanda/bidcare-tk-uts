# Generated by Django 4.1.2 on 2022-10-25 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lelang", "0007_alter_baranglelang_gambar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="baranglelang",
            name="gambar",
            field=models.ImageField(
                default="/lelang/upload/product-image-placeholder.jpg",
                upload_to="lelang/upload",
            ),
        ),
    ]
