Kubernetes GitOps CI/CD Pipeline

Docker · GitHub Actions · Kubernetes (Kind) · ArgoCD

Overview

This project demonstrates a GitOps-based CI/CD pipeline that automatically builds, stores, and deploys a containerized application to a Kubernetes cluster.

The system integrates:

GitHub Actions for Continuous Integration (CI)

Docker Hub as the container registry

Kubernetes (Kind) as the orchestration platform

ArgoCD as the GitOps Continuous Deployment (CD) controller

The pipeline automatically deploys application updates whenever changes are pushed to the Git repository.

Architecture
Developer
   │
   ▼
GitHub Repository
   │
   ▼
GitHub Actions (CI)
   │
   ├── Build Docker Image
   ├── Run CI Workflow
   └── Push Image → DockerHub
          │
          ▼
Git Repository (K8s Manifests)
          │
          ▼
ArgoCD (GitOps CD Controller)
          │
          ▼
Kubernetes Cluster (Kind)
          │
          ▼
Pods Running Application

Key Principle:

Git is the single source of truth for the Kubernetes cluster state.

Project Structure
project-root
│
├── app.py
├── requirements.txt
├── Dockerfile
│
├── k8s
│   ├── deployment.yaml
│   └── service.yaml
│
└── .github/workflows
    └── pipeline.yml
Kubernetes Deployment
Deployment Manifest

k8s/deployment.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: cicd-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: cicd-app
  template:
    metadata:
      labels:
        app: cicd-app
    spec:
      containers:
      - name: cicd-app
        image: sahilmahat/cicd:latest
        ports:
        - containerPort: 5000
Service Manifest

k8s/service.yaml

apiVersion: v1
kind: Service
metadata:
  name: cicd-service
spec:
  type: NodePort
  selector:
    app: cicd-app
  ports:
  - port: 80
    targetPort: 5000
    nodePort: 30007
Kubernetes Cluster Setup
Create Cluster Using Kind
kind create cluster --name cicd

Verify nodes:

kubectl get nodes
Deploy Application

Apply manifests:

kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

Verify resources:

kubectl get pods
kubectl get svc
kubectl get deployments
Access Application

Because Kind runs inside Docker, direct NodePort access may not work. Use port forwarding:

kubectl port-forward service/cicd-service 8080:80 --address 0.0.0.0

Access the application:

http://<EC2_PUBLIC_IP>:8080
Install ArgoCD

Create namespace:

kubectl create namespace argocd

Install ArgoCD:

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

Verify installation:

kubectl get pods -n argocd
Access ArgoCD Dashboard
kubectl port-forward svc/argocd-server -n argocd 9090:443 --address 0.0.0.0

Open browser:

http://<EC2_PUBLIC_IP>:9090
Retrieve ArgoCD Admin Password
kubectl get secret argocd-initial-admin-secret \
-n argocd \
-o jsonpath="{.data.password}" | base64 -d

Login credentials:

username: admin
password: <retrieved-password>
ArgoCD Deployment Flow

Once configured, ArgoCD continuously monitors the Git repository.

If Kubernetes manifests change:

Git change detected
      ↓
ArgoCD syncs manifests
      ↓
kubectl apply executed
      ↓
Kubernetes rolling update triggered
CI Pipeline (GitHub Actions)

The CI workflow performs:

Code checkout

Docker image build

Push image to DockerHub

Example image:

docker.io/sahilmahat/cicd
Kubernetes Rolling Updates

When a new image version is deployed:

Old Pod (v1)
     ↓
New Pod (v2) created
     ↓
Health check
     ↓
Traffic shifted
     ↓
Old Pod terminated

This ensures zero-downtime deployments.

Debugging Commands

Check pods:

kubectl get pods

View logs:

kubectl logs <pod-name>

Describe resources:

kubectl describe deployment cicd-app
kubectl describe pod <pod-name>
Restart Deployment (if needed)
kubectl rollout restart deployment cicd-app
Key Concepts Demonstrated

Containerization with Docker

CI automation with GitHub Actions

Kubernetes container orchestration

GitOps deployment model using ArgoCD

Declarative infrastructure via Kubernetes manifests

Rolling updates and high availability

Future Improvements

Possible extensions for production-grade environments:

Helm charts for Kubernetes packaging

Kubernetes Ingress for external access

Monitoring with Prometheus & Grafana

Centralized logging (ELK or Loki)

Automated image versioning and tagging

Multi-environment deployments (dev / staging / production)

License

This project is intended for learning and demonstration of modern DevOps CI/CD practices.
