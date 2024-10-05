from django.db import models

class Component(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    repair_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_new = models.BooleanField(default=True)  # Indicates whether the component is new or a repair part

    def _str_(self):
        return f"{self.name} ({'New' if self.is_new else 'Repair'})"


class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    date_added = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.name} - {self.model}"


class VehicleIssue(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    component = models.ForeignKey(Component, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_repair = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        return self.component.price * self.quantity

    def _str_(self):
        return f"Issue: {self.vehicle.name} - {self.component.name}"