from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests, time, asyncio

def get_access_token():
    url = 'http://localhost:8088/api/v1/security/login'
    body = {
        "password": "123456",
        "provider": "db",
        "refresh": True,
        "username": "dashviewer"
    }
    response = requests.post(url=url, json=body)
    tokens = response.json()
    return tokens["access_token"], tokens["refresh_token"]

def refresh_access_token():
    url = 'http://localhost:8088/api/v1/security/refresh'
    headers = {"Authorization": f'Bearer {refresh_token}'}
    response = requests.post(url=url, headers=headers)
    token = response.json()
    return token["access_token"]

access_token, refresh_token = get_access_token()

print(f'{access_token} \n{refresh_token}')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/test")
def test():
    return {"Hello": "World"}

@app.post("/fetchGuestToken")
def fetch_token():
    url = 'http://localhost:8088/api/v1/security/guest_token/'
    headers = {"Authorization": f'Bearer {access_token}'}
    body = {
        "resources": [
            {
                "id": "25578f18-4f06-4e2f-b53c-d97a1a2d6ae8",
                "type": "dashboard"
            }
        ],
        "rls": [
        ],
        "user": {
            "first_name": "abcd",
            "last_name": "abcd",
            "username": "abcd"
        }
    }
    response = requests.post(url=url, json=body, headers=headers)
    token = response.json()
    print(token)
    return token

async def refresher():
    while(True):
        await asyncio.sleep(120)
        access_token = refresh_access_token()
        print(f'at: {access_token} \nrt: {refresh_token}')

@app.on_event("startup")
async def periodic():
    asyncio.create_task(refresher())

