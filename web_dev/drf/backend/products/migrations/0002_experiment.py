# Generated by Django 4.0.8 on 2022-11-17 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ExperimentType', models.CharField(max_length=120)),
                ('ExperimentName', models.CharField(max_length=120)),
                ('RawDataFolder', models.CharField(blank=True, max_length=120, null=True)),
                ('PreprocessedDataFolder', models.FileField(default='', upload_to='')),
                ('mzMLDataFolder', models.CharField(blank=True, max_length=120, null=True)),
                ('FeatureDataFolder', models.CharField(blank=True, max_length=120, null=True)),
                ('CalibrantFile', models.CharField(blank=True, max_length=120, null=True)),
                ('AutoCCSConfigFile', models.CharField(blank=True, max_length=120, null=True)),
                ('IMSMetadataFolder', models.CharField(blank=True, max_length=120, null=True)),
                ('TargetListFile', models.CharField(blank=True, max_length=120, null=True)),
                ('MetadataFile', models.CharField(blank=True, max_length=120, null=True)),
            ],
        ),
    ]
