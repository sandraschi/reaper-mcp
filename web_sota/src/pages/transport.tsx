import { Activity, Circle, Pause, Play, Square } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export function Transport() {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Transport Control</h1>
        <p className="text-muted-foreground italic text-sm">Austrian Precision Playback Orchestration</p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Master Transport</CardTitle>
          </CardHeader>
          <CardContent className="flex flex-col items-center gap-8 py-10">
            <div className="text-6xl font-mono font-bold tracking-tighter text-red-500">14.2.00</div>
            <div className="flex gap-4">
              <Button
                size="icon"
                variant="outline"
                className="h-16 w-16 rounded-full border-slate-800 hover:bg-slate-800"
              >
                <Square className="h-8 w-8 text-white fill-white" />
              </Button>
              <Button
                size="icon"
                variant="outline"
                className="h-16 w-16 rounded-full border-slate-800 bg-red-500/10 hover:bg-red-500/20"
              >
                <Play className="h-8 w-8 text-red-500 fill-red-500" />
              </Button>
              <Button
                size="icon"
                variant="outline"
                className="h-16 w-16 rounded-full border-slate-800 hover:bg-slate-800"
              >
                <Pause className="h-8 w-8 text-white fill-white" />
              </Button>
              <Button
                size="icon"
                variant="outline"
                className="h-16 w-16 rounded-full border-slate-800 bg-red-900/20 hover:bg-red-900/30"
              >
                <Circle className="h-8 w-8 text-red-600 fill-red-600" />
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-2">
          <CardHeader>
            <CardTitle>Transport Telemetry</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex justify-between p-3 border rounded-lg bg-slate-500/5 items-center">
              <span className="text-sm font-medium">BPM</span>
              <span className="font-mono text-xl">120.00</span>
            </div>
            <div className="flex justify-between p-3 border rounded-lg bg-slate-500/5 items-center">
              <span className="text-sm font-medium">Time Signature</span>
              <span className="font-mono text-xl">4 / 4</span>
            </div>
            <div className="flex justify-between p-3 border rounded-lg bg-slate-500/5 items-center text-emerald-500">
              <span className="text-sm font-medium">Engine Status</span>
              <div className="flex items-center gap-2">
                <Activity className="h-4 w-4 animate-pulse" />
                <span className="font-mono">NOMINAL</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
