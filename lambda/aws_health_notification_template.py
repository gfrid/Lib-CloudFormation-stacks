import json

import boto3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
     # TODO implement
     # issues bellow only 
    ################################################
    if "issue" in json.dumps(event['detail']['eventTypeCategory']).strip('"'):
        if "us-east-1" in json.dumps(event['region']).strip('"'):
           SUBJECT = "Amazon Health Notification Issue US-EAST-1"
           colorcode = "#FF0000"
        else:
           SUBJECT = "Amazon Health Notification Issue"
           colorcode = "#FF9600"
    if "issue" not in json.dumps(event['detail']['eventTypeCategory']).strip('"'):
       SUBJECT = "Amazon Health Notification"
       colorcode = "#00FF00"
    if "resolved" in json.dumps(event['detail']['eventDescription'][0]['latestDescription']).strip('"'):
       if "issue" in json.dumps(event['detail']['eventTypeCategory']).strip('"'):
          colorcode = "#00FF00"
    if "operating normally" in json.dumps(event['detail']['eventDescription'][0]['latestDescription']).strip('"'):
       if "issue" in json.dumps(event['detail']['eventTypeCategory']).strip('"'):
          colorcode = "#00FF00"
    
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = "health@mycompany.com"
    
    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = "orgmail@mycompany.com"
    
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "us-east-1"
    
    # The subject line for the email.
    #SUBJECT = "Amazon Health Notification Alert"
    
    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = ("Amazon SES Alert\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )
                
    # The HTML body of the email.
    BODY_HTML = """<html>
    <head>
    </head>
    <body>
      <table class="reportWrapperTable" cellspacing="4" cellpadding="2" width="100%" rules="rows" style="border-collapse:collapse;color:#1f2240;background-color:#ffffff"><caption style="background-color:""" + colorcode + """;color:#1f2240;margin-bottom:.5em;font-size:18pt;width:100%;border:0">AWS Health Report</caption><thead style="100%;color:#ffffff;background-color:#1f2240;font-weight:bold"><tr><th scope="col" style="background-color:#1f2240">Detail Type</th><th scope="col" style="background-color:#1f2240">Time</th><th scope="col" style="background-color:#1f2240">Region</th><th scope="col" style="background-color:#1f2240">Service</th><th scope="col" style="background-color:#1f2240">Event Type Code</th><th scope="col" style="background-color:#1f2240">Event Type Category</th><th scope="col" style="background-color:#1f2240">Latest Description</th></tr></thead><tbody>
<tr><td>""" + json.dumps(event['detail-type']).strip('"') + """</td><td>""" + json.dumps(event['time']).strip('"') + """</td><td>""" + json.dumps(event['region']).strip('"') + """</td><td>""" + json.dumps(event['detail']['service']).strip('"') + """</td><td>""" + json.dumps(event['detail']['eventTypeCode']).strip('"') + """</td><td>""" + json.dumps(event['detail']['eventTypeCategory']).strip('"') + """</td><td>""" + json.dumps(event['detail']['eventDescription'][0]['latestDescription']).strip('"') + """</td></tr>
</tbody></table>
<br>
<br>
<br>
<br>
    <table class="reportWrapperTable" cellspacing="4" cellpadding="2" width="20%" rules="rows" style="border-collapse:collapse;color:#1f2240;background-color:#ffffff"><caption style="background-color:#ffffff;color:#1f2240;margin-bottom:.5em;font-size:14pt;width:100%;border:0">Color coding for notifications</caption><thead style="100%;color:#ffffff;background-color:#1f2240"><tr><th scope="col" style="background-color:#1f2240">Code</th><th scope="col" style="background-color:#1f2240">Category</th><th scope="col" style="background-color:#1f2240">Impact</th></tr></thead><tbody>
<tr><td bgcolor="#FF0000"></td><td>Open Issue</td><td>Service down main AWS Region</td></tr>
<tr><td bgcolor="#FF9600"></td><td>Open Issue</td><td>Service partially down<td></tr>
<tr><td bgcolor="#00FF00"></td><td>Notification</td><td>No impact</td></tr>
</tbody></table>
<br>
    <table class="reportWrapperTable" cellspacing="4" cellpadding="2" width="20%" rules="rows" style="border-collapse:collapse;color:#1f2240;background-color:#ffffff"><caption style="background-color:#ffffff;color:#1f2240;margin-bottom:.5em;font-size:14pt;width:100%;border:0">Alert Teams</caption><thead style="100%;color:#ffffff;background-color:#1f2240"><tr><th scope="col" style="background-color:#1f2240">Service</th><th scope="col" style="background-color:#1f2240">Team</th></tr></thead><tbody>
<tr><td>""" + json.dumps(event['detail']['service']).strip('"') + """</td><td>""" + alert + """</td></tr>
</tbody></table>
<br>
    </body>
    </html>"""            
    
    # The character encoding for the email.
    CHARSET = "UTF-8"
    
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])


    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }
