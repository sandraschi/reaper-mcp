import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { List, VolumeX, Headphones, Circle } from "lucide-react";
import { cn } from "@/common/utils";

const tracks = [
    { id: 1, name: "Vocal Main", muted: false, solo: true, armed: false },
    { id: 2, name: "Vocal Dub", muted: true, solo: false, armed: false },
    { id: 3, name: "Guitar L", muted: false, solo: false, armed: true },
    { id: 4, name: "Guitar R", muted: false, solo: false, armed: true },
    { id: 5, name: "Bass DI", muted: false, solo: false, armed: false },
    { id: 6, name: "Drum Bus", muted: false, solo: false, armed: false },
];

export function Tracks() {
    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div className="flex flex-col gap-2">
                    <h1 className="text-3xl font-bold tracking-tight">Tracks</h1>
                    <p className="text-muted-foreground italic text-sm">
                        Total Count: {tracks.length}
                    </p>
                </div>
                <Button className="bg-red-600 hover:bg-red-700">
                    <Circle className="mr-2 h-4 w-4 fill-white" />
                    Arm All
                </Button>
            </div>

            <Card>
                <CardHeader>
                    <CardTitle className="text-sm font-medium flex items-center gap-2">
                        <List className="h-4 w-4" />
                        Project Track List
                    </CardTitle>
                </CardHeader>
                <CardContent className="space-y-2">
                    {tracks.map((track) => (
                        <div key={track.id} className="flex items-center justify-between p-4 border rounded-lg bg-slate-500/5 group hover:bg-slate-500/10 transition-colors">
                            <div className="flex items-center gap-4">
                                <span className="font-mono text-slate-500 w-8">{track.id}</span>
                                <span className="font-medium">{track.name}</span>
                            </div>
                            <div className="flex gap-2">
                                <Button size="sm" variant="ghost" className={cn("h-8 w-8 p-0", track.muted && "text-yellow-500 bg-yellow-500/10")}>
                                    <VolumeX className="h-4 w-4" />
                                </Button>
                                <Button size="sm" variant="ghost" className={cn("h-8 w-8 p-0", track.solo && "text-emerald-500 bg-emerald-500/10")}>
                                    <Headphones className="h-4 w-4" />
                                </Button>
                                <Button size="sm" variant="ghost" className={cn("h-8 w-8 p-0", track.armed && "text-red-500 bg-red-500/10")}>
                                    <Circle className={cn("h-4 w-4", track.armed && "fill-red-500")} />
                                </Button>
                            </div>
                        </div>
                    ))}
                </CardContent>
            </Card>
        </div>
    );
}
