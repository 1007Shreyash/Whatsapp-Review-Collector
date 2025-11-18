# **WhatsApp Product Review Collector 💬**

A full-stack application developed as an SDE assignment for **Hyperint / Eternamind**.

This system automates the collection of product reviews using a conversational WhatsApp bot. It processes user inputs (Product Name, User Name, Review) via a state machine, stores them in a database, and streams them to a live React dashboard in real-time.

## **🚀 Features**

- **Conversational Bot:** A state-aware WhatsApp bot that guides users through a review flow.
- **Real-time Dashboard:** A React-based UI that auto-refreshes to show new feedback instantly.
- **Robust Backend:** Built with **FastAPI** and **SQLAlchemy** for high performance.
- **Data Simulation:** Includes a script to populate the database with mock data for demonstration purposes.
- **Fault Tolerance:** The frontend handles backend downtimes gracefully with a "Demo Mode".

## **🛠️ Tech Stack**

- **Backend:** Python, FastAPI, Uvicorn
- **Database:** SQLite (Default for portability) / PostgreSQL (Supported via config)
- **Frontend:** React.js (Standalone), Tailwind CSS, Lucide Icons
- **Integrations:** Twilio Sandbox for WhatsApp
- **Tunneling:** Ngrok (to expose localhost to Twilio)

## **📂 Project Structure**
```
├── main.py \# FastAPI Backend & DB Models  
├── index.html \# React Frontend Dashboard  
├── populate_db.py \# Script to generate dummy data (No WhatsApp needed)  
├── requirements.txt \# Python dependencies  
├── dashboard_preview.png \# Screenshot for README  
└── README.md \# Project Documentation
```

## **⚡ Step-by-Step Execution Guide**

### **1\. Prerequisite Setup**

Ensure you have Python installed.  
Clone this repository and navigate to the project folder.

### **2\. Backend Installation**

1. Create a virtual environment:  
   ```
   python \-m venv venv
   
   \# Windows:  
   .\\venv\\Scripts\\activate
   
   \# Mac/Linux:  
   source venv/bin/activate
   ```

3. Install dependencies:  
   ```
   pip install \-r requirements.txt
   ```

5. Start the server:  
   ```
   python \-m uvicorn main:app \--reload
   ```

   _The backend will start at http://localhost:8000._

### **3\. Frontend Launch**

Simply double-click **index.html** to open it in your browser.

- It connects to localhost:8000 automatically.
- If the backend is running, you will see "No reviews yet".
- If the backend is off, it will switch to **Demo Mode** with sample data.

## **🔗 Connecting to WhatsApp (Twilio)**

To test the actual chatbot flow, you need to expose your local server to the internet so Twilio can talk to it.

1. **Install Ngrok** (or a similar tunneling tool).
2. Run Ngrok on port 8000:  
   ```
   ngrok http 8000
   ```

4. Copy the **HTTPS Forwarding URL** (e.g., https://abc-123.ngrok-free.app).
5. Go to your [Twilio Console \> Messaging \> Sandbox Settings](https://console.twilio.com/).
6. Paste the URL into the **"When a message comes in"** field and append /whatsapp:
   - **Target URL:** https://abc-123.ngrok-free.app/whatsapp
7. Save settings.
8. Join the sandbox using your phone (send the specific "join code" to the Twilio number).

**Test Flow:**

User: Hi  
Bot: Which product is this review for?  
User: iPhone 15  
Bot: What's your name?  
User: Alex  
Bot: Please send your review for iPhone 15\.  
User: Great battery life\!

## **🧪 Quick Demo (No Twilio Required)**

If you don't want to configure Twilio, you can use the included simulation script to generate traffic.

1. Ensure the backend is running (uvicorn main:app \--reload).
2. Open a new terminal and run:  
   python populate_db.py

3. Watch the **index.html** dashboard. The table will automatically update with 5 distinct user reviews as the script runs.

## **⚙️ Configuration**

Switching to PostgreSQL:  
The project uses SQLite by default for zero-config testing. To use Postgres (as per the assignment requirement):

1. Open main.py.
2. Uncomment **Line 14**:  
   ```
   \# DATABASE_URL \= "postgresql://user:password@localhost/dbname"
   ```

4. Comment out the SQLite line.
5. Ensure you have psycopg2-binary installed.

## **📸 Screenshots**

![Dashboard Preview](dashboard_preview1.png)
![Dashboard Preview](dashboard_preview.png)

## **📝 Notes for Reviewer**

- **State Management:** The bot uses an in-memory dictionary for conversation state. In a production environment, this would be replaced with Redis.
- **Frontend:** Built as a Single File Component (SFC) for simplicity and ease of review, eliminating the need for a complex npm build step.
