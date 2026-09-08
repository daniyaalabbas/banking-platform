# SecureCore Banking — Cloud-Native Core Banking Platform

A production-grade, highly available, resilient Core Banking Microservice architecture deployed on **Red Hat OpenShift (Enterprise Kubernetes on AWS)** with automated GitOps CI/CD delivery.

## 🏛️ Architecture Overview

The platform decouples compute, state, network security, and configuration into isolated layers:

```text
[ Public Internet / Clients ]
              │
              ▼ HTTPS (TCP 443)
[ OpenShift Ingress Router (HAProxy) ]
   ├── Edge TLS Termination (Let's Encrypt Wildcard SSL)
   └── Auto HTTP -> HTTPS 302 Insecure Redirect
              │
              ▼ Internal HTTP (TCP 8080)
[ ClusterIP Service: banking-backend:8080 ]
              │
              ▼ Round-Robin Load Balancing
[ Stateless Application Tier: 3x Pod Replicas ]
   ├── Framework: Python Flask (REST API & Banking Portal UI)
   ├── Scaling: Horizontal Pod Autoscaler (HPA: min 2, max 5, target 70% CPU)
   ├── Reliability: Readiness (/health) and Liveness probes
   ├── Resource Management: Requests (50m CPU, 64Mi RAM) / Limits (250m CPU, 256Mi RAM)
   ├── Observability: Native Prometheus exposition endpoint (/metrics)
   ├── Config Injection: ConfigMap (banking-app-config)
   └── Secret Decoupling: Kubernetes Secret (banking-db-credentials)
              │
              ▼ TCP 5432 (Restricted by Zero-Trust NetworkPolicy)
[ Headless Service: banking-db (CoreDNS Discovery) ]
              │
              ▼ Stable Network Ordinals (0, 1)
[ Stateful Data Tier: 2x Database Nodes (StatefulSet) ]
   ├── banking-db-0 ──► PVC ──► AWS EBS gp3 Volume (1Gi)
   └── banking-db-1 ──► PVC ──► AWS EBS gp3 Volume (1Gi)
```


## 🚀 How I Built it

### 1. Application Containerization
* Developed the core banking API and banking dashboard web interface in Python.
* Packaged the microservice into a container image using multi-stage best practices.
* Implemented standardized `/health` probes and `/metrics` telemetry endpoints.

### 2. High-Availability Stateless Microservices
* Deployed the backend under a Kubernetes `Deployment` controller with **3 replicas** to guarantee zero downtime.
* Implemented strict CPU/Memory resource requests and limits to prevent runaway resource consumption.
* Connected the replicas behind a Kubernetes `ClusterIP` service for load-balanced internal traffic distribution.

### 3. Stateful Storage & Dynamic Cloud Provisioning
* Recognized that database workloads cannot run inside ephemeral deployments.
* Transitioned the database tier to a `StatefulSet` with stable network ordinals (`banking-db-0`, `banking-db-1`).
* Leveraged dynamic volume provisioning backed by **AWS EBS `gp3`** via Kubernetes `PersistentVolumeClaims` (PVCs).
* Verified data survival across simulated disaster recovery tests (deleting pods without losing ledger data).

### 4. Zero-Trust Network Security & Configuration Decoupling
* **ConfigMap (`banking-app-config`):** Decoupled non-sensitive runtime configurations (currency limits, environment flags, log levels).
* **Secret (`banking-db-credentials`):** Injected database credentials at runtime in memory without exposing raw secrets in Git.
* **NetworkPolicy (`allow-backend-to-db`):** Implemented a zero-trust network firewall rule blocking unauthorized namespace traffic and restricting DB port 5432 strictly to pods labeled `app: banking-backend`.

### 5. Ingress, Edge TLS & DNS
* Exposed the application securely using an OpenShift `Route`.
* Configured `termination: edge` to offload TLS processing onto OpenShift's HAProxy layer.
* Enforced `insecureEdgeTerminationPolicy: Redirect` to force all HTTP traffic to HTTPS.

### 6. Automated GitOps CI/CD Pipeline
* Built an automated delivery pipeline using **GitHub Actions**.
* On every commit to `main`, the pipeline runs tests, builds the container image, publishes to Docker Hub, and applies declarative manifests to OpenShift with zero-downtime rolling updates.

---

## 🛠️ Engineering Hurdles & How We Solved Them

| Issue / Failure | Root Cause | Engineering Resolution |
| :--- | :--- | :--- |
| **HTTP 503 "Application Not Available"** | Route port mismatch. The route targeted `targetPort: http`, but the Service defined its port as `8080-tcp`. | Aligned `targetPort: 8080-tcp` declaratively in `backend-route.yaml`. |
| **Certificate Insecurity / SSL Drop** | Initial route lacked edge termination, causing HAProxy to drop HTTPS connections on port 443. | Configured `termination: edge` and automated `Redirect` policies. |
| **Secret Commits Risk** | Risk of leaking raw database passwords in source control. | Sanitized Git manifests with placeholders and managed secrets out-of-band. |
| **HPA `<unknown>` Metric Status** | `metrics-server` requires an initial collection window before computing average CPU percentages across rolling pods. | Allowed metrics buffer window to settle and verified `resources.requests.cpu` presence. |
| **Exec Session Instant Disconnect** | Running non-interactive shell commands (`oc exec pod -- sh`) closed standard input immediately. | Passed `-it` flags (`oc exec -it banking-db-0 -- sh`) to allocate a TTY and keep stdin open. |

---

## 🌐 Live Application Verification

* **Public Web Interface:** `https://banking-backend-daniyaalabbas-dev.apps.rm1.0a51.p1.openshiftapps.com/`
* **JSON API Endpoint:** `/api/balance`
* **Health Check Probe:** `/health`
* **Prometheus Metrics:** `/metrics`

---

### 📁 Repository Structure
```
banking-platform/
├── .github/workflows/
│   └── deploy.yaml               # GitHub Actions CI/CD pipeline
├── k8s/
│   ├── app-configmap.yaml         # Environment and application parameters
│   ├── backend-deployment.yaml    # 3-replica backend microservice
│   ├── backend-hpa.yaml           # Horizontal Pod Autoscaler
│   ├── backend-route.yaml         # Edge TLS Ingress Route
│   ├── backend-service.yaml       # Internal ClusterIP Service
│   ├── banking-db-statefulset.yaml# Stateful database layer
│   ├── banking-pvc.yaml           # AWS gp3 PersistentVolumeClaims
│   ├── db-networkpolicy.yaml      # Zero-trust firewall rules
│   └── db-secret.yaml             # Database credentials template
├── services/
│   └── backend/
│       ├── app.py                # Flask microservice & UI portal
│       ├── Dockerfile            # Container build specification
│       └── requirements.txt      # Python dependencies
└── README.md
```

<img width="1903" height="947" alt="image" src="https://github.com/user-attachments/assets/b539749f-422e-4c3d-b35c-459711f54741" />




