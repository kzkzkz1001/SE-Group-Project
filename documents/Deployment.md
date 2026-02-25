# Deployment Guide - Dublin Bikes Backend Service

This document provides step-by-step instructions for setting up the EC2 environment, deploying the Flask backend, and accessing the API endpoints.

---

## 1. Infrastructure Overview
* **Cloud Provider**: AWS EC2 (Ubuntu 24.04 LTS)
* **Backend Framework**: Flask (Python 3)
* **WSGI Server**: Gunicorn
* **Database**: MySQL 8.0
* **Default Port**: `5001`

---

## 2. Locating the Server Address
Since EC2 Public IPs are dynamic and may change after an instance restart, follow these steps to retrieve the current address:

1.  **AWS Console**: Check the `Public IPv4 address` in your Instance list.
2.  **Terminal Command**: Run the following command via SSH:
    ```bash
    curl ifconfig.me
    ```
> **Note**: In the following sections, replace `<public_ip>` with the actual IP address retrieved.

---

## 3. Server Deployment Steps

### 3.1 Virtual Environment Activation
To ensure dependency consistency, always activate the virtual environment within the project directory:

```bash
cd ~/SE-Group-Project/flask_app
source venv/bin/activate
```
###3.2 Environment Variables (.env)Create a .env file in the flask_app root directory to store sensitive credentials. Note: Do not upload this file to GitHub.Ini, TOMLDB_HOST=127.0.0.1
DB_USER=flask_user
DB_PASS=your_password
DB_NAME=dublin_bikes
OPENWEATHER_API_KEY=your_api_key
###3.3 Running the Service (Background Mode)Use Gunicorn combined with nohup to ensure the service remains active after closing the SSH session:Bashnohup ./venv/bin/gunicorn --bind 0.0.0.0:5001 app:app > gunicorn.log 2>&1 &

##4. API Specification (Endpoints)Team members can use the following endpoints for frontend integration or data testing:

Feature               API Endpoint                                   Return Format 

Server Health Check   http://<public_ip>:5001/                       String
Static Station Data   http://<public_ip>:5001/api/db/stations        JSON Array
Current Weather       http://<public_ip>:5001/api/weatherJSON        Object
Weather Forecast      http://<public_ip>:5001/api/weather/forecast   JSON Array


##5. Troubleshooting & Key Terms
<public_ip>: The public IP address of the EC2 instance.

0.0.0.0: A binding configuration that allows the server to accept external requests from the internet.

Endpoint: The specific URL path used to access different data resources.

Internal Server Error (500): This typically indicates a database connection failure or missing environment variables in .env. Check gunicorn.log for details.
