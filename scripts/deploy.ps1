# Configuration
$STACK_NAME = "weather-alert-system"
$REGION = "us-east-1"  # Explicitly defined
$ALERT_EMAIL = "idankan571@gmail.com"

Write-Host "[*] Packaging Lambda function..." -ForegroundColor Cyan
if (Test-Path "dist") { Remove-Item "dist" -Recurse -Force }
New-Item -ItemType Directory -Path "dist"

# Flatten the zip structure correctly
Compress-Archive -Path src\* -DestinationPath dist\function.zip -Force

if (-not (Test-Path "dist\function.zip")) {
    Write-Error "Failed to create ZIP file. Deployment aborted."
    exit
}

Write-Host "[+] Deploying to AWS via CloudFormation..." -ForegroundColor Green
aws cloudformation deploy `
    --template-file infrastructure/cloudformation.yaml `
    --stack-name $STACK_NAME `
    --capabilities CAPABILITY_IAM `
    --region $REGION `
    --parameter-overrides `
        CityName="Nairobi" `
        AlertEmail=$ALERT_EMAIL

Write-Host "[DONE] Deployment Complete!" -ForegroundColor Green