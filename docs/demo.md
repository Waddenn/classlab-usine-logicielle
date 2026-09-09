# Démonstration de 5 minutes

## Préparation

- pipeline `main` vert et job production exécuté ;
- onglets ouverts : pipeline GitLab, application, Grafana ;
- terminal dans ce dossier avec `kubectl` configuré ;
- dashboard Grafana sur les 15 dernières minutes.

## 0:00 à 1:15 — pipeline

Montrer les stages et ouvrir le job de tests. Pointer le rapport de couverture, puis le scan de l'image. Expliquer que le SHA relie le commit, l'image et le déploiement.

## 1:15 à 2:20 — déploiement

```bash
kubectl -n factory get deployment,pods,service,ingress,hpa
curl -s http://factory.192.168.56.12.nip.io/api/v1/info
```

La réponse affiche `production` et la version. Montrer que deux pods servent l'application.

## 2:20 à 3:15 — rolling update

Dans GitLab, relancer le job production d'un nouveau commit ou utiliser une image déjà publiée. Pendant le rollout :

```bash
kubectl -n factory get pods -w
```

Le nouveau pod devient prêt avant la suppression de l'ancien grâce à `maxUnavailable: 0`.

## 3:15 à 4:15 — supervision

```bash
./scripts/demo.sh
```

Rafraîchir Grafana et montrer le trafic, la latence p95 et le taux d'erreurs.

## 4:15 à 5:00 — sécurité et conclusion

Montrer brièvement les champs `runAsNonRoot`, `readOnlyRootFilesystem` et `drop: ALL` du Deployment. Conclure : un commit validé devient une image analysée, déployée de façon contrôlée et supervisée.

## Plan B hors ligne

Si GitLab ou le cluster est indisponible, utiliser les captures du pipeline préparées avant l'oral, lancer les tests locaux et présenter les manifestes générés :

```bash
make test
kubectl kustomize k8s/overlays/production | less
```
