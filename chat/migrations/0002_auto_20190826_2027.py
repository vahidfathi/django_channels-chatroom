# Generated by Django 2.2.4 on 2019-08-26 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messages',
            old_name='recivere_id',
            new_name='recievere_id',
        ),
        migrations.RenameField(
            model_name='messages',
            old_name='recivere_type',
            new_name='recievere_type',
        ),
        migrations.AddField(
            model_name='messages',
            name='reciever_deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='messages',
            name='sender_deleted',
            field=models.BooleanField(default=False),
        ),
    ]
