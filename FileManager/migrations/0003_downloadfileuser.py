# Generated by Django 2.1.7 on 2019-05-24 11:18

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('FileManager', '0002_auto_20190521_1309'),
    ]

    operations = [
        migrations.CreateModel(
            name='DownloadFileUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('file', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='FileManager.File')),
            ],
            options={
                'db_table': 'users_downloads_files',
            },
        ),
    ]
