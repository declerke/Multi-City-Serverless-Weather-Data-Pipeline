# 🌦️ Multi-City Serverless Weather Data Pipeline

A production-grade, event-driven data engineering project that automates the collection, archival, and alerting of weather data for 5 major cities in Kenya. This system utilizes a completely serverless architecture on AWS, ensuring high availability, zero maintenance, and cost-efficiency.

---

## 🎯 Project Overview
The pipeline transitions from basic local scripts to a robust cloud-native solution. It features a modular Python architecture that fetches high-precision meteorological data from the **Open-Meteo API**, archives it in a structured S3 Data Lake, and utilizes SNS for intelligent alerting.

**Core Pipeline Logic:**
* **Automated Heartbeat:** Amazon EventBridge triggers the system every hour.
* **Multi-City Orchestration:** A single Lambda execution iterates through Nairobi, Mombasa, Kisumu, Nakuru, and Eldoret.
* **Tiered Storage:** JSON payloads are persisted in S3 using a partitioned prefix strategy: `weather-data/{city}/{YYYY-MM-DD-HHMM}.json`.
* **Proactive Notifications:** The system evaluates WMO weather codes to trigger real-time email alerts via SNS for severe conditions.

---

## 🏗️ Project Structure
```text
aws-weather-alert/
├── src/
│   ├── lambda_function.py    # Main loop and multi-city orchestration
│   ├── weather_client.py     # Open-Meteo API integration
│   ├── storage_handler.py    # S3 PutObject logic and prefix management
│   ├── alert_handler.py      # SNS filtering and publishing logic
│   └── utils.py              # Schema validation and config loading
├── infrastructure/
│   └── cloudformation.yaml   # Infrastructure as Code (Stack definition)
├── scripts/
│   └── deploy.ps1            # Automation script for packaging & deployment
├── requirements.txt          # Production dependencies (requests, boto3)
└── .env                      # Local environment secrets
```

---

## ⚡ Technical Stack & Comparison

| Feature | Local Exploratory Script | AWS Production Pipeline |
| :--- | :--- | :--- |
| **Data Source** | Open-Meteo API | **Open-Meteo API** |
| **Processing** | Manual Invocation | **EventBridge Hourly Schedule** |
| **Compute** | Local CPU | **AWS Lambda (Python 3.12)** |
| **Storage** | Local Disk | **Amazon S3 (Data Lake)** |
| **Messaging** | Terminal Output | **Amazon SNS (Email Alerts)** |

---

## 🔧 Installation & Deployment

### Prerequisites
* AWS CLI configured with appropriate IAM permissions.
* Python 3.12 environment.
* Verified SNS Email Subscription (Check your inbox for the AWS confirmation link).

### Automated Deployment Workflow
The system is deployed using a modular approach to ensure the Lambda environment has all necessary third-party libraries:

```powershell
# 1. Prepare deployment package
pip install --target ./package -r requirements.txt
Copy-Item "src/*" -Destination "./package" -Recurse -Force

# 2. Compress for Lambda
Compress-Archive -Path ./package/* -DestinationPath dist/function.zip -Force

# 3. Update Cloud Resources
aws lambda update-function-code --function-name weather-alert-Nairobi --zip-file fileb://dist/function.zip
```

---

## 📊 Analytics & Monitoring
The system provides deep observability into the data pipeline:
* **S3 Data Lake:** Objects are organized by city name to allow for easy partitioning if using **AWS Athena** for SQL queries.
* **CloudWatch Logs:** Every execution records the processing status of all 5 cities, API latency, and S3 upload confirmations.
* **Event-Driven Reliability:** The EventBridge rule `WeatherPulse` ensures data is collected even if the developer is offline.



---

## 🎓 Skills & Competencies Demonstrated
* **Serverless Engineering:** Architecting cost-effective systems using AWS Lambda and EventBridge.
* **Cloud Storage Design:** Implementing S3 prefix partitioning for scalable data management.
* **Resilient Code:** Developing Python logic that handles partial failures (e.g., if one city API call fails, the others continue).
* **Infrastructure as Code (IaC):** Utilizing CloudFormation to manage and decommission cloud stacks reliably.

---

## 🛠️ Maintenance & Cleanup
To avoid any AWS charges after testing, the entire infrastructure can be removed with a single command:
```powershell
aws cloudformation delete-stack --stack-name weather-alert-system
```
*Note: The S3 bucket must be emptied of all weather JSON objects before the stack deletion can complete.*
