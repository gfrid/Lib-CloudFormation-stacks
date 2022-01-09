# Lib_CloudFormation_stacks

Templates:
1. Useful Cloudformation stacks ready to use, inlcudes remidiation with Assume Role. Make sure you create IAM role that has access to resources you want to remediate.

Lambda:
1. IAMCreateUserEvent-AttachBoundryPolicy.py - Automaticly attaches AWS Boundary Permissions to IAM User upon cration. EventBridge must be configured to execute Lambda.
2. aws_health_notification_template.py - SES notification HTML teamplate, send out HTML mail when AWS health notification arrives from EvenBridge. EventBridge must be configured to execute Lambda. Verfied email (MX/DKIM) must be configured in your org O365/Exchange. 
