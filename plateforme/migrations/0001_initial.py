# Generated by Django 4.2.7 on 2023-11-28 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=200)),
                ('prenom', models.CharField(max_length=200)),
                ('structure', models.CharField(max_length=100)),
                ('lieu_travail', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_soumission', models.DateTimeField(auto_now_add=True)),
                ('information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plateforme.visitor')),
            ],
        ),
    ]
