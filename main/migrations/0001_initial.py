# Generated by Django 3.2.6 on 2021-08-14 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatusHome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('code', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Needy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('surName', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=11, verbose_name='Номер телефона')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('iin', models.CharField(max_length=12, verbose_name='ИИН')),
                ('childTotal', models.IntegerField(blank=True, null=True, verbose_name='Количество детей')),
                ('getHelp', models.TextField(verbose_name='Какую помощь получили')),
                ('period', models.CharField(max_length=255, verbose_name='Срок получение')),
                ('typeHelp', models.TextField(verbose_name='Какая помощь необходима')),
                ('statusHome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.statushome')),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('surName', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('iin', models.CharField(max_length=12, verbose_name='ИИН')),
                ('parents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='childs', to='main.needy')),
            ],
        ),
    ]
