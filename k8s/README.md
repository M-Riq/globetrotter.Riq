# Kubernetes manifests

Apply in this order:

```bash
kubectl apply -f namespace.yaml
kubectl apply -f configmap.yaml
# Edit secrets.yaml with real values first, or create the Secret via
# `kubectl create secret generic ...` as documented inside the file.
kubectl apply -f secrets.yaml
kubectl apply -f auth-service.yaml
kubectl apply -f user-service.yaml
kubectl apply -f destination-service.yaml
kubectl apply -f recommendation-service.yaml
kubectl apply -f itinerary-service.yaml
kubectl apply -f admin-service.yaml
kubectl apply -f api-gateway.yaml
kubectl apply -f ingress.yaml
```

Or simply `kubectl apply -f .` (namespace/configmap/secrets get
applied first alphabetically-ish, but Kubernetes retries transient
ordering issues on its own for a first apply; for CI pipelines the
explicit order above is safer).

## What's here

- `namespace.yaml` -- the `globetrotter` namespace everything lives in.
- `configmap.yaml` -- shared, non-secret config (service URLs, CORS).
- `secrets.yaml` -- **template only**. Replace values or generate via
  `kubectl create secret generic` before applying in a real cluster.
- One `<service>.yaml` per microservice -- a Deployment + Service
  (+ PersistentVolumeClaim for the four services still backed by
  JSON storage: auth, user, destination, itinerary).
- `ingress.yaml` -- routes external HTTPS traffic to the API Gateway
  only; every other service stays internal (`ClusterIP`).

## Notes / next steps for a production cluster

- Build and push each service's image (`globetrotter/<service>:latest`
  in these manifests) to a real registry, and update the `image:`
  field accordingly -- these manifests assume images are already
  available to the cluster.
- The JSON-file + PVC storage works for a small deployment but will
  not survive multiple replicas writing concurrently in a fully safe
  way at scale; migrating each stateful service's `JSONStorage` to a
  `PostgresStorage` (same `BaseStorage` interface, see
  `common/storage/`) removes this limitation without touching any
  Service-layer code.
- Add a `HorizontalPodAutoscaler` per service once real traffic
  patterns are known.
- Consider a service mesh (or at least mTLS between services) before
  handling real user data in production.
