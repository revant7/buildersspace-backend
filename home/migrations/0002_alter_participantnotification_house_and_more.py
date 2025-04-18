# Generated by Django 5.1.6 on 2025-03-02 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantnotification',
            name='house',
            field=models.CharField(choices=[('Gryffindor', 'Gryffindor'), ('Hufflepuff', 'Hufflepuff'), ('Ravenclaw', 'Ravenclaw'), ('Slytherin', 'Slytherin'), ('Phoenix', 'Phoenix')], max_length=64),
        ),
        migrations.AlterField(
            model_name='participantnotification',
            name='is_read',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='participantnotification',
            name='notification_message',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
