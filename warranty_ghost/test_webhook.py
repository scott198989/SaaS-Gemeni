import requests
import os

# Load environment variables if you have a .env file
# from dotenv import load_dotenv
# load_dotenv()

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
WEBHOOK_URL = f"{BASE_URL}/hooks/inbound"

# --- Test Data ---
# Simulate an email from Amazon
test_email = {
    "to": "your-unique-address@warrantyghost.com",
    "subject": "Your Amazon.com order of 'Super Amazing Gadget' has shipped!",
    "html": """
    <html>
        <head>
            <title>Your Amazon.com Order</title>
        </head>
        <body>
            <p>
                Hello,
            </p>
            <p>
                We're writing to confirm your order.
            </p>
            <p>
                <b>Order Date:</b> January 9, 2026
            </p>
            <p>
                Some other details about the item...
            </p>
            <p style="font-weight: bold;">
                Order Total: $99.99
            </p>
            <p>
                Thank you for shopping with us.
            </p>
        </body>
    </html>
    """
}

def test_inbound_hook():
    """
    Sends a test payload to the /hooks/inbound endpoint and prints the response.
    """
    print(f"[*] Sending test email payload to: {WEBHOOK_URL}")
    try:
        response = requests.post(WEBHOOK_URL, data=test_email)
        
        # Check for successful response
        if response.status_code == 200:
            print("[+] Success! Server responded with 200 OK.")
            print("[+] Response JSON:", response.json())
        else:
            print(f"[!] Error! Server responded with status code: {response.status_code}")
            print("[!] Response Content:", response.text)

    except requests.exceptions.ConnectionError as e:
        print(f"[!] Connection Error: Could not connect to the server at {BASE_URL}.")
        print("[!] Please make sure the FastAPI server is running.")
        print(f"[!] Details: {e}")
    except Exception as e:
        print(f"[!] An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_inbound_hook()
