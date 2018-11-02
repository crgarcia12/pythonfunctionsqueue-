# pythonfunctionsqueue-
Testing Azure functions in python v2 
Input Queue
Output CosmosDb 

Bindings: https://pythondeveloperguide.azurewebsites.net/api.html#azure-functions-reference
Dev Guide: https://github.com/Azure/azure-functions-python-worker/wiki/Developer-Guide
VSCode: https://github.com/Azure/azure-functions-python-worker/wiki/Develop-using-VS-Code
Limitations consumption plan: https://github.com/Azure/Azure-Functions/wiki/Azure-Functions-on-Linux-Preview#access-the-azure-functions-linux-consumption-preview

# How to create it
  az login
  az account set --subscription '930c11b0-5e6d-458f-b9e3-f3dda0734110'

  az extension add --source functionapp-0.0.2-py2.py3-none-any.whl

  az group create -n funcpyqueue2 -l "WestEurope"
  az storage account create -n funcpyqueue2storage -l "WestEurope" -g funcpyqueue2 --sku Standard_LRS
  az functionapp createpreviewapp -n funcpyqueue2app -g funcpyqueue2 -l "WestEurope" -s funcpyqueue2storage --runtime python --is-linux
