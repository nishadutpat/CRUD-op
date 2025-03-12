resource "aws_dynamodb_table" "api_table" {
  name         = "api_table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }


  tags = {
    Name = "api_table"
  }
}
