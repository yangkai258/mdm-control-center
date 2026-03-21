$url = 'https://i-blog.csdnimg.cn/img_convert/54b3d744727af27287ad7a86bcae7eb3.png'
$output = 'C:\Users\YKing\.openclaw\workspace\temp\arco_img.png'
try {
    Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing -TimeoutSec 15
    Write-Host "OK"
} catch {
    Write-Host "Error: $_"
}
