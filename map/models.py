from django.db import models

class PrefabsConveyor(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(primary_key=True, max_length=255)
    length = models.FloatField(blank=True, null=True, default=0.0)
    width = models.FloatField(blank=True, null=True, default=0.0)
    height = models.FloatField(blank=True, null=True, default=0.0)
    speed = models.FloatField(blank=True, null=True, default=0.0)

    image = models.ImageField(upload_to='prefab_images/', blank=True, null=True)

    def __str__(self):
        return str(self.timestamp) + ": " + self.name

class MapSetup(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(primary_key=True, max_length=255)
    grid_width = models.IntegerField(blank=True, null=True, default=24)
    grid_height = models.IntegerField(blank=True, null=True, default=24)

    def __str__(self):
        return str(self.timestamp) + ": " + self.name + " GridWidth: " + str(self.grid_width) + " GridHeight: " + str(self.grid_height)

class GridParts(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(max_length=255)
    map = models.ForeignKey(MapSetup, on_delete=models.CASCADE)
    position_x = models.IntegerField(blank=True, null=True)
    position_y = models.IntegerField(blank=True, null=True)
    length = models.FloatField(blank=True, null=True, default=0.0)
    width = models.FloatField(blank=True, null=True, default=0.0)
    height = models.FloatField(blank=True, null=True, default=0.0)
    speed = models.FloatField(blank=True, null=True, default=0.0)

    image = models.ImageField(upload_to='prefab_images/', blank=True, null=True)

    def __str__(self):
        return str(self.timestamp) + ": " + self.name + " Map: " + self.map.name