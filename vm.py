import requests
from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient

URL = 'https://management.azure.com/subscriptions/9feb4648-183f-4379-92b1-b004943a626a/resourceGroups/lab4/providers/Microsoft.Network/virtualNetworks/lab4_10000?api-version=2023-05-01'


data = '''
{
	"properties": {
    "addressSpace": {
      "addressPrefixes": [
        "10.0.0.0/16"
      ]
    },
    "flowTimeoutInMinutes": 10
  },
	"location": "westeurope"
}'''

headers = {'Authorization' : 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSIsImtpZCI6IjlHbW55RlBraGMzaE91UjIybXZTdmduTG83WSJ9.eyJhdWQiOiJodHRwczovL21hbmFnZW1lbnQuY29yZS53aW5kb3dzLm5ldCIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0Lzc2NjMxN2NiLWU5NDgtNGU1Zi04Y2VjLWRhYmM4ZTJmZDVkYS8iLCJpYXQiOjE3MDAwNjM5NzksIm5iZiI6MTcwMDA2Mzk3OSwiZXhwIjoxNzAwMDY5MzI4LCJhY3IiOiIxIiwiYWlvIjoiQVZRQXEvOFZBQUFBd1lpWUowaEdOMVRkTnhoa2MxVmZtQ3B0SkZyUW5Pd2o4S09pKzN1VTJQdkh3YldDWmppM2xDNENGdFpINDR6aVIzZTVuNXR0bU1IdjQwMzl6WHNzRXRVY3lrYnByUllxZVF3OHI0d1pRM009IiwiYW1yIjpbInJzYSIsIm1mYSJdLCJhcHBpZCI6IjE4ZmJjYTE2LTIyMjQtNDVmNi04NWIwLWY3YmYyYjM5YjNmMyIsImFwcGlkYWNyIjoiMCIsImZhbWlseV9uYW1lIjoiR29kemhhZXYiLCJnaXZlbl9uYW1lIjoiRnVhZCIsImdyb3VwcyI6WyI4MTA4YzUwMy1kNjU2LTQyY2YtOGVlNC04OTQ0YWVmMGZhZGUiLCI5N2FmODEyZC05NmU5LTRmMDEtOGExMS03NTgwMzM3NjIxN2EiLCI4N2Y2MDAzZC05NDcwLTQzOGYtYmZlZi04MTNiMzdmYzJiNjgiLCIzZTg0ODA5OC1iNGExLTQxN2QtYTFiYS1jOWNmM2ZjZTlmNTEiLCI4MzhhMjg5YS04NGE0LTRjYTgtYWVlYy1iMzFlYzFkNzFkNGEiLCI0ZGMwM2I5Zi0xYjZjLTQ0MTUtYWMwNS04MjQyNzEzYzc1MjAiLCI1YWQ3ZDZiNC1hZGFmLTRiOWQtOTU3Zi0wZjNiNjE0YmVlNjAiLCI4YWMxNTRkZC1kNDVmLTRjNDYtOTRlNS1iYjc4ZmVmYTNhZWYiLCI4YzgxODZlYS00MmE0LTQ0YWYtOGE3OC1hZTkxNDAxMWU2YjQiLCJkMmE2YThlZi00ZDI2LTRkOTUtYmQxMS1hYTFlYzYxOWY4MTgiXSwiaWR0eXAiOiJ1c2VyIiwiaXBhZGRyIjoiMTQ3LjI1Mi4xOS4yMTEiLCJuYW1lIjoiRDIwMTI0NjMwIEZ1YWQgR29kemhhZXYiLCJvaWQiOiJiYjY3ZDMyMi0yOGNjLTQwNmYtYWFiOC1kNGY2ZjIxZTUyNTciLCJvbnByZW1fc2lkIjoiUy0xLTUtMjEtNDAyMjk4ODQ5LTE3MzQ3MDUxMzEtMzEyMDAyNDAwMS00NDQxNiIsInB1aWQiOiIxMDAzMjAwMEQ3RTZENjk0IiwicmgiOiIwLkFURUF5eGRqZGtqcFgwNk03TnE4amlfVjJrWklmM2tBdXRkUHVrUGF3ZmoyTUJNeEFIOC4iLCJzY3AiOiJ1c2VyX2ltcGVyc29uYXRpb24iLCJzdWIiOiI3QmZTTWEyd2hjb2x4Tk1ybU1fLUxLSFFoX1lhQWpDdkd4aUpBZ0NnV0ZZIiwidGlkIjoiNzY2MzE3Y2ItZTk0OC00ZTVmLThjZWMtZGFiYzhlMmZkNWRhIiwidW5pcXVlX25hbWUiOiJEMjAxMjQ2MzBAbXl0dWR1Ymxpbi5pZSIsInVwbiI6IkQyMDEyNDYzMEBteXR1ZHVibGluLmllIiwidXRpIjoiYThKQ2pRZEw3a3ltYnB0aURtS21BQSIsInZlciI6IjEuMCIsIndpZHMiOlsiYjc5ZmJmNGQtM2VmOS00Njg5LTgxNDMtNzZiMTk0ZTg1NTA5Il0sInhtc19jYWUiOiIxIiwieG1zX3RjZHQiOjE1MjUzMzg5NDF9.qNzNT5tW_W5IlS4eIBODlkKDV7VOVuhyj-yU8HXo-Z4Zp-P7TG-cxwx7uUOsArUiUUfKx8g2cdVRBirN8KlHdA8-MnihigVlTzsasiCgGOtsGJbK5LgjnbPc_ifQEDN19rU9wxIEJXuVS7zy4L9pPAzmjvx0pAtcFQV0kW08yBTWlHtOKvVKu9-nAQkifyrPsarWUU8IBjsnR7B4VhrA9UhXFD59qz8R_rshIhIkylw2dSZeSGa07uFCZ9O4kkH1N_vnP5_Idb7Ii5OSmT9zX7PfzE6xsaRsgpF_hm3UfhHvsnbdqVAJzV4QfK7a16NdntSbITvLF5_wkhbDfSj4Hg', 'Content-type' : 'application/json'}


request = requests.put(url = URL, data=data, headers=headers)




pastebin_url = request.text
print('The pastebin URL is %s' % pastebin_url)



"""
# PREREQUISITES
    pip install azure-identity
    pip install azure-mgmt-network
# USAGE
    python public_ip_address_create_defaults.py

    Before run the sample, please set the values of the client ID, tenant ID and client secret
    of the AAD application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID,
    AZURE_CLIENT_SECRET. For more info about how to get the value, please see:
    https://docs.microsoft.com/azure/active-directory/develop/howto-create-service-principal-portal
"""


def main():
    client = NetworkManagementClient(
        credential=DefaultAzureCredential(),
        subscription_id="9feb4648-183f-4379-92b1-b004943a626a",
    )

    response = client.virtual_networks.begin_create_or_update(
        resource_group_name="lab4",
        virtual_network_name="lab4_10000",
        parameters={
            "location": "westeurope",
            "properties": {"addressSpace": {"addressPrefixes": ["10.0.0.0/16"]}, "flowTimeoutInMinutes": 10},
        },
    ).result()
    print(response)





# x-ms-original-file: specification/network/resource-manager/Microsoft.Network/stable/2023-05-01/examples/PublicIpAddressCreateDefaults.json
if __name__ == "__main__":
    main()

