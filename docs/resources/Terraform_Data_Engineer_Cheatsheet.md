# Terraform Cheatsheet

!!! note "AI Assisted (Grok 3)"

A cheatsheet which is actually useful to setup production grade IaC project using Terraform and Gitlab covering :

   - **Multi-Environment setup**
   - **CI/CD**
   - **State Management**
   - **Rollbacks**
   - **Capturing and Logging Outputs**

And more..

## 1. Core Concepts

- **Infrastructure as Code (IaC)**: Define  infrastructure (e.g., Lambdas, databases, data lakes, compute clusters) in `.tf` files.
- **Providers**: Plugins for cloud platforms (e.g., `aws`, `google`, `azurerm`) or tools (e.g., `snowflake`, `databricks`).
- **Resources**: Infrastructure components (e.g., S3 buckets, RDS instances, BigQuery datasets).
- **Modules**: Reusable, parameterized templates for common infrastructure patterns.
- **State**: Tracks infrastructure state, stored locally (`terraform.tfstate`) or remotely (e.g., S3, GCS).
- **Workspaces**: Isolate environments (e.g., `dev`, `staging`, `prod`) within a single configuration directory using multiple state files. **Note**: This project uses folder-based isolation (separate directories for each environment) instead of workspaces for better clarity and flexibility.

## 2. Key Terraform Components and State Management
- **State Management**: 
    - The `terraform.tfstate` file records the current state of your infrastructure, mapping Terraform configurations to real-world resources, including dynamically generated attributes (e.g., S3 bucket ARNs, RDS endpoints).
     - **Local State**: Stored locally by default; suitable for solo or small projects but risky for teams due to potential conflicts or loss.
     - **Remote State**: Store state in a remote backend (e.g., S3, GCS, Azure Blob) with locking (e.g., DynamoDB) to prevent concurrent modifications and enable team collaboration.
     - **Environment Isolation**: This project uses separate directories (`environments/dev`, `environments/staging`, `environments/prod`) with distinct state files (e.g., `data-infra/dev/terraform.tfstate`) instead of Terraform workspaces, providing clear separation and environment-specific configurations.
     - **Best Practices**: Use remote backends for production, encrypt state files, restrict access via IAM, and regularly back up state files.
     - **State Drift**: Occurs when manual changes bypass Terraform. Use `terraform refresh` to update state or `terraform import` to bring resources under management.
- **outputs.tf**: 

     - Defines output values exposed after `terraform apply`, such as resource IDs, endpoints, or computed values (e.g., S3 bucket ARN, RDS endpoint).
     - **How It Works**: Outputs reference attributes stored in the state file, which captures dynamically generated values during resource creation. `outputs.tf` itself does not store values but declares what to extract from the state.
     - **Example**:
       ```hcl
       output "s3_bucket_arn" {
         value       = aws_s3_bucket.bucket.arn
         description = "ARN of the S3 bucket"
       }
       ```
       - After `terraform apply`, the state file stores the bucket’s ARN, and the output retrieves it.
     - **Updating Outputs**: Edit `outputs.tf` in the repository to add, modify, or remove outputs. Commit changes to Git, and they take effect on the next `terraform apply` or `terraform output`.
     - **Usage**: Outputs are displayed in the CLI (`terraform output`), exported to JSON (`terraform output -json`), used in CI/CD pipelines, or referenced by other modules via remote state.
     - **Best Practices**: Use descriptive names and descriptions, avoid sensitive data in outputs, and capture outputs in pipelines for automation.
   
- **variables.tf**: Declares input variables with types, defaults, and validations to parameterize configurations.
- **terraform.tfvars**: Provides default variable values, overridden by environment-specific `.tfvars` files or CLI flags.
- **backend.tf**: Configures the remote state backend, specifying where and how state is stored and locked.

## 3. Repository Folder Structure

A well-organized repository structure ensures clarity, modularity, and scalability for managing data infrastructure across multiple environments.

```
data-infra/
├── modules/                     # Reusable Terraform modules
│   ├── s3_bucket/               # S3 bucket module
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── rds/                     # RDS module
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   ├── databricks/              # Databricks module
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── glue_job/                # Glue job module
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── environments/                # Environment-specific configurations
│   ├── dev/
│   │   ├── main.tf            # Dev-specific resources
│   │   ├── variables.tf
│   │   ├── outputs.tf         # Environment-specific outputs
│   │   ├── backend.tf
│   │   └── terraform.tfvars    # Dev variable values
│   ├── staging/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── backend.tf
│   │   └── terraform.tfvars
│   └── prod/
│       ├── main.tf
│       ├── variables.tf
│       ├── outputs.tf
│       ├── backend.tf
│       └── terraform.tfvars
├── scripts/                     # Supporting scripts (e.g., PySpark for Glue)
│   └── transform.py
├── .gitignore                   # Git ignore file
├── README.md                    # Project documentation
└── .gitlab-ci.yml               # CI/CD pipeline configuration
```

### Explanation

- **modules/**: Contains reusable modules for resources like S3, RDS, Databricks, and Glue jobs, each with its own `outputs.tf`.
- **environments/**: Separates configurations for `dev`, `staging`, and `prod`, each with its own `main.tf`, `variables.tf`, `outputs.tf`, `backend.tf`, and `terraform.tfvars`, providing isolation without workspaces.
- **scripts/**: Stores scripts (e.g., PySpark scripts for Glue jobs) uploaded to S3.
- **.gitignore**: Ignores `.terraform/`, `*.tfstate`, `*.tfstate.backup`, and sensitive files like `*.tfvars` with secrets.
- **README.md**: Documents setup instructions, module usage, CI/CD pipeline details, artifact review, rollback procedures, output management, and environment isolation.

## 4. Basic Commands

```bash
terraform init            # Initialize project, download providers
terraform plan            # Preview changes
terraform apply           # Apply changes
terraform destroy         # Tear down infrastructure
terraform state list      # View managed resources
terraform state show <resource>   # Inspect resource state
terraform output          # Display all output values
terraform output -json    # Export outputs as JSON
# Note: The following workspace commands are included for reference but are not used in this project, which uses folder-based environment isolation instead.
terraform workspace list  # List workspaces (not used)
terraform workspace select <env>  # Switch to environment (not used)
terraform workspace new <env>     # Create new workspace (not used)
```

## 5. Provider Configuration

```hcl
# environments/dev/main.tf
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    snowflake = {
      source  = "Snowflake-Labs/snowflake"
      version = "~> 0.76"
    }
  }
}

provider "aws" {
  region = var.region
  assume_role {
    role_arn = "arn:aws:iam::${var.account_id}:role/TerraformRole"
  }
}

provider "snowflake" {
  account = var.snowflake_account
  role    = "ACCOUNTADMIN"
}
```

## 6. Multi-Environment Configuration

### Variables

```hcl
# environments/dev/variables.tf
variable "region" {
  type    = string
  default = "us-east-1"
}

variable "account_id" {
  type = string
}

variable "environment" {
  type = string
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be dev, staging, or prod."
  }
}
```

### Environment-Specific `.tfvars`
```hcl
# environments/dev/terraform.tfvars
region      = "us-east-1"
account_id  = "123456789012"
environment = "dev"
```

### Applying Environment Config
```bash
cd environments/dev
terraform init
terraform apply -var-file=terraform.tfvars
```

## 7. Remote State Management
```hcl
# environments/dev/backend.tf
terraform {
  backend "s3" {
    bucket         = "my-terraform-state"
    key            = "data-infra/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
  }
}
```

## 8. Module Example: S3 Bucket
```hcl
# modules/s3_bucket/main.tf
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.environment}-${var.bucket_name}"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Environment = var.environment
  }
}

# modules/s3_bucket/variables.tf
variable "bucket_name" {
  type = string
}

variable "environment" {
  type = string
}

# modules/s3_bucket/outputs.tf
output "bucket_arn" {
  value       = aws_s3_bucket.bucket.arn
  description = "ARN of the S3 bucket"
}

output "bucket_name" {
  value       = aws_s3_bucket.bucket.id
  description = "Name of the S3 bucket"
}
```

### Using the Module
```hcl
# environments/dev/main.tf
module "data_lake" {
  source      = "../../modules/s3_bucket"
  bucket_name = "data-lake"
  environment = var.environment
}

# environments/dev/outputs.tf
output "data_lake_arn" {
  value       = module.data_lake.bucket_arn
  description = "ARN of the data lake S3 bucket"
}
```

## 9. Data Infrastructure Examples

### Snowflake Database
```hcl
# Fetch existing Snowflake role
data "snowflake_role" "admin" {
  name = "ACCOUNTADMIN"
}

resource "snowflake_database" "data_warehouse" {
  name = "${var.environment}_DATA_WAREHOUSE"
}

resource "snowflake_schema" "raw" {
  database = snowflake_database.data_warehouse.name
  name     = "RAW"
}

# outputs.tf
output "snowflake_database_name" {
  value       = snowflake_database.data_warehouse.name
  description = "Name of the Snowflake database"
}
```

### Databricks Cluster

```hcl
# Fetch existing Databricks workspace
data "databricks_spark_version" "latest" {
  latest = true
}

resource "databricks_cluster" "data_processing" {
  cluster_name            = "${var.environment}-data-processing"
  spark_version           = data.databricks_spark_version.latest.id
  node_type_id            = var.environment == "prod" ? "i3.2xlarge" : "i3.xlarge"
  autotermination_minutes = 30
}

# outputs.tf
output "databricks_cluster_id" {
  value       = databricks_cluster.data_processing.cluster_id
  description = "ID of the Databricks cluster"
}
```

### AWS Glue Crawler

```hcl
# Fetch existing Glue database
data "aws_glue_catalog_database" "main" {
  name = "${var.environment}_catalog"
}

resource "aws_glue_crawler" "s3_crawler" {
  name          = "${var.environment}-s3-crawler"
  database_name = data.aws_glue_catalog_database.main.name
  role          = aws_iam_role.glue_role.arn
  s3_target {
    path = module.data_lake.bucket
  }
}

# outputs.tf
output "glue_crawler_name" {
  value       = aws_glue_crawler.s3_crawler.name
  description = "Name of the Glue crawler"
}
```

### AWS RDS Database

```hcl
# Fetch existing VPC and subnets
data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "default_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# modules/rds/main.tf
resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "${var.environment}-rds-subnet-group"
  subnet_ids = var.subnet_ids
  tags = {
    Environment = var.environment
  }
}

resource "aws_db_instance" "rds_instance" {
  identifier              = "${var.environment}-${var.db_name}"
  engine                  = var.db_engine
  engine_version          = var.engine_version
  instance_class          = var.environment == "prod" ? var.prod_instance_class : var.dev_instance_class
  allocated_storage       = var.allocated_storage
  username                = var.db_username
  password                = var.db_password
  db_subnet_group_name    = aws_db_subnet_group.rds_subnet_group.name
  vpc_security_group_ids  = var.security_group_ids
  multi_az                = var.environment == "prod" ? true : false
  backup_retention_period = var.environment == "prod" ? 7 : 1
  skip_final_snapshot     = var.environment != "prod"
  tags = {
    Environment = var.environment
  }
}

# modules/rds/variables.tf
variable "db_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "db_engine" {
  type    = string
  default = "postgres"
}

variable "engine_version" {
  type    = string
  default = "15.3"
}

variable "prod_instance_class" {
  type    = string
  default = "db.m5.large"
}

variable "dev_instance_class" {
  type    = string
  default = "db.t3.micro"
}

variable "allocated_storage" {
  type    = number
  default = 20
}

variable "db_username" {
  type = string
}

variable "db_password" {
  type      = string
  sensitive = true
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_ids" {
  type = list(string)
}

# modules/rds/outputs.tf
output "rds_endpoint" {
  value       = aws_db_instance.rds_instance.endpoint
  description = "Endpoint of the RDS instance"
}

# Using the RDS Module
# environments/dev/main.tf
module "rds_postgres" {
  source             = "../../modules/rds"
  db_name            = "datawarehouse"
  environment        = var.environment
  db_engine          = "postgres"
  engine_version     = "15.3"
  prod_instance_class = "db.m5.large"
  dev_instance_class  = "db.t3.micro"
  allocated_storage   = 100
  db_username        = var.db_username
  db_password        = var.db_password
  subnet_ids         = data.aws_subnets.default_subnets.ids
  security_group_ids = [aws_security_group.rds_sg.id]
}

# environments/dev/outputs.tf
output "rds_postgres_endpoint" {
  value       = module.rds_postgres.rds_endpoint
  description = "Endpoint of the RDS PostgreSQL instance"
}
```

### AWS Glue PySpark Job

```hcl
# Fetch S3 bucket from another configuration
data "terraform_remote_state" "data_lake" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "data-infra/${var.environment}/terraform.tfstate"
    region = "us-east-1"
  }
}

# modules/glue_job/main.tf
resource "aws_glue_job" "pyspark_job" {
  name              = "${var.environment}-${var.job_name}"
  role_arn          = var.glue_role_arn
  glue_version      = "4.0"
  worker_type       = var.environment == "prod" ? "G.2X" : "G.1X"
  number_of_workers = var.environment == "prod" ? 10 : 2
  max_retries       = 1

  command {
    script_location = "s3://${var.script_bucket}/${var.script_path}"
    python_version  = "python3"
    name            = "glueetl"
  }

  default_arguments = {
    "--job-name"              = "${var.environment}-${var.job_name}"
    "--TempDir"               = "s3://${var.temp_bucket}/temp/"
    "--enable-metrics"         = "true"
    "--enable-continuous-log" = "true"
    "--environment"           = var.environment
  }

  tags = {
    Environment = var.environment
  }
}

# modules/glue_job/variables.tf
variable "job_name" {
  type = string
}

variable "environment" {
  type = string
}

variable "glue_role_arn" {
  type = string
}

variable "script_bucket" {
  type = string
}

variable "script_path" {
  type = string
}

variable "temp_bucket" {
  type = string
}

# modules/glue_job/outputs.tf
output "glue_job_name" {
  value       = aws_glue_job.pyspark_job.name
  description = "Name of the Glue PySpark job"
}

# Using the Glue Job Module
# environments/dev/main.tf
module "glue_job" {
  source         = "../../modules/glue_job"
  job_name       = "data-transform"
  environment    = var.environment
  glue_role_arn  = aws_iam_role.glue_role.arn
  script_bucket  = data.terraform_remote_state.data_lake.outputs.bucket_name
  script_path    = "scripts/transform.py"
  temp_bucket    = data.terraform_remote_state.data_lake.outputs.bucket_name
}

# environments/dev/outputs.tf
output "glue_job_name" {
  value       = module.glue_job.glue_job_name
  description = "Name of the Glue job"
}
```

## 10. GitLab CI/CD Pipeline for Terraform

A GitLab CI/CD pipeline automates validation, planning, and deployment of Terraform configurations across environments, with artifacts stored for review, auditing, and output capture. This project uses folder-based environment isolation (folders like `environments/dev`, `environments/staging`, etc.) instead of Terraform workspaces for clarity and flexibility.

### Terraform Artifacts

Terraform artifacts are files generated during pipeline jobs (e.g., `terraform plan`, `terraform apply`, or `terraform output`) saved in GitLab for review, auditing, or downstream use. They include:

- **Plan Artifacts**:

      - `tfplan`: Binary plan file from `terraform plan -out=tfplan`, used by `terraform apply`.
      - `tfplan.json`: JSON representation (`terraform show -json tfplan`) for programmatic analysis.
      - `tfplan.txt`: Human-readable text (`terraform show tfplan`) for manual review.
    
- **Apply Artifacts**:

      - `apply.log`: Log file capturing `terraform apply` output, detailing infrastructure changes.
    
- **Output Artifacts**:

      - `outputs.json`: JSON file capturing `terraform output -json`, containing dynamically generated values (e.g., S3 bucket ARNs, RDS endpoints).

- **Purpose**:

      - **Review**: Plan artifacts for verifying changes before applying.
      - **Audit**: Apply logs and outputs for compliance and debugging.
      - **Consistency**: Binary `tfplan` ensures `apply` matches the reviewed plan.
      - **Automation**: Outputs enable integration with other systems or modules.
- **Retention**:
      - GitLab artifacts can be stored for a specified period (e.g., `1 year` or `forever`, subject to GitLab plan).
      - For long-term audit, upload artifacts to S3 with custom retention policies.

### Capturing Terraform Outputs
Outputs defined in `outputs.tf` are captured in the pipeline to expose dynamically generated values for review, automation, or integration with other systems.

#### Steps to Capture Outputs

1. **Generate Outputs**: Run `terraform output -json > outputs.json` in the `apply` job to save outputs as a JSON file.
2. **Store as Artifacts**: Include `outputs.json` in the `artifacts` section of `.gitlab-ci.yml`.
3. **Review Outputs**: Download `outputs.json` from the GitLab pipeline UI or parse it programmatically (e.g., `jq '.s3_bucket_arn.value' outputs.json`).
4. **Use Outputs**: Reference `outputs.json` in downstream jobs (e.g., to configure applications) or upload to S3 for long-term storage.

#### Example Workflow

- After `apply_dev` runs, `outputs.json` is generated, containing values like `data_lake_arn` and `rds_postgres_endpoint`.
- The team downloads `outputs.json` to verify resource endpoints.
- Outputs are uploaded to S3 for audit or used in another job to configure a data pipeline.

### Pipeline Configuration

```yaml
# .gitlab-ci.yml
stages:
  - validate
  - plan
  - apply
  - backup

variables:
  AWS_REGION: "us-east-1"
  TF_VAR_account_id: "123456789012"

# Cache Terraform plugins
cache:
  key: ${CI_PROJECT_ID}
  paths:
    - .terraform/
    - environments/dev/.terraform/
    - environments/staging/.terraform/
    - environments/prod/.terraform/

# Base job template
.terraform_base:
  image: hashicorp/terraform:1.5.7
  before_script:
    - terraform --version
    - apk add --no-cache aws-cli
    - aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    - aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    - aws configure set region $AWS_REGION

# Validate Terraform configuration
validate:
  stage: validate
  extends: .terraform_base
  script:
    - cd environments/dev
    - terraform init -backend-config=backend.tf
    - terraform validate
    - cd ../staging
    - terraform init -backend-config=backend.tf
    - terraform validate
    - cd ../prod
    - terraform init -backend-config=backend.tf
    - terraform validate

# Plan for Dev
plan_dev:
  stage: plan
  extends: .terraform_base
  script:
    - cd environments/dev
    - terraform init -backend-config=backend.tf
    - terraform plan -var-file=terraform.tfvars -out=tfplan
    - terraform show -json tfplan > tfplan.json
    - terraform show tfplan > tfplan.txt
  artifacts:
    paths:
      - environments/dev/tfplan
      - environments/dev/tfplan.json
      - environments/dev/tfplan.txt
    expire_in: 1 week
  only:
    - main
    - merge_requests

# Plan for Staging
plan_staging:
  stage: plan
  extends: .terraform_base
  script:
    - cd environments/staging
    - terraform init -backend-config=backend.tf
    - terraform plan -var-file=terraform.tfvars -out=tfplan
    - terraform show -json tfplan > tfplan.json
    - terraform show tfplan > tfplan.txt
  artifacts:
    paths:
      - environments/staging/tfplan
      - environments/staging/tfplan.json
      - environments/staging/tfplan.txt
    expire_in: 1 week
  only:
    - main
    - merge_requests

# Plan for Prod
plan_prod:
  stage: plan
  extends: .terraform_base
  script:
    - cd environments/prod
    - terraform init -backend-config=backend.tf
    - terraform plan -var-file=terraform.tfvars -out=tfplan
    - terraform show -json tfplan > tfplan.json
    - terraform show tfplan > tfplan.txt
  artifacts:
    paths:
      - environments/prod/tfplan
      - environments/prod/tfplan.json
      - environments/prod/tfplan.txt
    expire_in: 1 week
  only:
    - main
    - merge_requests

# Apply for Dev
apply_dev:
  stage: apply
  extends: .terraform_base
  script:
    - cd environments/dev
    - terraform init -backend-config=backend.tf
    - terraform apply -auto-approve tfplan > apply.log 2>&1
    - terraform output -json > outputs.json
    - aws s3 cp apply.log s3://my-audit-logs/terraform-apply/dev/$(date +%Y-%m-%d_%H-%M-%S).log || true
    - aws s3 cp outputs.json s3://my-audit-logs/terraform-outputs/dev/$(date +%Y-%m-%d_%H-%M-%S).json || true
  artifacts:
    paths:
      - environments/dev/apply.log
      - environments/dev/outputs.json
    expire_in: 1 year
  dependencies:
    - plan_dev
  when: manual
  only:
    - main

# Apply for Staging
apply_staging:
  stage: apply
  extends: .terraform_base
  script:
    - cd environments/staging
    - terraform init -backend-config=backend.tf
    - terraform apply -auto-approve tfplan > apply.log 2>&1
    - terraform output -json > outputs.json
    - aws s3 cp apply.log s3://my-audit-logs/terraform-apply/staging/$(date +%Y-%m-%d_%H-%M-%S).log || true
    - aws s3 cp outputs.json s3://my-audit-logs/terraform-outputs/staging/$(date +%Y-%m-%d_%H-%M-%S).json || true
  artifacts:
    paths:
      - environments/staging/apply.log
      - environments/staging/outputs.json
    expire_in: 1 year
  dependencies:
    - plan_staging
  when: manual
  only:
    - main

# Apply for Prod
apply_prod:
  stage: apply
  extends: .terraform_base
  script:
    - cd environments/prod
    - terraform init -backend-config=backend.tf
    - terraform apply -auto-approve tfplan > apply.log 2>&1
    - terraform output -json > outputs.json
    - aws s3 cp apply.log s3://my-audit-logs/terraform-apply/prod/$(date +%Y-%m-%d_%H-%M-%S).log || true
    - aws s3 cp outputs.json s3://my-audit-logs/terraform-outputs/prod/$(date +%Y-%m-%d_%H-%M-%S).json || true
  artifacts:
    paths:
      - environments/prod/apply.log
      - environments/prod/outputs.json
    expire_in: 1 year
  dependencies:
    - plan_prod
  when: manual
  only:
      - main
  environment:
    name: production

# Backup State for Dev
backup_state_dev:
stage:
 backup
extends:
 .terraform_base
script:
  - cd environments/dev
  - terraform init - backend-config=backend.tf
  - aws s3 cp s3://my-terraform-state/data-infra/dev/terraform.tfstate s3://my-terraform-state-backup/data-infra/dev/$(date +%Y-%m-%d_%H-%M-%S).tfstate || true
when:
 always
only:
 - main
dependencies:
 - apply_dev

# Backup State for Staging
backup_state:
 stage: backup
 extends: .terraform_base
 script:
  - cd environments/staging
  - terraform init -backend-config=backend.tf
  - aws s3 cp s3://my-terraform-state/data-infra/staging/terraform.tfstate s3://my-terraform-state-backup/data-infra/staging/$(date +%Y-%m-%d_%H-%M-%S).tfstate || true
 when: always
  only:
      - main
      dependencies:
        - apply_staging

# Backup State for Prod
backup_state_prod:
 stage: apply
 extends: .terraform_base
  script:
   - cd environments/prod
   - terraform init -backend-config=backend.tf
   - aws s3 cp s3://my-terraform-state/data-infra/prod/terraform.tfstate s3://my-terraform-state-backup/data-infra/prod/$(date +%Y-%m-%d_%H-%M-%S).tfstate || true
  when: always
  only:
   - main
  dependencies:
   - apply_prod
```

### Reviewing Plan, Apply, and Output Artifacts

Plan artifacts (`tfplan`, `tfplan.json`, `tfplan.txt`), apply logs (`apply.log`), and output files (`outputs.json`) are generated during the `plan` and `apply` stages and stored in GitLab for review, auditing, and automation.

#### Steps to Review

1. **Access Artifacts**: In GitLab, navigate to the pipeline or merge request, go to the `plan_dev`, `plan_staging`, `plan_prod`, `apply_dev`, `apply_staging`, or `apply_prod` job, and download the artifacts.

2. **Review Plan Artifacts**:

    - Open `tfplan.txt` for a human-readable summary of proposed changes.
    - Use `tfplan.json` for programmatic analysis with tools like `jq` (e.g., `jq '.resource_changes[] | {address: .address, change: .change.actions}' tfplan.json`).

3. **Review Apply Logs**:

    - Open `apply.log` to review the changes applied, including resources created, updated, or deleted.
    - For long-term audit, retrieve logs from S3: `aws s3 cp s3://my-audit-logs/terraform-apply/<env>/<timestamp>.log .`

4. **Review Output Artifacts**:

    - Open `outputs.json` to inspect dynamically generated values (e.g., S3 bucket ARNs, RDS endpoints).
    - Parse with `jq` (e.g., `jq '.data_lake_arn.value' outputs.json`).
    - For audit or integration, retrieve from S3: `aws s3 cp s3://my-audit-logs/terraform-outputs/<env>/<timestamp>.json .`

5. **Team Review**:

    - Share artifact links in merge request comments or integrate with notification tools (e.g., Slack) to alert reviewers.
    - Require approval from team members before triggering `apply` jobs.

6. **Apply Changes**: After approving plan artifacts, trigger the corresponding `apply` job, which uses the `tfplan` artifact, generates `apply.log`, and captures `outputs.json`.

#### Example Workflow

- A developer pushes a change to the `main` branch, triggering `plan_dev`.
- The team downloads `environments/dev/tfplan.txt` to review changes (e.g., new S3 bucket).
- They check `tfplan.json` with `jq` to verify compliance (e.g., correct instance types).
- After approval, a team member triggers `apply_dev`, generating `apply.log` and `outputs.json`, which are stored as artifacts and uploaded to S3 for audit.
- The team reviews `outputs.json` to confirm resource endpoints (e.g., `data_lake_arn`).

## 11. Best Practices (General)

- **Modularize**: Break infrastructure into reusable modules (e.g., S3, RDS, Databricks, Glue).
- **Version Control**: Store Terraform code in Git, with separate branches for environments.
- **State Security**: Use remote backends with encryption and locking (e.g., S3 + DynamoDB).
- **Least Privilege**: Use IAM roles with minimal permissions for Terraform execution.
- **Tagging**: Enforce consistent tagging for cost allocation and resource tracking.
- **DRY Principle**: Use variables, modules, and `for_each` to avoid duplication.
- **Testing**: Use `terraform plan` to validate changes; consider tools like `terratest`.
- **CI/CD Integration**: Integrate with GitLab CI/CD for automated deployments.
- **Environment Isolation**: Use separate folders or state files for `dev`, `staging`, `prod` instead of workspaces for better clarity and flexibility.

- **RDS-Specific Best Practices**:

    - Use `multi_az` for production to ensure high availability.
    - Store `db_password` in AWS Secrets Manager and reference it via `data` sources.
    - Enable automated backups with appropriate retention periods.
    - Use parameter groups to tune database performance per environment.

- **Glue-Specific Best Practices**:

    - Store PySpark scripts in S3 and reference them in `script_location`.
    - Use environment-specific worker types and counts to optimize cost and performance.
    - Enable CloudWatch metrics and logs for job monitoring.
    - Use IAM roles with specific permissions for S3, CloudWatch, and other services.
  
## 12. Best Practices for CI/CD Pipelines with IaC

- **Separate Environments**: Use distinct jobs for each environment (`dev`, `staging`, `prod`) to prevent cross-contamination. This project uses separate folders (`environments/<env>`) instead of Terraform workspaces for clear isolation and environment-specific configurations.
- **Manual Approvals**: Require manual triggers for `apply` jobs, especially for production, to avoid unintended changes.
- **State Management**: Use remote backends with locking (e.g., S3 with DynamoDB) to prevent concurrent state modifications.
- **Secrets Management**: Store sensitive data (e.g., AWS credentials, DB passwords) in GitLab CI/CD variables or a secrets manager like AWS Secrets Manager.
- **Linting and Validation**: Run `terraform validate` and tools like `tflint` in the pipeline to catch errors early.
- **Plan Artifacts**: Store `terraform plan` outputs to (`tfplan`, `tfplan.json`, `tfplan.txt`) for review before applying, with JSON for automation and text for human-readable review.
- **Apply Log Retention**: Store `terraform apply` logs (`apply.log`) as GitLab artifacts (e.g., for 1 year) or upload to S3 (e.g., my-audit-logs) for long-term audit retention, with encryption and access controls to meet compliance requirements.
- **Output Management**: Capture `terraform output -json` as `outputs.json` artifacts for review, audit, or integration with other systems.
Avoid sensitive data in outputs and store in secure storage (e.g., S3) for long-term retention.

- **Data Source Management**:

    - Minimize data source queries to reduce API calls and improve pipeline performance.
    - Use precise filters (e.g., tags, IDs) to avoid ambiguous results.
    - Handle missing resources with `count` or `try` to prevent pipeline failures.
    - Validate data source resolution in the `plan` stage to catch errors early.
    - Document data source dependencies in `README.md` or comments in `.tf` files.

- **Secure Artifacts**: Restrict access to artifacts to authorized users to protect sensitive data in plan, apply, log, and output files.
- **Role-Based Access**: Use least-privilege IAM roles for CI/CD runners, scoped to specific environments.
- **Testing**: Integrate testing tools like `terratest` or `checkov` for unit, integration, and compliance testing of Terraform modules and plans.
- **Pipeline Triggers**: Run pipelines on merge requests and main branch pushes to catch issues early.
- **Version Pinning**: Pin Terraform and provider versions in the pipeline to avoid breaking changes.

- **Rollback Strategy**:

    - **State Backups**: Regularly back up `terraform.tfstate` to a separate S3 bucket after `apply` to enable recovery from failures or unintended changes. Use versioning on the backup bucket for additional protection.
    - **Terraform Destroy**: Document procedures for `terraform destroy` to remove all managed resources in an environment, including prerequisites (e.g., emptying S3 buckets) and post-cleanup steps (e.g., removing state files).
    - **Manual Rollback**: Maintain documentation for manual rollback of specific resources (e.g., reverting RDS instance types, deleting Glue jobs) when `destroy` is too destructive, including steps to restore from backups or previous state files.
    - **Implementation**: Automate state backups in the CI/CD pipeline post-`apply`. Include rollback instructions in `README.md` or a dedicated `ROLLBACK.md`.
  
- **Monitoring and Logging**: Enable verbose logging (`TF_LOG=DEBUG`) for debugging and monitor pipeline logs in GitLab.
- **Code Reviews**: Require peer reviews for merge requests to ensure quality and catch potential issues.
- **Documentation**: Include pipeline setup, artifact review, log retention, rollback procedures, output management, and data source usage instructions in `README.md`.

### Rollback Strategy Details

#### State Backups

- **Why**: The `terraform.tfstate` file tracks resource mappings, critical for recovery after failed `apply` or unintended changes.
- **How**:

    - Configure the pipeline to copy `terraform.tfstate` to a backup S3 bucket post-`apply` (see `backup_state_*` jobs).
    - Enable versioning on the backup bucket (`my-terraform-state-backup`) to retain historical states.
    - Example: `aws s3 cp s3://my-terraform-state/data-infra/dev/terraform.tfstate s3://my-terraform-state-backup/data-infra/dev/$(date +%Y-%m-%d_%H-%M-%S).tfstate`

- **Restore Process**:
     1. Identify the backup state file (e.g., via S3 console or `aws s3 ls`).
     2. Copy to the active state location: `aws s3 cp s3://my-terraform-state-backup/data-infra/dev/<timestamp>.tfstate s3://my-terraform-state/data-infra/dev/terraform.tfstate`.
     3. Run `terraform plan` to verify alignment with infrastructure.
     4. Apply changes if needed: `terraform apply`.

- **Best Practices**:

    - Encrypt backups with S3 server-side encryption.
    - Restrict access via IAM policies.
    - Schedule regular backup jobs or trigger post-`apply`.
    - Test restoration periodically to ensure reliability.

#### Terraform Destroy

- **Why**: `terraform destroy` removes all Terraform-managed resources in an environment, useful for complete rollback.
- **How**:
  
    - Run `terraform destroy` in the environment directory (e.g., `environments/dev`).
    - Example: `cd environments/dev; terraform init; terraform destroy -var-file=terraform.tfvars`.
  
- **Prerequisites**:

    - Empty S3 buckets (delete objects or disable versioning).
    - Remove dependent resources not managed by Terraform (e.g., manually created RDS snapshots).
    - Verify state file integrity before execution.

- **Post-Cleanup**:

    - Remove state file from S3: `aws s3 rm s3://my-terraform-state/data-infra/dev/terraform.tfstate`.
    - Update lock table (e.g., DynamoDB) if necessary.

- **Documentation**:

    - Create a `ROLLBACK.md` with steps:
      ```markdown
      # Terraform Destroy Rollback
      1. Navigate to the environment: `cd environments/<env>`.
      2. Initialize: `terraform init -backend-config=backend.tf`.
      3. Empty S3 buckets: `aws s3 rm s3://<bucket> --recursive`.
      4. Run destroy: `terraform destroy -var-file=terraform.tfvars`.
      5. Remove state: `aws s3 rm s3://my-terraform-state/data-infra/<env>/terraform.tfstate`.
      ```
- **Risks**:

    - Destructive; unsuitable for partial rollbacks.
    - Requires careful validation to avoid data loss.

#### Manual Rollback

- **Why**: For targeted rollbacks when `destroy` is too aggressive (e.g., reverting an RDS instance type change).
- **How**:
    - Modify Terraform code to revert changes (e.g., set `instance_class` back to original value).
    - Use a previous state backup to restore resource mappings.
    - Example (RDS rollback):
  
      1. Restore state: `aws s3 cp s3://my-terraform-state-backup/data-infra/dev/<timestamp>.tfstate s3://my-terraform-state/data-infra/dev/terraform.tfstate`.
      2. Update `main.tf` or variables (e.g., `instance_class = "db.t3.micro"`).
      3. Run `terraform plan` and `terraform apply`.
  
- **Specific Cases**:

    - **S3**: Delete objects or restore from versioning.
    - **RDS**: Revert instance type, restore from snapshot, or adjust parameters.
    - **Glue**: Delete jobs or revert configurations via Terraform.
      - **Snowflake**: Drop schemas/tables or restore from time travel.

- **Documentation**:

  - In `ROLLBACK.md`, detail resource-specific rollback steps:
    ```markdown
    ## Manual Rollback
    # RDS Example

    1. Restore state: `aws s3 cp s3://my-terraform-state-backup/...`.
    2. Update `instance_class` in `modules/rds/main.tf`.
    3. Run `terraform plan` and `terraform apply`.

    ## S3 Bucket

    1. Delete objects: `aws s3 rm s3://<bucket> --recursive`.
    2. Update Terraform to remove or bucket or adjust policies.
    ```
- **Best Practices**:

    - Test rollbacks in `dev` before applying to production.
    - Maintain backups (e.g., RDS snapshots) before applying changes.
    - Log all rollback actions for audit purposes.

## 13. Common Gotchas

- **State Drift**: Use `terraform refresh` to sync state with actual infrastructure.
- **Provider Versions**: Pin versions to avoid breaking changes.
- **Resource Dependencies**: Use `depends_on` or implicit dependencies (e.g., referencing outputs).
- **Sensitive Data**: Store secrets in AWS Secrets Manager or HashiCorp Vault, not `.tfvars`.
- **Rate Limits**: Handle cloud provider API limits with `terraform plan` retries or delays.

- **RDS-Specific Gotchas**:

    - Changing `allocated_storage` or `instance_class` may cause downtime.
    - Ensure `subnet_ids` are in the same VPC as `security_group_ids`.
    - Avoid `skip_final_snapshot` in production to prevent data loss.

- **Glue-Specific Gotchas**:

    - Ensure the Glue IAM role has permissions for S3 bucket script and temp directories.
    - Verify `glue_version` compatibility with PySpark script dependencies.
    - Monitor job execution time to avoid unexpected costs in production.

- **CI/CD-Specific Gotchas**:

    - Ensure CI/CD runners have correct permissions for each environment.
    - Avoid caching sensitive state files or logs in CI/CD pipelines.
    - Test pipeline changes in a non-production branch first.

  - **Output-Specific Gotchas**:

       - Avoid outputting sensitive data (e.g., database passwords) in `outputs.tf`.
       - Outputs are only updated after `terraform apply` or `terraform refresh` if state changes.
       - Missing outputs in `outputs.tf` can’t be retrieved without redefining them.

  - **Data Source-Specific Gotchas**:

       - Missing resources cause errors unless handled (e.g., with `count` or `try`).
       - Ambiguous data sources (e.g., no filters) may return multiple results, causing failures.
       - Excessive API queries from data sources can hit provider rate limits, slowing pipelines.
       - Ensure provider versions support required data source attributes.

## 14. Advanced Features

- **Dynamic Blocks**: Generate repetitive resource configurations.
  ```hcl
  resource "aws_s3_bucket" "bucket" {
    bucket = "${var.environment}-${var.bucket_name}"
    dynamic "lifecycle_rule" {
      for_each = var.lifecycle_rules
      content {
        id      = lifecycle_rule.value.id
        status  = "Enabled"
        expiration {
          days = lifecycle_rule.value.days
        }
      }
    }
  }
  ```

- **Count and For_Each**: Create multiple resources dynamically.
  ```hcl
  resource "aws_s3_bucket" "buckets" {
    for_each = var.bucket_names
    bucket   = "${each.key}-${var.environment}"
  }
  ```

- **Data Sources**:

    - **Definition**: Query existing resources or external data without managing them to retrieve attributes (e.g., VPC IDs, AMI IDs, database names).
    - **Syntax**:
      ```hcl
      data "<PROVIDER>_<TYPE>" "<NAME>" {
        [CONFIG]
      }
      ```
      Example: Fetch a VPC:
      ```hcl
      data "aws_vpc" "default" {
        default = true
      }
      ```
  
    - **Use Cases**:
  
         - Reference existing infrastructure (e.g., VPCs, IAM roles).
         - Fetch dynamic values (e.g., latest AMI ID, availability zones).
         - Integrate with other Terraform state files (e.g., `terraform_remote_state`).
         - Query external APIs or scripts (e.g., `external` provider).
  
    - **Examples**:
  
        - **AWS**: Fetch subnets for an RDS instance:
          ```hcl
          data "aws_vpc" "default" {
            default = true
          }
    
          data "aws_subnets" "default_subnets" {
            filter {
              name   = "vpc-id"
              values = [data.aws_vpc.default.id]
            }
          }
    
          resource "aws_db_instance" "rds" {
            db_subnet_group_name = aws_db_subnet_group.rds.name
            vpc_security_group_ids = [aws_security_group.rds.id]
            subnet_ids = data.aws_subnets.default_subnets.ids
          }
          ```
    
        - **Remote State**: Access another project’s outputs:
          ```hcl
          # Fetch outputs from another Terraform configuration
          data "terraform_remote_state" "network" {
            backend = "s3"
            config = {
              bucket = "my-terraform-state"
              key    = "networking/terraform.tfstate"
              region = "us-east-1"
            }
          }
          # Use the remote state output in a resource
          resource "aws_s3_bucket" "bucket" {
            bucket = "${var.environment}-data-lake"
            tags = {
              VPC = data.terraform_remote_state.network.outputs.vpc_id
            }
          }
          ```
        - **External Data**: Fetch data from a script:
          ```hcl
          data "external" "config" {
            program = ["bash", "${path.module}/get_config.sh"]
          }
    
          resource "aws_s3_bucket" "bucket" {
            bucket = "${var.environment}-${data.external.config.result.bucket_suffix}"
          }
          ```
  
    - **Best Practices**:
  
        - Minimize queries to reduce API calls and improve performance.
        - Use specific filters (e.g., `tags`, `id`) to avoid ambiguity.
        - Handle missing resources with `count` or `try`:
          ```hcl
          data "aws_vpc" "existing" {
            count = var.vpc_id != "" ? 1 : 0
            id    = var.vpc_id
          }
          ```
        - Avoid sensitive data in data source outputs.
        - Pin provider versions to ensure data source compatibility.
        - Document usage with comments in `.tf` files.
  
    - **Gotchas**:
  
        - Missing resources cause errors unless handled.
        - Ambiguous results (e.g., no filters) cause failures.
        - Rate limits may slow pipelines with many data sources.
        - Ensure state file access for `terraform_remote_state`.

    - **examples:**
  
         - **Snowflake**: `data.snowflake_role` to fetch an existing role.
         - **Databricks**: `data.databricks_spark_version` to get the latest Spark version.
         - **Glue Crawler**: `data.aws_glue_catalog_database` to reference an existing database.
         - **RDS**: `data.aws_vpc` and `data.aws_subnets` to fetch VPC and subnets.
         - **Glue Job**: `data.terraform_remote_state` to access the S3 bucket from another configuration.
    
## 15. Debugging

- **Verbose Logging**: `export TF_LOG=DEBUG`
- **State Inspection**: `terraform state show aws_s3_bucket.bucket`
- **Plan Analysis**: `terraform plan -out=tfplan; terraform show -json tfplan`
- **Output Inspection**: `terraform output -json` or `terraform output <output_name>`
- **Data Source Debugging**: Check `TF_LOG=DEBUG` for data source query details; use `terraform plan` to verify fetched values.
- **Error Handling**: Check provider-specific error codes in logs.

## 16. Tools & Extensions

- **Terraform CLI**: Core tool for managing infrastructure.
- **tfenv**: Manage multiple Terraform versions.
- **tflint**: Linter for Terraform code.
- **terraform-docs**: Generate documentation from `.tf` files.
- **VS Code Terraform Extension**: Syntax highlighting and autocompletion.


### Notes

- **Provider Requirements**: Ensure providers (e.g., `aws`, `snowflake`, `databricks`) are configured in `terraform.tf` or `main.tf` for data sources to work. The cheatsheet’s **Section 5** already includes AWS and Snowflake providers.
- **IAM Permissions**: Data sources require read permissions for the queried resources (e.g., `ec2:DescribeVpcs` for `data.aws_vpc`). Ensure the CI/CD runner’s IAM role includes these.
- **Pipeline Integration**: Data sources are resolved in the `plan` and `apply` jobs without changes to `.gitlab-ci.yml`. Monitor pipeline logs for data source errors.
- **Testing**: Run `terraform plan` locally in `environments/dev` to verify data sources fetch expected values. Check `tfplan.json` for details.
- Use `data` blocks to fetch existing resources (e.g., VPCs, Snowflake roles) or dynamic values (e.g., AMI IDs).
- Define in `main.tf` (e.g., `data.aws_vpc.default`) and reference in resources or modules.
- Document dependencies in `main.tf` comments.
- Validate in CI/CD `plan` jobs to catch errors.
- Minimize queries, use filters, handle missing resources, validate in `plan`, and document dependencies.


## Appendix

### A More Detailed Look at Data Sources

- **Definition**: Data sources in Terraform allow you to fetch information about **existing resources** or **external data** that are not managed by your current Terraform configuration. They provide a way to query cloud providers, APIs, or other systems to retrieve attributes like IDs, ARNs, or configurations without creating or modifying resources.

- **Purpose**:

    - Reference resources created outside Terraform (e.g., an existing VPC or IAM role).
    - Access computed values (e.g., the latest AMI ID, availability zones).
    - Integrate with other Terraform configurations via remote state.
    - Avoid hardcoding values by dynamically retrieving them.

- **How They Work**:

     - Data sources are defined using the `data` block in Terraform configuration files (e.g., `main.tf`).
     - They query the provider’s API (e.g., AWS, Snowflake, Databricks) during `terraform plan` or `terraform apply` to fetch data.
     - The retrieved data is stored in the Terraform **state file** for the duration of the operation but does not manage the underlying resource.
     - Data source attributes can be referenced in other resources, outputs, or modules, just like managed resources.

#### Syntax and Structure

A data source block follows this format:
```hcl
data "<PROVIDER>_<TYPE>" "<NAME>" {
  [CONFIGURATION]
}
```

- **PROVIDER**: The provider (e.g., `aws`, `snowflake`, `databricks`).
- **TYPE**: The resource type to query (e.g., `aws_vpc`, `snowflake_database`).
- **NAME**: A local name for referencing the data source in your configuration.
- **CONFIGURATION**: Filters or parameters to identify the resource (e.g., `id`, `name`, `tags`).

Example:
```hcl
data "aws_vpc" "default" {
  default = true
}
```

- This queries AWS for the default VPC and makes its attributes (e.g., `id`, `cidr_block`) available as `data.aws_vpc.default.<attribute>`.

#### Key Characteristics

- **Read-Only**: Data sources only fetch data; they cannot create, update, or delete resources.
- **Provider Dependency**: Each data source is tied to a specific provider, which must be configured in your Terraform setup (e.g., `provider "aws"`).
- **State Integration**: Data source results are cached in the state file during execution but do not persist as managed resources.
- **Dynamic Values**: Data sources are ideal for retrieving values that change over time (e.g., latest AMI IDs, external resource IDs).
- **Lifecycle**: Data sources are refreshed during `terraform plan` or `terraform apply` unless explicitly skipped (e.g., using `-refresh=false`).

#### Common Use Cases

1. **Referencing Existing Infrastructure**:
   - Fetch details of resources created manually or by other Terraform configurations (e.g., VPCs, subnets, IAM roles).
   - Example: Use an existing security group for an RDS instance.
2. **Dynamic Resource Configuration**:
   - Retrieve dynamic values like the latest AMI ID or availability zones to configure resources.
   - Example: Select the latest Ubuntu AMI for an EC2 instance.
3. **Cross-Module Integration**:
   - Access outputs from another Terraform configuration using the `terraform_remote_state` data source.
   - Example: Reference an S3 bucket ARN from a different project’s state.
4. **Environment-Specific Configurations**:
   - Query environment-specific resources (e.g., a Snowflake database in `prod`).
   - Example: Fetch a Snowflake database name for a schema.
5. **External Data**:
   - Use the `http` or `external` provider to fetch data from APIs or scripts.
   - Example: Retrieve a configuration value from an external API.

#### Example: Fetching an Existing VPC

```hcl
# Fetch the default VPC
data "aws_vpc" "default" {
  default = true
}

# Fetch subnets in the VPC
data "aws_subnets" "default_subnets" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Use the subnet IDs in an RDS instance
module "rds_postgres" {
  source         = "../../modules/rds"
  db_name        = "datawarehouse"
  environment    = var.environment
  subnet_ids     = data.aws_subnets.default_subnets.ids
  security_group_ids = [aws_security_group.rds_sg.id]
}
```

- Here, `data.aws_vpc.default` retrieves the default VPC’s ID, and `data.aws_subnets.default_subnets` fetches its subnets, which are then used in the RDS module.

#### Example: Remote State Data Source

```hcl
# Fetch outputs from another Terraform configuration
data "terraform_remote_state" "network" {
  backend = "s3"
  config = {
    bucket = "my-terraform-state"
    key    = "networking/terraform.tfstate"
    region = "us-east-1"
  }
}

# Use the remote state output in a resource
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.environment}-data-lake"
  tags = {
    VPC = data.terraform_remote_state.network.outputs.vpc_id
  }
}
```
- This retrieves the `vpc_id` output from a separate Terraform configuration’s state file.

#### Example: External Data Source

```hcl
# Use the external provider to run a script
data "external" "config" {
  program = ["bash", "${path.module}/get_config.sh"]
}

# Use the result in a resource
resource "aws_s3_bucket" "bucket" {
  bucket = "${var.environment}-${data.external.config.result.bucket_suffix}"
}
```

- The `get_config.sh` script returns JSON (e.g., `{"bucket_suffix": "data-lake"}`), which is used to name the bucket.

#### Integration with CI/CD  Setup

- **Folder-Based Structure**: The project uses separate directories (`environments/dev`, `environments/staging`, `environments/prod`) for environment isolation. Data sources can be defined in each environment’s `main.tf` to fetch environment-specific resources (e.g., a `prod` VPC).
- **CI/CD Pipeline**: Data sources are queried during `terraform plan` and `terraform apply` jobs in the GitLab pipeline, ensuring dynamic values are resolved automatically.
- **Modules**: Data sources can be used in modules (e.g., `modules/rds`) to reference existing infrastructure, as shown in the RDS example above.
- **State Management**: Data source results are stored in the environment-specific state file (e.g., `data-infra/dev/terraform.tfstate`) during execution.

#### Best Practices

1. **Minimize Queries**: Avoid excessive data source queries to reduce API calls and improve performance.
2. **Use Filters**: Specify precise filters (e.g., `tags`, `id`) to avoid ambiguous results.
3. **Handle Missing Resources**:
   - Use `count` or `try` to handle cases where a data source might not return results.
   - Example:
     ```hcl
     data "aws_vpc" "existing" {
       count = var.vpc_id != "" ? 1 : 0
       id    = var.vpc_id
     }
     ```
4. **Avoid Sensitive Data**: Don’t expose sensitive attributes (e.g., secrets) in data source outputs.
5. **Pin Provider Versions**: Ensure the provider version supports the data source type and attributes.
6. **Document Usage**: Include comments in `main.tf` explaining why a data source is used.
7. **Test in CI/CD**: Verify data sources resolve correctly in the pipeline’s `plan` stage.

#### Common Gotchas

- **Missing Resources**: If a data source can’t find a resource, Terraform will error unless handled (e.g., with `count` or `try`).
- **Stale Data**: Data sources rely on provider APIs; ensure the provider is up-to-date to avoid stale results.
- **Rate Limits**: Excessive data source queries may hit provider API limits, causing failures in `plan` or `apply`.
- **State Dependency**: Data sources are resolved during execution, so ensure the state file is accessible (e.g., in remote backends).
- **Ambiguous Results**: Without proper filters, data sources may return multiple results, causing errors.



### A deeper look into Environment Isolation Approaches

#### Folder-Based Isolation

Folder-based isolation involves organizing Terraform configurations into separate directories for each environment (e.g., `environments/dev/`, `environments/staging/`, `environments/prod/`). Each directory contains its own `main.tf`, `variables.tf`, `outputs.tf`, `backend.tf`, and `terraform.tfvars`, with distinct state files and configurations tailored to the environment.

#### Terraform Workspaces

Terraform workspaces allow multiple environments to share the same configuration files within a single directory, using different state files for each workspace (e.g., `default`, `dev`, `staging`, `prod`). Workspaces are managed with commands like `terraform workspace new <env>` and `terraform workspace select <env>`, and variables are typically controlled via CLI flags or conditional logic.

#### Advantages of Folder-Based Isolation

The folder-based isolation approach, as demonstrated in the cheatsheet's `environments/` structure, offers several advantages over workspaces, particularly for data infrastructure projects involving complex resources like S3 buckets, RDS databases, Snowflake, Databricks, and Glue jobs.

##### 1. **Clear Separation of Configurations**

- **Advantage**: Each environment has its own dedicated directory with independent configuration files, making it easier to customize resources, variables, and outputs without relying on conditional logic.
- **Example**: In the cheatsheet, `environments/dev/main.tf` might define a smaller RDS instance (`db.t3.micro`) compared to `environments/prod/main.tf` (`db.m5.large`). This is explicit and avoids complex `if` statements or workspace-specific variables.
- **Workspace Challenge**: With workspaces, all environments share the same `main.tf`, requiring conditional logic (e.g., `count = terraform.workspace == "prod" ? 1 : 0`) or variable overrides, which can lead to errors or reduced readability.
- **Impact**: Folder-based isolation improves maintainability and reduces the risk of misconfiguration, especially for data engineers managing diverse infrastructure across environments.

##### 2. **Independent State Files and Backends**

- **Advantage**: Each environment has its own state file and backend configuration, stored in separate paths (e.g., `s3://my-terraform-state/data-infra/dev/terraform.tfstate` vs. `s3://my-terraform-state/data-infra/prod/terraform.tfstate`), ensuring complete isolation.
- **Example**: The cheatsheet's `environments/dev/backend.tf` specifies:
  ```hcl
  terraform {
    backend "s3" {
      bucket         = "my-terraform-state"
      key            = "data-infra/dev/terraform.tfstate"
      region         = "us-east-1"
      dynamodb_table = "terraform-locks"
    }
  }
  ```
  This isolates `dev` state from `prod`, preventing accidental cross-environment changes.
- **Workspace Challenge**: Workspaces store state files in the same backend with a workspace prefix (e.g., `env:/dev/terraform.tfstate`), which can lead to accidental state overwrites if the wrong workspace is selected. Additionally, all workspaces share the same backend configuration, limiting flexibility.
- **Impact**: Folder-based isolation enhances security and auditability by ensuring state files are distinctly managed, critical for compliance in data infrastructure projects.

##### 3. **Simplified CI/CD Pipelines**

- **Advantage**: Folder-based isolation aligns naturally with CI/CD pipelines, as each environment's directory can be targeted independently, reducing complexity in pipeline scripts.
- **Example**: The cheatsheet's `.gitlab-ci.yml` defines separate jobs (`plan_dev`, `apply_dev`, `plan_staging`, etc.) that operate on specific directories (e.g., `cd environments/dev`). This avoids the need to switch workspaces in the pipeline, simplifying configuration and reducing errors.
  ```yaml
  plan_dev:
    stage: plan
    script:
      - cd environments/dev
      - terraform init -backend-config=backend.tf
      - terraform plan -var-file=terraform.tfvars -out=tfplan
  ```
- **Workspace Challenge**: With workspaces, pipelines must run `terraform workspace select <env>` before each job, increasing the risk of selecting the wrong workspace or encountering state conflicts. This adds complexity to pipeline scripts and requires careful error handling.
- **Impact**: Folder-based isolation streamlines GitLab CI/CD pipelines, improving reliability and auditability for automated deployments of data infrastructure.

##### 4. **Enhanced Team Collaboration**

- **Advantage**: Separate directories make it easier for teams to work on different environments simultaneously without conflicts, as each environment's configuration and state are isolated.
- **Example**: In the cheatsheet, a developer can modify `environments/dev/main.tf` to test a new Glue job while another team member updates `environments/prod/main.tf` to adjust RDS settings, without risking state or configuration clashes.
- **Workspace Challenge**: Workspaces share a single directory, so concurrent changes to `main.tf` or state files can lead to conflicts, especially in large teams. Developers must carefully coordinate workspace selection to avoid overwriting each other's changes.
- **Impact**: Folder-based isolation supports parallel development, critical for data engineering teams managing complex, multi-environment setups.

##### 5. **Better Auditability and Traceability**
- **Advantage**: Folder-based isolation provides clear, environment-specific configuration files and state files, making it easier to audit changes and track infrastructure history.
- **Example**: The cheatsheet's structure allows auditors to review `environments/prod/terraform.tfvars` and `apply.log` (stored as artifacts) to verify production settings and changes. State backups in `s3://my-terraform-state/backups/prod/` provide a clear history for rollback or compliance.
- **Workspace Challenge**: Workspaces mix configurations in a single `main.tf`, requiring auditors to parse conditional logic or variable overrides to understand environment-specific settings. State files are less distinctly separated, complicating audit trails.
- **Impact**: Folder-based isolation simplifies compliance with regulatory requirements (e.g., GDPR, HIPAA) by providing transparent, environment-specific records.

##### 6. **Flexibility for Environment-Specific Customization**

- **Advantage**: Each environment can have unique configurations, providers, or even Terraform versions without affecting others, offering maximum flexibility.
- **Example**: In the cheatsheet, `environments/staging/` might use a different AWS region or provider version than `environments/prod/`, defined in their respective `main.tf` and `backend.tf`. This is straightforward with separate directories.
- **Workspace Challenge**: Workspaces share the same provider configuration and Terraform version, limiting customization unless complex workarounds (e.g., provider aliases) are used.
- **Impact**: Folder-based isolation supports diverse data infrastructure requirements, such as regional differences or provider-specific settings for Snowflake or Databricks.

##### 7. **Reduced Risk of Human Error**

- **Advantage**: Operating within a specific directory (e.g., `environments/dev/`) eliminates the need to select a workspace, reducing the chance of applying changes to the wrong environment.
- **Example**: Running `terraform apply` in `environments/dev/` affects only the `dev` environment, with no risk of accidentally targeting `prod`. The cheatsheet's pipeline reinforces this by scoping jobs to directories.
- **Workspace Challenge**: Forgetting to run `terraform workspace select prod` before `terraform apply` can result in catastrophic changes to the wrong environment, a common error in high-pressure scenarios.
- **Impact**: Folder-based isolation enhances safety, particularly for production data infrastructure where errors can lead to data loss or downtime.

##### When to Use Workspaces

While folder-based isolation is generally preferred, workspaces may be suitable for:

- **Simple Projects**: Small projects with minimal configuration differences between environments (e.g., a single S3 bucket with different names).
- **Temporary Environments**: Spinning up ephemeral environments (e.g., feature branches) where maintaining separate directories is overkill.
- **Legacy Projects**: Existing setups already using workspaces, where migration to folders is not cost-effective.

However, for data infrastructure projects with complex resources, multiple team members, and strict compliance requirements, folder-based isolation (as in the cheatsheet) is superior.

##### Recommendations

- **Adopt Folder-Based Isolation**: Use the cheatsheet's `environments/` structure to organize `dev`, `staging`, and `prod` configurations in separate directories.
- **Document in `README.md`**: Include setup instructions for navigating environment directories and running Terraform commands, as shown in the cheatsheet:
  ```markdown
  ## Running Terraform
  - Navigate to the environment directory: `cd environments/dev`
  - Initialize: `terraform init`
  - Apply: `terraform apply -var-file=terraform.tfvars`
  ```
- **Leverage CI/CD**: Configure pipelines (e.g., `.gitlab-ci.yml`) to target specific directories, as in the cheatsheet, to enforce environment isolation.
- **Secure State Files**: Use distinct backend paths and versioning (e.g., `s3://my-terraform-state/data-infra/<env>/terraform.tfstate`) to protect state files, as shown in the cheatsheet's `backend.tf`.

