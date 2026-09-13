# CloudForge

**CloudForge** is a cloud-native DevOps project focused on building an automated, observable, and recoverable deployment environment for containerized applications running on Kubernetes.

The project is designed around the infrastructure and operational lifecycle of an application rather than application features.

Its goal is to demonstrate practical experience with:

* Kubernetes orchestration
* Docker containerization
* CI/CD automation
* Infrastructure as Code
* AWS cloud infrastructure
* Monitoring and observability
* Centralized logging
* Deployment health checks
* Failure investigation
* Rollbacks and recovery
* Linux-based troubleshooting

> **Project Status:** In development. Features described in this documentation represent the target architecture.

---

## 1. Project Goals

CloudForge aims to answer a practical DevOps question:

> How can an application move safely and automatically from source code to a monitored Kubernetes environment?

The intended workflow is:

```text
Developer
    |
    | git push / pull request
    v
GitHub
    |
    v
GitHub Actions
    |
    +----> Lint & Test
    |
    +----> Build Docker Image
    |
    +----> Push Image to Registry
    |
    v
Kubernetes
    |
    +----> Deploy Application
    +----> Run Health Checks
    +----> Rolling Updates
    +----> Resource Management
    |
    v
Observability
    |
    +----> Prometheus
    +----> Grafana
    +----> Loki
```

The application itself intentionally remains simple. The primary engineering focus is the infrastructure surrounding it.

---

## 2. Technology Stack

### Infrastructure & DevOps

| Technology     | Purpose                           |
| -------------- | --------------------------------- |
| Kubernetes     | Container orchestration           |
| Docker         | Application containerization      |
| Terraform      | Infrastructure as Code            |
| AWS            | Cloud infrastructure              |
| GitHub Actions | CI/CD automation                  |
| Git & GitHub   | Version control and collaboration |

### Observability

| Technology | Purpose                                   |
| ---------- | ----------------------------------------- |
| Prometheus | Metrics collection                        |
| Grafana    | Metrics visualization and dashboards      |
| Loki       | Centralized application/container logging |

### Demo Application

| Technology | Purpose                 |
| ---------- | ----------------------- |
| FastAPI    | Backend API             |
| PostgreSQL | Persistent data storage |

---

## 3. Target Architecture

```text
                        Developer
                            |
                         Git Push
                            |
                            v
                         GitHub
                            |
                            v
                     GitHub Actions
                  /        |         \
              Tests    Docker Build   Validation
                          |
                          v
                   Container Registry
                          |
                          v
                +---------------------+
                |     Kubernetes      |
                |                     |
                |   +-------------+   |
                |   | FastAPI API |   |
                |   +------+------+   |
                |          |          |
                |   +------v------+   |
                |   | PostgreSQL  |   |
                |   +-------------+   |
                +----------+----------+
                           |
                  +--------+--------+
                  |                 |
                  v                 v
             Prometheus           Loki
                  |                 |
                  +--------+--------+
                           |
                           v
                        Grafana
```

Terraform is responsible for provisioning the required cloud infrastructure.

Kubernetes is responsible for application deployment, service discovery, configuration, resource management, health checking, and deployment lifecycle management.

---

## 4. CI/CD Pipeline

CloudForge uses GitHub Actions to automate the software delivery lifecycle.

### Pull Request Pipeline

A pull request should trigger:

```text
Pull Request
     |
     v
Code Checkout
     |
     v
Dependency Installation
     |
     v
Linting
     |
     v
Automated Tests
     |
     v
Docker Build Validation
```

The purpose is to prevent invalid changes from reaching the deployment pipeline.

### Deployment Pipeline

Changes merged into the deployment branch will eventually follow:

```text
Merge
  |
  v
Run Tests
  |
  v
Build Docker Image
  |
  v
Push Image
  |
  v
Deploy to Kubernetes
  |
  v
Wait for Rollout
  |
  v
Health Validation
```

A failed health validation should prevent a broken deployment from being treated as successful.

---

## 5. Kubernetes

Kubernetes is the central component of CloudForge.

The project will cover the following concepts:

### Deployments

Deployments manage application replicas and rolling updates.

### Services

Services provide stable network access to application pods.

### ConfigMaps

Non-sensitive application configuration is separated from container images.

### Secrets

Sensitive configuration must not be committed directly into the repository.

### Resource Requests and Limits

Containers receive explicit CPU and memory configuration to improve scheduling and prevent uncontrolled resource consumption.

### Health Probes

CloudForge distinguishes between:

**Readiness probes**

Determine whether a container is ready to receive traffic.

**Liveness probes**

Determine whether a running container should be restarted.

### Rolling Updates

New application versions should be introduced gradually rather than replacing every running instance simultaneously.

---

## 6. Infrastructure as Code

Cloud infrastructure will be managed through Terraform rather than manually created resources.

Target structure:

```text
terraform/
├── modules/
│   ├── network/
│   ├── cluster/
│   └── database/
│
├── environments/
│   ├── staging/
│   └── production/
│
├── providers.tf
├── variables.tf
└── outputs.tf
```

The infrastructure layer is intended to cover:

* networking
* security configuration
* compute/Kubernetes infrastructure
* container registry
* database infrastructure
* IAM permissions


---

## 7. Observability

Deploying an application successfully does not guarantee that it is healthy.

CloudForge therefore includes an observability layer.

### Prometheus

Prometheus will collect metrics related to application and Kubernetes health.

Potential metrics include:

* CPU usage
* memory usage
* pod availability
* request rate
* request latency
* HTTP error rate

### Grafana

Grafana will visualize collected metrics through dashboards.

A target dashboard should make it possible to quickly answer:

* Is the application available?
* Are all expected pods healthy?
* Is CPU or memory consumption abnormal?
* Has the HTTP error rate increased?
* Did application behavior change after a deployment?

### Loki

Loki will provide centralized log aggregation.

The objective is to correlate metrics with application/container logs during incident investigation.

---

## 8. Failure Investigation

CloudForge intentionally includes failure scenarios.

A DevOps environment should demonstrate not only successful deployment but also the ability to investigate failures.

Planned scenarios include:

```text
failure-scenarios/
├── crash-loop.md
├── failed-readiness-probe.md
├── invalid-image.md
├── configuration-error.md
├── database-failure.md
└── failed-deployment.md
```

Each scenario should document:

```text
Symptom
   |
   v
Observation
   |
   v
Investigation
   |
   v
Root Cause
   |
   v
Resolution
   |
   v
Verification
   |
   v
Prevention
```

Example troubleshooting tools may include:

```bash
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl get events
kubectl rollout status deployment/<deployment>
kubectl rollout history deployment/<deployment>
```

---

## 9. Deployment Recovery

CloudForge will demonstrate how failed releases can be identified and recovered.

Target scenario:

```text
Version 1
   |
   v
Healthy Deployment
   |
   v
Deploy Version 2
   |
   v
Health Check Failure
   |
   v
Investigate
   |
   v
Rollback
   |
   v
Version 1 Restored
```

Kubernetes rollout history and rollback mechanisms will be explored as part of this process.

---

## 10. Optimization

Optimization will be treated as an engineering exercise rather than a claim.

Potential areas include:

### Docker

* smaller images
* improved layer caching
* `.dockerignore`
* dependency caching
* appropriate base images
* non-root execution

### CI/CD

* dependency caching
* avoiding unnecessary builds
* separating validation from deployment
* parallelizing independent jobs where useful

### Kubernetes

* CPU requests
* memory requests
* CPU limits
* memory limits
* replica configuration

Before/after measurements will be documented whenever an optimization produces a measurable result.

No performance numbers will be claimed without measurement.

---

## 11. Linux & Troubleshooting

The project  provide practical exposure to Linux-based environments.

Relevant areas include:

* processes
* filesystem and disk usage
* permissions
* networking
* environment variables
* logs
* services
* resource utilization

Typical diagnostic commands may include:

```bash
ps
top
df
du
free
ss
curl
grep
chmod
chown
journalctl
systemctl
```

---

## 12. Repository Structure

Target repository structure:

```text
cloud-forge/
│
├── app/
│   ├── api/
│   └── tests/
│
├── kubernetes/
│   ├── base/
│   └── overlays/
│       ├── staging/
│       └── production/
│
├── terraform/
│   ├── modules/
│   └── environments/
│
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── loki/
│
├── scripts/
│   ├── deploy.sh
│   ├── health-check.sh
│   └── rollback.sh
│
├── failure-scenarios/
│
├── docs/
│   ├── architecture.md
│   ├── ci-cd.md
│   ├── kubernetes.md
│   ├── infrastructure.md
│   ├── observability.md
│   └── failure-recovery.md
│
├── .github/
│   └── workflows/
│
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 13. Implementation Roadmap followed!

### Phase 1 — Application & Docker

* Build minimal FastAPI application
* Connect PostgreSQL
* Add automated tests
* Create Dockerfile
* Create Docker Compose development environment
* Validate container networking

### Phase 2 — CI

* Configure GitHub Actions
* Run tests on pull requests
* Build Docker image
* Validate failed builds/tests
* Add image publishing

### Phase 3 — Kubernetes

* Deploy application
* Configure Services
* Add ConfigMaps/Secrets
* Add readiness probes
* Add liveness probes
* Configure resource requests/limits
* Test rolling updates

### Phase 4 — Terraform & AWS

* Define infrastructure
* Configure networking
* Configure required IAM permissions
* Provision cloud resources
* Deploy application environment

### Phase 5 — Observability

* Install/configure Prometheus
* Configure Grafana
* Build dashboards
* Add centralized logging
* Validate metrics during deployments

### Phase 6 — Reliability

* Simulate pod failures
* Simulate configuration failures
* Test failed deployments
* Perform rollbacks
* Document investigations

### Phase 7 — Optimization & Documentation

* Analyze Docker image
* Analyze CI/CD execution
* Review Kubernetes resources
* Record genuine before/after measurements
* Complete architecture documentation
* Document engineering decisions
* Add screenshots and diagrams

---

## 14. Engineering Principles

CloudForge follows several principles:

**Automate repetitive operations.**

If a deployment step can be reliably automated, it should not depend on repeated manual execution.

**Infrastructure should be reproducible.**

Infrastructure configuration belongs in version-controlled Infrastructure as Code.

**A deployment is not successful merely because a container started.**

Health validation and observability are part of deployment.

**Failures should be diagnosable.**

Metrics, logs, Kubernetes events, and documented troubleshooting procedures should make failures understandable.

**Recovery should be tested.**

Rollback procedures should be exercised before they are needed.

**Measure before claiming optimization.**

Performance improvements should be supported by actual measurements.

