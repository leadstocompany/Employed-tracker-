# Generated by Django 4.1.4 on 2024-06-06 08:13

from django.conf import settings
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False, verbose_name='Is Admin')),
                ('is_subadmin', models.BooleanField(default=False, verbose_name='Is Subadmin')),
                ('is_company', models.BooleanField(default=False, verbose_name='Is Company')),
                ('is_employee', models.BooleanField(default=False, verbose_name='Is Employee')),
                ('cats', models.IntegerField(blank=True, default=0, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SubAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200)),
                ('password', models.CharField(blank=True, editable=False, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=200, unique=True)),
                ('mobile', models.CharField(blank=True, max_length=13, unique=True)),
                ('img', models.ImageField(blank=True, upload_to='subadmin/')),
                ('user_type', models.CharField(blank=True, max_length=200)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('udpate_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='superusername +', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SubAdmin.user_name +', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(blank=True, max_length=200)),
                ('password', models.CharField(blank=True, editable=False, max_length=200)),
                ('person_name', models.CharField(blank=True, max_length=200)),
                ('mobile', models.CharField(blank=True, max_length=13)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('img', models.ImageField(blank=True, upload_to='employee/')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('udpate_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company.sub_manager +', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee.user_name +', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('user_type', models.CharField(blank=True, default='is_employee', max_length=200, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='android_data +', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Manage ContactDetails',
            },
        ),
        migrations.CreateModel(
            name='CompanyAdmin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(blank=True, max_length=200)),
                ('password', models.CharField(blank=True, editable=False, max_length=200)),
                ('company_name', models.CharField(blank=True, max_length=200)),
                ('person_name', models.CharField(blank=True, max_length=200)),
                ('mobile', models.CharField(blank=True, max_length=13)),
                ('email', models.CharField(blank=True, max_length=200)),
                ('img', models.ImageField(blank=True, upload_to='company/')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('udpate_at', models.DateTimeField(auto_now=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subadmin.sub_manager +', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company.user_name +', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AndroidData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('duration', models.CharField(blank=True, max_length=200, null=True)),
                ('category', models.CharField(blank=True, max_length=20, null=True)),
                ('type', models.CharField(blank=True, max_length=200, null=True)),
                ('date', models.DateTimeField(null=True)),
                ('user_type', models.CharField(blank=True, default='is_employee', max_length=200, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='android_data +', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Manage AndroidData ',
            },
        ),
        migrations.AddConstraint(
            model_name='contactdetails',
            constraint=models.UniqueConstraint(fields=('user', 'mobile'), name='unique_contact'),
        ),
    ]
