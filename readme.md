# **Sales Performance Analysis API**
This project provides an API for uploading and analyzing employee sales performance data. It includes endpoints for uploading employee performance data, analyzing individual employee performance, generating team performance feedback, and forecasting sales performance trends.

## Features

* Upload Employee Data: Upload CSV or JSON files containing employee performance data.
* Rep Performance: Get performance insights and feedback for a specific sales representative.
* Team Performance: Get overall team performance insights and feedback.
* Sales Performance Trends and Forecasting: Analyze sales trends over a specified time period (monthly or quarterly) and forecast future performance.

## API Endpoints

### 1. Upload Employee Data

* Endpoint: /api/upload/
* Method: POST
* Parameters: A file (.csv or .json) containing employee performance data.
* Description: Uploads employee performance data to the database. The file should contain columns like employee_id, employee_name, created, lead_taken, revenue_confirmed, etc.
* Example Request:
* `curl -X POST -F "file=@employee_data.csv" http://localhost:8000/api/upload/`
* Response:
* Success: `{"message": "Data uploaded successfully!"}`
* Error: `{"error": "An error occurred: [error details]"}`

### 2. Rep Performance

* Endpoint: /api/rep/performance/
* Method: GET
* Parameters:
* rep_id: The employee ID of the representative.
* Description: Analyzes the performance of a specific sales representative and provides qualitative feedback and actionable insights.
* Example Request:
* 
* `curl -X GET "http://localhost:8000/api/rep/performance/?rep_id=12345"`
* Response:
* Success:
`{
  "employee_id": "12345",
  "employee_name": "John Doe",
  "feedback": "Excellent performance. Focus on increasing lead conversion rates."
}`
* Error: `{"error": "rep_id parameter is required"}`

### 3. Team Performance

* Endpoint: /api/team/performance/
* Method: GET
* Description: Analyzes the overall sales team performance and provides qualitative feedback and actionable insights.
* Example Request:
* `curl -X GET "http://localhost:8000/api/team/performance/"`
* Response:
* Success:
* `{"feedback": "The team is performing well overall. Focus on increasing tour bookings."}`
* Error: `{"error": "An error occurred: [error details]"}`

### 4. Sales Performance Trends and Forecasting

* Endpoint: /api/trends/performance/
* Method: GET
* Parameters:
* time_period: The time period for analysis, can be monthly or quarterly.
* Description: Analyzes sales data over a specified time period and forecasts future performance.
* Example Request:
* curl -X GET "http://localhost:8000/api/trends/performance/?time_period=monthly"
* Response:
* Success:
`{
"trend_data": [
    {
      "period": "2025-01",
      "revenue_confirmed": 50000,
      "lead_taken": 200,
      "applications": 150
    },
    {
      "period": "2025-02",
      "revenue_confirmed": 60000,
      "lead_taken": 220,
      "applications": 170
    }
],
"forecast": {
    "forecast_revenue_confirmed": 60000,
    "forecast_lead_taken": 220,
    "forecast_applications": 170
}
}`
* Error: `{"error": "time_period parameter is required"}`


# Installation

### Clone the repository:

* git clone `https://github.com/yourusername/sales-performance-api.git`

### Install the required dependencies:

`pip install -r requirements.txt`

### Apply migrations to set up the database:

`python manage.py migrate`

### Run the development server:

`python manage.py runserver`
* The API will be available at `http://localhost:8000`.

### Dependencies
* Django
* Pandas
* Cohere API (for AI-powered performance feedback)
* Django Rest Framework
* Other dependencies listed in requirements.txt