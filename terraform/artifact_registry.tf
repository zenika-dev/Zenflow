resource "google_artifact_registry_repository" "zenflow" {
  depends_on = [google_project_service.apis]

  project       = var.project_id
  location      = var.region
  repository_id = "zenflow"
  format        = "DOCKER"
  description   = "Container images for the Zenflow frontend and backend."
}
