# Generated by Django 3.1.6 on 2021-02-13 00:52

from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('H', 'Home'), ('W', 'Work'), ('O', 'Other')], max_length=1, verbose_name='address type')),
                ('street', models.CharField(max_length=128, verbose_name='street')),
                ('street2', models.CharField(blank=True, max_length=128, verbose_name='unit/apartment/suite')),
                ('city', models.CharField(max_length=62, verbose_name='city')),
                ('state', localflavor.us.models.USStateField(max_length=2, verbose_name='state')),
                ('zip_code', localflavor.us.models.USZipCodeField(max_length=10, verbose_name='ZIP code')),
                ('is_published', models.BooleanField(default=True, help_text='Show this address to other members of the pack in the directory', verbose_name='published')),
            ],
            options={
                'verbose_name': 'Address',
                'verbose_name_plural': 'Addresses',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('H', 'home'), ('W', 'work'), ('O', 'other')], max_length=1, verbose_name='email type')),
                ('address', models.EmailField(max_length=254, verbose_name='email address')),
                ('is_published', models.BooleanField(default=True, help_text='Show this address to other members of the pack in the directory', verbose_name='published')),
                ('is_subscribed', models.BooleanField(default=True, help_text='Subscribe to periodical e-mails form the pack at this address', verbose_name='subscribed')),
            ],
            options={
                'verbose_name': 'Email Address',
                'verbose_name_plural': 'Email Addresses',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('H', 'home'), ('M', 'mobile'), ('W', 'work'), ('O', 'other')], max_length=1, verbose_name='phone type')),
                ('number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='phone number')),
                ('is_published', models.BooleanField(default=True, help_text='Show this number to other members of the pack in the directory', verbose_name='published')),
            ],
            options={
                'verbose_name': 'Phone Number',
                'verbose_name_plural': 'Phone Numbers',
            },
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('categories', models.ManyToManyField(related_name='venues', to='addresses.Category')),
            ],
            options={
                'verbose_name': 'Venue',
                'verbose_name_plural': 'Venues',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(verbose_name='Website URL')),
                ('venue', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='websites', to='addresses.venue')),
            ],
            options={
                'verbose_name': 'Website',
                'verbose_name_plural': 'Websites',
            },
        ),
    ]
