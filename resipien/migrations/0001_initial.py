# Generated by Django 4.1.2 on 2022-10-31 10:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("general_user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="GalangDana",
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
                ("tujuan", models.CharField(max_length=20)),
                ("judul", models.CharField(max_length=255)),
                ("deskripsi", models.TextField()),
                ("terkumpul", models.PositiveIntegerField()),
                ("target", models.PositiveIntegerField()),
                ("gambar", models.ImageField(blank=True, upload_to="resipien/upload")),
                ("tanggal_pembuatan", models.DateField(auto_now_add=True)),
                ("tanggal_berakhir", models.DateField(default=None)),
                ("status_keaktifan", models.BooleanField(default=True)),
                (
                    "akun_bank",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="general_user.rekeningbank",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="general_user.generaluser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="KomentarGalang",
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
                ("username", models.CharField(max_length=40)),
                ("komentar", models.TextField()),
                ("tanggal_komentar", models.DateField(auto_now_add=True)),
                (
                    "objek_galang",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="resipien.galangdana",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="general_user.generaluser",
                    ),
                ),
            ],
        ),
    ]
