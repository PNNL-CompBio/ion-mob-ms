from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from products.models import Product
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from products.serializers import ProductSerializer, ExperimentSerializer
import json,requests
from django.views.decorators.csrf import csrf_exempt
from subprocess import Popen, PIPE, STDOUT
from minio import Minio
# from minio.error import S3Error
import io
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from minio_storage.storage import MinioMediaStorage
import tempfile
#creating custom storage backend
# from django.views import View
# from django.http import JsonResponse
# from django_backend.custom_storages import MediaStorage

# @api_view(["POST"])
# def api_home(request, *args, **kwargs):
#     """
#     DRF API View
#     """
#     #model_data = Product.objects.all().order_by("?").first()
#     #data = {}

#     # if model_data:
#     #     data['id'] = model_data.id
#     #     data['title'] = model_data.title
#     #     data['content'] = model_data.content
#     #     data['price'] = model_data.price
#         #model instance -> turn to py dict -> return json to client

#     # if model_data:
#     #     data = model_to_dict(model_data, fields=['id', 'title', 'price', 'sale_price'])

#     data= request.data
#     instance = Product.objects.all().order_by("?").first()
#     data = {}

#     if instance:
#         data = ProductSerializer(instance).data

#     return JsonResponse(data)
#     #     print(data)
#     #     json_data_str = json.dumps(data)
#     # return HttpResponse(json_data_str, headers={"content-type":"application/json"})


def Single_Field_Exp(filepath1):
    command = ["python","/Users/jaco059/dev/run_minio_file_copy.py","-f", filepath1, "-b", "bucketofapples", "-n", "myapplefile" ]
    try:            
            process = Popen(command, stdout=PIPE, stderr=STDOUT)
            output = process.stdout.read()
            exitstatus = process.poll()
            if (exitstatus==0):
                    return {"status": "Success", "output":str(output)}
            else:
                    return {"status": "Failed", "output":str(output)}
    except Exception as e:
            return {"status": "failed", "output":str(e)}



def main(data):
    # Create a client with the MinIO server playground, its access key
    # and secret key.
    client = Minio(
        "127.0.0.1:9000",
        access_key="ROOTNAME",
        secret_key="CHANGEME123",
        secure=False
    )
    value_as_bytes = data.encode('utf-8')
    value_as_a_stream = io.BytesIO(value_as_bytes)

    client.put_object("my_bucket", "my_key", value_as_a_stream , length=len(value_as_bytes))
    # Make 'asiatrip' bucket if not exist.
    # found = client.bucket_exists(args['bucket'])
    # if not found:
    #     client.make_bucket(args['bucket'])
    # else:
    #     print("Bucket",args['bucket'], "already exists")

    # Upload '/home/user/Photos/asiaphotos.zip' as object name
    # 'asiaphotos-2015.zip' to bucket 'asiatrip'.
    # client.put_object(
    #     args['bucket'], args['newname'], args['file'],
    # )
    # print(
    #      args['file'], " is successfully uploaded as ",
    #      args['newname'], " to bucket ", args['file']
    # )




# @api_view(["POST"])
# def apo_home(request, *args, **kwargs):
#     """
#     DRF API View
#     """
#     serializer = ProductSerializer(data=request.data)
#     if serializer.is_valid(raise_exception=True):
#         #instance = serializer.save()
#         #instance = form.save
#         #print(instance)
#         # data= serializer.data
#         print(serializer.data)
#         return Response(serializer.data)
#     return Response({"invalid": "not good data"}, status=400)



@api_view(["POST", "GET"])
def api_home(request, *args, **kwargs):
    """
    DRF API View
    """
    serializer = ExperimentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        print("files: ",request.FILES,"/n")
        print("post: ",request.POST,"/n")

        #write json file
        file_json = tempfile.TemporaryFile()
        data = str(serializer.data)
        value_as_bytes = data.encode('utf-8')
        file_json.write(value_as_bytes)
        default_storage.save("JSON_metadata", file_json)
        #write all other files
        if "PreprocessedDataFolder" in request.FILES:
            file_pp = request.FILES.get('PreprocessedDataFolder')
            default_storage.save("PreProcessedData_ZipFile", file_pp)
        if "mzMLDataFolder" in request.FILES:
            file_mz = request.FILES.get('mzMLDataFolder')
            default_storage.save("mzMLData_ZipFile", file_mz)
        if "FeatureDataFolder" in request.FILES:
            file_fd = request.FILES.get('FeatureDataFolder')
            default_storage.save("FeatureData_ZipFile", file_fd)
        if "CalibrantFile" in request.FILES:
            file_cbf = request.FILES.get('CalibrantFile')
            default_storage.save("CalibrantFile", file_cbf)
        if "AutoCCSConfigFile" in request.FILES:
            file_acf = request.FILES.get('AutoCCSConfigFile')
            default_storage.save("AutoCCSConfigFile", file_acf)
        if "IMSMetadataFolder" in request.FILES:
            file_ims = request.FILES.get('IMSMetadataFolder')
            default_storage.save("IMSMetadata_ZipFile", file_ims)
        if "TargetListFile" in request.FILES:
            file_tlf = request.FILES.get('TargetListFile')
            default_storage.save("TargetListFile", file_tlf)
        if "MetadataFile" in request.FILES:
            file_md = request.FILES.get('MetadataFile')
            default_storage.save("MetadataFile", file_md)#
        response = HttpResponse(content_type='application/json', status=200)
            # if data:
            #     fs = FileSystemStorage()
            #     filename = fs.save("uploaded_file_name", data)
            #     uploaded_file_url = fs.url(filename)
                # print(request.data[0])
                # print(request.data[1])
                # print("attempted")
                # main(data)
                # print("attempt maybe didnt fail")
        return response
    else:
        return Response(serializer.data)
        
    # return Response({"invalid": "not good data"}, status=400)












# def api_home(request, *args, **kwargs):
#     # request  -> HttpRequest -> Django
#     # print(dir(request))
#     # request.body
#     data={}
    
#     print(request.headers)
#     print(request.GET) # url query params
#     print(request.POST)

#     body = request.body #byte string of JSON data
#     print(body)
#     try:
#         data = json.loads(body) # takes string of json data and converts to python dictionary
#     except:
#         pass
#     print(data)

#     data['params'] = dict(request.GET)
#     data['headers'] = dict(request.headers)
#     data['content_type'] = request.content_type

#     return JsonResponse(data)


