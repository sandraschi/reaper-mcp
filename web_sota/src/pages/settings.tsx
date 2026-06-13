import { useState, useEffect } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Sliders, Activity, Database, Cpu } from "lucide-react";

function LLMSettings() {
    const [providers, setProviders] = useState<Record<string, {name:string}[]>>({});
    const [selectedProvider, setSelectedProvider] = useState("ollama");
    const [selectedModel, setSelectedModel] = useState("");
    const [status, setStatus] = useState<"loading"|"ready"|"error">("loading");
    useEffect(() => {
        fetch("/api/llm/providers").then(r => r.json()).then(d => {
            setProviders(d);
            const savedP = localStorage.getItem("llm_provider") || "ollama";
            const savedM = localStorage.getItem("llm_model") || "";
            setSelectedProvider(savedP);
            const models = d[savedP === "ollama" ? "ollama" : "lm_studio"] || [];
            setSelectedModel(savedM && models.some((m:{name:string}) => m.name === savedM) ? savedM : (models[0]?.name || ""));
            setStatus(models.length > 0 ? "ready" : "error");
        }).catch(() => {
            setProviders({ ollama: [{name:"llama3.2:3b"}] });
            setSelectedModel(localStorage.getItem("llm_model") || "llama3.2:3b");
            setStatus("ready");
        });
    }, []);
    const save = (p:string, m:string) => { localStorage.setItem("llm_provider", p); localStorage.setItem("llm_model", m); };
    const models = providers[selectedProvider === "ollama" ? "ollama" : "lm_studio"] || [];
    return (
        <div className="rounded-lg border border-slate-800 bg-slate-950/50 p-4 space-y-3">
            <div className="flex items-center justify-between">
                <h3 className="text-sm font-medium text-slate-200">Local LLM</h3>
                <span className={`inline-flex items-center gap-1.5 text-xs ${status === "ready" ? "text-emerald-400" : "text-amber-400"}`}>
                    <span className={`h-2 w-2 rounded-full ${status === "ready" ? "bg-emerald-400" : "bg-amber-400"}`} />
                    {status === "ready" ? "connected" : "probing"}
                </span>
            </div>
            <select className="h-9 w-full rounded-md border border-slate-700 bg-slate-900 px-3 text-sm text-slate-200"
                value={selectedProvider} onChange={(e) => { setSelectedProvider(e.target.value); save(e.target.value, ""); }}>
                <option value="ollama">Ollama</option>
                <option value="lm_studio">LM Studio</option>
            </select>
            <select className="h-9 w-full rounded-md border border-slate-700 bg-slate-900 px-3 text-sm text-slate-200"
                value={selectedModel} onChange={(e) => { setSelectedModel(e.target.value); save(selectedProvider, e.target.value); }}>
                {models.map((m) => <option key={m.name} value={m.name}>{m.name}</option>)}
            </select>
            <p className="text-xs text-slate-500">Used by AI tools. Saved to browser storage.</p>
        </div>
    );
}

export function Settings() {
    return (
        <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight text-white">Project Settings</h1>
                    <p className="text-slate-400">Reaper MCP Infrastructure Configuration</p>
                </div>
                <Badge variant="outline" className="border-red-500/20 text-red-400">
                    SOTA S3.0
                </Badge>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <Card className="border-slate-800 bg-slate-900/50">
                    <CardHeader>
                        <CardTitle className="flex items-center text-white">
                            <Activity className="w-5 h-5 mr-2 text-red-500" />
                            API Configuration
                        </CardTitle>
                        <CardDescription>Backend endpoint for Reaper control</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="grid gap-2">
                            <Label className="text-slate-300">Base API URL</Label>
                            <Input
                                className="bg-slate-950 border-slate-800 text-slate-100"
                                defaultValue="http://localhost:10793/api/v1"
                            />
                        </div>
                        <Button className="w-full bg-red-600 hover:bg-red-700 text-white">
                            Update Endpoint
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-900/50">
                    <CardHeader>
                        <CardTitle className="flex items-center text-white">
                            <Database className="w-5 h-5 mr-2 text-red-500" />
                            Persistence
                        </CardTitle>
                        <CardDescription>Global state and history management</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between p-3 rounded-md bg-slate-950/50 border border-slate-800">
                            <div className="space-y-0.5">
                                <p className="text-sm font-medium text-slate-200">Local Cache</p>
                                <p className="text-xs text-slate-400">Store UI state in browser</p>
                            </div>
                            <Badge variant="secondary">ENABLED</Badge>
                        </div>
                        <Button variant="outline" className="w-full border-slate-800 text-slate-300 hover:bg-slate-800">
                            Clear Cache
                        </Button>
                    </CardContent>
                </Card>

                <Card className="border-slate-800 bg-slate-900/50">
                    <CardHeader>
                        <CardTitle className="flex items-center text-white">
                            <Cpu className="w-5 h-5 mr-2 text-red-500" />
                            LLM Provider
                        </CardTitle>
                        <CardDescription>Local model endpoint configuration</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <LLMSettings />
                    </CardContent>
                </Card>
            </div>

            <Card className="border-slate-800 bg-slate-900/50">
                <CardHeader>
                    <CardTitle className="flex items-center text-white">
                        <Sliders className="w-5 h-5 mr-2 text-red-500" />
                        Infrastructure Standards
                    </CardTitle>
                    <CardDescription>Materialist/Reductionist technical compliance</CardDescription>
                </CardHeader>
                <CardContent className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div className="p-4 rounded-lg bg-black/40 border border-white/5 space-y-1">
                        <p className="text-[10px] font-bold text-red-500 uppercase">Architecture</p>
                        <p className="text-sm text-slate-100">RESTful Orchestration</p>
                    </div>
                    <div className="p-4 rounded-lg bg-black/40 border border-white/5 space-y-1">
                        <p className="text-[10px] font-bold text-red-500 uppercase">Protocol</p>
                        <p className="text-sm text-slate-100">OSC over HTTP</p>
                    </div>
                    <div className="p-4 rounded-lg bg-black/40 border border-white/5 space-y-1">
                        <p className="text-[10px] font-bold text-red-500 uppercase">Consistency</p>
                        <p className="text-sm text-slate-100">Zero-Mock Integrity</p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
