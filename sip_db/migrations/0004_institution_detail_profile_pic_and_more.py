# Generated by Django 4.1 on 2022-08-25 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sip_db', '0003_account_detail_holder_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='institution_detail',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profilepic/institutuion/'),
        ),
        migrations.AlterField(
            model_name='student_detail',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='profilepic/student'),
        ),
    ]
