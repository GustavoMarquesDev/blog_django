# Generated by Django 4.2.21 on 2025-05-21 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_setup', '0003_alter_sitesetup_options_menulink_site_setup'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetup',
            name='favicon',
            field=models.ImageField(blank=True, default='', null=True, upload_to='assets/favicon/%Y/%m/%d'),
        ),
    ]
