output "api_url" {
  value = format(
    "https://%s.execute-api.%s.amazonaws.com/%s/wait",
    aws_api_gateway_rest_api.api.id,
    "us-east-1",
    aws_api_gateway_stage.prod.stage_name
  )
}
