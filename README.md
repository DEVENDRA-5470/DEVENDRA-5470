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

<sub>Senior Infrastructure/SRE engineer designing and operating platform-level systems — multi-cluster Kubernetes, org-wide CI/CD, cost governance, and compliance-grade security — for engineering orgs, not single apps.</sub>

<br/>

Currently building out a self-service internal platform on top of a multi-cluster Kubernetes fleet, and driving cost + compliance governance across a multi-account AWS Organization.

<br/>

## 🏛️ &nbsp;Platform & architecture initiatives

<sub>Systems built for organizational scale — multiple teams, multiple environments, real business constraints. Each one written as Problem → Architecture → Business impact.</sub>

<br/>

<table>
<tr>
<td width="50%" valign="top">

#### 🌐 &nbsp;Multi-Cluster Kubernetes Platform
<sub>Fleet management across prod, staging & DR</sub>

<sub>*Problem* — 15+ microservices deployed inconsistently across environments, no shared golden path, each team reinventing manifests<br/>
*Architecture* — 3-cluster fleet (prod / staging / DR across regions) managed via ArgoCD ApplicationSets, shared Helm library charts, centralized RBAC + OPA/Gatekeeper policy enforcement, Cilium for cross-cluster networking<br/>
*Business impact* — cut new-service provisioning from days to under an hour; policy-as-code eliminated an entire class of misconfiguration incidents across teams</sub>

<sub>`ArgoCD` `OPA/Gatekeeper` `Cilium` `Helm`</sub>

</td>
<td width="50%" valign="top">

#### 💵 &nbsp;Org-Wide Cost Governance (FinOps)
<sub>Multi-account AWS Organization, $50K+/mo spend</sub>

<sub>*Problem* — no cost visibility across 10+ AWS accounts, no accountability per team, spend growing faster than usage<br/>
*Architecture* — AWS Organizations + Control Tower guardrails, Cost & Usage Reports into Athena/QuickSight, per-team showback dashboards, automated Savings Plan/RI purchase recommendations, budget alerts tied to Slack<br/>
*Business impact* — ~22% reduction in monthly cloud spend org-wide, full cost attribution per team enabling accurate project P&L</sub>

<sub>`AWS Organizations` `Athena` `Control Tower`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 🔁 &nbsp;Monolith → Microservices Migration
<sub>Zero-downtime cutover of a live production system</sub>

<sub>*Problem* — legacy monolith blocking independent team releases, single point of failure for the whole platform<br/>
*Architecture* — strangler-fig pattern: new services stood up behind an API gateway, traffic shifted incrementally via weighted routing, dual-write + backfill for data consistency, rollback plan rehearsed before each cutover phase<br/>
*Business impact* — migrated a live revenue-generating system with zero customer-facing downtime; independent team deploys went from weekly-coordinated releases to on-demand</sub>

<sub>`API Gateway` `Strangler Fig` `Dual-Write`</sub>

</td>
<td width="50%" valign="top">

#### 🛡️ &nbsp;Compliance-Grade Infrastructure
<sub>Audit-ready hardening (SOC 2 / PCI-DSS style controls)</sub>

<sub>*Problem* — infra couldn't pass a compliance audit: no encryption enforcement, no access reviews, no tamper-evident logs<br/>
*Architecture* — encryption-at-rest/in-transit enforced via SCPs, quarterly IAM access reviews automated with a Lambda, immutable CloudTrail → S3 Object Lock audit trail, compliance-as-code checks (Conftest/OPA) gating every CI pipeline<br/>
*Business impact* — passed external audit readiness review with zero critical findings; compliance checks now block non-compliant infra before it ships</sub>

<sub>`SCP` `CloudTrail` `Conftest`</sub>

</td>
</tr>
<tr>
<td width="50%" valign="top">

#### 🚨 &nbsp;Incident Command & SLO Program
<sub>Formal on-call, postmortems & error-budget enforcement</sub>

<sub>*Problem* — incidents handled ad hoc, no on-call rotation, repeat outages from the same unaddressed root causes<br/>
*Architecture* — SLO/error-budget framework per service, PagerDuty-based on-call rotation with clear escalation paths, blameless postmortem process with tracked action items, runbook library tied to alerts<br/>
*Business impact* — reduced MTTR org-wide, repeat-incident rate dropped as postmortem action items were enforced through the sprint process</sub>

<sub>`SLO/Error Budgets` `PagerDuty` `Postmortems`</sub>

</td>
<td width="50%" valign="top">

#### 🧭 &nbsp;Internal Developer Platform (Self-Service)
<sub>Golden paths for 20+ engineers across product teams</sub>

<sub>*Problem* — platform team was a bottleneck for every new service, environment, or pipeline request<br/>
*Architecture* — Backstage developer portal + ArgoCD GitOps backend, scaffolded golden-path templates (service + CI + monitoring + alerting in one PR), self-service environment provisioning with guardrails baked in<br/>
*Business impact* — platform-team ticket load dropped sharply as teams self-served; new-service lead time went from multi-day platform-team dependency to same-day, engineer-driven</sub>

<sub>`Backstage` `ArgoCD` `Golden Paths`</sub>

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
