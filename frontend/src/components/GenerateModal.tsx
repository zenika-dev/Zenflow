import { useState } from "react";
import { initProject } from "@/api/init";
import { Button } from "@/components/ui/Button";
import type { GuidelineSelection, InitResponse, ToolSelection } from "@/types/zenflow";

type Phase = "input" | "loading" | "success" | "error";

interface GenerateModalProps {
  open: boolean;
  tools: ToolSelection;
  guidelines: GuidelineSelection;
  onClose: () => void;
}

export function GenerateModal({ open, tools, guidelines, onClose }: GenerateModalProps) {
  const [targetPath, setTargetPath] = useState("");
  const [phase, setPhase] = useState<Phase>("input");
  const [result, setResult] = useState<InitResponse | null>(null);
  const [errorMessage, setErrorMessage] = useState("");

  if (!open) return null;

  function handleClose() {
    setTargetPath("");
    setPhase("input");
    setResult(null);
    setErrorMessage("");
    onClose();
  }

  async function handleConfirm() {
    setPhase("loading");
    try {
      const response = await initProject({ target_path: targetPath.trim(), tools, guidelines });
      setResult(response);
      setPhase("success");
    } catch (err) {
      setErrorMessage(err instanceof Error ? err.message : "Something went wrong");
      setPhase("error");
    }
  }

  return (
    <div
      className="fixed inset-0 z-20 grid place-items-center bg-[rgba(40,15,30,0.35)] p-6"
      onClick={handleClose}
    >
      <div
        className="w-full max-w-[480px] rounded-[24px] bg-white p-7 shadow-[0_30px_60px_-20px_rgba(60,20,50,0.4)]"
        onClick={(e) => e.stopPropagation()}
      >
        {phase === "success" && result ? (
          <>
            <div className="mb-2 text-xl font-extrabold text-[#161217]">Done!</div>
            <p className="mb-4 text-sm text-[#5c5560]">Deployed to {result.target_path}:</p>
            <div className="mb-5 max-h-60 overflow-y-auto rounded-[14px] bg-[#f6f3f7] p-4">
              {Object.entries(result.deployed).map(([tool, path]) => (
                <div key={tool} className="py-0.5 font-mono text-[13px] text-[#5c5560]">
                  {tool}: {path}
                </div>
              ))}
            </div>
            <div className="flex justify-end">
              <Button variant="primary" onClick={handleClose}>
                Close
              </Button>
            </div>
          </>
        ) : (
          <>
            <div className="mb-2 text-xl font-extrabold text-[#161217]">Generate agent files?</div>
            <p className="mb-4 text-sm text-[#5c5560]">
              Enter the target directory on the machine running the API — files will be written there.
            </p>
            <input
              type="text"
              value={targetPath}
              onChange={(e) => setTargetPath(e.target.value)}
              placeholder="/path/to/your/project"
              disabled={phase === "loading"}
              className="mb-1 w-full rounded-xl border-[1.5px] border-[#e3c9d3] px-4 py-3 text-sm font-medium text-[#161217] outline-none focus:border-[#c81c5c] disabled:opacity-60"
            />
            {phase === "error" && (
              <p className="mt-2 text-sm font-semibold text-[#c81c5c]">{errorMessage}</p>
            )}
            <div className="mt-5 flex justify-end gap-3">
              <Button variant="secondary" onClick={handleClose}>
                Cancel
              </Button>
              <Button variant="primary" onClick={handleConfirm} disabled={!targetPath.trim() || phase === "loading"}>
                {phase === "loading" ? "Generating…" : "Yes"}
              </Button>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
