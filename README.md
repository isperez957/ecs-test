# ecs-test

Simple Flask app deployed on AWS ECS Fargate with Terraform + GitHub Actions CI/CD.

## App

Three endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | JSON with hostname, version, timestamp |
| GET | `/health` | Health check (returns `{"status": "healthy"}`) |
| POST | `/echo` | Echo back the JSON body received |

### Local dev

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:5000
```

### Docker

```bash
docker build -t ecs-test .
docker run -p 5000:5000 ecs-test
```

## Infrastructure (Terraform)

Deployed in `eu-west-1` (Ireland). All resources defined in `terraform/`.

| Resource | Detail |
|---|---|
| VPC | 10.0.0.0/16, 2 AZs, public + private subnets, NAT Gateway |
| ALB | `ecs-test-alb-1973441836.eu-west-1.elb.amazonaws.com` (HTTP :80) |
| ECS Cluster | `ecs-test-cluster` |
| ECS Service | `ecs-test-svc` — 1 task, 256 CPU / 512 MB, Fargate |
| ECR | `649091762015.dkr.ecr.eu-west-1.amazonaws.com/ecs-test` |
| IAM OIDC | Role `ecs-test-github-actions` — GitHub Actions assume-role |

### Terraform state

Remote state in S3 (`ecs-test-terraform-state-649091762015`) with DynamoDB locking.

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## CI/CD Pipeline

Workflow: `.github/workflows/deploy.yml`

- Triggered on push to `main` or manual `workflow_dispatch`
- Authenticates via OIDC (no long-lived credentials) using the `AWS_ROLE_ARN` secret
- Builds Docker image, pushes to ECR
- Runs `aws ecs update-service --force-new-deployment`

## Live endpoint

```
http://ecs-test-alb-1973441836.eu-west-1.elb.amazonaws.com/
```

```json
{
  "service": "ecs-test",
  "version": "latest",
  "hostname": "ip-10-0-2-159.eu-west-1.compute.internal",
  "time": "2026-07-03T08:49:03Z"
}
```
