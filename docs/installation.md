# Installation et mise en service

## 1. Préparer le cluster ClassLab

Depuis la racine de ClassLab :

```bash
vagrant up
vagrant ssh VM1
ansible-playbook /vagrant/ansible/playbooks/k3s-deploiement.yaml
sudo /vagrant/setup-helm-kubectl-vm1.sh
kubectl get nodes
```

Les nœuds `vm2` et `vm3` doivent être `Ready` avant de continuer.

## 2. Tester le projet en local

```bash
cd usine-logicielle
make install
make validate
```

La pile locale complète se lance avec :

```bash
docker compose up --build -d
docker compose ps
```

L'application répond sur le port 8000, Prometheus sur 9090 et Grafana sur 3000. Les identifiants Grafana de démonstration sont `admin` / `classlab`, sauf surcharge dans `.env`.

## 3. Tester l'image

```bash
docker build -t factory-api:local .
docker run --rm -d --name factory-api -p 8000:8000 factory-api:local
./scripts/smoke-test.sh http://127.0.0.1:8000
docker stop factory-api
```

## 4. Connecter GitLab à K3s

Dans GitLab, ouvrir **Operate > Kubernetes clusters**, créer l'agent `k3s`, puis exécuter dans le cluster la commande Helm proposée. Adapter `.gitlab/agents/k3s/config.yaml` au chemin réel du projet et renseigner `KUBE_CONTEXT` dans **Settings > CI/CD > Variables**.

## 5. Publier

```bash
git init
git add .
git commit -m "feat: deliver ClassLab software factory"
git branch -M main
git remote add origin git@gitlab.com:<groupe>/<projet>.git
git push -u origin main
```

Créer ensuite la branche `develop`. Son premier push déclenche automatiquement le staging. Le job production reste manuel sur `main`.

## 6. Installer la supervision

Suivre les commandes de la section « Supervision » du README. Vérifier ensuite :

```bash
kubectl -n monitoring get pods
kubectl -n factory get pods
kubectl -n monitoring port-forward svc/prometheus-server 9090:80
```

Dans Prometheus, la requête `up{job="factory-api"}` doit retourner `1` pour chaque pod.
