
import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Activity, Power, Server, Link as LinkIcon, AlertCircle } from 'lucide-react';
import { callMcpTool } from '../lib/mcp_client';

export function Status() {
    const [status, setStatus] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [startLoading, setStartLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchStatus = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await callMcpTool('reaper_system', { operation: 'status' });
            // REST response: { status, result?, message? }; tool output is in result
            setStatus(data.result ?? { message: data.message });
        } catch (err) {
            setError(String(err));
        } finally {
            setLoading(false);
        }
    };

    const handleStartReaper = async () => {
        setStartLoading(true);
        try {
            await callMcpTool('reaper_system', { operation: 'start_reaper' });
            // Wait a bit then refresh status
            setTimeout(fetchStatus, 3000);
        } catch (err) {
            setError('Failed to start Reaper: ' + String(err));
        } finally {
            setStartLoading(false);
        }
    };

    useEffect(() => {
        fetchStatus();
        const interval = setInterval(fetchStatus, 10000); // Auto refresh
        return () => clearInterval(interval);
    }, []);

    const isConnected = status?.reaper_connection?.connected;

    return (
        <div className="p-6 space-y-6">
            <div className="flex items-center justify-between">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">System Status</h1>
                    <p className="text-muted-foreground">Monitor Reaper MCP connection and health</p>
                </div>
                <Button onClick={fetchStatus} variant="outline" size="sm" disabled={loading}>
                    <Activity className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
                    Refresh
                </Button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Server Card */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center">
                            <Server className="w-5 h-5 mr-2 text-blue-400" />
                            MCP Server
                        </CardTitle>
                        <CardDescription>Backend Infrastructure</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">Status</span>
                            <Badge variant={error ? "destructive" : "default"} className="bg-emerald-500/10 text-emerald-500 border-emerald-500/20">
                                {error ? "Error" : "Running"}
                            </Badge>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">Port</span>
                            <span className="text-sm text-muted-foreground">10797 (REST + MCP /mcp)</span>
                        </div>
                        {error && (
                            <div className="p-3 text-sm text-red-400 bg-red-950/20 rounded border border-red-900/50">
                                <AlertCircle className="w-4 h-4 inline mr-2" />
                                {error}
                            </div>
                        )}
                    </CardContent>
                </Card>

                {/* Reaper Connection Card */}
                <Card>
                    <CardHeader>
                        <CardTitle className="flex items-center">
                            <LinkIcon className={`w-5 h-5 mr-2 ${isConnected ? 'text-emerald-400' : 'text-amber-400'}`} />
                            Reaper Interface
                        </CardTitle>
                        <CardDescription>DAW Connectivity (OSC)</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">Connection</span>
                            <Badge variant={isConnected ? "default" : "secondary"} className={isConnected ? "bg-emerald-500/10 text-emerald-500" : "bg-amber-500/10 text-amber-500"}>
                                {isConnected ? "Connected" : "Disconnected"}
                            </Badge>
                        </div>
                        <div className="flex items-center justify-between">
                            <span className="text-sm font-medium">Host IP</span>
                            <span className="text-sm text-muted-foreground">{status?.reaper_connection?.host || 'N/A'}</span>
                        </div>

                        {!isConnected && (
                            <div className="pt-2">
                                <Button
                                    className="w-full bg-blue-600 hover:bg-blue-700"
                                    onClick={handleStartReaper}
                                    disabled={startLoading}
                                >
                                    <Power className="w-4 h-4 mr-2" />
                                    {startLoading ? "Starting..." : "Start Reaper"}
                                </Button>
                                <p className="text-xs text-muted-foreground mt-2 text-center">
                                    Targeting default installation paths
                                </p>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>

            {/* Raw JSON Debug (Optional) */}
            {status && (
                <Card className="bg-slate-950 border-slate-800">
                    <CardHeader>
                        <CardTitle className="text-sm font-mono text-slate-500">Raw Diagnostics</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <pre className="text-xs font-mono text-slate-400 overflow-auto max-h-40">
                            {JSON.stringify(status, null, 2)}
                        </pre>
                    </CardContent>
                </Card>
            )}
        </div>
    );
}
