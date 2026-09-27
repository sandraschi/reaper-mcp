import { cn } from "@/common/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
	Card,
	CardContent,
	CardDescription,
	CardHeader,
	CardTitle,
} from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { ScrollArea } from "@/components/ui/scroll-area";
import { callMcpTool } from "@/lib/mcp_client";
import { BookOpen, FileCode2, Play, Plus, Save, Trash2 } from "lucide-react";
import { useCallback, useEffect, useState } from "react";

interface LuaExample {
	name: string;
	description: string;
	code: string;
}

const EXAMPLES: LuaExample[] = [
	{
		name: "Console Hello",
		description: "Print to the Reaper console (real reaper.* API)",
		code: `reaper.ShowConsoleMsg("Hello from Lua!\\n")`,
	},
	{
		name: "Count Tracks",
		description: "Show how many tracks the project has",
		code: `local n = reaper.CountTracks(0)\nreaper.ShowConsoleMsg("Tracks: " .. n .. "\\n")`,
	},
	{
		name: "Mute Selected",
		description: "Mute every selected track",
		code: `for i = 0, reaper.CountSelectedTracks(0) - 1 do\n  local tr = reaper.GetSelectedTrack(0, i)\n  reaper.SetMediaTrackInfoValue(tr, "B_MUTE", 1)\nend\nreaper.ShowConsoleMsg("Muted selected tracks\\n")`,
	},
];

async function luaOp(
	operation: string,
	extra: Record<string, unknown> = {},
): Promise<unknown> {
	const data = await callMcpTool("reaper_reascript", { operation, ...extra });
	const raw = data.result;
	if (typeof raw === "string") {
		try {
			return JSON.parse(raw);
		} catch {
			return raw;
		}
	}
	return raw ?? data.message ?? "";
}

export function LuaScripts() {
	const [scripts, setScripts] = useState<string[]>([]);
	const [selected, setSelected] = useState<string | null>(null);
	const [name, setName] = useState("untitled.lua");
	const [code, setCode] = useState(
		"-- pick a script or an example, or write a new one",
	);
	const [output, setOutput] = useState("");
	const [loading, setLoading] = useState(false);
	const [confirmDelete, setConfirmDelete] = useState(false);

	const refresh = useCallback(async () => {
		try {
			const list = (await luaOp("lua_list")) as string[];
			setScripts(Array.isArray(list) ? list : []);
		} catch (e) {
			setOutput(`List failed: ${String(e)}`);
		}
	}, []);

	useEffect(() => {
		refresh();
	}, [refresh]);

	const openScript = async (n: string) => {
		setLoading(true);
		try {
			const got = (await luaOp("lua_get", { script_name: n })) as {
				success?: boolean;
				code?: string;
				error?: string;
			};
			if (got && typeof got === "object" && "code" in got) {
				setName(n);
				setCode(String(got.code ?? ""));
				setSelected(n);
				setConfirmDelete(false);
			} else {
				setOutput(
					`Open failed: ${(got as { error?: string }).error ?? "unknown"}`,
				);
			}
		} catch (e) {
			setOutput(`Open failed: ${String(e)}`);
		} finally {
			setLoading(false);
		}
	};

	const save = async () => {
		setLoading(true);
		try {
			const out = (await luaOp("lua_save", { script_name: name, code })) as {
				success?: boolean;
				message?: string;
				error?: string;
			};
			setOutput(out.message ?? out.error ?? "");
			await refresh();
		} catch (e) {
			setOutput(`Save failed: ${String(e)}`);
		} finally {
			setLoading(false);
		}
	};

	const run = async () => {
		setLoading(true);
		try {
			const out = (await luaOp("lua_run", { script_name: name })) as {
				message?: string;
				error?: string;
			};
			setOutput(out.message ?? out.error ?? "");
		} catch (e) {
			setOutput(`Run failed: ${String(e)}`);
		} finally {
			setLoading(false);
		}
	};

	const removeScript = async () => {
		setLoading(true);
		try {
			const out = (await luaOp("lua_delete", { script_name: name })) as {
				message?: string;
				error?: string;
			};
			setOutput(out.message ?? out.error ?? "");
			setConfirmDelete(false);
			await refresh();
		} catch (e) {
			setOutput(`Delete failed: ${String(e)}`);
		} finally {
			setLoading(false);
		}
	};

	return (
		<div className="p-6 space-y-6">
			<div className="flex items-center justify-between">
				<div>
					<h1 className="text-3xl font-bold tracking-tight">Lua Scripts</h1>
					<p className="text-muted-foreground">
						CRUD + execute for REAPER-native Lua (reaper.* API) - Python lives
						on the ReaScript IDE page
					</p>
				</div>
				<Badge
					variant="outline"
					className="px-3 py-1 border-amber-500/20 text-amber-400"
				>
					<FileCode2 className="w-3 h-3 mr-2" />
					LUA RUNTIME
				</Badge>
			</div>

			<div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
				<Card className="lg:col-span-1 border-slate-800 bg-slate-900/50 flex flex-col h-[calc(100vh-200px)]">
					<CardHeader>
						<CardTitle className="flex items-center text-lg">
							<BookOpen className="w-5 h-5 mr-2" />
							Library
						</CardTitle>
						<CardDescription>Saved scripts & bundled examples</CardDescription>
					</CardHeader>
					<CardContent className="flex-1 overflow-hidden">
						<ScrollArea className="h-full pr-4">
							<div className="space-y-4">
								<div>
									<h3 className="text-sm font-semibold text-slate-400 mb-2 uppercase tracking-wider">
										Saved
									</h3>
									<div className="space-y-2">
										{scripts.length === 0 && (
											<p className="text-xs text-slate-600 italic">
												No scripts yet - save one from the editor.
											</p>
										)}
										{scripts.map((s) => (
											<Button
												key={s}
												variant="ghost"
												onClick={() => openScript(s)}
												className={cn(
													"w-full justify-start text-left h-auto py-2 px-3 border hover:border-slate-700 hover:bg-slate-800",
													selected === s
														? "border-amber-500/50"
														: "border-transparent",
												)}
											>
												<span className="font-mono text-sm text-slate-200">
													{s}
												</span>
											</Button>
										))}
									</div>
								</div>
								<div>
									<h3 className="text-sm font-semibold text-slate-400 mb-2 uppercase tracking-wider">
										Examples
									</h3>
									<div className="space-y-2">
										{EXAMPLES.map((ex) => (
											<Button
												key={ex.name}
												variant="ghost"
												className="w-full justify-start text-left h-auto py-2 px-3 border border-dashed border-transparent hover:border-slate-700 hover:bg-slate-800"
												onClick={() => {
													setName(
														`${ex.name.toLowerCase().replace(/[^a-z0-9]+/g, "-")}.lua`,
													);
													setCode(ex.code);
													setSelected(null);
													setConfirmDelete(false);
												}}
											>
												<div className="flex flex-col">
													<span className="font-medium text-slate-200">
														{ex.name}
													</span>
													<span className="text-xs text-muted-foreground line-clamp-1">
														{ex.description}
													</span>
												</div>
											</Button>
										))}
									</div>
								</div>
							</div>
						</ScrollArea>
					</CardContent>
				</Card>

				<div className="lg:col-span-2 space-y-6 flex flex-col h-[calc(100vh-200px)]">
					<Card className="flex-1 border-slate-800 bg-slate-900/50 flex flex-col">
						<CardHeader className="pb-3">
							<div className="flex items-center justify-between gap-2 flex-wrap">
								<input
									value={name}
									onChange={(e) => setName(e.target.value)}
									spellCheck={false}
									aria-label="Script filename"
									className="font-mono text-sm bg-slate-950 border border-slate-800 rounded px-2 py-1.5 text-slate-200 focus:outline-none focus:ring-1 focus:ring-amber-500/50"
								/>
								<div className="space-x-2">
									<Button
										variant="outline"
										onClick={() => {
											setName("untitled.lua");
											setCode("-- new script\n");
											setSelected(null);
											setConfirmDelete(false);
										}}
										className="border-slate-700 hover:bg-slate-800 text-slate-300"
									>
										<Plus className="w-4 h-4 mr-2" />
										New
									</Button>
									<Button
										variant="outline"
										onClick={save}
										disabled={loading}
										className="border-slate-700 hover:bg-slate-800 text-slate-300"
									>
										<Save className="w-4 h-4 mr-2" />
										Save
									</Button>
									{confirmDelete ? (
										<Button
											variant="destructive"
											onClick={removeScript}
											disabled={loading}
										>
											Confirm delete {name}?
										</Button>
									) : (
										<Button
											variant="outline"
											onClick={() => setConfirmDelete(true)}
											disabled={loading}
											className="border-red-900 text-red-300 hover:bg-red-950"
										>
											<Trash2 className="w-4 h-4 mr-2" />
											Delete
										</Button>
									)}
									<Button
										onClick={run}
										disabled={loading}
										className={cn(
											"bg-emerald-600 hover:bg-emerald-700 text-white min-w-[100px]",
											loading && "opacity-50 cursor-not-allowed",
										)}
									>
										<Play className="w-4 h-4 mr-2" />
										{loading ? "Running..." : "Run in REAPER"}
									</Button>
								</div>
							</div>
						</CardHeader>
						<CardContent className="flex-1 p-0 flex flex-col">
							<div className="flex-1 relative">
								<textarea
									className="w-full h-full min-h-[300px] bg-slate-950 p-4 font-mono text-sm text-slate-300 resize-none focus:outline-none focus:ring-1 focus:ring-amber-500/50 border-y border-slate-800"
									value={code}
									onChange={(e) => setCode(e.target.value)}
									spellCheck={false}
									aria-label="Lua Editor"
								/>
							</div>
							<div className="h-[150px] bg-black border-t border-slate-800 p-4 overflow-hidden flex flex-col">
								<Label className="text-xs font-bold uppercase tracking-wider text-muted-foreground mb-2">
									Output
								</Label>
								<ScrollArea className="flex-1">
									{output ? (
										<div className="whitespace-pre-wrap break-all font-mono text-sm text-slate-300">
											{output}
										</div>
									) : (
										<span className="text-slate-600 italic">
											Run needs reapy + a running REAPER. CRUD works without.
										</span>
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
