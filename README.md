Set-up minikube
-----------------------------------------
```commandline
docker network create pings

docker build -f ping.Containerfile -t ping-server .
docker run --name pingserver --network pings -d -p 127.0.0.1:8002:8080 ping-server

docker build -f pingping.Containerfile -t pingping-server .
docker run --name pingpingserver --network pings -d -p 127.0.0.1:8003:8081 pingping-server

minikube start --cpus=4 --memory=8g --addons=ingress
```

https://github.com/kubernetes/minikube/issues/18021#issuecomment-1953589210
```commandline
docker image save -o ~/Desktop/ping-server.tar ping-server
minikube image load ~/Desktop/ping-server.tar
docker image save -o ~/Desktop/pingping-server.tar pingping-server
minikube image load ~/Desktop/pingping-server.tar
```

Separate Pod/Deployment/Services
-----------------------------------------
https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ping-server-deployment
  namespace: manstis
  labels:
    app: ping-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ping-server
  template:
    metadata:
      labels:
        app: ping-server
    spec:
      containers:
      - name: ping-server
        image: ping-server
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pingping-server-deployment
  namespace: manstis
  labels:
    app: pingping-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: pingping-server
  template:
    metadata:
      labels:
        app: pingping-server
    spec:
      containers:
      - name: pingping-server
        image: pingping-server
        imagePullPolicy: Never
        ports:
        - containerPort: 8081
```

https://kubernetes.io/docs/concepts/services-networking/service/
```yaml
kind: Service
apiVersion: v1
metadata:
  name: ping-server-service
  namespace: manstis
  labels:
    app: ping-server
spec:
  ports:
    - protocol: TCP
      port: 8080
      targetPort: 8080
      nodePort: 30220
  selector:
    app: ping-server
  type: NodePort
```

```yaml
kind: Service
apiVersion: v1
metadata:
  name: pingping-server-service
  namespace: manstis
  labels:
    app: pingping-server
spec:
  ports:
    - protocol: TCP
      port: 8081
      targetPort: 8081
      nodePort: 30221
  selector:
    app: pingping-server
  type: NodePort
```

```commandline
minikube service ping-server-service --url -n manstis

minikube service pingping-server-service --url -n manstis
```

Sidecar Container
-----------------------------------------
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ping-server-deployment
  namespace: manstis
  labels:
    app: ping-server
spec:
  replicas: 1
  selector:
    matchLabels:
      app: ping-server
  template:
    metadata:
      labels:
        app: ping-server
    spec:
      containers:
      - name: ping-server
        image: ping-server
        imagePullPolicy: Never
        ports:
        - containerPort: 8080
      - name: pingping-server
        image: pingping-server
        imagePullPolicy: Never
        ports:
          - containerPort: 8081
```

```yaml
kind: Service
apiVersion: v1
metadata:
  name: ping-server-service
  namespace: manstis
  labels:
    app: ping-server
spec:
  ports:
    - protocol: TCP
      port: 8081
      targetPort: 8081
      nodePort: 30220
  selector:
    app: ping-server
  type: NodePort
```
https://stackoverflow.com/questions/52133186/how-do-i-talk-to-a-pod-from-sidecar-container-in-kubernetes

[debugging]
```
kubectl exec -it <pod-name> -c <container-name> -n manstis -- /bin/bash
```
