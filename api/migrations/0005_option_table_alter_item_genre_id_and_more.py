# Generated by Django 4.1.2 on 2022-10-06 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_item_is_delivered'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.AlterField(
            model_name='item',
            name='genre_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.itemgenre'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.item'),
        ),
        migrations.AlterField(
            model_name='orderdetail',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.order'),
        ),
        migrations.AlterField(
            model_name='orderedoption',
            name='order_detail_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.orderdetail'),
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('table_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.table')),
            ],
        ),
        migrations.CreateModel(
            name='AvailableOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.item')),
                ('option_id', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='api.option')),
            ],
        ),
        migrations.AlterField(
            model_name='order',
            name='table_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.table'),
        ),
        migrations.AlterField(
            model_name='orderedoption',
            name='option_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.option'),
        ),
    ]
