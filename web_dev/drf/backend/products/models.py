from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=120)
    content = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=99.99)

    @property
    def sale_price(self):
        return "%.2f" %(float(self.price) * 0.8)

    def get_discount(self):
        return "122"
#add all experiment params here




class Experiment(models.Model):
    ExperimentType = models.CharField(max_length=120)
    ExperimentName = models.CharField(max_length=120)
    # RawDataFolder = models.FileField()
    PreprocessedDataFolder = models.FileField(blank=True)
    mzMLDataFolder = models.FileField(blank=True)
    FeatureDataFolder = models.FileField(blank=True)
    CalibrantFile = models.FileField(blank=True)
    AutoCCSConfigFile = models.FileField(blank=True)
    IMSMetadataFolder = models.FileField(blank=True)
    TargetListFile = models.FileField(blank=True)
    MetadataFile = models.FileField(blank=True)



    #PreprocessedDataFolder = models.CharField(max_length=120,blank=True, null=True)
    #mzMLDataFolder = models.CharField(max_length=120,blank=True, null=True)
    # FeatureDataFolder = models.CharField(max_length=120,blank=True, null=True)
    # CalibrantFile = models.CharField(max_length=120,blank=True, null=True)
    # AutoCCSConfigFile = models.CharField(max_length=120,blank=True, null=True)
    # IMSMetadataFolder = models.CharField(max_length=120,blank=True, null=True)
    # TargetListFile = models.CharField(max_length=120,blank=True, null=True)
    # MetadataFile = models.CharField(max_length=120,blank=True, null=True)


