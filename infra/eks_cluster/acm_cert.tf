resource "aws_acm_certificate" "kube_cert" {
  domain_name       = "<domain_name>"
  validation_method = "DNS"

  tags = {
    APP = "data_kube"
  }
}