import asyncio
from stealth_client import StealthClient

async def verify():
    print("=== Testing TLS Fingerprint via StealthClient ===")
    client = StealthClient(impersonate="chrome120")
    
    try:
        response = await client.get("https://tls.browserleaks.com/json")
        print(f"Status Code: {response.status_code}")
        print("Response Body:")
        print(response.text)
    except Exception as e:
        print(f"Error fetching fingerprint: {e}")
    finally:
        await client.close()

if __name__ == "__main__":
    asyncio.run(verify())
