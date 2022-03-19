from django.db import models


class Insight(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(blank=True, null=True, auto_now=True)
    date = models.DateField(db_index=True)
    channel = models.CharField(max_length=20, db_index=True)
    country = models.CharField(max_length=2, db_index=True)
    os = models.CharField(max_length=10, db_index=True)
    impressions = models.PositiveIntegerField(blank=True, null=True)
    clicks = models.PositiveIntegerField(blank=True, null=True)
    installs = models.PositiveIntegerField(blank=True, null=True)
    spend = models.FloatField(blank=True, null=True)
    revenue = models.FloatField(blank=True, null=True)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Insight {self.id} for {self.date}"
