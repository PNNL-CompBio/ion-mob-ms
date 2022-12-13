import requests


# endpoint = "https://httpbin.ore/status/200"
# endpoint = "https://httpbin.org/anything"
endpoint = "http://localhost:8000/api/"

# notes.. A REST API is a web based API that uses HTTP Request
# get_response = requests.get(endpoint, json={"product_id":123})   # API = Application programming Interface
# print(get_response.json())



# get_response = requests.post(endpoint, json={"title":"hello world"})   # API = Application programming Interface
# print(get_response.json())

# HTTP Request -> HTML
# REST API HTTP Request -> JSON



get_response = requests.post(endpoint, json={"ExperimentType":"SingleField",
"ExperimentName":"hello b",
 "RawDataFolder":"/Users/jaco059/dev/apple",
 "PreprocessedDataFolder":"/Users/jaco059/dev/apple",
 "mzMLDataFolder":"hello e",
 "FeatureDataFolder":"hello f",
 "CalibrantFile":"hello g",
 "AutoCCSConfigFile":"hello g",
 "IMSMetadataFolder":"hello h",
 "TargetListFile":"hello i",
 "MetadataFile":None,
})   # API = Application programming Interface
print(get_response.json())