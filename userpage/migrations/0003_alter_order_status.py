# Generated by Django 4.2.4 on 2023-08-31 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0002_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(default='Pending...', max_length=200, null=True),
        ),
    ]
