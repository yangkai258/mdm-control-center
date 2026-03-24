$token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwicm9sZV9pZCI6MCwidGVuYW50X2lkIjoiIiwiaXNfc3VwZXJfYWRtaW4iOmZhbHNlLCJleHAiOjE3NzQzNTg4NDQsImlhdCI6MTc3NDI3MjQ0NH0.ZPIakWOUr16IK9bx9XSyLNtGKLYTH1jMCAgOlcvVXAY"
$r = Invoke-WebRequest -Uri 'http://10.10.1.1:8080/api/v1/devices' -Headers @{"Authorization"="Bearer $token"}
$r.Content
