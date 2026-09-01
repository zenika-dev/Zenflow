resource "google_cloud_run_v2_service" "backend" {
  depends_on = [google_project_service.apis]

  name                = "zenflow-backend"
  project             = var.project_id
  location            = var.region
  deletion_protection = false
  ingress             = "INGRESS_TRAFFIC_ALL"

  template {
    containers {
      image = var.backend_image
      ports {
        container_port = 8080
      }
    }
  }
}

# Testing-phase: open to the public internet with no auth. Tighten this (and
# the backend's CORS allow_origins) once the frontend URL is finalized.
resource "google_cloud_run_v2_service_iam_member" "backend_public" {
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.backend.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
