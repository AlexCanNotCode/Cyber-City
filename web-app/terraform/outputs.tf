output "api_url" {
  description = "Invoke URL for the GET /wait endpoint"
  value = format(
    "https://%s.execute-api.%s.amazonaws.com/%s/wait",
    aws_api_gateway_rest_api.api.id,
    "us-east-1",                            # Update this if you're in a different AWS region
    aws_api_gateway_stage.prod.stage_name
  )
}
