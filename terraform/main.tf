provider "aws" {
    region = "eu-west-2"
    access_key = var.AWS_ACCESS_KEY_ID
    secret_key = var.AWS_SECRET_ACCESS_KEY
  
}

resource "aws_security_group" "c10-mahin-rds-sg" {
    name        = "c10-mahin-museum-db-sg"
    description = "Allow inbound Postgres access"
    vpc_id      = var.VPC_ID

  ingress {
    description      = "Postgres access"
    from_port        = 5432
    to_port          = 5432
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "museum_db" {
  allocated_storage            = 10
  db_name                      = "museum"
  identifier                   = "c10-mahin-museum-db"
  engine                       = "postgres"
  engine_version               = "16.1"
  instance_class               = "db.t3.micro"
  publicly_accessible          = true
  performance_insights_enabled = false
  skip_final_snapshot          = true
  db_subnet_group_name         = "public_subnet_group"
  vpc_security_group_ids       = [aws_security_group.c10-mahin-rds-sg.id]
  username                     = var.DB_USERNAME      
  password                     = var.DB_PASSWORD
}
