The vulnerabilities listed below are present within the application:

Insecure Direct Object Reference (Broken Access Control) - Although Views do check for authorization of the Task ID parameter provided in the request URL, they do not check if the User associated with that parameter is indeed the Owner of the Task.

Cross-Site Request Forgery (CSRF) - There are no CSRF Tokens used to verify User requests for State Changes from the Insecure HTTP message method.

SQL Injection - Submitted User Input data is not validated or checked prior to being used in Database Queries.

Stored/Persistent Cross-Site Scripting (XSS) – The displayed comments made by Users are rendered through the |safe filter within Templates and are not automatically HTML escaped, thus allowing Forgeries containing Malicious JavaScript code to execute within the Browsers of all Users that view the Comments, including those who are not participating in an attack.

Insecure Data Binding (Mass Assignment / Privilege Escalation) - Users may gain Administrator Level Access to the system by submitting Payloads using the Profile Update View.
