$body = '{"username":"admin","password":"admin123"}'
$r = Invoke-WebRequest -Uri 'http://10.10.1.1:8080/api/v1/auth/login' -Method POST -ContentType 'application/json' -Body $body
$r.Content
