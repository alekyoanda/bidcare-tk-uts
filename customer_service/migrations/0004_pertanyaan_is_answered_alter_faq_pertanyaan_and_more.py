# Generated by Django 4.1.2 on 2022-10-27 03:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_service', '0003_remove_faq_is_answered_alter_faq_jawaban'),
    ]

    operations = [
        migrations.AddField(
            model_name='pertanyaan',
            name='is_answered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='faq',
            name='pertanyaan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_service.pertanyaan'),
        ),
        migrations.AlterField(
            model_name='pertanyaan',
            name='teks_pertanyaan',
            field=models.TextField(max_length=500),
        ),
    ]
