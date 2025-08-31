# 👋 Hi, I'm Aqeel Raza

![Visitors](https://visitor-badge.laobi.icu/badge?page_id=aqeelrazagondal.aqeelrazagondal)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=102)](https://github.com/ellerbrock/open-source-badge/)
[![Profile Views](https://komarev.com/ghpvc/?username=aqeelrazagondal&color=0e75b6&style=flat)](https://github.com/aqeelrazagondal)

I'm a Senior Backend Developer focused on scalable, secure, and high‑performance systems with Node.js, NestJS, TypeScript, and AWS. I design cloud-native backends, decompose monoliths, and ship reliable distributed services.

- 🔭 Open to backend roles (UK/EU-friendly, remote or hybrid)
- 🌱 Deepening expertise in cloud architecture and distributed systems
- 🛠️ Building and contributing to open-source, infra tooling, and backend templates
- 💬 Ask me about Node.js, microservices, AWS, event-driven design, and observability

---

## 🔎 What I Do (at a glance)

- Microservices and serverless backends on AWS (Lambda, ECS Fargate)  
- Event-driven systems with Kafka/SNS/SQS  
- API platforms (REST + GraphQL), auth with Cognito/JWT  
- Performance tuning, caching (Redis), and cost-aware cloud design  
- CI/CD pipelines with GitHub Actions/CodeDeploy, blue/green, and canary releases  
- Observability with CloudWatch/X-Ray/log correlation

---

## 🧠 Core Competencies

- Languages/Frameworks: Node.js, TypeScript, NestJS, Express, Koa, Python  
- Cloud: AWS (Lambda, EC2, S3, Cognito, CloudWatch, SES, SNS, SQS, VPC, IAM)  
- Data: PostgreSQL, MySQL, MongoDB, DynamoDB, Redis, ClickHouse  
- Architecture: Microservices, Serverless, EDA, CQRS-lite, Monorepos (Nx)  
- Messaging: Kafka, SQS/SNS  
- Testing/Quality: Jest, Mocha, Jasmine, Supertest, eslint + prettier  
- DevOps: Docker, GitHub Actions, CodeDeploy, IaC-lite, blue/green  
- Tooling: WebStorm, VS Code, GitHub/GitLab

---

## 📌 Impact Highlights

- 30% faster deployments via robust CI/CD pipelines on AWS (Artifacts, staged rollouts)  
- 35% latency improvement on a municipal services backend (query/caching/profile-driven tuning)  
- 40% maintenance time reduction by splitting monoliths into focused services and adopting Nx  
- 25% infra cost savings by moving suitable workloads to Lambda + SQS fan-out  
- Production-grade observability: actionable logs/metrics/traces with CloudWatch + X-Ray

---

## 🧩 Select Case Studies

- ChainGPT – AI-integrated platform for secure NLP processing  
  - Hardened API gateway, request tracing, burst control, and safe job processing with queues

- CNBC Arabia – Real-time media publishing backend  
  - Built event-driven ingestion + publishing flows with durable queues and cache-first delivery

- Secure EHR System – HIPAA-informed design  
  - Role-based access, audit trails, and encrypted-at-rest storage; standardized interfaces

- ATS + Talent Acquisition – Occy  
  - Scalable, low-latency APIs and data pipelines improving recruiter workflows and reporting

- PackageX – Vision-powered logistics  
  - Serverless API integrations with performance-optimized Lambdas and cost-aware design

- Election Management System – Secure, audit‑ready voter & results services (AWS + DevSecOps)  
  - Platform: API Gateway → Lambda and NestJS on ECS Fargate; Cognito (RBAC), WAF + Shield, CloudFront + S3 for static artifacts; Aurora PostgreSQL (core) + DynamoDB (event/audit) with KMS CMKs  
  - Data integrity: end‑to‑end encryption (in transit/at rest), S3 Object Lock (immutability), idempotent writes, append‑only audit trail via Streams/Firehose → S3/Glacier  
  - Messaging & scale: SQS/SNS fan‑out for tallying, notifications, and reconciliation; autoscaling at queue depth and p95 latency targets  
  - Observability: structured logging with correlation IDs, CloudWatch metrics/alarms, X‑Ray traces across API/Lambda/services  
  - DevSecOps: CodeCommit → CodeBuild → CodeDeploy/CodePipeline with gated stages; SCA (OWASP Dependency‑Check), SAST (SonarQube), DAST (OWASP ZAP), container/IaC scanning (e.g., Trivy/grype, cfn‑nag); SBOM generation, secrets scanning, policy‑as‑code (OPA/Conftest); findings normalized and aggregated in Security Hub; CloudTrail + Config for audit  
  - Delivery: blue/green + manual approval for prod, automated rollbacks on health/regression checks

<details>
  <summary>Pipeline snapshot (DevSecOps)</summary>

- Source: CodeCommit, branch policies; git hooks + secrets scanning  
- Build: CodeBuild with parallel SCA/SAST, unit/integration tests, SBOM; artifact signing  
- Test: Ephemeral environment deploy → DAST (ZAP) → results to Security Hub  
- Approve/Deploy: Severity thresholds gate promotion → blue/green on ECS/Lambda; canary where applicable  
- Monitor/Audit: CloudWatch, X‑Ray, GuardDuty, Security Hub; CloudTrail and Config rules enforce best practices
</details>

---

## 🧭 Architecture Notes

- Standardized service blueprint:
  - API: REST/GraphQL with NestJS Modules, DTOs, class-validator  
  - Resilience: retries + backoff, idempotency keys, circuit breakers where needed  
  - Messaging: outbox pattern where persistence consistency matters  
  - Observability: structured logs, correlation IDs, RED/USE metrics  
  - Security: least-privileged IAM, token scoping, secret hygiene, encryption

- Data patterns I apply:
  - Read/write segregation for heavy domains  
  - Caching tiers (Redis) with cache stampede controls  
  - Async projections for analytics/reporting (ClickHouse/Elasticsearch)

---

## 🛠️ Tech Stack

- Languages: Node.js, TypeScript, Python  
- Frameworks: NestJS, Express, Koa  
- Databases: PostgreSQL, MySQL, MongoDB, DynamoDB, Redis, ClickHouse  
- Cloud: AWS Lambda, ECS Fargate, EC2, S3, Cognito, SES, SNS, SQS, VPC, IAM, CloudWatch, X-Ray  
- DevOps: Docker, CI/CD, GitHub Actions

Badges:
![AWS](https://img.shields.io/badge/Cloud-AWS-informational?style=flat&logo=amazon-aws&logoColor=white&color=6aa6f8)
![Lambda](https://img.shields.io/badge/Compute-Lambda-informational?style=flat&logo=aws-lambda&logoColor=white&color=6aa6f8)
![DynamoDB](https://img.shields.io/badge/Database-DynamoDB-informational?style=flat&logo=amazon-dynamodb&logoColor=white&color=6aa6f8)
![S3](https://img.shields.io/badge/Storage-S3-informational?style=flat&logo=amazon-s3&logoColor=white&color=6aa6f8)
![SQS](https://img.shields.io/badge/Queue-SQS-informational?style=flat&logo=amazon-sqs&logoColor=white&color=6aa6f8)
![SNS](https://img.shields.io/badge/Pub/Sub-SNS-informational?style=flat&logo=amazon-sns&logoColor=white&color=6aa6f8)
![ECS Fargate](https://img.shields.io/badge/Container-ECS_Fargate-informational?style=flat&logo=amazon-ecs&logoColor=white&color=6aa6f8)
![Cognito](https://img.shields.io/badge/Auth-Cognito-informational?style=flat&logo=amazon-aws&logoColor=white&color=6aa6f8)
![PostgreSQL](https://img.shields.io/badge/DB-PostgreSQL-informational?style=flat&logo=postgresql&logoColor=white&color=6aa6f8)
![Redis](https://img.shields.io/badge/Cache-Redis-informational?style=flat&logo=redis&logoColor=white&color=6aa6f8)
![Kafka](https://img.shields.io/badge/Streaming-Kafka-informational?style=flat&logo=apache-kafka&logoColor=white&color=6aa6f8)
![Docker](https://img.shields.io/badge/DevOps-Docker-informational?style=flat&logo=docker&logoColor=white&color=6aa6f8)
![NestJS](https://img.shields.io/badge/Framework-NestJS-informational?style=flat&logo=nestjs&logoColor=white&color=6aa6f8)
![TypeScript](https://img.shields.io/badge/Language-TypeScript-informational?style=flat&logo=typescript&logoColor=white&color=6aa6f8)

---

## 🗂️ Featured Projects

- ChainGPT – AI-integrated platform for secure NLP processing  
- CNBC Arabia Backend – Real-time media publishing backend  
- Secure EHR System – Privacy-first records with audit-ready flows  
- Election Management System – Secure, scalable voter & results services (AWS + DevSecOps)  
- ATS + Talent Acquisition – https://occy.com/  
- PackageX – https://packagex.io/

Tip: Some repositories are private or client-owned. I’m happy to walk through architecture and anonymized code samples upon request.

---

## 🧪 Example Topics I Write/Build About

- End-to-end tracing in serverless with correlation IDs  
- SQS + Lambda patterns: batching, DLQs, idempotency  
- Scaling read-heavy APIs with Redis and projection tables  
- Safe schema evolution and zero-downtime releases  
- API rate limiting: token bucket vs fixed window vs leaky bucket

---

## 🏆 Trophies & Stats

[![trophy](https://github-profile-trophy.vercel.app/?username=aqeelrazagondal&theme=nord&column=7)](https://github.com/ryo-ma/github-profile-trophy)

![Aqeel’s GitHub Stats](https://github-readme-stats.vercel.app/api?username=aqeelrazagondal&show_icons=true&theme=tokyonight)
![Top Langs](https://github-readme-stats.vercel.app/api/top-langs/?username=aqeelrazagondal&layout=compact&theme=tokyonight)

---

## 🎓 Certifications

- AWS Lambda & Serverless Architecture Bootcamp – Udemy  
- Node.js: Complete Guide to Building RESTful APIs – Udemy (Mosh Hamedani)  
- Elasticsearch Essential Training – Lynda.com

---

## 📮 Contact

- 📍 Northampton, UK  
- ✉ Email: <your-email>  
- 📞 Phone: <your-phone>  
- 🔗 LinkedIn: https://www.linkedin.com/in/aqeel-raza-5b64887b/  
- 💻 GitHub: https://github.com/aqeelrazagondal

---

> “Consistency beats talent. Code daily. Learn always.”
