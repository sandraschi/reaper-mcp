import { BookOpen, Code, Play, Settings, Terminal } from "lucide-react";
import { useState } from "react";
import { cn } from "@/common/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { callMcpTool } from "@/lib/mcp_client";

interface Snippet {
  name: string;
  description: string;
  code: string;
}

interface McpContentItem {
  type: string;
  text: string;
}

interface McpResponse {
  content?: McpContentItem[];
  [key: string]: unknown;
}

const EXAMPLES: Snippet[] = [
  {
    name: "Console Hello World",
    description: "Print a message to the Reaper console",
    code: `RPR_ShowConsoleMsg("Hello from ReaScript Web Interface!\\n")`,
  },
  {
    name: "Create Track",
    description: "Add a new track securely using reapy",
    code: `project = reapy.Project.today()
track = project.add_track(name="Web Created Track")
RPR_ShowConsoleMsg(f"Created track: {track.name}\\n")`,
  },
  {
    name: "List Tracks",
    description: "Get names of all tracks",
    code: `project = reapy.Project.today()
names = [t.name for t in project.tracks]
RPR_ShowConsoleMsg(f"Tracks: {names}\\n")
return names  # This will be returned to the web interface`,
  },
  {
    name: "Arm First Track",
    description: "Arm the first track for recording",
    code: `project = reapy.Project.today()
if project.n_tracks > 0:
    project.tracks[0].arm()
    RPR_ShowConsoleMsg("Armed first track\\n")
else:
    RPR_ShowConsoleMsg("No tracks to arm\\n")`,
  },
  {
    name: "Complex Logic Loop",
    description: "Loop through tracks and color them",
    code: `import random
project = reapy.Project.today()
for track in project.tracks:
    # Random RGB color
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    native_color = reapy.rgb_to_native((r, g, b))
    track.color = native_color`,
  },
];

export function Reascript() {
  const [code, setCode] = useState<string>(EXAMPLES[0].code);
  const [result, setResult] = useState<McpResponse | null>(null);
  const [loading, setLoading] = useState(false);
  // const [customSnippets, setCustomSnippets] = useState<Snippet[]>([]); // TODO: Implement custom snippets

  const handleRun = async () => {
    setLoading(true);
    setResult(null);
    try {
      const data = await callMcpTool("reaper_reascript", {
        operation: "run",
        code,
      });
      const raw = data.result;
      const displayContent = typeof raw === "string" ? raw : JSON.stringify(raw ?? data.message ?? "", null, 2);
      setResult({ content: [{ type: "text", text: displayContent }] });
    } catch (error) {
      setResult({ content: [{ type: "text", text: String(error) }] });
    } finally {
      setLoading(false);
    }
  };

  const handleSetup = async () => {
    setLoading(true);
    setResult(null);
    try {
      const data = await callMcpTool("reaper_reascript", {
        operation: "setup",
      });
      const text = (typeof data.result === "string" ? data.result : data.message) || "Reapy setup initiated.";
      setResult({ content: [{ type: "text", text }] });
    } catch (error) {
      console.error("Error setting up reapy:", error);
      setResult({
        content: [
          {
            type: "text",
            text: "Failed to setup reapy. Is the MCP server running?",
          },
        ],
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">ReaScript IDE</h1>
          <p className="text-muted-foreground">Execute Python code directly in Reaper via reapy-boost</p>
        </div>
        <Badge variant="outline" className="px-3 py-1 border-emerald-500/20 text-emerald-400">
          <Code className="w-3 h-3 mr-2" />
          PYTHON RUNTIME
        </Badge>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Sidebar: Snippets */}
        <Card className="lg:col-span-1 border-slate-800 bg-slate-900/50 flex flex-col h-[calc(100vh-200px)]">
          <CardHeader>
            <CardTitle className="flex items-center text-lg">
              <BookOpen className="w-5 h-5 mr-2" />
              Snippet Library
            </CardTitle>
            <CardDescription>Examples & saved scripts</CardDescription>
          </CardHeader>
          <CardContent className="flex-1 overflow-hidden">
            <ScrollArea className="h-full pr-4">
              <div className="space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-slate-400 mb-2 uppercase tracking-wider">Examples</h3>
                  <div className="space-y-2">
                    {EXAMPLES.map((snippet, idx) => (
                      <Button
                        key={idx}
                        variant="ghost"
                        className="w-full justify-start text-left h-auto py-2 px-3 border border-transparent hover:border-slate-700 hover:bg-slate-800"
                        onClick={() => setCode(snippet.code)}
                      >
                        <div className="flex flex-col">
                          <span className="font-medium text-slate-200">{snippet.name}</span>
                          <span className="text-xs text-muted-foreground line-clamp-1">{snippet.description}</span>
                        </div>
                      </Button>
                    ))}
                  </div>
                </div>
              </div>
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Main: Editor & Output */}
        <div className="lg:col-span-2 space-y-6 flex flex-col h-[calc(100vh-200px)]">
          <Card className="flex-1 border-slate-800 bg-slate-900/50 flex flex-col">
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <CardTitle className="flex items-center text-lg">
                  <Terminal className="w-5 h-5 mr-2 text-emerald-500" />
                  Code Editor
                </CardTitle>
                <div className="space-x-2">
                  <Button
                    variant="outline"
                    onClick={handleSetup}
                    disabled={loading}
                    className="border-slate-700 hover:bg-slate-800 text-slate-300"
                  >
                    <Settings className="w-4 h-4 mr-2" />
                    Setup Reapy
                  </Button>
                  <Button
                    onClick={handleRun}
                    disabled={loading}
                    className={cn(
                      "bg-emerald-600 hover:bg-emerald-700 text-white min-w-[100px]",
                      loading && "opacity-50 cursor-not-allowed",
                    )}
                  >
                    <Play className="w-4 h-4 mr-2" />
                    {loading ? "Running..." : "Run Script"}
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent className="flex-1 p-0 flex flex-col">
              <div className="flex-1 relative">
                <textarea
                  className="w-full h-full min-h-[300px] bg-slate-950 p-4 font-mono text-sm text-slate-300 resize-none focus:outline-none focus:ring-1 focus:ring-emerald-500/50 border-y border-slate-800"
                  value={code}
                  onChange={(e) => setCode(e.target.value)}
                  spellCheck={false}
                  aria-label="Code Editor"
                />
              </div>

              {/* Output Console */}
              <div className="h-[200px] bg-black border-t border-slate-800 p-4 overflow-hidden flex flex-col">
                <Label className="flex items-center text-xs font-bold uppercase tracking-wider text-muted-foreground mb-2">
                  <Activity className="w-3 h-3 mr-2" />
                  Execution Output
                </Label>
                <ScrollArea className="flex-1">
                  {result ? (
                    <div className="space-y-2 font-mono text-sm">
                      {result.content && Array.isArray(result.content) ? (
                        result.content.map((item: McpContentItem, i: number) => (
                          <div
                            key={i}
                            className={cn(
                              "whitespace-pre-wrap break-all",
                              item.type === "text" ? "text-slate-300" : "text-amber-400",
                            )}
                          >
                            {item.text}
                          </div>
                        ))
                      ) : (
                        <pre className="text-slate-300 whitespace-pre-wrap">{JSON.stringify(result, null, 2)}</pre>
                      )}
                    </div>
                  ) : (
                    <span className="text-slate-600 italic">Ready to execute. Press Run to start.</span>
                  )}
                </ScrollArea>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}

// Helper icon
function Activity({ className }: { className?: string }) {
  return (
    <svg
      className={className}
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M22 12h-4l-3 9L9 3l-3 9H2" />
    </svg>
  );
}
