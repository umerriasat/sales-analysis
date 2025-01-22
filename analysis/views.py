import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from .models import EmployeePerformance
import cohere
from collections import defaultdict
from datetime import datetime

cohere_api_key = "Cm64CRD65ERzwF4bM8uiVZFHazvTBMzGp2Q0WaZ6"  # Replace with your Cohere API key
co = cohere.Client(cohere_api_key)


def query_llm(prompt):
    response = co.generate(
        model="command-r-plus",
        prompt=prompt,
        max_tokens=150,
        temperature=0.4,
    )
    return response.generations[0].text.strip()


class UploadEmployeeData(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        file = request.FILES.get('file', None)
        if not file:
            return Response({"error": "No file provided"}, status=400)

        if not (file.name.endswith('.csv') or file.name.endswith('.json')):
            return Response({"error": "Unsupported file format. Please upload a CSV or JSON file."}, status=400)

        try:
            if file.name.endswith('.csv'):
                data = pd.read_csv(file)
            elif file.name.endswith('.json'):
                data = pd.read_json(file)

            for _, row in data.iterrows():
                EmployeePerformance.objects.create(
                    employee_id=row['employee_id'],
                    employee_name=row['employee_name'],
                    created=row['created'],
                    dated=row['dated'],
                    lead_taken=row['lead_taken'],
                    tours_booked=row['tours_booked'],
                    applications=row['applications'],
                    tours_per_lead=row['tours_per_lead'],
                    apps_per_tour=row['apps_per_tour'],
                    apps_per_lead=row['apps_per_lead'],
                    revenue_confirmed=row['revenue_confirmed'],
                    revenue_pending=row['revenue_pending'],
                    revenue_runrate=row['revenue_runrate'],
                    tours_in_pipeline=row['tours_in_pipeline'],
                    avg_deal_value_30_days=row['avg_deal_value_30_days'],
                    avg_close_rate_30_days=row['avg_close_rate_30_days'],
                    estimated_revenue=row['estimated_revenue'],
                    tours=row['tours'],
                    tours_runrate=row['tours_runrate'],
                    tours_scheduled=row['tours_scheduled'],
                    tours_pending=row['tours_pending'],
                    tours_cancelled=row['tours_cancelled'],
                    mon_text=row['mon_text'],
                    tue_text=row['tue_text'],
                    wed_text=row['wed_text'],
                    thur_text=row['thur_text'],
                    fri_text=row['fri_text'],
                    sat_text=row['sat_text'],
                    sun_text=row['sun_text'],
                    mon_call=row['mon_call'],
                    tue_call=row['tue_call'],
                    wed_call=row['wed_call'],
                    thur_call=row['thur_call'],
                    fri_call=row['fri_call'],
                    sat_call=row['sat_call'],
                    sun_call=row['sun_call']
                )

            return Response({"message": "Data uploaded successfully!"})

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)


class RepPerformance(APIView):
    def get(self, request):
        rep_id = request.query_params.get('rep_id')
        if not rep_id:
            return Response({"error": "rep_id parameter is required"}, status=400)

        try:
            data = EmployeePerformance.objects.filter(employee_id=rep_id).first()
            if not data:
                return Response({"error": "Employee not found"}, status=404)

            prompt = f"""
            Analyze the performance of {data.employee_name}:
            - Leads taken: {data.lead_taken}
            - Tours booked: {data.tours_booked}
            - Applications: {data.applications}
            - Revenue confirmed: {data.revenue_confirmed}
            - Revenue pending: {data.revenue_pending}
            Provide qualitative feedback and actionable insights.
            """

            feedback = query_llm(prompt)
            return Response({
                "employee_id": rep_id,
                "employee_name": data.employee_name,
                "feedback": feedback
            })

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)


class TeamPerformance(APIView):
    def get(self, request):
        data = EmployeePerformance.objects.all()
        total_leads = sum([d.lead_taken for d in data])
        total_revenue = sum([d.revenue_confirmed for d in data])

        prompt = f"""
        Analyze the performance of the entire sales team:
        - Total leads taken: {total_leads}
        - Total revenue confirmed: {total_revenue}
        Provide qualitative feedback and actionable insights.
        """

        feedback = query_llm(prompt)
        return Response({"feedback": feedback})


import pandas as pd
from rest_framework.views import APIView
from rest_framework.response import Response
from datetime import datetime
from .models import EmployeePerformance
from collections import defaultdict


class PerformanceTrends(APIView):
    def get(self, request):
        try:
            time_period = request.query_params.get('time_period')
            if not time_period:
                return Response({"error": "time_period parameter is required"}, status=400)

            # Check if time_period is valid
            if time_period not in ['monthly', 'quarterly']:
                return Response({"error": "Invalid time_period. Please use 'monthly' or 'quarterly'."}, status=400)

            # Fetch all employee performance data
            data = EmployeePerformance.objects.all()

            # Create an empty dictionary to store aggregated data
            aggregated_data = defaultdict(lambda: {'revenue_confirmed': 0, 'lead_taken': 0, 'applications': 0})

            # Group data by the required time period
            for record in data:
                # Convert the created field (which is a string) to a datetime object
                record_date = pd.to_datetime(record.created,
                                             errors='coerce')  # Coerce invalid dates to NaT (Not a Time)
                if pd.isna(record_date):  # If the conversion failed
                    continue  # Skip this record or handle the error appropriately

                # Extract month and quarter
                if time_period == 'monthly':
                    period_key = record_date.strftime('%Y-%m')  # Year-Month format
                elif time_period == 'quarterly':
                    quarter = (record_date.month - 1) // 3 + 1  # Get quarter (1, 2, 3, 4)
                    period_key = f"{record_date.year}-Q{quarter}"

                # Aggregate data based on the period (month or quarter)
                aggregated_data[period_key]['revenue_confirmed'] += record.revenue_confirmed
                aggregated_data[period_key]['lead_taken'] += record.lead_taken
                aggregated_data[period_key]['applications'] += record.applications

            # Forecasting (for simplicity, let's assume a basic trend of calculating the average of the last period)
            # Example: Simple linear forecast (basic, for illustrative purposes)

            trend_data = []
            periods = sorted(aggregated_data.keys())  # Sort periods in chronological order

            # Calculate the trend (you can replace this with a more sophisticated forecasting algorithm)
            for period in periods:
                data_point = aggregated_data[period]
                trend_data.append({
                    "period": period,
                    "revenue_confirmed": data_point['revenue_confirmed'],
                    "lead_taken": data_point['lead_taken'],
                    "applications": data_point['applications']
                })

            # Basic forecast (simply averaging the last period’s values)
            if trend_data:
                last_period = trend_data[-1]
                forecast = {
                    "forecast_revenue_confirmed": last_period['revenue_confirmed'],
                    "forecast_lead_taken": last_period['lead_taken'],
                    "forecast_applications": last_period['applications']
                }
            else:
                forecast = {}

            # Return response
            return Response({
                "trend_data": trend_data,
                "forecast": forecast
            })

        except Exception as e:
            return Response({"error": f"An error occurred: {str(e)}"}, status=500)

