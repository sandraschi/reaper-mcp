import { Code, Server } from "lucide-react";
import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { callMcpTool } from "../lib/mcp_client";

export function Help() {
  const [serverHelp, setServerHelp] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchHelp = async () => {
      setLoading(true);
      try {
        const data = await callMcpTool("reaper_system", { operation: "help" });
        const raw = data.result;
        setServerHelp(typeof raw === "object" && raw !== null ? raw : { text: raw ?? data.message });
      } catch (err) {
        console.error("Failed to fetch server help", err);
      } finally {
        setLoading(false);
      }
    };
    fetchHelp();
  }, []);

  return (
    <div className="p-6 space-y-6 h-full flex flex-col">
      <div className="flex items-center justify-between shrink-0">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Documentation</h1>
          <p className="text-muted-foreground">Resources for using Reaper MCP</p>
        </div>
      </div>

      <Tabs defaultValue="webapp" className="flex-1 flex flex-col min-h-0">
        <TabsList>
          <TabsTrigger value="webapp">Webapp Guide</TabsTrigger>
          <TabsTrigger value="server">Server API</TabsTrigger>
          <TabsTrigger value="reascript">ReaScript</TabsTrigger>
        </TabsList>

        <TabsContent value="webapp" className="flex-1 overflow-hidden mt-4">
          <ScrollArea className="h-full pr-4">
            <div className="space-y-6">
              <Card>
                <CardHeader>
                  <CardTitle>Getting Started</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4 text-slate-300">
                  <p>
                    Welcome to the <strong>Reaper MCP Neural Interface</strong>. This application allows AI agents and
                    humans to interact with Reaper DAW through a unified protocol.
                  </p>

                  <h3 className="text-lg font-semibold text-white mt-4">Key Features</h3>
                  <ul className="list-disc list-inside space-y-2 ml-2">
                    <li>
                      <strong>Tools Hub:</strong> Browse and execute available MCP tools manually.
                    </li>
                    <li>
                      <strong>ReaScript IDE:</strong> Write and run Python scripts directly inside Reaper.
                    </li>
                    <li>
                      <strong>Status Monitor:</strong> Check connection health and start Reaper remotely.
                    </li>
                  </ul>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Common Workflows</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4 text-slate-300">
                  <div className="border-l-2 border-slate-700 pl-4">
                    <h4 className="font-semibold text-white">1. Starting Up</h4>
                    <p>
                      Ensure `start.ps1` or `start.bat` is running. Check the <strong>Status</strong> page to verify
                      Reaper connection.
                    </p>
                  </div>
                  <div className="border-l-2 border-slate-700 pl-4">
                    <h4 className="font-semibold text-white">2. Using Tools</h4>
                    <p>
                      Navigate to <strong>Tools</strong>. Select `reaper_transport` to control playback or
                      `reaper_tracks` to manage tracks. Inputs are JSON-formatted.
                    </p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </ScrollArea>
        </TabsContent>

        <TabsContent value="server" className="flex-1 overflow-hidden mt-4">
          <Card className="h-full flex flex-col">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Server className="w-5 h-5 mr-2" />
                Available Tools (Live from Server)
              </CardTitle>
            </CardHeader>
            <CardContent className="flex-1 overflow-hidden p-0">
              <ScrollArea className="h-full p-6 pt-0">
                {loading ? (
                  <div className="text-center p-10 text-muted-foreground">Loading server help...</div>
                ) : (
                  <pre className="font-mono text-sm text-slate-300 whitespace-pre-wrap">
                    {JSON.stringify(serverHelp, null, 2)}
                  </pre>
                )}
              </ScrollArea>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="reascript" className="flex-1 overflow-hidden mt-4">
          <Card className="h-full">
            <CardHeader>
              <CardTitle className="flex items-center">
                <Code className="w-5 h-5 mr-2" />
                ReaScript Python Guide
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4 text-slate-300">
              <p>You can execute arbitrary Python code. The environment comes pre-loaded with:</p>
              <ul className="list-disc list-inside space-y-1 font-mono text-sm text-emerald-400">
                <li>reapy (as `reapy`)</li>
                <li>reapy.reascript_api (functions available directly or via RPR_)</li>
              </ul>

              <h4 className="font-semibold text-white mt-4">Returning Data</h4>
              <p>To return JSON data to the UI, assign a dictionary to `_result`:</p>
              <pre className="bg-slate-950 p-4 rounded-md mt-2 border border-slate-800">
                {`_result = {
  "track_count": 5,
  "status": "active"
}`}
              </pre>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
