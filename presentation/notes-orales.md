# Notes orales — 10 minutes

## 1. Usine logicielle ClassLab — 30 s

Nous avons construit une chaîne complète pour supprimer les builds manuels et rendre chaque livraison traçable. L'application sert de témoin ; la valeur principale se trouve dans le processus automatisé.

## 2. Point de départ et objectifs — 1 min

Le besoin décrit cinq faiblesses : opérations manuelles, tests irréguliers, environnements hétérogènes, sécurité insuffisante et supervision limitée. Notre réponse associe une preuve concrète à chaque faiblesse : rapports de tests, image immuable, manifestes versionnés, scan et métriques.

## 3. Architecture — 1 min 30

Le développeur pousse sur GitLab. Les jobs de qualité s'exécutent avant la construction. Docker publie une image marquée par le SHA. Trivy bloque les vulnérabilités corrigibles de gravité haute ou critique. L'agent GitLab transmet le déploiement à K3s. Prometheus collecte les métriques et Grafana les présente.

## 4. Pipeline GitLab CI — 1 min 30

Le lint et la validation Kubernetes commencent tôt. Les tests produisent des rapports intégrés à GitLab. Une image n'est publiée qu'après ces contrôles. `develop` alimente automatiquement le staging. `main` ouvre une validation manuelle avant production, ce qui protège l'environnement sensible.

## 5. Déploiement Kubernetes — 1 min 15

Kustomize évite de recopier les mêmes manifestes. La production utilise deux replicas. Le rolling update interdit toute indisponibilité planifiée. Les readiness probes contrôlent l'entrée dans le trafic ; les liveness probes redémarrent un processus bloqué. Le HPA peut monter à cinq replicas.

## 6. Sécurité — 1 min

Le conteneur utilise un UID non privilégié, perd toutes ses capabilities Linux et ne peut pas écrire dans son système de fichiers. Kubernetes ne monte pas automatiquement de jeton de service account. La NetworkPolicy limite le trafic aux composants qui doivent joindre l'API. Aucun secret de cluster n'entre dans Git.

## 7. Supervision — 1 min

L'application expose le nombre de requêtes et leur latence. Le dashboard montre les signaux utiles : débit, erreurs et latence. Deux règles alertent sur l'indisponibilité et le taux de 5xx. Le monitoring vérifie ainsi le service utilisateur, pas uniquement l'état des machines.

## 8. Démonstration — 45 s

La démonstration prouve la continuité : pipeline vert, image SHA, deux pods prêts, version renvoyée par l'API, puis apparition du trafic dans Grafana.

## 9. Limites et suite — 45 s

Le lab reste en HTTP et ne contient pas de données persistantes. Une version d'entreprise ajouterait TLS, gestion externe des secrets, signature des images, SAST et sauvegardes. Ces extensions ne changent pas l'architecture générale.

## 10. Conclusion — 45 s

Le projet transforme un commit en livraison contrôlée. Les tests réduisent les régressions, l'image immuable assure la traçabilité, Kubernetes fiabilise le déploiement et la supervision ferme la boucle d'exploitation.
