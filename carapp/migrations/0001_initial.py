# Generated by Django 4.1 on 2024-08-10 10:11

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Car",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("make", models.CharField(max_length=100)),
                ("num_doors", models.CharField(default="4", max_length=100)),
                ("price", models.FloatField()),
                ("description", models.TextField(blank=True)),
                ("body_style", models.CharField(max_length=100)),
                ("engine_type", models.CharField(max_length=100)),
                ("fuel_system", models.CharField(max_length=100)),
                ("wheelbase", models.FloatField()),
                ("length", models.FloatField()),
                ("width", models.FloatField()),
                ("height", models.FloatField()),
                ("curb_weight", models.FloatField()),
                ("fuel_capacity", models.CharField(max_length=100)),
                ("city_mpg", models.IntegerField()),
                ("highway_mpg", models.IntegerField()),
            ],
        ),
    ]
