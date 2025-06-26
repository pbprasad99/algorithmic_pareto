# Terraform Scenarios

!!! note "AI Assisted (Grok 3)"

Common Scenarios and how to handle them.

## Project Structure Reference

```
data-infra/
├── modules/                     # Reusable Terraform modules (e.g., s3_bucket, rds, glue_job)
├── environments/                # Environment-specific configurations
│   ├── dev/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── backend.tf
│   │   └── terraform.tfvars
│   ├── staging/
│   └── prod/
├── scripts/
├── .gitignore
├── README.md
└── .gitlab-ci.yml               # CI/CD pipeline with validate, plan, and apply stages
```

## 1. What happens if your state file is accidentally deleted?

**Answer**: If the Terraform state file (`terraform.tfstate`) is deleted, Terraform loses track of managed infrastructure. The next `terraform apply` assumes resources don’t exist and attempts to recreate them, potentially causing duplicates or failures. Recovery involves restoring a backup or manually importing resources with `terraform import`. Always enable versioning on remote state storage (e.g., S3).

**Example**:

- **Project Context**: The project uses an S3 backend for state storage (`s3://my-terraform-state/data-infra/dev/terraform.tfstate`) with versioning enabled.
- **Scenario**: The `dev` state file is deleted.
- **Recovery**:

  ```bash
  # Restore from S3 versioned backup
  aws s3api get-object --bucket my-terraform-state --key data-infra/dev/terraform.tfstate --version-id <version-id> terraform.tfstate
  cd environments/dev
  terraform init
  terraform apply
  ```
  Alternatively, import an existing S3 bucket:
  ```bash
  terraform import module.data_lake.aws_s3_bucket.bucket dev-data-lake
  ```
- **Best Practice**: Enable S3 bucket versioning and backup state files before `apply` in the pipeline (see `apply_dev` job in `.gitlab-ci.yml`)

## 2. How do you handle large-scale refactoring without downtime?

**Answer**: For most resources, use `terraform state mv` to rename them in the state file without destruction. For S3 buckets, which have immutable names in AWS, create a new bucket, copy data, and update the state. Split refactoring into smaller, non-destructive pull requests (PRs), use targeted applies (`terraform apply -target`), and verify plans to prevent resource destruction. Test in `dev` before `staging` or `prod`.

**Example**:

- **Project Context**: Refactor the `s3_bucket` module to rename the bucket from `dev-data-lake` to `dev-data-lake-v2` in `environments/dev/main.tf`. Since S3 bucket names are immutable, a new bucket is created, and data is copied.
- **Step-by-Step Process**:

  1. **Add New Bucket Module**:
     - Update `environments/dev/main.tf` to define a temporary module (`data_lake_v2`) alongside `data_lake`.
       ```hcl
       # environments/dev/main.tf
       module "data_lake" {
         source      = "../../modules/s3_bucket"
         bucket_name = "data-lake"  # Original: dev-data-lake
         environment = var.environment
       }

       module "data_lake_v2" {
         source      = "../../modules/s3_bucket"
         bucket_name = "data-lake-v2"  # New: dev-data-lake-v2
         environment = var.environment
       }
       ```
     - Run:
       ```bash
       cd environments/dev
       terraform init
       terraform apply -var-file=terraform.tfvars
       ```
     - **Outcome**: Creates `dev-data-lake-v2`. `dev-data-lake` remains active, ensuring no downtime.

  2. **Copy Data**:
     - Sync data from `dev-data-lake` to `dev-data-lake-v2`.
       ```bash
       aws s3 sync s3://dev-data-lake s3://dev-data-lake-v2
       ```
     - **Outcome**: `dev-data-lake-v2` contains all data. Services using `dev-data-lake` are unaffected.

  3. **Update State**:
     - Move the state entry for `dev-data-lake-v2` to replace `dev-data-lake`.
       ```bash
       terraform state mv module.data_lake.aws_s3_bucket.bucket module.data_lake_v2.aws_s3_bucket.bucket
       ```
     - **Outcome**: State now maps `module.data_lake_v2.aws_s3_bucket.bucket` to `dev-data-lake-v2`.

  4. **Remove Old Bucket from State**:
     - Remove `dev-data-lake` from state.
       ```bash
       terraform state rm module.data_lake.aws_s3_bucket.bucket
       ```
     - **Outcome**: Terraform no longer manages `dev-data-lake`, which remains in AWS.

  5. **Update Configuration**:
     - Revise `main.tf` to use only the new bucket.
       ```hcl
       # environments/dev/main.tf
       module "data_lake" {
         source      = "../../modules/s3_bucket"
         bucket_name = "data-lake-v2"
         environment = var.environment
       }
       ```
     - Run:
       ```bash
       terraform plan -var-file=terraform.tfvars  # Verify no destroy
       terraform apply -var-file=terraform.tfvars
       ```
     - **Outcome**: Terraform manages `dev-data-lake-v2` under `module.data_lake`.

  6. **Update Dependencies**:
     - Modify dependent resources (e.g., Glue jobs) to reference `dev-data-lake-v2`.
       ```hcl
       # modules/glue_job/main.tf
       data "aws_s3_bucket" "bucket" {
         bucket = "${var.environment}-data-lake-v2"
       }
       ```
     - Apply changes in a separate PR.
     - **Outcome**: Services transition to `dev-data-lake-v2` without disruption.

  7. **Delete Old Bucket (Optional)**:
     - If safe, delete `dev-data-lake`.
       ```bash
       aws s3 rb s3://dev-data-lake --force
       ```
     - Ensure `force_destroy = false` in `modules/s3_bucket/main.tf` to prevent accidental deletion:
       ```hcl
       resource "aws_s3_bucket" "bucket" {
         bucket        = "${var.environment}-${var.bucket_name}"
         force_destroy = false
       }
       ```
     - **Outcome**: Old bucket is removed after confirmation.

- **Best Practice**: Test in `dev` using the `plan_dev` job, automate data sync in `apply_dev`, document in PRs, and ensure `force_destroy = false`. Update `README.md`:

  ```markdown
  ## S3 Bucket Renaming
  - Add new module in `main.tf`.
  - Sync data: `aws s3 sync s3://dev-data-lake s3://dev-data-lake-v2`.
  - Update state: `terraform state mv`.
  - Remove old module and state entry.
  - Delete old bucket if safe.
  ```

## 3. What happens if a resource fails halfway through a terraform apply?

**Answer**: If a resource fails during `terraform apply`, Terraform creates a partial deployment. Successful resources are applied, but failed ones are marked as tainted in the state file. Use targeted applies (`terraform apply -target`) or `-refresh-only` to recover systematically, addressing failures one by one.

**Example**:

- **Project Context**: The `apply_dev` job fails when creating an RDS instance due to an invalid parameter.
- **Scenario**: The `module.rds_postgres.aws_db_instance.rds_instance` fails, but the `module.data_lake.aws_s3_bucket.bucket` is created.
- **Recovery**:

  ```bash
  cd environments/dev
  terraform init
  terraform plan -var-file=terraform.tfvars  # Check tainted resources
  terraform apply -target=module.rds_postgres.aws_db_instance.rds_instance  # Retry specific resource
  ```
  Review `apply.log` artifact from the `apply_dev` job in GitLab to diagnose the error.

- **Best Practice**: Use the pipeline’s `apply.log` (stored in S3: `s3://my-audit-logs/terraform-apply/dev/`) for debugging and target specific resources to minimize disruption.

## 4. How do you manage secrets in Terraform?

**Answer**: Store secrets in external systems like AWS Secrets Manager or HashiCorp Vault, use encrypted remote state, mark outputs as sensitive, and integrate with CI/CD securely. Avoid hardcoding secrets in `.tfvars` or code, and consider managing highly sensitive values outside Terraform.

**Example**:

- **Project Context**: The RDS module in `environments/dev/main.tf` requires a `db_password`.
- **Implementation**:

  ```hcl
  # environments/dev/main.tf
  data "aws_secretsmanager_secret_version" "db_password" {
    secret_id = "dev/rds/password"
  }

  module "rds_postgres" {
    source             = "../../modules/rds"
    db_name            = "datawarehouse"
    environment        = var.environment
    db_username        = var.db_username
    db_password        = data.aws_secretsmanager_secret_version.db_password.secret_string
    subnet_ids         = data.aws_subnet_ids.default.ids
    security_group_ids = [aws_security_group.rds_sg.id]
  }

  # outputs.tf
  output "rds_endpoint" {
    value     = module.rds_postgres.aws_db_instance.rds_instance.endpoint
    sensitive = true
  }
  ```
  Store `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` in GitLab CI/CD variables for pipeline authentication.

- **Best Practice**: Use the `backend.tf` S3 backend with encryption and restrict access via IAM policies. Avoid storing secrets in `terraform.tfvars`.

## 5. What happens if terraform plan shows no changes but infrastructure was modified outside Terraform?

**Answer**: Terraform is unaware of external changes (state drift) until `terraform refresh` updates the state file. Implement regular drift detection in CI/CD pipelines to catch unauthorized modifications and reconcile them with `terraform apply` or `terraform import`.

**Example**:

- **Project Context**: An S3 bucket (`dev-data-lake`) is manually modified in the AWS Console to change its ACL.
- **Detection**:

  ```yaml
  # .gitlab-ci.yml
  drift_detection:
    stage: validate
    extends: .terraform_base
    script:
      - cd environments/dev
      - terraform init -backend-config=backend.tf
      - terraform refresh -var-file=terraform.tfvars
      - terraform plan -var-file=terraform.tfvars -out=tfplan
    artifacts:
      paths:
        - environments/dev/tfplan.txt
      expire_in: 1 week
  ```
  ```bash
  cd environments/dev
  terraform init
  terraform refresh -var-file=terraform.tfvars
  terraform plan -var-file=terraform.tfvars  # Shows drift
  terraform apply -var-file=terraform.tfvars  # Reconcile changes
  ```

- **Best Practice**: Schedule a `drift_detection` job weekly in `.gitlab-ci.yml` and review `tfplan.txt` artifacts to identify drift.

## 6. What happens if you delete a resource definition from your configuration?

**Answer**: Removing a resource from Terraform configuration causes `terraform apply` to destroy the corresponding infrastructure. Use `terraform state rm` to remove the resource from state without destroying it, or add `lifecycle { prevent_destroy = true }` for critical resources.

**Example**:

- **Project Context**: The `module.data_lake.aws_s3_bucket.bucket` is removed from `environments/prod/main.tf`.
- **Prevention**:

  ```hcl
  # modules/s3_bucket/main.tf
  resource "aws_s3_bucket" "bucket" {
    bucket = "${var.environment}-${var.bucket_name}"
    lifecycle {
      prevent_destroy = true
    }
  }
  ```
  If removed accidentally:
  ```bash
  cd environments/prod
  terraform state rm module.data_lake.aws_s3_bucket.bucket
  terraform plan -var-file=terraform.tfvars  # Verify no destroy
  ```

- **Best Practice**: Apply `prevent_destroy` to critical resources like production S3 buckets or RDS instances in the `modules/` directory.

## 7. What happens if Terraform provider APIs change between versions?

**Answer**: Provider API changes can break compatibility, causing errors in resource creation or updates. Read release notes, pin provider versions, test upgrades in `dev`, and use targeted applies for gradual migration.

**Example**:

- **Project Context**: Upgrading the AWS provider from `~> 4.0` to `~> 5.0` in `environments/dev/main.tf`.
- **Implementation**:

  ```hcl
  # environments/dev/main.tf
  terraform {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "~> 5.0"  # Upgraded from 4.0
      }
    }
  }
  ```
  ```bash
  cd environments/dev
  terraform init -upgrade
  terraform plan -var-file=terraform.tfvars  # Check for breaking changes
  terraform apply -var-file=terraform.tfvars
  ```

- **Best Practice**: Test upgrades in the `plan_dev` job, review release notes (e.g., AWS provider changelog), and update one environment at a time.

## 8. How do you implement zero-downtime infrastructure updates?

**Answer**: Use `create_before_destroy` lifecycle blocks, blue-green deployments, health checks, and state manipulation. For databases, leverage replicas or managed services with failover capabilities to avoid downtime.

**Example**:

- **Project Context**: Update the RDS instance class in `environments/prod/main.tf` without downtime.
- **Implementation**:

  ```hcl
  # modules/rds/main.tf
  resource "aws_db_instance" "rds_instance" {
    identifier           = "${var.environment}-${var.db_name}"
    instance_class       = var.prod_instance_class
    allocated_storage    = var.allocated_storage
    multi_az             = true  # Enable for failover
    apply_immediately    = false # Apply during maintenance window
    lifecycle {
      create_before_destroy = true
    }
  }
  ```
  ```bash
  cd environments/prod
  terraform init
  terraform plan -var-file=terraform.tfvars -out=tfplan
  terraform apply tfplan
  ```

- **Best Practice**: Enable `multi_az` for production RDS (as in the cheatsheet), use `apply_immediately = false`, and test in `staging` via the `apply_staging` job.

## 9. What happens if you have circular dependencies in your Terraform modules?

**Answer**: Circular dependencies cause Terraform to fail with "dependency cycle" errors. Refactor modules using data sources, outputs, or restructured resources to establish a clear dependency hierarchy.

**Example**:

- **Project Context**: The `s3_bucket` module depends on a `glue_job` module, which references the S3 bucket’s ARN.
- **Resolution**:

  ```hcl
  # modules/s3_bucket/main.tf
  resource "aws_s3_bucket" "bucket" {
    bucket = "${var.environment}-${var.bucket_name}"
  }

  output "bucket_arn" {
    value = aws_s3_bucket.bucket.arn
  }

  # modules/glue_job/main.tf
  data "aws_s3_bucket" "bucket" {
    bucket = "${var.environment}-${var.bucket_name}"
  }

  resource "aws_glue_job" "pyspark_job" {
    name     = "${var.environment}-${var.job_name}"
    role_arn = var.glue_role_arn
    command {
      script_location = "s3://${data.aws_s3_bucket.bucket.bucket}/${var.script_path}"
    }
  }
  ```

- **Best Practice**: Use data sources to fetch existing resources, avoiding direct dependencies. Validate with the `validate` job in `.gitlab-ci.yml`.

## 10. What happens if you rename a resource in your Terraform code?

**Answer**: Renaming a resource in Terraform code is interpreted as destroying and recreating the resource. Use `terraform state mv` to update the state file, preserving the existing infrastructure and avoiding rebuilds or downtime. For S3 buckets, create a new bucket and copy data, as bucket names are immutable.

**Example**:

- **Project Context**: Rename `module.data_lake.aws_s3_bucket.bucket` to `module.data_lake.aws_s3_bucket.data_lake` in `environments/dev/main.tf`.
- **Steps**:

  ```hcl
  # Original: environments/dev/main.tf
  module "data_lake" {
    source      = "../../modules/s3_bucket"
    bucket_name = "data-lake"
    environment = var.environment
  }
  ```
  ```hcl
  # Updated: modules/s3_bucket/main.tf
  resource "aws_s3_bucket" "data_lake" {  # Renamed from bucket
    bucket = "${var.environment}-${var.bucket_name}"
  }
  ```
  ```bash
  cd environments/dev
  terraform init
  terraform state mv module.data_lake.aws_s3_bucket.bucket module.data_lake.aws_s3_bucket.data_lake
  terraform plan -var-file=terraform.tfvars  # Verify no destroy
  terraform apply -var-file=terraform.tfvars
  ```

- **Best Practice**: Run `terraform state mv` in the `plan_dev` job to preview changes, and document renaming in PRs for team review.

## Additional Notes

- **Pipeline Integration**: Use the `.gitlab-ci.yml` from the main cheatsheet to automate validation, planning, and applying changes, ensuring safe handling of state, secrets, and drift detection.
- **Documentation**: Update `README.md` to include recovery steps for each scenario (e.g., state restoration, drift detection setup).

  ```markdown
  ## Handling Terraform Scenarios
  - State Deletion: Restore from `s3://my-terraform-state/backups/<env>/<timestamp>.tfstate`.
  - S3 Bucket Renaming: See Scenario 2 for detailed steps.
  - Drift Detection: Run the `drift_detection` job in GitLab CI/CD.
  - Zero-Downtime Updates: Enable `create_before_destroy` and `multi_az` for RDS in `modules/rds/main.tf`.
  ```

- **Testing**: Test all changes in `dev` or `staging` environments using the `plan_dev` and `apply_dev` jobs before applying to `prod`.