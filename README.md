# CLO835 Final Project – Kubernetes Application Deployment on AWS

## 📌 Project Overview
This project demonstrates the deployment of a containerized Flask web application on **Amazon EKS (Elastic Kubernetes Service)**. The application integrates with **MySQL for data storage** and **Amazon S3 for dynamic background images**, showcasing a complete cloud-native architecture using AWS services and Kubernetes.

---

## 👨‍💻 Group Members
- Maharshi Mehta – maharshimehta.me@gmail.com  
- Ghufran Ataie – ghufranataie@hotmail.com  
- Vibha Thakkar – thakkarvibha20@gmail.com  

---

## 🏗️ Architecture
The application uses the following components:

- Amazon EKS – 

The application integrates:
- **MySQL** for persistent data storage  
- **Amazon S3** for dynamic background images Kubernetes cluster for orchestration  
- Docker – Containerized Flask application  
- Amazon ECR – Container image storage  
- MySQL (Kubernetes Deployment) – Backend database  
- Persistent Volume (EBS) – Data persistence  
- Amazon S3 – Dynamic background image storage  
- ConfigMap & Secret – Configuration and credentials  
- LoadBalancer Service – Public access to the app  

---

## 📁 Repository Structure


final-project/
├── app/
│ ├── app.py
│ ├── Dockerfile
│ ├── requirements.txt
│ ├── templates/
│ └── .github/workflows/
│
├── manifests/
│ ├── configmap.yaml
│ ├── secret.yaml
│ ├── pvc.yaml
│ ├── mysql-deployment.yaml
│ ├── mysql-service.yaml
│ ├── flask-deployment.yaml
│ ├── flask-service.yaml


---

## 🚀 Features
- Add employee records  
- Retrieve employee information  
- Persistent storage using Kubernetes PVC (EBS)  
- Dynamic background image loading from S3  
- Containerized deployment using Docker and Kubernetes  

---

## ⚙️ Deployment Steps (Summary)

### Build Docker Image
```bash
docker build -t clo835-final-app .


Push to Amazon ECR

docker tag clo835-final-app:latest <ECR_REPO_URI>
docker push <ECR_REPO_URI>

Deploy to Kubernetes
kubectl apply -f manifests/

🚀 CI/CD Pipeline
GitHub Actions automatically:
Builds Docker image
Pushes to Amazon ECR
Triggers deployment workflow





Verify Deployment
kubectl get pods -n final
kubectl get svc -n final
🧪 Testing
Application Functionality
Add employee
Retrieve employee
Persistence Test
Delete MySQL pod
Verify data remains intact
S3 Integration
Update background image in S3
Modify ConfigMap
Restart Flask deployment
Verify updated UI
🛠️ Challenges Faced
EBS volume provisioning issue (resolved using EBS CSI driver)
MySQL CrashLoopBackOff issue (resolved using fresh PVC and subPath)
ConfigMap updates not reflecting immediately (resolved via pod restart)
📜 Logs Verification

The application logs confirm successful S3 integration:

Background image location: s3://<bucket-name>/<image>
📊 AWS Services Used
Amazon EKS
Amazon EC2
Amazon ECR
Amazon S3
Amazon EBS
IAM
📌 Conclusion

This project demonstrates a complete cloud-native deployment using Kubernetes and AWS. It highlights container orchestration, persistent storage, and dynamic configuration in a scalable environment.


---

## ✅ Now run:

```bash


