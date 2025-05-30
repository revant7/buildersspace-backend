# Generated by Django 5.1.6 on 2025-03-04 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_participant_designation_participant_domain_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='profile_picture',
            field=models.ImageField(default='default/Profile.png', upload_to='participant/profile/'),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='commudle_profile',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='github',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='instagram',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='linkedin',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='sociallinks',
            name='twitter',
            field=models.TextField(),
        ),
    ]
