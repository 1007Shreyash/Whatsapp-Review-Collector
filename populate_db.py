import requests
import time
import random

# The URL of your local FastAPI server
BASE_URL = "http://localhost:8000/whatsapp"

# Sample data to populate (Phone, Name, Product, Review)
mock_users = [
    {
        "phone": "whatsapp:+15550101", 
        "name": "Rohan", 
        "product": "Espresso Machine X200", 
        "review": "It started leaking water after just 2 days. Very disappointed."
    },
    {
        "phone": "whatsapp:+15550102", 
        "name": "Sarah", 
        "product": "Nike Air Jordans", 
        "review": "Perfect fit. Love them."
    },
    {
        "phone": "whatsapp:+15550103", 
        "name": "Arjun", 
        "product": "Dell XPS 15", 
        "review": "The 4K OLED screen is stunning, but the battery life is only about 5 hours."
    },
    {
        "phone": "whatsapp:+15550104", 
        "name": "Priya", 
        "product": "Air Fryer Pro", 
        "review": "Cooks chicken wings perfectly crispy without oil! Cleaning is tricky though."
    },
    {
        "phone": "whatsapp:+15550105", 
        "name": "Vikram", 
        "product": "PS5 DualSense", 
        "review": "The haptic feedback is a game changer. Best controller I've ever held."
    }
]

def send_message(phone, body):
    """Sends a message to the local backend acting as Twilio"""
    payload = {
        "From": phone,
        "Body": body
    }
    try:
        response = requests.post(BASE_URL, data=payload)
        return response.status_code
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to localhost:8000. Is the server running?")
        return None

def simulate_user_flow(user):
    print(f"--- Simulating User: {user['name']} ({user['phone']}) ---")
    
    # Step 1: Say Hi
    print(f"1. Sending 'Hi'...")
    send_message(user['phone'], "Hi")
    time.sleep(0.5) 

    # Step 2: Send Product
    print(f"2. Sending Product: {user['product']}...")
    send_message(user['phone'], user['product'])
    time.sleep(0.5)

    # Step 3: Send Name
    print(f"3. Sending Name: {user['name']}...")
    send_message(user['phone'], user['name'])
    time.sleep(0.5)

    # Step 4: Send Review
    print(f"4. Sending Review...")
    send_message(user['phone'], user['review'])
    time.sleep(0.5)
    
    print(f"✓ Completed flow for {user['name']}\n")

if __name__ == "__main__":
    print("Starting database population...\n")
    
    # Check if server is alive first
    try:
        requests.get("http://localhost:8000")
    except:
        print("❌ Error: Your FastAPI backend is NOT running.")
        print("Please run 'uvicorn main:app --reload' in a separate terminal first.")
        exit()

    for user in mock_users:
        simulate_user_flow(user)
        
    print("🎉 All users created! Refresh index.html to see the data.")