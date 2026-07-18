<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f2027,50:2c5364,100:00c6ff&height=200&section=header&text=Hi%20There,%20I'm%20Devendra&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Senior%20DevOps%20%26%20SRE%20Engineer&descAlignY=58&descSize=18" width="100%"/>

<a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white"/>
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

**Stack:** `AWS ECS Fargate` `React` `Node.js` `MongoDB` `Docker` `GitHub Actions`

</td>
<td width="50%">

### 🏦 SimpleBank — Zero-SSH AWS-Native CI/CD
Flask + MySQL app with a fully **keyless CI/CD pipeline**: GitHub Actions via OIDC (no long-lived credentials), deploys to EC2 through SSM Session Manager (zero SSH exposure), secrets from SSM Parameter Store, images through ECR, Docker Compose orchestration across dual EC2 instances.

**Stack:** `AWS ECR` `SSM` `OIDC` `EC2` `Docker Compose` `GitHub Actions`

</td>
</tr>
<tr>
<td width="50%">

### ⚙️ Electronix — Enterprise Jenkins CI/CD
Full-stack MERN e-commerce platform on a **self-hosted, distributed Jenkins architecture**: dedicated SSH-based Jenkins agent on EC2 (Java 21), declarative pipeline (Checkout → Build → S3 Upload → CloudFront Invalidation), IAM Role-based auth (zero hardcoded keys), CloudFront OAC over public S3. Migrated backend MongoDB → MySQL/Sequelize across 5 relational models with junction tables. Razorpay payments + Recharts analytics dashboard.

**Stack:** `Jenkins` `AWS S3/CloudFront` `MySQL/Sequelize` `IAM` `MERN` `Razorpay`

</td>
<td width="50%">

### 📚 BookVault — K3s Cluster & Service Mesh
Django + MySQL app on a **self-managed K3s Kubernetes cluster**, instrumented with Prometheus + Grafana. Extended into a 3-node **Linkerd service mesh**, tracking golden signal metrics (latency, traffic, errors, saturation) — hands-on infra built for CKA-level Kubernetes operations.

**Stack:** `K3s` `Kubernetes` `Linkerd` `Prometheus` `Grafana` `Django`

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

**Stack:** `S3` `CloudFront` `Lambda` `API Gateway` `DynamoDB` `Cognito` `SES`

</td>
<td width="50%">

### 🚨 SSH Intrusion Monitor
Security monitoring system on EC2: a `systemd`-managed service tails `/var/log/auth.log` in real time, geolocates suspicious IPs via ip-api.com, and fires Gmail SMTP alerts. Paired with a cron-driven bash-history digest tool for daily command audit summaries.

**Stack:** `Python` `systemd` `EC2` `SMTP` `Cron`

</td>
</tr>
<tr>
<td width="50%">

### ☁️ TaskMaster — Terraform-Provisioned App
Flask + MongoDB Atlas task manager with infrastructure fully defined and provisioned via **Terraform** (EC2 deploy target), shipped as a versioned Docker Hub image (`deviliam/task-manager:v1`).

**Stack:** `Terraform` `EC2` `MongoDB Atlas` `Docker Hub`

</td>
<td width="50%">

### 📖 Kubernetes Learning Guide
A 20-section, ~260KB self-authored technical reference on Kubernetes internals — written while building hands-on cluster experience, used as a personal + training resource.

**Stack:** `Kubernetes` `Technical Writing`

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
