<div align="center">
  <img src="./assets/generated/galaxy-header.svg" width="100%" alt="Devendra — Infrastructure Engineer"/>
</div>

<br/>

<div align="center">

<a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE"><img src="https://img.shields.io/badge/-LinkedIn-080c14?style=for-the-badge&logo=linkedin&logoColor=38BDF8"/></a>
<a href="mailto:YOUR-EMAIL"><img src="https://img.shields.io/badge/-Email-080c14?style=for-the-badge&logo=gmail&logoColor=f87171"/></a>

<sub><img src="https://komarev.com/ghpvc/?username=DEVENDRA-5470&label=Profile%20Views&color=080c14&style=for-the-badge"/></sub>

</div>

<br/>

<div align="center">
  <img src="./assets/generated/stats-card.svg" width="100%" alt="Mission Telemetry"/>
</div>

<br/>

## 🧰 &nbsp;Stack

<div align="center">
  <img src="./assets/generated/tech-stack.svg" width="100%" alt="Tech Stack"/>
</div>

<br/>

<div align="center">
  <img src="https://raw.githubusercontent.com/DEVENDRA-5470/DEVENDRA-5470/output/github-contribution-grid-snake-dark.svg" width="100%"/>
</div>

<br/>

## 🎯 &nbsp;Focus

<sub>Infrastructure engineer designing and operating the Kubernetes, CI/CD, and observability stacks behind production systems — from self-managed K3s clusters and service meshes to zero-trust, keyless CI/CD pipelines running in AWS.</sub>

<br/>

Currently building out service mesh + GitOps delivery on a self-managed K3s cluster, and running production CI/CD for a MERN e-commerce platform on self-hosted Jenkins.

<br/>

## 🚀 &nbsp;Capstone initiatives

<sub>Production-grade infrastructure patterns I'm building out to cover the full SRE/platform surface area — resilience, cost, security, and delivery.</sub>

<br/>

<table>
<tr>
<td width="50%" valign="top">

#### 🌍 &nbsp;Multi-Region Disaster Recovery
<sub>Active-passive AWS DR architecture</sub>

<sub>*Approach* — active-passive infrastructure across two AWS regions using Route 53 health-check-based failover, RDS cross-region read replicas, and S3 cross-region replication for critical data<br/>
*Outcome* — RTO under 15 minutes, RPO under 5 minutes, validated through simulated region-failure drills</sub>

<sub>`Route 53` `RDS` `S3 CRR`</sub>

</td>
<td width="50%" valign="top">

#### 🛠️ &nbsp;GitOps Internal Developer Platform
<sub>Self-service microservice provisioning</sub>

<sub>*Approach* — ArgoCD for GitOps delivery + Backstage as developer portal, letting engineers provision a new microservice from a single YAML manifest<br/>
*Outcome* — onboarding time cut from 2-3 days to under 30 minutes, standardized namespace/CI/monitoring setup across services</sub>

<sub>`ArgoCD` `Backstage` `Kubernetes`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 💰 &nbsp;FinOps Cost Dashboard
<sub>Real-time cloud cost visibility</sub>

<sub>*Approach* — AWS Cost Explorer API + Lambda + Grafana for real-time anomaly detection, AWS Config tagging enforcement, automated idle-resource shutdown<br/>
*Outcome* — ~25% reduction in monthly AWS spend, cost anomalies surfaced within 24 hours, 100% tagging compliance</sub>

<sub>`Cost Explorer` `Lambda` `Grafana`</sub>

</td>
<td width="50%" valign="top">

#### 🔄 &nbsp;Zero-Downtime Canary Deployments
<sub>Metrics-gated progressive delivery</sub>

<sub>*Approach* — Argo Rollouts on Kubernetes with canary stages gated by Prometheus metrics (error rate, p99 latency) before traffic promotion<br/>
*Outcome* — zero-downtime releases with automated rollback on SLO breach, blast radius capped at 5% traffic per stage</sub>

<sub>`Argo Rollouts` `Prometheus` `Kubernetes`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 📊 &nbsp;Centralized Observability Stack
<sub>Unified logs, metrics & traces</sub>

<sub>*Approach* — Grafana Loki (logs), Tempo (tracing), Prometheus (metrics) unified across a multi-service architecture with SLO/SLI dashboards and alerting<br/>
*Outcome* — ~40% reduction in mean-time-to-detection via centralized cross-service trace correlation</sub>

<sub>`Loki` `Tempo` `Prometheus`</sub>

</td>
<td width="50%" valign="top">

#### 🔒 &nbsp;Zero-Trust Secrets & Security Pipeline
<sub>Dynamic secrets + CI/CD security gates</sub>

<sub>*Approach* — HashiCorp Vault integrated with Kubernetes for dynamic, short-lived secrets; Trivy (container scanning) + SonarQube (code quality) as mandatory CI/CD gates<br/>
*Outcome* — zero hardcoded secrets in codebases, critical/high vulnerabilities blocked pre-deployment</sub>

<sub>`Vault` `Trivy` `SonarQube`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 📡 &nbsp;Event-Driven Data Pipeline
<sub>Real-time Kafka streaming</sub>

<sub>*Approach* — Apache Kafka with producer/consumer microservices and Kafka Connect for DB sync, monitored via Kafka Exporter + Grafana<br/>
*Outcome* — sub-second end-to-end latency at 99.9% delivery reliability, services decoupled for independent scaling</sub>

<sub>`Kafka` `Kafka Connect` `Grafana`</sub>

</td>
<td width="50%" valign="top">

#### 💥 &nbsp;Chaos Engineering Platform
<sub>Automated resilience testing</sub>

<sub>*Approach* — LitmusChaos on Kubernetes running scheduled pod-kill, network-latency, and node-failure experiments against production-like environments<br/>
*Outcome* — 3+ critical single-points-of-failure identified pre-incident, automated resilience scoring reports</sub>

<sub>`LitmusChaos` `Kubernetes`</sub>

</td>
</tr>
</table>

<br/>

## ⚙️ &nbsp;Infrastructure in production

<sub>Systems I've designed, deployed, and currently operate — written as case studies because the decisions matter more than the tech list.</sub>

<br/>

<table>
<tr>
<td width="50%" valign="top">

#### 🧩 &nbsp;BookVault
<sub>Self-managed K3s cluster, service mesh & GitOps</sub>

A 3-node K3s cluster running Django/MySQL, built as hands-on infra for CKA-level operations — not a managed EKS shortcut.

<sub>*Problem* — needed real exposure to scheduling, networking, and RBAC that managed Kubernetes abstracts away<br/>
*Approach* — self-managed control plane, Linkerd mesh tracking golden-signal metrics, Jenkins + ArgoCD GitOps delivery, Traefik + cert-manager TLS<br/>
*Hardening* — RBAC, NetworkPolicy, HPA/VPA, node affinity, init containers, Redis caching<br/>
*Observability* — Prometheus + Grafana + AlertManager → Telegram</sub>

<sub>`K3s` `Linkerd` `ArgoCD` `Jenkins` `Prometheus`</sub>

</td>
<td width="50%" valign="top">

#### ⚙️ &nbsp;Electronix
<sub>Distributed Jenkins CI/CD, production MERN app</sub>

Full-stack e-commerce platform where the interesting work is the delivery pipeline.

<sub>*Problem* — needed zero hardcoded credentials and a clean deploy path to S3/CloudFront<br/>
*Approach* — dedicated SSH-based Jenkins agent, declarative pipeline (build → S3 → CloudFront invalidation), IAM role-based auth, CloudFront OAC over private S3<br/>
*Migration* — moved backend from MongoDB to MySQL/Sequelize across 5 relational models with junction tables — a schema redesign, not a lift-and-shift</sub>

<sub>`Jenkins` `S3/CloudFront` `MySQL` `Razorpay`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 🔐 &nbsp;SimpleBank
<sub>Zero-SSH, keyless AWS-native CI/CD</sub>

Design goal: eliminate standing access, not just automate deploys.

<sub>*Problem* — long-lived SSH keys and static credentials are a standing attack surface<br/>
*Approach* — GitHub Actions via OIDC (no stored credentials), deploys through SSM Session Manager (no open SSH port), secrets from SSM Parameter Store, images through ECR</sub>

<sub>`Flask` `OIDC` `SSM` `ECR`</sub>

</td>
<td width="50%" valign="top">

#### 🎯 &nbsp;IQuiz Hub
<sub>Production platform on ECS Fargate</sub>

React/Node/MongoDB quiz platform with a proctored coding-exam module.

<sub>*Problem* — ECS deployments were failing silently under the circuit breaker<br/>
*Approach* — diagnosed and resolved circuit-breaker rollback failures and an nginx port-mapping misconfig in production — failures that only surface under real deploy conditions<br/>
*Features* — Monaco-based anti-cheat exam module, cascade-delete data integrity</sub>

<sub>`ECS Fargate` `React` `MongoDB`</sub>

</td>
</tr>
</table>

<details>
<summary><sub>📂 &nbsp;More projects — serverless blog, security tooling, IaC deployment</sub></summary>

<br/>

<sub>🌐 &nbsp;**DevOps World** — fully serverless blog (`blog.devilhai.info`): S3 + CloudFront (OAC) + Route 53 + ACM for the frontend, Cognito for auth, SES for email, Lambda behind API Gateway for subscriber onboarding, DynamoDB for post metadata.

🚨 &nbsp;**SSH Intrusion Monitor** — `systemd`-managed service tailing `/var/log/auth.log` in real time, geolocating suspicious source IPs and firing SMTP alerts, paired with a cron-driven bash-history audit digest.

☁️ &nbsp;**TaskMaster** — Flask/MongoDB Atlas app with infrastructure fully defined in Terraform, shipped as a versioned Docker image.

📖 &nbsp;**Kubernetes Internals Guide** — a 20-section, self-authored technical reference written while building the K3s cluster above, now used as training material.</sub>

</details>

<br/>

## 📈 &nbsp;GitHub activity

<div align="center">
<img height="150" src="https://github-readme-stats.vercel.app/api?username=DEVENDRA-5470&show_icons=true&theme=tokyonight&hide_border=true&bg_color=0d1117" />
<img height="150" src="https://github-readme-stats.vercel.app/api/top-langs/?username=DEVENDRA-5470&layout=compact&theme=tokyonight&hide_border=true&bg_color=0d1117" />

<br/>

<img src="https://github-readme-streak-stats.herokuapp.com?user=DEVENDRA-5470&theme=tokyonight&hide_border=true&background=0d1117" />

<br/>

<img src="https://github-profile-trophy.vercel.app/?username=DEVENDRA-5470&theme=tokyonight&no-frame=true&no-bg=true&margin-w=8&row=1" />

</div>

<br/>

<div align="center">

<sub>💬 &nbsp;Open to conversations on SRE practice, cloud architecture, or mentoring engineers.</sub>
<br/>
<sub><a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE">LinkedIn</a> · <a href="https://blog.devilhai.info">Blog</a></sub>

</div>
