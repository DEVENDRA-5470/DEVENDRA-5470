<div align="center">

<img src="assets/header.svg" width="850" alt="Devendra — Infrastructure Engineer"/>

<a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE"><img src="https://img.shields.io/badge/LinkedIn-black?style=flat-square&logo=linkedin&logoColor=0A66C2"/></a>
<a href="https://blog.devilhai.info"><img src="https://img.shields.io/badge/Blog-black?style=flat-square&logo=hashnode&logoColor=2962FF"/></a>
<a href="mailto:YOUR-EMAIL"><img src="https://img.shields.io/badge/Email-black?style=flat-square&logo=gmail&logoColor=EA4335"/></a>
&nbsp;&nbsp;
<img src="https://img.shields.io/badge/Status-Building%20in%20Production-2BEDA7?style=flat-square"/>
<img src="https://img.shields.io/badge/Location-DELHI%2C%20IN-38BDF8?style=flat-square"/>
<img src="https://komarev.com/ghpvc/?username=DEVENDRA-5470&label=Profile%20Views&color=38BDF8&style=flat-square"/>

<br/><br/>

<img src="assets/stats.svg" width="850" alt="Stats"/>

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=400&size=16&pause=1000&color=38BDF8&center=true&vCenter=true&width=850&lines=Designing+production-grade+Kubernetes+infrastructure;Building+zero-trust%2C+keyless+CI%2FCD+pipelines;3.5%2B+years+running+systems+that+don%27t+go+down"/>

<img src="https://raw.githubusercontent.com/DEVENDRA-5470/DEVENDRA-5470/output/github-contribution-grid-snake-dark.svg" width="850"/>

<table width="850">
<tr><td align="center">

<sub>Infrastructure engineer designing and operating the Kubernetes, CI/CD, and observability stacks behind production systems — from self-managed K3s clusters and service meshes to zero-trust, keyless CI/CD pipelines running in AWS.</sub>

</td></tr>
</table>

</div>

<br/>

<img align="center" src="https://capsule-render.vercel.app/api?type=rect&color=0:0f2027,100:2c5364&height=2&width=1000"/>

## 🎯 &nbsp;Focus

<div align="center">

<sub>`Kubernetes & Service Mesh` &nbsp;·&nbsp; `AWS (ECS · Lambda · IAM/OIDC)` &nbsp;·&nbsp; `CI/CD (Jenkins · Actions · ArgoCD)` &nbsp;·&nbsp; `Observability (Prometheus/Grafana)` &nbsp;·&nbsp; `IaC (Terraform · Ansible)`</sub>

</div>

<sub>Currently building out service mesh + GitOps delivery on a self-managed K3s cluster, and running production CI/CD for a MERN e-commerce platform on self-hosted Jenkins.</sub>

<br/>

<img align="center" src="https://capsule-render.vercel.app/api?type=rect&color=0:0f2027,100:2c5364&height=2&width=1000"/>

## 🧰 &nbsp;Stack

<div align="center">
<img src="assets/techstack.svg" width="850" alt="Tech stack constellation"/>
</div>

<br/>

<img align="center" src="https://capsule-render.vercel.app/api?type=rect&color=0:0f2027,100:2c5364&height=2&width=1000"/>

## 📁 &nbsp;Case studies

<div align="center">
<img src="assets/projects.svg" width="850" alt="Featured projects"/>
</div>

<br/>

<sub>Each project below is infrastructure I designed, deployed, and operate — written as a case study because the decisions matter more than the tech list.</sub>

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

<img align="center" src="https://capsule-render.vercel.app/api?type=rect&color=0:0f2027,100:2c5364&height=2&width=1000"/>

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

<img align="center" src="https://capsule-render.vercel.app/api?type=rect&color=0:0f2027,100:2c5364&height=2&width=1000"/>

<div align="center">

<img src="assets/footer.svg" width="850" alt="Footer"/>

<sub>💬 &nbsp;Open to conversations on SRE practice, cloud architecture, or mentoring engineers.</sub>
<br/>
<sub><a href="https://www.linkedin.com/in/YOUR-LINKEDIN-HANDLE">LinkedIn</a> · <a href="https://blog.devilhai.info">Blog</a></sub>

</div>
