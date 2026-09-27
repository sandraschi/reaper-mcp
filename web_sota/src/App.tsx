import { AppLayout } from "@/components/layout/app-layout";
import Logging from "@/pages/Logging";
import { Dashboard } from "@/pages/dashboard";
import { Help } from "@/pages/help";
import { LuaScripts } from "@/pages/lua-scripts";
import { Mixer } from "@/pages/mixer";
import { Reascript } from "@/pages/reascript";
import { Settings } from "@/pages/settings";
import { Status } from "@/pages/status";
import { Tools } from "@/pages/tools";
import { Tracks } from "@/pages/tracks";
import { Transport } from "@/pages/transport";
import {
	Navigate,
	Route,
	BrowserRouter as Router,
	Routes,
} from "react-router-dom";
import { ApiDocsPage } from "./pages/api-docs";

function App() {
	return (
		<Router>
			<AppLayout>
				<Routes>
					<Route path="/" element={<Dashboard />} />
					<Route path="/transport" element={<Transport />} />
					<Route path="/tracks" element={<Tracks />} />
					<Route path="/mixer" element={<Mixer />} />
					<Route path="/tools" element={<Tools />} />
					<Route path="/reascript" element={<Reascript />} />
					<Route path="/lua-scripts" element={<LuaScripts />} />
					<Route path="/status" element={<Status />} />
					<Route path="/help" element={<Help />} />
					<Route path="/api-docs" element={<ApiDocsPage />} />
					<Route path="/settings" element={<Settings />} />
					<Route path="/logs" element={<Logging />} />
					<Route path="*" element={<Navigate to="/" replace />} />
				</Routes>
			</AppLayout>
		</Router>
	);
}

export default App;
