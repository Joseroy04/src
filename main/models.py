from django.db import models
from django.utils.translation import gettext as _

# Create your models here.
class driver(models.Model):
    driver_name = models.CharField(_("driver name"), max_length=50)
    license_no = models.CharField(_("license no"), max_length=50)
    age = models.IntegerField(_("age"))
    phone_no = models.IntegerField(_("phone no"))

    class Meta:
        verbose_name = _("driver")
        verbose_name_plural = _("drivers")

    def __str__(self):
        return self.driver_name


class bus(models.Model):
    bus_name = models.CharField(_("bus name"), max_length=50)
    bus_no = models.CharField(_("bus no"), max_length=50 ,unique=True)
    class Meta:
        verbose_name = _("bus")
        verbose_name_plural = _("buses")

    def __str__(self):
        return self.bus_no

class bus_stop(models.Model):
    city_name = models.CharField(_("city name"), max_length=50)
    pincode = models.IntegerField(_("pincode"))
    latitude = models.FloatField(_("latitude"))
    longitude = models.FloatField(_("longitude"))

    class Meta:
        verbose_name = _("bus_stop")
        verbose_name_plural = _("bus_stops")

    def __str__(self):
        return self.city_name

class rutes(models.Model):
    rute_name = models.CharField(_("rute name"), max_length=50)
    bus = models.ForeignKey(bus, verbose_name=_("bus "), on_delete=models.CASCADE)
    bus_driver = models.ForeignKey(driver, verbose_name=_("deiver "), on_delete=models.SET_NULL ,null=True)
    bus_rutes = models.ManyToManyField(bus_stop, verbose_name=_(" rutes"))
    bus_date = models.DateField(_("rute date"), auto_now=False, auto_now_add=False ,null=True)

    class Meta:
        verbose_name = _("rutes")
        verbose_name_plural = _("rutes")
        
    def __str__(self):
        return self.rute_name

