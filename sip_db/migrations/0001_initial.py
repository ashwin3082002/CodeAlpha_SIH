# Generated by Django 4.1 on 2023-04-22 19:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='api_details',
            fields=[
                ('api_id', models.AutoField(primary_key=True, serialize=False)),
                ('org_name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('api_key', models.CharField(max_length=200)),
                ('permissions', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='institution_detail',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('type_insti', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('pincode', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('contact', models.CharField(blank=True, max_length=14, null=True)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profilepic/institutuion/')),
            ],
        ),
        migrations.CreateModel(
            name='institution_id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instiid', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='student_detail',
            fields=[
                ('sid', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('dob', models.CharField(max_length=20)),
                ('guardian_name', models.CharField(max_length=120)),
                ('email', models.EmailField(max_length=254)),
                ('mobile', models.CharField(max_length=10)),
                ('aadhar', models.CharField(max_length=12)),
                ('gender', models.CharField(max_length=10)),
                ('active_status', models.CharField(max_length=20)),
                ('community', models.CharField(max_length=10)),
                ('address', models.TextField(default='')),
                ('city', models.CharField(default='', max_length=30)),
                ('state', models.CharField(default='', max_length=20)),
                ('pincode', models.CharField(default='', max_length=6)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profilepic/student')),
            ],
        ),
        migrations.CreateModel(
            name='student_id',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stuid', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='docreq',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('doc_type', models.CharField(max_length=20)),
                ('reason', models.CharField(max_length=200)),
                ('status', models.CharField(max_length=20)),
                ('i_id', models.ForeignKey(db_column='i_id', on_delete=django.db.models.deletion.CASCADE, to='sip_db.institution_detail')),
                ('sid', models.ForeignKey(db_column='sid', on_delete=django.db.models.deletion.CASCADE, to='sip_db.student_detail')),
            ],
        ),
        migrations.CreateModel(
            name='degree',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=10)),
                ('discipline', models.CharField(max_length=20)),
                ('year_join', models.CharField(max_length=10)),
                ('year_leave', models.CharField(blank=True, max_length=10, null=True)),
                ('grade', models.CharField(blank=True, max_length=10, null=True)),
                ('iid', models.ForeignKey(db_column='iid', on_delete=django.db.models.deletion.CASCADE, to='sip_db.institution_detail')),
                ('sid', models.ForeignKey(db_column='sid', on_delete=django.db.models.deletion.CASCADE, to='sip_db.student_detail')),
            ],
        ),
        migrations.CreateModel(
            name='course',
            fields=[
                ('cid', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('total_marks', models.CharField(max_length=10)),
                ('obtained_marks', models.CharField(max_length=10)),
                ('credits', models.CharField(max_length=10)),
                ('semester', models.CharField(max_length=2)),
                ('did', models.ForeignKey(db_column='did', on_delete=django.db.models.deletion.CASCADE, to='sip_db.degree')),
            ],
        ),
        migrations.CreateModel(
            name='account_detail',
            fields=[
                ('acc_id', models.AutoField(primary_key=True, serialize=False)),
                ('holder_name', models.CharField(max_length=50)),
                ('acc_number', models.CharField(max_length=20)),
                ('bank_name', models.CharField(max_length=50)),
                ('branch_name', models.CharField(max_length=100)),
                ('ifsc', models.CharField(max_length=50)),
                ('sid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sip_db.student_detail')),
            ],
        ),
    ]
