terraform {
  required_version = ">= 1.6"

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }

  # Local state to start. Migrate to a GCS backend (see README.md) once this
  # needs to be shared or you want state stored more durably.
}

provider "google" {
  project = var.project_id
  region  = var.region
}
