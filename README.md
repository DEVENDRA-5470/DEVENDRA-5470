<div align="center">

# Devendra — Senior DevOps & SRE Engineer

Infrastructure engineer with 3.5+ years running production systems — designing and operating the Kubernetes, CI/CD, and observability stacks underneath them.

[LinkedIn](https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE) · [Blog](https://blog.devilhai.info) · Faridabad, India (IST)

</div>

---

## Focus areas

`Kubernetes & Service Mesh` · `AWS (ECS, Lambda, IAM/OIDC)` · `CI/CD (Jenkins, GitHub Actions, ArgoCD)` · `Observability (Prometheus/Grafana/AlertManager)` · `IaC (Terraform, Ansible)`

Currently: building out service mesh + GitOps delivery on a self-managed K3s cluster, and running production CI/CD for a MERN e-commerce platform on self-hosted Jenkins.

---

## Case studies

Each project below is infrastructure I designed, deployed, and operate — not a tutorial clone. Written as case studies because the *decisions* matter more than the tech list.

### BookVault — Self-managed Kubernetes cluster with service mesh & GitOps
A 3-node K3s cluster (1 control plane, 2 workers) running a Django/MySQL app, built as hands-on infrastructure for CKA-level Kubernetes operations — not a managed EKS shortcut.

- **Problem:** needed real operational exposure to cluster internals (scheduling, networking, RBAC) that managed Kubernetes abstracts away.
- **Approach:** self-managed control plane; Linkerd service mesh instrumented for golden-signal metrics (latency, traffic, errors, saturation); Jenkins + ArgoCD for GitOps-style delivery; Traefik Ingress with cert-manager for TLS.
- **Hardening:** RBAC, NetworkPolicy, HPA/VPA, node affinity, init containers, Redis caching layer.
- **Observability:** Prometheus + Grafana + AlertManager wired to Telegram for on-call-style alerting.
- **Stack:** K3s · Kubernetes · Linkerd · ArgoCD · Jenkins · Prometheus · Grafana · Traefik

### Electronix — Distributed Jenkins CI/CD for a production MERN app
Full-stack e-commerce platform where the interesting work is the delivery pipeline, not the storefront.

- **Problem:** needed a CI/CD path with zero hardcoded credentials and a clean deploy story to S3/CloudFront.
- **Approach:** dedicated SSH-based Jenkins agent on EC2, declarative pipeline (checkout → build → S3 upload → CloudFront invalidation), IAM role-based auth end to end, CloudFront Origin Access Control over an otherwise-public S3 bucket.
- **Migration:** moved the backend data layer from MongoDB to MySQL/Sequelize across 5 relational models with junction tables — a schema redesign, not a lift-and-shift.
- **Stack:** Jenkins · AWS S3/CloudFront · MySQL/Sequelize · React · Razorpay

### SimpleBank — Zero-SSH, keyless AWS-native CI/CD
The design goal here was eliminating standing access, not just automating deploys.

- **Problem:** long-lived SSH keys and static AWS credentials are a standing attack surface.
- **Approach:** GitHub Actions authenticates via OIDC (no stored credentials), deploys reach EC2 through SSM Session Manager (no open SSH port at all), runtime secrets pulled from SSM Parameter Store, images shipped through ECR, orchestrated with Docker Compose across dual EC2 instances.
- **Stack:** Flask · MySQL · AWS ECR/EC2/SSM · OIDC · GitHub Actions

### IQuiz Hub — Production platform on ECS Fargate
React/Node/MongoDB quiz platform, including a proctored coding-exam module (Monaco editor, anti-cheat, auto-submit) and cascade-delete data integrity across related collections.

- **Problem:** ECS deployments were failing silently under the circuit breaker; a working container image doesn't guarantee a working service.
- **Approach:** diagnosed and resolved ECS circuit-breaker rollback failures and an nginx port-mapping misconfiguration in production — the kind of failure that only shows up under real deploy conditions, not in local `docker run`.
- **Delivery:** versioned Docker releases through GitHub Actions CI/CD.
- **Stack:** AWS ECS Fargate · React · Node/Express · MongoDB · GitHub Actions

### DevOps World — Serverless blog platform
Built to prove out a fully serverless architecture end to end, not just host a blog.

- **Approach:** S3 + CloudFront (OAC) + Route 53 + ACM for the static frontend, Cognito for auth, SES for transactional email, a Lambda function behind API Gateway for subscriber onboarding, DynamoDB for post metadata.
- **Stack:** S3 · CloudFront · Lambda · API Gateway · DynamoDB · Cognito · SES

### SSH Intrusion Monitor — Security tooling on EC2
A `systemd`-managed service tailing `/var/log/auth.log` in real time, geolocating suspicious source IPs and firing SMTP alerts — plus a cron-driven bash-history digest for daily command auditing.

- **Stack:** Python · systemd · Linux · Cron

### TaskMaster — Terraform-provisioned deployment
Flask/MongoDB Atlas app with infrastructure fully defined as code rather than console-clicked, shipped as a versioned image.

- **Stack:** Terraform · Flask · MongoDB Atlas · Docker Hub

---

## Reference work

**Kubernetes Internals Guide** — a 20-section, self-authored technical reference written while building the K3s cluster above, now used as training material at the institute where I teach.

---

## GitHub activity

<div align="center">
<img height="165" src="https://github-readme-stats.vercel.app/api?username=DEVENDRA-5470&show_icons=true&theme=tokyonight&hide_border=true" />
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=DEVENDRA-5470&layout=compact&theme=tokyonight&hide_border=true" />
</div>

---

<div align="center">

Open to conversations on SRE practice, cloud architecture, or mentoring self-taught engineers.

[LinkedIn](https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE) · [Blog](https://blog.devilhai.info)

</div>
