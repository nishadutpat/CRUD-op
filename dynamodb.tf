resource "aws_dynamodb_table" "deplo_table" {
  name         = "deplo_table"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "id"

  attribute {
    name = "id"
    type = "S"
  }


  tags = {
    Name = "deplo_table"
  }
}
