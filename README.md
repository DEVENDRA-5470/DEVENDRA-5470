<div align="center">
<a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>
<a href="https://blog.devilhai.info">
  <img src="https://img.shields.io/badge/Blog-devilhai.info-FF5722?style=for-the-badge&logo=hashnode&logoColor=white"/>
</a>
<a href="mailto:YOUR-EMAIL">
  <img src="https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white"/>
</a>

</div>

<br/>

## 👨‍💻 About Me

I'm a **self-taught DevOps & SRE Engineer** with **3.5+ years of experience**, currently building and maintaining production infrastructure while also teaching AWS, DevOps, and backend engineering to the next generation of engineers.

- 🔭 **Currently working on:** Kubernetes service mesh work on `BookVault` & CI/CD infra for `Electronix`
- 🌱 **Currently learning / pursuing:** CKA (Certified Kubernetes Administrator) & AZ-104 (Azure Administrator)
- 💼 **Day job:** Managing production infra + delivering AWS/DevOps/Python training at an institute
- 📈 **Started coding:** December 2022 — no CS background, 100% self-taught
- 🌍 **Based in:** Faridabad, India (IST, UTC+5:30)
- ⚡ **Fun fact:** Went from zero coding experience to running production SRE workloads in under 4 years

<br/>

## 🛠️ Tech Stack

<div align="center">

**Cloud & Infrastructure**
<br/>
<img src="https://skillicons.dev/icons?i=aws,azure,terraform,ansible" />

**Containers & Orchestration**
<br/>
<img src="https://skillicons.dev/icons?i=docker,kubernetes,jenkins" />

**Monitoring & Observability**
<br/>
<img src="https://skillicons.dev/icons?i=prometheus,grafana" />

**Languages & Data**
<br/>
<img src="https://skillicons.dev/icons?i=python,bash,mongodb,mysql" />

**CI/CD & Version Control**
<br/>
<img src="https://skillicons.dev/icons?i=git,github,githubactions,linux" />

</div>

<br/>

## 🚀 Featured Projects — Tier 1 (Production-Grade Infra)

<table>
<tr>
<td width="50%">

### 🎯 IQuiz Hub — AWS ECS Fargate Platform
Production quiz platform (React + Node.js/Express/MongoDB) on **AWS ECS Fargate**. Full CI/CD via GitHub Actions with versioned Docker releases. Google OAuth, Monaco-editor coding-exam module with anti-cheat + auto-submit, cascade-delete data integrity. Debugged and resolved ECS circuit-breaker failures and nginx port-mapping issues in production.

<img src="https://img.shields.io/badge/AWS_ECS_Fargate-FF9900?style=flat-square&logo=amazonecs&logoColor=white"/> <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black"/> <img src="https://img.shields.io/badge/Node.js-339933?style=flat-square&logo=node.js&logoColor=white"/> <img src="https://img.shields.io/badge/MongoDB-47A248?style=flat-square&logo=mongodb&logoColor=white"/> <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white"/> <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white"/>

</td>
<td width="50%">

### 🏦 SimpleBank — Zero-SSH AWS-Native CI/CD
Flask + MySQL app with a fully **keyless CI/CD pipeline**: GitHub Actions via OIDC (no long-lived credentials), deploys to EC2 through SSM Session Manager (zero SSH exposure), secrets from SSM Parameter Store, images through ECR, Docker Compose orchestration across dual EC2 instances.

<img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white"/> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white"/> <img src="https://img.shields.io/badge/AWS_ECR-FF9900?style=flat-square&logo=amazonaws&logoColor=white"/> <img src="https://img.shields.io/badge/EC2-FF9900?style=flat-square&logo=amazonec2&logoColor=white"/> <img src="https://img.shields.io/badge/OIDC-4A90D9?style=flat-square&logo=openid&logoColor=white"/> <img src="https://img.shields.io/badge/GitHub_Actions-2088FF?style=flat-square&logo=githubactions&logoColor=white"/>

</td>
</tr>
<tr>
<td width="50%">

### ⚙️ Electronix — Enterprise Jenkins CI/CD
Full-stack MERN e-commerce platform on a **self-hosted, distributed Jenkins architecture**: dedicated SSH-based Jenkins agent on EC2 (Java 21), declarative pipeline (Checkout → Build → S3 Upload → CloudFront Invalidation), IAM Role-based auth (zero hardcoded keys), CloudFront OAC over public S3. Migrated backend MongoDB → MySQL/Sequelize across 5 relational models with junction tables. Razorpay payments + Recharts analytics dashboard.

<img src="https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white"/> <img src="https://img.shields.io/badge/AWS_S3-569A31?style=flat-square&logo=amazons3&logoColor=white"/> <img src="https://img.shields.io/badge/CloudFront-FF9900?style=flat-square&logo=amazonaws&logoColor=white"/> <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white"/> <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black"/> <img src="https://img.shields.io/badge/Razorpay-0C2451?style=flat-square&logo=razorpay&logoColor=white"/>

</td>
<td width="50%">

### 📚 BookVault — K3s Cluster & Service Mesh
Django + MySQL app on a **self-managed, live 3-node K3s Kubernetes cluster** (`bookvault.devilhai.online`), instrumented with Prometheus + Grafana + AlertManager (Telegram alerting). Extended into a **Linkerd service mesh** tracking golden signal metrics. Implements RBAC, NetworkPolicy, HPA/VPA, NodeAffinity, InitContainers, Redis caching, Traefik Ingress with cert-manager TLS — built as hands-on infra for CKA-level Kubernetes operations.

<img src="https://img.shields.io/badge/K3s-FFC61C?style=flat-square&logo=k3s&logoColor=black"/> <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white"/> <img src="https://img.shields.io/badge/Linkerd-2BEDA7?style=flat-square&logo=linkerd&logoColor=black"/> <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white"/> <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white"/> <img src="https://img.shields.io/badge/Traefik-24A1C1?style=flat-square&logo=traefikproxy&logoColor=white"/>

</td>
</tr>
<tr>
<td width="100%">

### 🏗️ [PROJECT NAME] — Multi-Tier GitOps Deployment
<!-- TODO: Replace with your actual project details -->
_Add description here: e.g. "2-tier / 3-tier architecture deployed on Kubernetes using GitOps principles with ArgoCD for continuous delivery, Jenkins for CI, and Helm for release management."_

<img src="https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white"/> <img src="https://img.shields.io/badge/ArgoCD-EF7B4D?style=flat-square&logo=argo&logoColor=white"/> <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white"/> <img src="https://img.shields.io/badge/GitOps-4A90D9?style=flat-square&logo=git&logoColor=white"/>

</td>
</tr>
</table>

<br/>

## 🔧 Featured Projects — Tier 2 (Infra Tooling & Automation)

<table>
<tr>
<td width="50%">

### 🌐 DevOps World — Serverless Blog Platform
Fully serverless blog at `blog.devilhai.info`: **S3 + CloudFront (OAC) + Route 53 + ACM** for the static frontend, **Cognito** for auth, **SES** for email, **Lambda** (welcome-subscriber function) behind **API Gateway**, and **DynamoDB** for post metadata. Custom terminal-themed UI with a local Python publishing script.

<img src="https://img.shields.io/badge/AWS_S3-569A31?style=flat-square&logo=amazons3&logoColor=white"/> <img src="https://img.shields.io/badge/CloudFront-FF9900?style=flat-square&logo=amazonaws&logoColor=white"/> <img src="https://img.shields.io/badge/Lambda-FF9900?style=flat-square&logo=awslambda&logoColor=white"/> <img src="https://img.shields.io/badge/DynamoDB-4053D6?style=flat-square&logo=amazondynamodb&logoColor=white"/> <img src="https://img.shields.io/badge/Cognito-DD344C?style=flat-square&logo=amazoncognito&logoColor=white"/>

</td>
<td width="50%">

### 🚨 SSH Intrusion Monitor
Security monitoring system on EC2: a `systemd`-managed service tails `/var/log/auth.log` in real time, geolocates suspicious IPs via ip-api.com, and fires Gmail SMTP alerts. Paired with a cron-driven bash-history digest tool for daily command audit summaries.

<img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/EC2-FF9900?style=flat-square&logo=amazonec2&logoColor=white"/> <img src="https://img.shields.io/badge/Linux-FCC624?style=flat-square&logo=linux&logoColor=black"/> <img src="https://img.shields.io/badge/Cron-4A90D9?style=flat-square&logo=clockify&logoColor=white"/>

</td>
</tr>
<tr>
<td width="50%">

### ☁️ TaskMaster — Terraform-Provisioned App
Flask + MongoDB Atlas task manager with infrastructure fully defined and provisioned via **Terraform** (EC2 deploy target), shipped as a versioned Docker Hub image (`deviliam/task-manager:v1`).

<img src="https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white"/> <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white"/> <img src="https://img.shields.io/badge/MongoDB_Atlas-47A248?style=flat-square&logo=mongodb&logoColor=white"/> <img src="https://img.shields.io/badge/Docker_Hub-2496ED?style=flat-square&logo=docker&logoColor=white"/>

</td>
<td width="50%">

### 📖 Kubernetes Learning Guide
A 20-section, ~260KB self-authored technical reference on Kubernetes internals — written while building hands-on cluster experience, used as a personal + training resource.

<img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white"/> <img src="https://img.shields.io/badge/Technical_Writing-4A90D9?style=flat-square&logo=markdown&logoColor=white"/>

</td>
</tr>
</table>

<br/>

## 📊 GitHub Stats

<div align="center">

<img height="165" src="https://github-readme-stats.vercel.app/api?username=DEVENDRA-5470&show_icons=true&theme=tokyonight&hide_border=true&count_private=true" />
<img height="165" src="https://github-readme-stats.vercel.app/api/top-langs/?username=DEVENDRA-5470&layout=compact&theme=tokyonight&hide_border=true" />

<br/>

<img src="https://github-readme-streak-stats.herokuapp.com/?user=DEVENDRA-5470&theme=tokyonight&hide_border=true" />

</div>

<br/>

## 📫 Let's Connect

<div align="center">

I'm always happy to talk DevOps, SRE practices, cloud architecture, or mentoring self-taught engineers.

<a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
</a>
<a href="https://blog.devilhai.info">
  <img src="https://img.shields.io/badge/Blog-devilhai.info-FF5722?style=for-the-badge&logo=hashnode&logoColor=white"/>
</a>

<br/><br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:2c5364,100:00c6ff&height=100&section=footer"/>

</div>
