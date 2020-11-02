### get token
```command
curl -i -X POST -u Olivier http://127.0.0.1:5000/login

Enter host password for user 'Olivier': <password>
```
```
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 191
Server: Werkzeug/1.0.1 Python/3.8.1
Date: Mon, 02 Nov 2020 16:40:41 GMT
```
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIyMmI5M2JmNy03NGYzLTRiODktYWY1YS03OTA1YTgwYzVkMTUiLCJleHAiOjE2MDQzMzU1NDF9.4AqWFk-X1myDsRf0AgRIVMjDE4Vx9ZRQUggIYOVUHzU"
}
```
### Use token
```bat
set token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiIyMmI5M2JmNy03NGYzLTRiODktYWY1YS03OTA1YTgwYzVkMTUiLCJleHAiOjE2MDQzMzU1NDF9.4AqWFk-X1myDsRf0AgRIVMjDE4Vx9ZRQUggIYOVUHzU
``` 

```command 
curl -i -X GET -H "x-access-token: %token%" http://127.0.0.1:5000/user
```
```json
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 465
Server: Werkzeug/1.0.1 Python/3.8.1
Date: Mon, 02 Nov 2020 16:43:10 GMT

{
  "users": [
    {
      "admin": true,
      "name": "Olivier",
      "password": "sha256$XXSjnTvi$3db45150e5595dad91ea94ed687988e8a59e9f974ea46d0581195f16e0771518",
      "public_id": "22b93bf7-74f3-4b89-af5a-7905a80c5d15"
    },
    {
      "admin": true,
      "name": "Yoshiro",
      "password": "sha256$j0dOcY56$9eb022321a0dbd329757461dca4d826c540663ea01219fee6585d79960b082c8",
      "public_id": "da40af9c-5429-44f2-ad6f-ac54c39a6676"
    }
  ]
}
``` 
 