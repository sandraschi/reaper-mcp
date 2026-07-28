import { Activity, Shield, Wifi, WifiOff, Zap } from "lucide-react";
import { useCallback, useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { API_BASE } from "../lib/api";

const BACKOFF_INTERVALS = [1, 2, 4, 8, 16];

export function Dashboard() {
  const [health, setHealth] = useState<{
    status: string;
    service: string;
  } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [logCount, setLogCount] = useState(0);
  const [_restarting, _setRestarting] = useState(false);
  const [_backendOk, setBackendOk] = useState<boolean | null>(null);

  const fetchHealth = useCallback(async (): Promise<boolean> => {
    try {
      const r = await fetch(API_BASE + "/api/health");
      if (!r.ok) return false;
      const d = await r.json();
      setHealth(d);
      setError(null);
      return true;
    } catch (e) {
      setError(String(e));
      return false;
    }
  }, []);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      for (const delay of BACKOFF_INTERVALS) {
        if (cancelled) return;
        const ok = await fetchHealth();
        setBackendOk(ok);
        if (ok) break;
        await new Promise((r) => setTimeout(r, delay * 1000));
      }
      if (!cancelled) {
        const ok = await fetchHealth();
        setBackendOk(ok);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [fetchHealth]);

  useEffect(() => {
    fetch(API_BASE + "/api/logs/stats")
      .then((r) => r.json())
      .then((d) => setLogCount(d.total || 0))
      .catch(() => {});
  }, []);

  const connected = health?.status === "ok";

  return (
    <div className="space-y-6" data-testid="dashboard">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold tracking-tight text-white">Reaper Dashboard</h2>
          <p className="text-slate-400">DAW orchestration and transport telemetry</p>
        </div>
        <div className="flex items-center gap-3">
          <div
            className={[
              "flex items-center gap-2 px-4 py-2 rounded-xl border text-sm",
              connected
                ? "bg-emerald-500/10 border-emerald-500/20 text-emerald-400"
                : "bg-red-500/10 border-red-500/20 text-red-400",
            ].join(" ")}
          >
            {connected ? <Wifi size={14} /> : <WifiOff size={14} />}
            <span data-testid="backend-dot">{connected ? "Connected" : "Offline"}</span>
          </div>
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Backend Status</CardTitle>
            <Wifi className={connected ? "h-4 w-4 text-emerald-500" : "h-4 w-4 text-red-500"} />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{connected ? "Online" : "Offline"}</div>
            <p className="text-xs text-slate-400">API health check</p>
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Service</CardTitle>
            <Shield className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{health?.service || "reaper-mcp"}</div>
            <p className="text-xs text-slate-400">MCP server</p>
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Log Entries</CardTitle>
            <Activity className="h-4 w-4 text-purple-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{logCount}</div>
            <p className="text-xs text-slate-400">total recorded</p>
          </CardContent>
        </Card>

        <Card className="border-slate-800 bg-slate-950/50">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-slate-200">Health</CardTitle>
            <Zap className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-white">{connected ? "OK" : "Error"}</div>
            <p className="text-xs text-slate-400">{health?.status || error || "unknown"}</p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
