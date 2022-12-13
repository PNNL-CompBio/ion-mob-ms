from django import forms

from .models import Product
from .models import Experiment

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'content','price']

    
class ExperimentForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ['ExperimentType',
        'ExperimentName',
        'RawDataFolder',
        'PreprocessedDataFolder',
        'mzMLDataFolder',
        'FeatureDataFolder',
        'CalibrantFile',
        'AutoCCSConfigFile',
        'IMSMetadataFolder',
        'TargetListFile',
        'MetadataFile']
