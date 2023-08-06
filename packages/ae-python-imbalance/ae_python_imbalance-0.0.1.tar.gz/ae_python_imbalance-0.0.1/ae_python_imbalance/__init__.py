# Python Imbalance helper package
#
# Will do the following when included:
#   - Load environment variables
#   - Get Azure credentials
#   - Define constants for the datalakes
#
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

 
def init():
    global azure_credential

    # take environment variables from .env. (this file contains the AZURE_TENANT_ID, AZURE_CLIENT_ID and AZURE_CLIENT_SECRET)
    load_dotenv()

    # Get the Azure Credentials
    azure_credential = DefaultAzureCredential()

# Code run
init()
