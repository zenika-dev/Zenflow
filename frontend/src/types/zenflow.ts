// Mirrors zenflow.routers.schemas / zenflow.core.models on the backend.

export interface FrameworkOption {
  label: string;
  arch_file: string;
  doc_file: string;
}

export interface StackCatalog {
  backend: Record<string, FrameworkOption[]>;
  frontend: Record<string, FrameworkOption[]>;
}

export type AssistantId = "claude" | "copilot" | "opencode";

export interface ToolSelection {
  copilot: boolean;
  opencode: boolean;
  claude: boolean;
}

export interface GuidelineSelection {
  backend_arch_file: string;
  backend_doc_file: string;
  frontend_arch_file: string;
  frontend_doc_file: string;
  include_conventions: boolean;
}
