resource "kubernetes_deployment" "temporal_preview" {
  metadata {
    name      = "temporal-deployment"
    namespace = "default"
    labels = {
      app = "temporal"
    }
  }

  spec {
    replicas = 1
    selector {
      match_labels = {
        app = "temporal"
      }
    }
    template {
      metadata {
        labels = {
          app = "temporal"
        }
      }
      spec {
        container {
          name  = "temporal-server"
          image = "temporalio/auto-setup:latest"
          port {
            container_port = 7233
          }
        }

        container {
          name  = "temporal-ui"
          image = "temporalio/ui:latest"
          port {
            container_port = 8080
          }
        }

        container {
          name  = "python-worker"
          image = var.kube_deployment_image
          command = ["python3", "/app/temporal_server.py"]
          env {
            name  = "TEMPORAL_SERVER"
            value = "temporal-service:7233"
          }
        }
      }
    }
  }
}

resource "kubernetes_service" "temporal_service" {
  metadata {
    name      = "temporal-service"
    namespace = "default"
  }

  spec {
    selector = {
      app = "temporal"
    }

    port {
      protocol    = "TCP"
      port        = 7233
      target_port = 7233
    }

    port {
      protocol    = "TCP"
      port        = 8080
      target_port = 8080
    }

    type = "LoadBalancer"
  }
}
