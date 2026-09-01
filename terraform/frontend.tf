# Note: NEXT_PUBLIC_API_BASE_URL is NOT set here as a container env var — it's
# a client component fetch URL, so Next.js inlines it into the JS bundle at
# `next build` time (see frontend/Dockerfile's build arg). Setting it here
# would have no effect on the already-built image.
resource "google_cloud_run_v2_service" "frontend" {
  depends_on = [google_project_service.apis]

  name                = "zenflow-frontend"
  project             = var.project_id
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.frontend_image
      ports {
        container_port = 8080
      }
    }
  }
}

resource "google_cloud_run_v2_service_iam_member" "frontend_public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.frontend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
