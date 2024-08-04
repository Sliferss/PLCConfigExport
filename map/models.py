from django.db import models

class PrefabsConveyor(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(primary_key=True, max_length=255)
    length = models.FloatField(blank=True, null=True, default=0.0)
    width = models.FloatField(blank=True, null=True, default=0.0)
    height = models.FloatField(blank=True, null=True, default=0.0)
    speed1 = models.FloatField(blank=True, null=True, default=0.0)
    speed2 = models.FloatField(blank=True, null=True, default=0.0)
    speed3 = models.FloatField(blank=True, null=True, default=0.0)
    stand_by_time = models.IntegerField(blank=True, null=True, default=0)
    head_pec_fitted = models.BooleanField(default=False)
    tail_pec_fitted = models.BooleanField(default=False)
    head_pect_distance = models.IntegerField(blank=True, null=True, default=0)
    tail_pect_distance = models.IntegerField(blank=True, null=True, default=0)
    cm_number = models.IntegerField(blank=True, null=True, default=0)
    encoder_fitted = models.BooleanField(default=False)
    ramp_up = models.IntegerField(blank=True, null=True, default=0)
    ramp_down = models.IntegerField(blank=True, null=True, default=0)
    start_position_fwd = models.IntegerField(blank=True, null=True, default=0)
    start_position_rev = models.IntegerField(blank=True, null=True, default=0)
    group_id = models.IntegerField(blank=True, null=True, default=0)
    cm_head = models.IntegerField(blank=True, null=True, default=0)
    cm_tail = models.IntegerField(blank=True, null=True, default=0)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.timestamp) + ": " + self.name

class MapSetup(models.Model):
    timestamp = models.DateTimeField(auto_now=True, null=True)
    name = models.CharField(primary_key=True, max_length=255)
    grid_width = models.IntegerField(blank=True, null=True, default=24)
    grid_height = models.IntegerField(blank=True, null=True, default=24)

    image = models.ImageField(upload_to='map_images/', blank=True, null=True)

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
    speed1 = models.FloatField(blank=True, null=True, default=0.0)
    speed2 = models.FloatField(blank=True, null=True, default=0.0)
    speed3 = models.FloatField(blank=True, null=True, default=0.0)
    stand_by_time = models.IntegerField(blank=True, null=True, default=0)
    head_pec_fitted = models.BooleanField(default=False)
    tail_pec_fitted = models.BooleanField(default=False)
    head_pect_distance = models.IntegerField(blank=True, null=True, default=0)
    tail_pect_distance = models.IntegerField(blank=True, null=True, default=0)
    cm_number = models.IntegerField(blank=True, null=True, default=0)
    encoder_fitted = models.BooleanField(default=False)
    ramp_up = models.IntegerField(blank=True, null=True, default=0)
    ramp_down = models.IntegerField(blank=True, null=True, default=0)
    start_position_fwd = models.IntegerField(blank=True, null=True, default=0)
    start_position_rev = models.IntegerField(blank=True, null=True, default=0)
    group_id = models.IntegerField(blank=True, null=True, default=0)
    cm_head = models.IntegerField(blank=True, null=True, default=0)
    cm_tail = models.IntegerField(blank=True, null=True, default=0)

    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.timestamp) + ": " + self.name + " Map: " + self.map.name