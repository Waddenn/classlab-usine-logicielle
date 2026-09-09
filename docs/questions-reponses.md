# Questions et réponses possibles

**Pourquoi un déploiement manuel en production ?**
Le pipeline automatise l'opération, mais conserve une validation humaine avant l'environnement sensible. Le staging reste automatique pour fournir un retour rapide.

**Pourquoi taguer avec le SHA plutôt qu'avec `latest` ?**
Le SHA identifie un contenu précis et permet l'audit ou le rollback. `latest` change avec le temps.

**Que se passe-t-il si un test échoue ?**
GitLab arrête le pipeline avant la construction et le déploiement. L'ancien ReplicaSet continue de servir le trafic.

**Différence entre readiness et liveness ?**
La readiness décide si un pod reçoit du trafic. La liveness décide si Kubernetes doit redémarrer le conteneur.

**Pourquoi deux replicas ?**
Ils permettent un rolling update sans indisponibilité et tolèrent la perte d'un pod. Le lab n'assure toutefois pas une haute disponibilité complète du control plane.

**Comment revenir en arrière ?**
`kubectl rollout undo` restaure le ReplicaSet précédent, puis un smoke test confirme le retour du service.

**Comment les secrets sont-ils protégés ?**
Le pipeline utilise les variables protégées de GitLab et l'agent Kubernetes. Aucun kubeconfig ni mot de passe n'est versionné.

**Pourquoi Prometheus en mode pull ?**
Prometheus contrôle la fréquence de collecte et identifie aussi une cible qui ne répond plus. Grafana interroge ensuite les séries avec PromQL.

**Le projet est-il prêt pour la production ?**
Il démontre les mécanismes attendus, mais un système réel doit ajouter TLS, politiques de sauvegarde, gestion externe des secrets et haute disponibilité du cluster.
