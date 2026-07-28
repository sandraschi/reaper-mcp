import { Radio, Sliders } from "lucide-react";
import { useState } from "react";
import { cn } from "@/common/utils";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Slider } from "@/components/ui/slider";

interface TrackProps {
  id: number;
  name: string;
  isMaster?: boolean;
}

function FaderStrip({ id, name, isMaster }: TrackProps) {
  const [volume, setVolume] = useState([75]);
  const [pan, setPan] = useState([50]);
  const [isMuted, setIsMuted] = useState(false);
  const [isSolo, setIsSolo] = useState(false);

  return (
    <div
      className={cn(
        "flex flex-col items-center gap-4 p-4 rounded-lg bg-slate-900/40 border border-slate-800 w-32",
        isMaster && "border-emerald-500/30 bg-emerald-500/5",
      )}
    >
      <div className="text-[10px] font-bold uppercase tracking-widest text-slate-500 mb-2 truncate w-full text-center">
        {name}
      </div>

      {/* Pan Slider */}
      <div className="w-full px-2">
        <Slider value={pan} onValueChange={setPan} max={100} step={1} className="h-1" />
        <div className="flex justify-between text-[8px] text-slate-600 mt-1">
          <span>L</span>
          <span>C</span>
          <span>R</span>
        </div>
      </div>

      {/* Main Fader */}
      <div className="h-64 py-4 flex flex-col items-center">
        <Slider orientation="vertical" value={volume} onValueChange={setVolume} max={100} step={1} className="h-full" />
      </div>

      {/* Solo / Mute */}
      <div className="grid grid-cols-2 gap-2 w-full">
        <Button
          variant="outline"
          size="sm"
          className={cn(
            "h-8 text-[10px] font-bold p-0",
            isSolo ? "bg-yellow-500 text-black border-yellow-500 hover:bg-yellow-400" : "text-slate-400",
          )}
          onClick={() => setIsSolo(!isSolo)}
        >
          S
        </Button>
        <Button
          variant="outline"
          size="sm"
          className={cn(
            "h-8 text-[10px] font-bold p-0",
            isMuted ? "bg-red-500 text-white border-red-500 hover:bg-red-400" : "text-slate-400",
          )}
          onClick={() => setIsMuted(!isMuted)}
        >
          M
        </Button>
      </div>

      <div className="text-[12px] font-mono text-emerald-500 mt-2">{Math.round((volume[0] / 100) * 12 - 12)} dB</div>

      <div className="mt-auto pt-2 border-t border-slate-800 w-full text-center text-[10px] font-bold text-slate-400">
        CH {id}
      </div>
    </div>
  );
}

export function Mixer() {
  const tracks = [
    { id: 1, name: "Kick" },
    { id: 2, name: "Snare" },
    { id: 3, name: "Overheads" },
    { id: 4, name: "Bass" },
    { id: 5, name: "Guitars" },
    { id: 6, name: "Vocals" },
    { id: 7, name: "Reverb" },
    { id: 8, name: "Delay" },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-end">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold tracking-tight">Mixer</h1>
          <p className="text-muted-foreground italic text-sm">Console Emulation & Summing</p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="gap-2">
            <Radio className="h-4 w-4 text-emerald-500" />
            Live Link
          </Button>
        </div>
      </div>

      <Card className="bg-slate-950/50 border-slate-800 overflow-hidden">
        <CardHeader className="border-b border-slate-800 bg-slate-900/50">
          <CardTitle className="text-sm font-medium flex items-center gap-2">
            <Sliders className="h-4 w-4 text-emerald-500" />
            Console View
          </CardTitle>
        </CardHeader>
        <CardContent className="p-6">
          <div className="flex gap-4 overflow-x-auto pb-4 scrollbar-thin scrollbar-thumb-slate-800">
            {tracks.map((track) => (
              <FaderStrip key={track.id} id={track.id} name={track.name} />
            ))}
            <div className="w-4 border-r border-slate-800 mx-2" />
            <FaderStrip id={0} name="MASTER" isMaster />
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
