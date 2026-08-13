import { useEffect, useMemo, useState } from "react";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  CircleStop,
  CloudRain,
  Gauge,
  Layers3,
  MapPin,
  Pause,
  Play,
  Plus,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  SquareTerminal,
  TrainFront,
  TriangleAlert,
  X,
  Zap,
} from "lucide-react";

const API_BASE = "http://localhost:8000";

type Asset = {
  asset_id: string;
  asset_name?: string;
  asset_type: string;
  latitude: number;
  longitude: number;
  health_score: number;
  degradation_rate: number;
  age_days: number;
};

type Scenario = {
  name: string;
  type?: string;
  severity?: number;
  start_step?: number;
  duration_steps?: number;
};

type Status = {
  simulation_id?: string;
  status?: string;
  running?: boolean;
  paused?: boolean;
  completed?: boolean;
  current_step?: number;
  total_steps?: number;
  progress?: number;
};

type Results = {
  simulation_id: string;
  simulation_name: string;
  success: boolean;
  duration_seconds: number;
  simulation_steps: number;
  total_assets: number;
  healthy_assets: number;
  degraded_assets: number;
  failed_assets: number;
  average_health_score: number;
  asset_results?: Array<{
    asset_id: string;
    health_score: number;
    predicted_risk: string;
    maintenance_required: boolean;
    failed: boolean;
  }>;
  prediction?: {
    failure_probability: number;
    remaining_useful_life_days: number;
    predicted_health_score: number;
    confidence: number;
  } | null;
};

const SCENARIOS: Array<{
  name: string;
  label: string;
  description: string;
  icon: typeof CloudRain;
}> = [
  { name: "RAIN", label: "Heavy Rain", description: "Simulates sustained rainfall and moisture stress.", icon: CloudRain },
  { name: "FLOOD", label: "Flood", description: "Introduces flooding stress across vulnerable assets.", icon: TriangleAlert },
  { name: "CRACK_GROWTH", label: "Crack Growth", description: "Accelerates rail degradation and failure risk.", icon: AlertTriangle },
  { name: "BALLAST_FAILURE", label: "Ballast Failure", description: "Models progressive ballast condition loss.", icon: Layers3 },
  { name: "GPS_DRIFT", label: "GPS Drift", description: "Injects positioning uncertainty into operations.", icon: MapPin },
  { name: "TRAIN_OVERLOAD", label: "Train Overload", description: "Raises operational load on infrastructure.", icon: TrainFront },
];

const ASSET_TYPES = ["RAIL", "SLEEPER", "FASTENER", "BALLAST", "TURNOUT", "BRIDGE", "SIGNAL"];

function App() {
  const [name, setName] = useState("TDOS Demonstration Run");
  const [steps, setSteps] = useState(100);
  const [assets, setAssets] = useState<Asset[]>([
  {
    asset_id: "AST-001",
    asset_name: "Mainline Rail A",
    asset_type: "RAIL",
    latitude: 13.0827,
    longitude: 80.2707,
    health_score: 96,
    degradation_rate: 0.08,
    age_days: 120,
  },
  {
    asset_id: "AST-002",
    asset_name: "Sleeper Cluster A",
    asset_type: "SLEEPER",
    latitude: 13.0832,
    longitude: 80.2712,
    health_score: 91,
    degradation_rate: 0.05,
    age_days: 90,
  },
  {
    asset_id: "AST-003",
    asset_name: "Turnout 01",
    asset_type: "TURNOUT",
    latitude: 13.0838,
    longitude: 80.2718,
    health_score: 88,
    degradation_rate: 0.11,
    age_days: 240,
  },
]);
  const [selectedScenarios, setSelectedScenarios] = useState<string[]>(["CRACK_GROWTH"]);
  const [simulationId, setSimulationId] = useState<string | null>(null);
  const [status, setStatus] = useState<Status | null>(null);
  const [results, setResults] = useState<Results | null>(null);
  const [loading, setLoading] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"overview" | "setup" | "results">("overview");

  const progress = Math.max(0, Math.min(100, status?.progress ?? 0));
  const isRunning = Boolean(status?.running && !status?.completed);
  const isPaused = Boolean(status?.paused);
  const canControl = Boolean(simulationId);

  const healthTone = useMemo(() => {
    const score = results?.average_health_score ?? 0;
    if (score >= 80) return "good";
    if (score >= 40) return "warn";
    return "bad";
  }, [results]);

  useEffect(() => {
    if (!simulationId || !isRunning) return;
    const timer = window.setInterval(async () => {
      try {
        const data = await api<Status>(`/simulations/${simulationId}`);
        setStatus(data);
        if (data.completed) {
          const finalResult = await api<Results>(`/simulations/${simulationId}/results`);
          setResults(finalResult);
          setActiveTab("results");
        }
      } catch {
        // Keep polling silent; the banner will surface explicit command errors.
      }
    }, 900);
    return () => window.clearInterval(timer);
  }, [simulationId, isRunning]);

  async function createSimulation() {
    setLoading(true);
    setNotice(null);
    try {
      const payload = {
        name,
        total_steps: steps,
        assets,
        scenarios: selectedScenarios.map((scenarioName) => ({
  scenario_id: `SCN-${scenarioName}`,
  name: scenarioName,
  category: getScenarioCategory(scenarioName),
  type: scenarioName,
  severity: 0.7,
  start_step: 0,
  duration_steps: steps,
})),
      };
      const created = await api<Status>("/simulations", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setSimulationId(created.simulation_id ?? null);
      setStatus(created);
      setResults(null);
      setNotice("Simulation created. Ready to run.");
      setActiveTab("overview");
    } catch (error) {
      setNotice(errorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  async function startSimulation() {
    if (!simulationId) return;
    setLoading(true);
    setNotice(null);
    try {
      const data = await api<Status>(`/simulations/${simulationId}/start`, { method: "POST" });
      setStatus(data);
      setNotice("Simulation started.");
    } catch (error) {
      setNotice(errorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  async function runToCompletion() {
    if (!simulationId) return;
    setLoading(true);
    setNotice(null);
    try {
      const data = await api<Results>(`/simulations/${simulationId}/run`, { method: "POST" });
      setResults(data);
      setStatus((previous) => ({ ...previous, completed: true, running: false, progress: 100 }));
      setActiveTab("results");
      setNotice("Simulation completed successfully.");
    } catch (error) {
      setNotice(errorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  async function control(action: "pause" | "resume" | "stop" | "reset") {
    if (!simulationId) return;
    setLoading(true);
    setNotice(null);
    try {
      const data = await api<Status>(`/simulations/${simulationId}/${action}`, { method: "POST" });
      setStatus(data);
      if (action === "reset") setResults(null);
      setNotice(`Simulation ${action} successful.`);
    } catch (error) {
      setNotice(errorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  function addAsset() {
    const next = assets.length + 1;
    setAssets([
      ...assets,
      {
        asset_id: `AST-${String(next).padStart(3, "0")}`,
        asset_name: `Asset ${next}`,
        asset_type: "RAIL",
        latitude: 13.0840 + next * 0.0001,
        longitude: 80.2720 + next * 0.0001,
        health_score: 95,
        degradation_rate: 0.05,
        age_days: 30,
      },
    ]);
  }

  function updateAsset(index: number, patch: Partial<Asset>) {
    setAssets((current) => current.map((asset, i) => (i === index ? { ...asset, ...patch } : asset)));
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark"><TrainFront size={22} /></div>
          <div>
            <div className="brand-title">TDOS <span>Sandbox</span></div>
            <div className="brand-subtitle">Track Digital Operations Simulation</div>
          </div>
        </div>
        <div className="topbar-right">
          <div className="connection"><span className="live-dot" /> Backend connected</div>
          <div className="version-pill">v1.0</div>
        </div>
      </header>

      <main className="page">
        <section className="hero">
          <div>
            <div className="eyebrow"><Sparkles size={15} /> RAILWAY DIGITAL OPERATIONS</div>
            <h1>Model the railway.<br /><em>Test the future.</em></h1>
            <p>Run realistic infrastructure scenarios, watch asset health evolve, and turn simulation data into maintenance insight.</p>
          </div>
          <div className="hero-orb">
            <div className="orb-ring ring-one" />
            <div className="orb-ring ring-two" />
            <TrainFront size={58} strokeWidth={1.4} />
          </div>
        </section>

        <nav className="tabs">
          <button className={activeTab === "overview" ? "tab active" : "tab"} onClick={() => setActiveTab("overview")}><Gauge size={17} /> Overview</button>
          <button className={activeTab === "setup" ? "tab active" : "tab"} onClick={() => setActiveTab("setup")}><Layers3 size={17} /> Simulation Setup</button>
          <button className={activeTab === "results" ? "tab active" : "tab"} onClick={() => setActiveTab("results")}><BarChart3 size={17} /> Results</button>
        </nav>

        {notice && (
          <div className="notice">
            <div><Zap size={17} /> {notice}</div>
            <button onClick={() => setNotice(null)}><X size={17} /></button>
          </div>
        )}

        {activeTab === "setup" && (
          <section className="content-grid">
            <div className="panel span-two">
              <div className="panel-head">
                <div><span className="section-kicker">01</span><h2>Simulation parameters</h2></div>
                <div className="small-status">{simulationId ? `ID ${simulationId}` : "Not created"}</div>
              </div>
              <div className="form-grid">
                <label className="field">
                  <span>Simulation name</span>
                  <input value={name} onChange={(e) => setName(e.target.value)} />
                </label>
                <label className="field">
                  <span>Total steps</span>
                  <input type="number" min={1} max={1000000} value={steps} onChange={(e) => setSteps(Number(e.target.value))} />
                </label>
              </div>
            </div>

            <div className="panel span-two">
              <div className="panel-head">
                <div><span className="section-kicker">02</span><h2>Railway assets</h2></div>
                <button className="ghost-button" onClick={addAsset}><Plus size={16} /> Add asset</button>
              </div>
              <div className="asset-table">
                <div className="asset-row asset-head"><span>ID</span><span>Name</span><span>Type</span><span>Health</span><span>Age</span></div>
                {assets.map((asset, index) => (
                  <div className="asset-row" key={asset.asset_id}>
                    <span className="mono">{asset.asset_id}</span>
                    <input value={asset.asset_name ?? ""} onChange={(e) => updateAsset(index, { asset_name: e.target.value })} />
                    <select value={asset.asset_type} onChange={(e) => updateAsset(index, { asset_type: e.target.value })}>
                      {ASSET_TYPES.map((type) => <option key={type}>{type}</option>)}
                    </select>
                    <input type="number" min={0} max={100} value={asset.health_score} onChange={(e) => updateAsset(index, { health_score: Number(e.target.value) })} />
                    <input type="number" min={0} value={asset.age_days} onChange={(e) => updateAsset(index, { age_days: Number(e.target.value) })} />
                  </div>
                ))}
              </div>
            </div>

            <div className="panel span-two">
              <div className="panel-head">
                <div><span className="section-kicker">03</span><h2>Scenario library</h2></div>
                <span className="small-status">{selectedScenarios.length} selected</span>
              </div>
              <div className="scenario-grid">
                {SCENARIOS.map((scenario) => {
                  const Icon = scenario.icon;
                  const selected = selectedScenarios.includes(scenario.name);
                  return (
                    <button
                      key={scenario.name}
                      className={`scenario-card ${selected ? "selected" : ""}`}
                      onClick={() => setSelectedScenarios((current) => selected ? current.filter((x) => x !== scenario.name) : [...current, scenario.name])}
                    >
                      <div className="scenario-icon"><Icon size={19} /></div>
                      <div className="scenario-copy"><strong>{scenario.label}</strong><span>{scenario.description}</span></div>
                      <div className="scenario-check">{selected && <CheckCircle2 size={18} />}</div>
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="action-bar span-two">
              <div><strong>Ready to simulate?</strong><span>Configure your railway and launch a live TDOS run.</span></div>
              <div className="action-buttons">
                <button className="secondary-button" onClick={() => setActiveTab("overview")}>Cancel</button>
                <button className="primary-button" disabled={loading} onClick={createSimulation}><Zap size={17} /> {loading ? "Creating..." : "Create simulation"}</button>
              </div>
            </div>
          </section>
        )}

        {activeTab === "overview" && (
          <section className="content-grid">
            <div className="panel run-panel span-two">
              <div className="panel-head">
                <div><span className="section-kicker">LIVE CONTROL</span><h2>{simulationId ? name : "No simulation loaded"}</h2></div>
                <StatusBadge status={status?.status} completed={status?.completed} paused={status?.paused} />
              </div>
              <div className="run-layout">
                <div className="progress-block">
                  <div className="progress-number">{Math.round(progress)}<small>%</small></div>
                  <div className="progress-track"><div className="progress-fill" style={{ width: `${progress}%` }} /></div>
                  <div className="progress-meta"><span>Step {status?.current_step ?? 0}</span><span>{status?.total_steps ?? steps} total</span></div>
                </div>
                <div className="control-stack">
                  <button className="primary-button large" disabled={!canControl || loading || isRunning} onClick={runToCompletion}><Play size={18} /> Run to completion</button>
                  <div className="control-row">
                    {!isPaused
                      ? <button className="secondary-button" disabled={!canControl || !isRunning || loading} onClick={() => control("pause")}><Pause size={16} /> Pause</button>
                      : <button className="secondary-button" disabled={!canControl || loading} onClick={() => control("resume")}><Play size={16} /> Resume</button>}
                    <button className="danger-button" disabled={!canControl || !isRunning || loading} onClick={() => control("stop")}><CircleStop size={16} /> Stop</button>
                    <button className="icon-button" title="Reset" disabled={!canControl || loading} onClick={() => control("reset")}><RotateCcw size={17} /></button>
                  </div>
                </div>
              </div>
            </div>

            <MetricCard icon={<ShieldCheck />} label="Healthy assets" value={results?.healthy_assets ?? "—"} detail={results ? `${results.total_assets} total assets` : "Run a simulation"} tone="green" />
            <MetricCard icon={<TriangleAlert />} label="Degraded assets" value={results?.degraded_assets ?? "—"} detail="Requires attention" tone="amber" />
            <MetricCard icon={<AlertTriangle />} label="Failed assets" value={results?.failed_assets ?? "—"} detail="Critical condition" tone="red" />
            <MetricCard icon={<Activity />} label="Average health" value={results ? results.average_health_score.toFixed(1) : "—"} detail="0–100 score" tone="blue" />

            <div className="panel span-two">
              <div className="panel-head"><div><span className="section-kicker">SIMULATION SNAPSHOT</span><h2>Operational health</h2></div><button className="link-button" onClick={() => setActiveTab("results")}>View full results <ChevronRight size={16} /></button></div>
              <div className="health-summary">
                <div className={`health-dial ${healthTone}`}><div><strong>{results ? Math.round(results.average_health_score) : "—"}</strong><span>HEALTH</span></div></div>
                <div className="health-copy">
                  <h3>{results ? healthHeadline(results.average_health_score) : "Your railway at a glance"}</h3>
                  <p>{results ? `Simulation ${results.simulation_name} completed in ${results.duration_seconds.toFixed(2)} seconds across ${results.simulation_steps} steps.` : "Create a simulation in Setup, then run it here. TDOS will stream the simulation state into this dashboard."}</p>
                  <div className="mini-bars">
                    <MiniBar label="Healthy" value={results?.healthy_assets ?? 0} total={results?.total_assets ?? 1} />
                    <MiniBar label="Degraded" value={results?.degraded_assets ?? 0} total={results?.total_assets ?? 1} />
                    <MiniBar label="Failed" value={results?.failed_assets ?? 0} total={results?.total_assets ?? 1} />
                  </div>
                </div>
              </div>
            </div>

            <div className="panel">
              <div className="panel-head"><div><span className="section-kicker">ACTIVE SCENARIOS</span><h2>Stressors</h2></div></div>
              <div className="active-scenarios">
                {selectedScenarios.length ? selectedScenarios.map((item) => <div className="active-scenario" key={item}><div className="tiny-icon"><AlertTriangle size={15} /></div><div><strong>{item.replace(/_/g, " ")}</strong><span>Severity 70%</span></div></div>) : <div className="empty-state">No active scenarios.</div>}
              </div>
            </div>

            <div className="panel">
              <div className="panel-head"><div><span className="section-kicker">PREDICTION</span><h2>AI outlook</h2></div><BrainCircuit size={20} className="accent-icon" /></div>
              {results?.prediction ? (
                <div className="prediction">
                  <div><span>Failure probability</span><strong>{Math.round(results.prediction.failure_probability * 100)}%</strong></div>
                  <div><span>Remaining useful life</span><strong>{results.prediction.remaining_useful_life_days} <small>days</small></strong></div>
                  <div><span>Confidence</span><strong>{Math.round(results.prediction.confidence * 100)}%</strong></div>
                </div>
              ) : <div className="empty-state">Run a simulation to generate prediction outputs.</div>}
            </div>
          </section>
        )}

        {activeTab === "results" && (
          <section className="content-grid">
            <div className="panel span-two">
              <div className="panel-head"><div><span className="section-kicker">FINAL OUTPUT</span><h2>Simulation results</h2></div>{results?.success && <div className="success-chip"><CheckCircle2 size={16} /> Completed successfully</div>}</div>
              {!results ? <div className="empty-large"><BarChart3 size={40} /><h3>No results yet</h3><p>Run a TDOS simulation and the final analysis will appear here.</p><button className="primary-button" onClick={() => setActiveTab("setup")}>Configure simulation</button></div> : (
                <>
                  <div className="result-grid">
                    <ResultStat label="Simulation" value={results.simulation_name} />
                    <ResultStat label="Steps" value={String(results.simulation_steps)} />
                    <ResultStat label="Duration" value={`${results.duration_seconds.toFixed(2)} s`} />
                    <ResultStat label="Average health" value={results.average_health_score.toFixed(1)} />
                  </div>
                  <div className="result-table">
                    <div className="result-row result-head"><span>Asset</span><span>Health</span><span>Risk</span><span>Maintenance</span><span>State</span></div>
                    {(results.asset_results ?? []).map((asset) => (
                      <div className="result-row" key={asset.asset_id}>
                        <span className="mono">{asset.asset_id}</span>
                        <span><HealthPill score={asset.health_score} /></span>
                        <span className="risk">{asset.predicted_risk}</span>
                        <span>{asset.maintenance_required ? "Required" : "Clear"}</span>
                        <span>{asset.failed ? <span className="bad-text">FAILED</span> : <span className="good-text">OPERATIONAL</span>}</span>
                      </div>
                    ))}
                  </div>
                </>
              )}
            </div>
          </section>
        )}
      </main>

      <footer className="footer">
        <span>TDOS Sandbox · Track Digital Operations</span>
        <span><SquareTerminal size={14} /> Simulation environment</span>
      </footer>
    </div>
  );
}

async function api<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers: { "Content-Type": "application/json", ...(options.headers ?? {}) },
  });
  if (!response.ok) {
    let message = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      message = typeof body.detail === "string" ? body.detail : JSON.stringify(body.detail ?? body);
    } catch {}
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

function getScenarioCategory(name: string): string {
  const weather = ["RAIN", "FLOOD", "FOG", "SNOW", "HEAT", "DUST"];
  const infrastructure = [
    "CRACK_GROWTH", "BALLAST_FAILURE", "SLEEPER_DAMAGE", "FASTENER_FAILURE",
    "TURNOUT_FAILURE", "RAIL_MISALIGNMENT", "BRIDGE_DEFORMATION",
  ];
  const sensor = [
    "GPS_FAILURE", "GPS_DRIFT", "CAMERA_FAILURE", "IR_FAILURE",
    "ULTRASONIC_FAILURE", "SENSOR_NOISE", "PACKET_LOSS",
  ];
  if (weather.includes(name)) return "WEATHER";
  if (infrastructure.includes(name)) return "INFRASTRUCTURE";
  if (sensor.includes(name)) return "SENSOR";
  return "OPERATION";
}

function errorMessage(error: unknown) {
  return error instanceof TypeError ? "Cannot reach the TDOS backend. Start FastAPI and check VITE_API_BASE_URL." : error instanceof Error ? error.message : "Unexpected error.";
}

function StatusBadge({ status, completed, paused }: { status?: string; completed?: boolean; paused?: boolean }) {
  const label = completed ? "COMPLETED" : paused ? "PAUSED" : status ?? "IDLE";
  return <span className={`status-badge ${label.toLowerCase()}`}><span />{label}</span>;
}

function MetricCard({ icon, label, value, detail, tone }: { icon: React.ReactNode; label: string; value: string | number; detail: string; tone: string }) {
  return <div className="metric-card"><div className={`metric-icon ${tone}`}>{icon}</div><div><span>{label}</span><strong>{value}</strong><small>{detail}</small></div></div>;
}

function MiniBar({ label, value, total }: { label: string; value: number; total: number }) {
  const width = Math.min(100, (value / total) * 100);
  return <div className="mini-bar"><div><span>{label}</span><b>{value}</b></div><div className="mini-track"><div style={{ width: `${width}%` }} /></div></div>;
}

function ResultStat({ label, value }: { label: string; value: string }) {
  return <div className="result-stat"><span>{label}</span><strong>{value}</strong></div>;
}

function HealthPill({ score }: { score: number }) {
  const cls = score >= 80 ? "good" : score >= 40 ? "warn" : "bad";
  return <span className={`health-pill ${cls}`}>{score.toFixed(1)}</span>;
}

function healthHeadline(score: number) {
  if (score >= 90) return "Railway condition is excellent.";
  if (score >= 80) return "Railway condition is healthy.";
  if (score >= 60) return "Early degradation is visible.";
  if (score >= 40) return "Attention is recommended.";
  return "Critical degradation detected.";
}


export default App;