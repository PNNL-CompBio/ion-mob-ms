from rest_framework import serializers
from .models import Product, Experiment



class ProductSerializer(serializers.ModelSerializer):
    my_discount = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Product
        fields = ['title', 'content','price', 'sale_price', 'my_discount']

    # def get_my_discount(self,obj):
    #     try:
    #         return obj.get_discount()
    #     except:
    #         return None


    def get_my_discount(self,obj):
        if not hasattr(obj,'id'):
            return None
        if not isinstance(obj,Product):
            return None
        return obj.get_discount()



class ExperimentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experiment
        fields = ['ExperimentType',
                'ExperimentName', 
                #'RawDataFolder',
                'PreprocessedDataFolder',
                'mzMLDataFolder', 
                'FeatureDataFolder', 
                'CalibrantFile', 
                'AutoCCSConfigFile', 
                'IMSMetadataFolder', 
                'TargetListFile', 
                'MetadataFile', ]
    

    