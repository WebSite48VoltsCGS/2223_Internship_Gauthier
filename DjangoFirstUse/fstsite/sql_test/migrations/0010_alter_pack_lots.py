# Generated by Django 4.2.2 on 2023-08-14 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sql_test', '0009_rename_lot_pack_lots_lot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pack',
            name='lots',
            field=models.ManyToManyField(to='sql_test.lot'),
        ),
    ]
