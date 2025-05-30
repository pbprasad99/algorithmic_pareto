---
title: Anatomy of an AWS Policy
slug: Anatomy of an AWS Policy
date: 2025-05-17

tags :
  - AWS
  - IAM
categories:
  - AWS
  - IAM
---

# Anatomy of an AWS Policy

AWS Policies are json documents which declare the access permissions for certain services or resources at a granular level. They can be attached to roles, users or resources. Let us understand how this works by looking at an example policy. 

<!-- more -->

## The philosophy of AWS Security

AWS IAM operates on the principle of the shared responsibility model. This means AWS provides the MEANS of implementing security but YOU are responsible for using them effectively. This means having to manage lots of policies.

Another important principle is the principle of LEAST PRIVILEGE. In case of a hypthetical security breach, the BLAST RADIUS should be as small as possible.


Blast Radius for the following policy is a single Lambda Function being invoked: 

```json
{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "VisualEditor1",
              "Effect": "Allow",
              "Action": "lambda:InvokeFunction",
              "Resource": [
                "arn:aws:lambda:<your_account_id>:<us-east-1>:function:MyFunction"
              ]
            }
          ]
}
```

Now , if you want to use a generic role to invoke ANY lambda function in the acccount, you would use a wild card in the Resource : "arn:aws:lambda:<your_account_id>:<us-east-1>:function:*" .

Now the blast radius is invocation of any function.

And if you want to have a generic role which can pretty much do anything with lambda functions like create, modify, delete and invoke lambdas, you would use a wildcard to define the Action as "lambda:*". So, the blast radius just increased to include anything which can be done to or with lambda functions. Somebody could just list and delete all your lambda functions.

## When does IAM apply?

Whenever you request anything through an AWS API its going to go through IAM. But but, there is a case when it does not apply : When you have an HTTP server running on an AWS EC3 instance and http requests are directly made to the elastic ip address, there is no AWS service in between, so no IAM policy evaluation is done in this case.


```json
{
          "Version": "2012-10-17",
          "Statement": [
            {
              "Sid": "VisualEditor1",
              "Effect": "Allow",
              "Action": "lambda:InvokeFunction",
              "Resource": [
                "arn:aws:lambda:<your_account_id>:<us-east-1>:function:MyFunction"
              ]
            }
          ]
}

```


## TRUST POlICY

A trust policy is an IAM policy attached to a Role which specifies who (which Principal) can assume it. This is typically used to allow services to assume the role. A typical example is API Gateway assuming a role which Has permissions to invoke a Lambda function.

https://aws.amazon.com/blogs/security/how-to-use-trust-policies-with-iam-roles/


## Invocation Role vs Execution Role

A question may arise: Does the invoking role/user need all the permisions of the execution role?
Say, a user does not have direct permission to delete an item from an s3 bucket, but he does have access to invoke a lambda function which can perform this action through its execution role. Can the user invoke the lambda and delete files? The answer is yes. Once the Lambda is invoked it autmoatically assumes the execution roles and performs whatever actions it does with the execution role. 


"The policies that are attached to the credentials that made the original call to AssumeRole are not evaluated by AWS when making the "allow" or "deny" authorization decision. The user temporarily gives up its original permissions in favor of the permissions assigned by the assumed role. In the case of the AssumeRoleWithSAML and AssumeRoleWithWebIdentity API operations, there are no policies to evaluate because the caller of the API is not an AWS identity." [Ref 5]

## Resource Policies


## A special Note on S3 Policies

When it comes to S3 buckets there two types of ARNs
1. ARN to match the bucket : arn:aws:s3:::my-bucket
2. ARN to match objects: arn:aws:s3:::my-bucket/* , arn:aws:s3:::my-bucket/somepath/* ,arn:aws:s3:::my-bucket/somepath/*, arn:aws:s3:::my-bucket/somepath/somekey.txt

There are also two types of actions : Bucket level and Object level. 

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": [
                "arn:aws:s3:::mybucket",
                "arn:aws:s3:::mybucket/resports/diabetes/*"
            ]
        }
    ]
}
```

In the policy above, s3:ListBucket applies to the Bucket ARN and s3:GetObject applies to the arn matching objects with this pattern mybucket/resports/diabetes/*.
A clearer way to write the same policy is using two separate statemnets, one for bucket level actions and another for Object level actions :


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:ListBucket"],
            "Resource": "arn:aws:s3:::mybucket"
        }.
        {
            "Effect": "Allow",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::mybucket/reports/diabetes/*"
        }
    ]
}
```

The most common example of Bucket Level action is ListBucket. PutObject, GetObject are examples of  Object Level actions.

A common mistake when writing bucket policies is not including the bucket arn as a Resource in the policy. Then you will be left wondowering why I cannot list operations fail even though I have s3:Listbucket action in my policy.

## Cross account resource access

Consider this quote from S3 ducumentation : 

"If the requester is an IAM principal, Amazon S3 must determine if the parent AWS account to which the principal belongs has granted the principal necessary permission to perform the operation. In addition, if the request is for a bucket operation, such as a request to list the bucket content, Amazon S3 must verify that the bucket owner has granted permission for the requester to perform the operation. To perform a specific operation on a resource, an IAM principal needs permission from both the parent AWS account to which it belongs and the AWS account that owns the resource"  [ Ref 7 ]

This applies in general to any resource. What this means in practice is :

1. If the principal and the resource belong to the same account: Either the resource policy OR the policy attached to the principal (i.e. user/role) should explicitly Allow the action on the target resource.

2. If they belong to different accounts: Both, the resource policy AND the policy attached to the principal (i.e. user/role) MUST explicitly Allow the action on the target resource.




## References

1. https://docs.aws.amazon.com/pdfs/whitepapers/latest/aws-fault-isolation-boundaries/aws-fault-isolation-boundaries.pdf

2. https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html

3. https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html

4. https://docs.aws.amazon.com/awscloudtrail/latest/userguide/view-cloudtrail-events-cli.html

5. https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_temp_control-access_assumerole.html

6. https://docs.aws.amazon.com/service-authorization/latest/reference/reference_policies_actions-resources-contextkeys.html

7. https://docs.aws.amazon.com/IAM/latest/UserGuide/reference-arns.html#supported-arns

8. https://docs.aws.amazon.com/AmazonS3/latest/userguide/how-s3-evaluates-access-control.html



