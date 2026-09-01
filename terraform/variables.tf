variable "project_id" {
  description = "GCP project ID to deploy into."
  type        = string
}

variable "region" {
  description = "GCP region for Artifact Registry and Cloud Run."
  type        = string
  default     = "us-central1"
}

variable "backend_image" {
  description = <<-EOT
    Full Artifact Registry image reference for the backend, e.g.
    us-central1-docker.pkg.dev/PROJECT/zenflow/backend:TAG.
    Build and push it (see README.md) before the first apply that targets
    google_cloud_run_v2_service.backend. Left blank so the initial apply
    (Artifact Registry only) doesn't require a value yet.
  EOT
  type        = string
  default     = ""
}

variable "frontend_image" {
  description = <<-EOT
    Full Artifact Registry image reference for the frontend, e.g.
    us-central1-docker.pkg.dev/PROJECT/zenflow/frontend:TAG.
    Must be built with --build-arg NEXT_PUBLIC_API_BASE_URL=<backend_url>
    (see README.md) — that value is compiled into the JS bundle, so this
    image can only be built after the backend service exists. Left blank so
    earlier applies don't require a value yet.
  EOT
  type        = string
  default     = ""
}
