import boto3
import datetime
import csv

# This script uses the 'lookup_events' cloudtrail function. It intializes a cloudtrail client,
# defines the time window of 14 days for log retrieval and sets up an output CSV file. After 
# querying and processing the logs, it writes the log records to a CSV file and prints a 
# message indicating the location of the CSV file. The script also handles potential 
# exceptions that may occur during the process.

cloudtrail_client = boto3.client('cloudtrail')

start_time = datetime.datetime.now() - datetime.timedelta(days=14)
end_time = datetime.datetime.now()

output_file = 'cloudtrail_audit_log.csv'

csv_fields = ['EventTime', 'EventName', 'Username', 'ResourceName', 'EventSource', 'ErrorCode']

log_records = []

def query_cloudtrail_logs():
    try:
        response = cloudtrail_client.lookup_events(
            StartTime=start_time,
            EndTime=end_time
        )
        
        for event in response['Events']:
            event_time = event['EventTime']
            event_name = event['EventName']
            username = event.get('Username', 'N/A')
            resource_name = event['Resources'][0]['ResourceName'] if event['Resources'] else 'N/A'
            event_source = event['EventSource']
            error_code = event.get('ErrorCode', 'N/A')
            
            log_records.append([event_time, event_name, username, resource_name, event_source, error_code])
    
    except Exception as e:
        print(f"An error occurred: {e}")
        log_records.append(['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'Error'])

query_cloudtrail_logs()

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(csv_fields)
    
    writer.writerows(log_records)

print(f"CloudTrail audit log has been saved to {output_file}")
