# Generated by Django 2.1.1 on 2018-09-13 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Include',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('news', models.ManyToManyField(through='dict.Include', to='dict.News')),
            ],
        ),
        migrations.AddField(
            model_name='include',
            name='news',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dict.News'),
        ),
        migrations.AddField(
            model_name='include',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dict.Word'),
        ),
    ]
