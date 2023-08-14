# Generated by Django 4.2.2 on 2023-08-14 22:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sql_test', '0008_pack_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pack',
            old_name='lot',
            new_name='lots',
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField(default=1)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sql_test.article')),
            ],
        ),
    ]