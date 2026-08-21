"use client";

import { useEffect, useState } from "react";
import { getStacks } from "@/api/stacks";
import { AssistantPicker } from "@/components/AssistantPicker";
import { LanguageStackPicker } from "@/components/LanguageStackPicker";
import { Button } from "@/components/ui/Button";
import type { AssistantId, GuidelineSelection, StackCatalog, ToolSelection } from "@/types/zenflow";

export default function Home() {
  const [catalog, setCatalog] = useState<StackCatalog | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);
  const [assistant, setAssistant] = useState<AssistantId>("claude");
  const [backendArchFile, setBackendArchFile] = useState("");
  const [frontendArchFile, setFrontendArchFile] = useState("");

  useEffect(() => {
    getStacks()
      .then(setCatalog)
      .catch((err) => setLoadError(err instanceof Error ? err.message : "Failed to load stacks"));
  }, []);

  function handleReset() {
    setAssistant("claude");
    setBackendArchFile("");
    setFrontendArchFile("");
  }

  function handleGenerate() {
    const tools: ToolSelection = {
      claude: assistant === "claude",
      copilot: assistant === "copilot",
      opencode: assistant === "opencode",
    };
    const guidelines: GuidelineSelection = {
      backend_arch_file: backendArchFile,
      backend_doc_file: "",
      frontend_arch_file: frontendArchFile,
      frontend_doc_file: "",
      include_conventions: true,
    };
    // TODO: wire up to POST /init once the confirm modal (and its target_path input) is built.
    console.log("Generate (stub)", { tools, guidelines });
  }

  return (
    <div className="min-h-screen bg-[linear-gradient(135deg,#fdf1f4_0%,#f6eefb_55%,#eef1fb_100%)] text-[#161217]">
      <div className="mx-auto max-w-[1120px] px-6 pt-14 pb-8">
        <div className="mb-2 text-[56px] leading-none font-extrabold tracking-[-0.01em] text-[#c81c5c]">
          ZENFLOW
        </div>
        <h1 className="mb-4 max-w-[40ch] text-lg leading-snug font-bold text-[#5c5560]">
          Generate agent skills for your AI assistant.
        </h1>
        <p className="mb-6 max-w-[56ch] text-base leading-relaxed text-[#5c5560]">
          Pick an assistant, a stack, and the skills you want your agents to carry — then export the files
          it reads on day one.
        </p>

        <div className="mt-7 grid grid-cols-1 gap-6 rounded-[24px] bg-white p-6 shadow-[0_20px_40px_-20px_rgba(120,40,80,0.25)] sm:grid-cols-2">
          <AssistantPicker selected={assistant} onSelect={setAssistant} />
          {catalog ? (
            <LanguageStackPicker
              catalog={catalog}
              backendArchFile={backendArchFile}
              frontendArchFile={frontendArchFile}
              onSelectBackend={setBackendArchFile}
              onSelectFrontend={setFrontendArchFile}
            />
          ) : (
            <div className="text-sm text-[#8a8290]">
              {loadError ? `Couldn't load stacks: ${loadError}` : "Loading stacks…"}
            </div>
          )}
        </div>
      </div>

      <div className="border-t-[1.5px] border-[#e9dde3]">
        <div className="mx-auto flex max-w-[1120px] items-center justify-end gap-4 px-6 py-5">
          <Button variant="secondary" onClick={handleReset}>
            Reset
          </Button>
          <Button variant="primary" onClick={handleGenerate}>
            Generate
          </Button>
        </div>
      </div>
    </div>
  );
}
