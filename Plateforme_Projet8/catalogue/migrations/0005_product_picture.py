# Generated by Django 2.0.7 on 2018-07-31 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_auto_20180731_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='picture',
            field=models.URLField(default=1),
            preserve_default=False,
        ),
    ]
