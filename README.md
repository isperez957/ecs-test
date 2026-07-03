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

## Infrastructure

IaC managed in the consolidated [terraform](https://github.com/isperez957/terraform) repo (`ecs-test/` folder).

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
