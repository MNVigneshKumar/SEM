# Generated by Django 4.2.5 on 2023-11-14 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pedal', '0017_payment_orders'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Orders',
            new_name='Order',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='cycle',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='payment_staus',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.CreateModel(
            name='Rent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('is_avail', models.BooleanField(default=True)),
                ('cycle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pedal.cycle')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='pedal.appuser')),
            ],
        ),
    ]