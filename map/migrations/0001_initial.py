# Generated by Django 5.0.7 on 2024-07-14 07:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MapSetup",
            fields=[
                ("timestamp", models.DateTimeField(auto_now=True, null=True)),
                (
                    "name",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("grid_width", models.IntegerField(blank=True, default=24, null=True)),
                ("grid_height", models.IntegerField(blank=True, default=24, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="PrefabsConveyor",
            fields=[
                ("timestamp", models.DateTimeField(auto_now=True, null=True)),
                (
                    "name",
                    models.CharField(max_length=255, primary_key=True, serialize=False),
                ),
                ("length", models.FloatField(blank=True, default=0.0, null=True)),
                ("width", models.FloatField(blank=True, default=0.0, null=True)),
                ("height", models.FloatField(blank=True, default=0.0, null=True)),
                ("speed", models.FloatField(blank=True, default=0.0, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True, null=True, upload_to="prefab_images/"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GridParts",
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
                ("timestamp", models.DateTimeField(auto_now=True, null=True)),
                ("name", models.CharField(max_length=255)),
                ("position_x", models.IntegerField(blank=True, null=True)),
                ("position_y", models.IntegerField(blank=True, null=True)),
                ("length", models.FloatField(blank=True, default=0.0, null=True)),
                ("width", models.FloatField(blank=True, default=0.0, null=True)),
                ("height", models.FloatField(blank=True, default=0.0, null=True)),
                ("speed", models.FloatField(blank=True, default=0.0, null=True)),
                (
                    "map",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="map.mapsetup"
                    ),
                ),
            ],
        ),
    ]
