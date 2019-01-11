# Generated by Django 2.1.5 on 2019-01-11 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('commerce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='id',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='items',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_id',
            field=models.AutoField(default=2, max_length=30, primary_key=True, serialize=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='itemorder',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='commerce.Cart'),
        ),
    ]
