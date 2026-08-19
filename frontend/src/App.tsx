import { useEffect, useMemo, useState } from "react";
import CommandCenter from "./CommandCenter";
import {
  Activity,
  AlertTriangle,
  BarChart3,
  BrainCircuit,
  CheckCircle2,
  ChevronRight,
  CircleStop,
  FlaskConical,
  CloudRain,
  Gauge,
  Info,
  Layers3,
  MapPin,
  Pause,
  Play,
  Plus,
  RotateCcw,
  Radio,
  ShieldCheck,
  Sparkles,
  Rocket,
  Check,
  ListChecks,
  SquareTerminal,
  TrainFront,
  Trash2,
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
  scenario_id: string;
  name: string;
  type: string;
  category: string;
  description: string;
  enabled: boolean;
  severity: number;
  probability: number;
  start_step: number;
  duration: number;
  target_asset: string | null;
  affected_assets: string[];
  parameters: Record<string, number | string | boolean>;
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

type ReplayAsset = Asset & {
  active?: boolean;
  under_maintenance?: boolean;
  failed?: boolean;
};

type ReplayFrame = {
  step: number;
  timestamp: string;
  assets: ReplayAsset[];
};

type ReplayResponse = {
  simulation_id: string;
  total_frames: number;
  duration_seconds: number;
  frames: ReplayFrame[];
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
    degradation?: number;
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
  metadata?: {
    engine?: string;
    version?: string;
    replay_frames?: string;
    digital_twins?: string;
    [key: string]: string | undefined;
  };
};


type RAMSComponent = {
  score: number;
  grade: string;
  rationale: string;
};

type RAMSAsset = {
  asset_id: string;
  asset_name: string;
  asset_type: string;
  rams_score: number;
  rams_grade: string;
  reliability: RAMSComponent;
  availability: RAMSComponent;
  maintainability: RAMSComponent;
  safety: RAMSComponent;
  failure_probability: number;
  remaining_useful_life_days: number;
  maintenance_priority: string;
  criticality: string;
  operational_availability_percent: number;
  health_score: number;
  failed: boolean;
};

type RAMSResult = {
  simulation_id: string;
  simulation_name: string;
  methodology: string;
  weights: Record<string, number>;
  fleet: {
    rams_score: number;
    rams_grade: string;
    reliability_score: number;
    availability_score: number;
    maintainability_score: number;
    safety_score: number;
    critical_assets: number;
    immediate_maintenance: number;
    high_priority_maintenance: number;
    fleet_operational_availability_percent: number;
  };
  assets: RAMSAsset[];
};

type Decision = {
  asset_id: string; asset_name: string; asset_type: string; priority: string; action: string; timing: string; reason: string;
  health_score: number; rams_score: number; failure_probability: number; remaining_useful_life_days: number; criticality: string;
  maintenance_required: boolean; factors: Record<string, number>;
};
type DecisionResult = { simulation_id: string; simulation_name: string; methodology: string; summary: { critical:number; high:number; medium:number; low:number; immediate_actions:number; planned_actions:number }; decisions: Decision[] };
type WhatIfResult = { asset_id:string; asset_name:string; intervention:{health_recovery:number; degradation_reduction_percent:number}; before:Decision; after:Decision; changes:{health_score:number; rams_score:number; failure_probability:number; remaining_useful_life_days:number}; scenario_id?:string; scenario_name?:string };
type WhatIfBatchResult = { simulation_id:string; scenario_count:number; scenarios:WhatIfResult[] };
type WhatIfScenario = { id:string; name:string; asset_id:string; health_recovery:number; degradation_reduction_percent:number };

const SCENARIO_LIBRARY: Array<{
  name: string;
  label: string;
  category: string;
  description: string;
  icon: typeof CloudRain;
  defaultSeverity: number;
}> = [
  { name: "RAIN", label: "Heavy Rain", category: "WEATHER", description: "Sustained rainfall and moisture stress across railway infrastructure.", icon: CloudRain, defaultSeverity: 0.65 },
  { name: "FLOOD", label: "Flood", category: "WEATHER", description: "Flooding stress affecting vulnerable infrastructure zones.", icon: TriangleAlert, defaultSeverity: 0.75 },
  { name: "CRACK_GROWTH", label: "Crack Growth", category: "INFRASTRUCTURE", description: "Progressive structural degradation and increasing failure exposure.", icon: AlertTriangle, defaultSeverity: 0.70 },
  { name: "BALLAST_FAILURE", label: "Ballast Failure", category: "INFRASTRUCTURE", description: "Progressive ballast condition loss and track-support degradation.", icon: Layers3, defaultSeverity: 0.60 },
  { name: "GPS_DRIFT", label: "GPS Drift", category: "SENSOR", description: "Positioning uncertainty affecting operational awareness.", icon: MapPin, defaultSeverity: 0.45 },
  { name: "TRAIN_OVERLOAD", label: "Train Overload", category: "OPERATION", description: "Elevated operational loading across railway assets.", icon: TrainFront, defaultSeverity: 0.55 },
  { name: "MAINTENANCE_DELAY", label: "Maintenance Delay", category: "OPERATION", description: "Delays planned maintenance and increases exposure duration.", icon: RotateCcw, defaultSeverity: 0.50 },
  { name: "INSPECTION_SKIP", label: "Inspection Skip", category: "OPERATION", description: "Removes an expected inspection opportunity during the simulation.", icon: ShieldCheck, defaultSeverity: 0.45 },
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
  const [selectedScenarios, setSelectedScenarios] = useState<Scenario[]>([
    {
      scenario_id: "SCN-CRACK_GROWTH-01",
      name: "Crack Growth",
      type: "CRACK_GROWTH",
      category: "INFRASTRUCTURE",
      description: "Progressive structural degradation and increasing failure exposure.",
      enabled: true,
      severity: 0.70,
      probability: 0.90,
      start_step: 10,
      duration: 80,
      target_asset: "AST-001",
      affected_assets: ["AST-001"],
      parameters: {},
    },
  ]);
  const [simulationId, setSimulationId] = useState<string | null>(null);
  const [status, setStatus] = useState<Status | null>(null);
  const [results, setResults] = useState<Results | null>(null);
  const [rams, setRams] = useState<RAMSResult | null>(null);
  const [decisions, setDecisions] = useState<DecisionResult | null>(null);
  const [whatIf, setWhatIf] = useState<WhatIfBatchResult | null>(null);
  const [whatIfRunning, setWhatIfRunning] = useState(false);
  const [whatIfScenarios, setWhatIfScenarios] = useState<WhatIfScenario[]>([]);
  const [replay, setReplay] = useState<ReplayResponse | null>(null);
  const [selectedReplayAsset, setSelectedReplayAsset] = useState<string>("");
  const [replayStep, setReplayStep] = useState(0);
  const [isReplayPlaying, setIsReplayPlaying] = useState(false);
  const [replaySpeed, setReplaySpeed] = useState(1);
  const [loading, setLoading] = useState(false);
  const [notice, setNotice] = useState<string | null>(null);
  const [demoMode, setDemoMode] = useState(false);
  const [demoRunning, setDemoRunning] = useState(false);
  const [demoStage, setDemoStage] = useState(0);
  const [activeTab, setActiveTab] = useState<"command" | "overview" | "setup" | "results" | "replay" | "rams" | "decisions">("overview");

  const progress = Math.max(0, Math.min(100, status?.progress ?? 0));
  const isRunning = Boolean(status?.running && !status?.completed);
  const isPaused = Boolean(status?.paused);
  const canControl = Boolean(simulationId);

  useEffect(() => {
    if (!isReplayPlaying || !replay?.frames.length) return;

    const lastIndex = replay.frames.length - 1;

    if (replayStep >= lastIndex) {
      setIsReplayPlaying(false);
      return;
    }

    const timer = window.setInterval(() => {
      setReplayStep((current) => {
        if (current >= lastIndex) {
          setIsReplayPlaying(false);
          return lastIndex;
        }
        return current + 1;
      });
    }, Math.max(70, Math.round(650 / replaySpeed)));

    return () => window.clearInterval(timer);
  }, [isReplayPlaying, replay, replayStep, replaySpeed]);

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
          await loadReplay(simulationId);
          await loadRams(simulationId);
          await loadDecisions(simulationId);
          setActiveTab("results");
        }
      } catch {
        // Keep polling silent; the banner will surface explicit command errors.
      }
    }, 900);
    return () => window.clearInterval(timer);
  }, [simulationId, isRunning]);

  // Load analytics intelligence on demand after a completed simulation.
  // This prevents Replay/RAMS/Decisions from appearing empty when their
  // initial background load failed or the user switches tabs later.
  useEffect(() => {
    if (!simulationId || !results) return;

    if (activeTab === "replay" && !replay) {
      void loadReplay(simulationId);
    }

    if (activeTab === "rams" && !rams) {
      void loadRams(simulationId);
    }

    if (activeTab === "decisions" && !decisions) {
      void loadDecisions(simulationId);
    }
  }, [activeTab, simulationId, results, replay, rams, decisions]);

  async function loadReplay(id: string) {
    try {
      const data = await api<ReplayResponse>(`/simulations/${id}/replay`);
      setReplay(data);
      setReplayStep(Math.max(0, data.frames.length - 1));
      if (data.frames.length) {
        setSelectedReplayAsset((current) => current || data.frames[0].assets[0]?.asset_id || "");
      }
    } catch (error) {
      setReplay(null);
      setNotice(errorMessage(error));
    }
  }

  async function loadRams(id: string) {
    try {
      const data = await api<RAMSResult>(`/simulations/${id}/rams`);
      setRams(data);
    } catch (error) {
      setRams(null);
      setNotice(errorMessage(error));
    }
  }

  async function loadDecisions(id: string) {
    try {
      const data = await api<DecisionResult>(`/simulations/${id}/decision-support`);
      setDecisions(data);
      setWhatIf(null);
      setWhatIfScenarios(data.decisions.length ? [{ id: crypto.randomUUID(), name: "Scenario 1", asset_id: data.decisions[0].asset_id, health_recovery: 15, degradation_reduction_percent: 30 }] : []);
    } catch (error) {
      setDecisions(null);
      setNotice(errorMessage(error));
    }
  }

  function addWhatIfScenario() {
    if (!decisions || whatIfScenarios.length >= 12) return;
    const firstAsset = decisions.decisions[0]?.asset_id ?? "";
    setWhatIfScenarios((current) => [
      ...current,
      {
        id: crypto.randomUUID(),
        name: `Scenario ${current.length + 1}`,
        asset_id: firstAsset,
        health_recovery: 15,
        degradation_reduction_percent: 30,
      },
    ]);
  }

  function updateWhatIfScenario(id: string, patch: Partial<WhatIfScenario>) {
    setWhatIfScenarios((current) => current.map((scenario) => scenario.id === id ? { ...scenario, ...patch } : scenario));
  }

  function removeWhatIfScenario(id: string) {
    setWhatIfScenarios((current) => current.filter((scenario) => scenario.id !== id));
  }

  async function runWhatIf() {
    if (!simulationId || !whatIfScenarios.length || !decisions) {
      setNotice("Run a simulation and configure at least one maintenance strategy first.");
      return;
    }

    setWhatIfRunning(true);
    setNotice(null);

    const payload = {
      scenarios: whatIfScenarios.map((scenario) => ({
        scenario_id: scenario.id,
        scenario_name: scenario.name,
        asset_id: scenario.asset_id,
        health_recovery: scenario.health_recovery,
        degradation_reduction_percent: scenario.degradation_reduction_percent,
      })),
    };

    try {
      const data = await api<WhatIfBatchResult>(`/simulations/${simulationId}/maintenance-what-if/batch`, {
        method: "POST",
        body: JSON.stringify(payload),
      });
      setWhatIf(data);
      setNotice(`Compared ${data.scenario_count} maintenance strateg${data.scenario_count === 1 ? "y" : "ies"} successfully.`);
    } catch (error) {
      setWhatIf(null);
      setNotice(errorMessage(error));
    } finally {
      setWhatIfRunning(false);
    }
  }

  function addScenario(type: string) {
    if (selectedScenarios.length >= 12) {
      setNotice("Maximum of 12 scenarios per simulation.");
      return;
    }

    const definition = SCENARIO_LIBRARY.find((item) => item.name === type);
    if (!definition) return;

    const occurrence = selectedScenarios.filter((item) => item.type === type).length + 1;
    const firstAsset = assets[0]?.asset_id ?? null;

    const scenario: Scenario = {
      scenario_id: `SCN-${type}-${String(occurrence).padStart(2, "0")}`,
      name: `${definition.label}${occurrence > 1 ? ` ${occurrence}` : ""}`,
      type: definition.name,
      category: definition.category,
      description: definition.description,
      enabled: true,
      severity: definition.defaultSeverity,
      probability: 0.85,
      start_step: 0,
      duration: steps,
      target_asset: firstAsset,
      affected_assets: firstAsset ? [firstAsset] : [],
      parameters: {},
    };

    setSelectedScenarios((current) => [...current, scenario]);
  }

  function updateScenario(scenarioId: string, patch: Partial<Scenario>) {
    setSelectedScenarios((current) =>
      current.map((scenario) =>
        scenario.scenario_id === scenarioId ? { ...scenario, ...patch } : scenario
      )
    );
  }

  function removeScenario(scenarioId: string) {
    setSelectedScenarios((current) =>
      current.filter((scenario) => scenario.scenario_id !== scenarioId)
    );
  }

  function toggleScenarioAsset(scenarioId: string, assetId: string) {
    setSelectedScenarios((current) =>
      current.map((scenario) => {
        if (scenario.scenario_id !== scenarioId) return scenario;

        const exists = scenario.affected_assets.includes(assetId);
        const affected_assets = exists
          ? scenario.affected_assets.filter((id) => id !== assetId)
          : [...scenario.affected_assets, assetId];

        return { ...scenario, affected_assets };
      })
    );
  }

  async function createSimulation() {
    setLoading(true);
    setNotice(null);

    try {
      const activeScenarios = selectedScenarios.filter((scenario) => scenario.enabled);

      if (!activeScenarios.length) {
        throw new Error("Add at least one enabled scenario before creating the simulation.");
      }

      const payload = {
        name,
        total_steps: steps,
        assets,
        scenarios: activeScenarios.map((scenario) => ({
          scenario_id: scenario.scenario_id,
          name: scenario.name,
          category: scenario.category,
          type: scenario.type,
          description: scenario.description,
          enabled: scenario.enabled,
          severity: scenario.severity,
          probability: scenario.probability,
          start_step: scenario.start_step,
          duration_steps: scenario.duration,
          target_asset: scenario.target_asset,
          affected_assets: scenario.affected_assets,
          parameters: scenario.parameters,
        })),
      };

      const created = await api<Status>("/simulations", {
        method: "POST",
        body: JSON.stringify(payload),
      });

      setSimulationId(created.simulation_id ?? null);
      setStatus(created);
      setResults(null);
      setRams(null);
      setDecisions(null);
      setWhatIf(null);
      setReplay(null);
      setReplayStep(0);
      setSelectedReplayAsset("");
      setNotice(`Simulation created with ${activeScenarios.length} active scenario${activeScenarios.length === 1 ? "" : "s"}.`);
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
      await loadReplay(simulationId);
      await loadRams(simulationId);
      await loadDecisions(simulationId);
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
      if (action === "reset") {
        setResults(null);
        setRams(null);
        setReplay(null);
        setReplayStep(0);
        setSelectedReplayAsset("");
      }
      setNotice(`Simulation ${action} successful.`);
    } catch (error) {
      setNotice(errorMessage(error));
    } finally {
      setLoading(false);
    }
  }

  async function runDemoMode() {
    if (demoRunning) return;
    setDemoRunning(true);
    setDemoMode(true);
    setDemoStage(1);
    setNotice(null);

    try {
      const demoAssets = [
        { ...assets[0], asset_id: "AST-001", asset_name: "Mainline Rail A", health_score: 96, degradation_rate: 0.08 },
        { ...assets[1], asset_id: "AST-002", asset_name: "Sleeper Cluster A", health_score: 91, degradation_rate: 0.05 },
        { ...assets[2], asset_id: "AST-003", asset_name: "Turnout 01", health_score: 88, degradation_rate: 0.11 },
      ];

      const demoScenarios = selectedScenarios.length ? selectedScenarios : [{
        scenario_id: "SCN-CRACK_GROWTH-01", name: "Crack Growth", type: "CRACK_GROWTH", category: "INFRASTRUCTURE",
        description: "Progressive structural degradation and increasing failure exposure.", enabled: true, severity: 0.7, probability: 0.9,
        start_step: 10, duration: steps, target_asset: "AST-001", affected_assets: ["AST-001"], parameters: {},
      }];

      setAssets(demoAssets);
      setSteps(100);
      setName("TDOS Command Center Demonstration");

      setDemoStage(2);
      const created = await api<Status>("/simulations", {
        method: "POST",
        body: JSON.stringify({
          name: "TDOS Command Center Demonstration",
          total_steps: 100,
          assets: demoAssets,
          scenarios: demoScenarios.filter((scenario) => scenario.enabled).map((scenario) => ({
            scenario_id: scenario.scenario_id, name: scenario.name, category: scenario.category, type: scenario.type,
            description: scenario.description, enabled: true, severity: scenario.severity, probability: scenario.probability,
            start_step: scenario.start_step, duration_steps: scenario.duration, target_asset: scenario.target_asset,
            affected_assets: scenario.affected_assets, parameters: scenario.parameters,
          })),
        }),
      });

      const id = created.simulation_id;
      if (!id) throw new Error("Demo simulation could not be created.");
      setSimulationId(id);
      setStatus(created);

      setDemoStage(3);
      const finalResult = await api<Results>(`/simulations/${id}/run`, { method: "POST" });
      setResults(finalResult);

      setDemoStage(4);
      await loadReplay(id);
      await loadRams(id);
      await loadDecisions(id);

      setStatus({ ...created, completed: true, running: false, progress: 100, current_step: 100, total_steps: 100 });
      setActiveTab("command");
      setDemoStage(5);
      setNotice("Demo simulation completed. Explore the Command Center, Replay, RAMS and Decisions.");
    } catch (error) {
      setNotice(errorMessage(error));
      setDemoStage(0);
    } finally {
      setDemoRunning(false);
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
            <div className="brand-title brand-display">TDOS <span>Sandbox</span></div>
            <div className="brand-subtitle">Track Digital Operations Simulation</div>
          </div>
        </div>
        <div className="topbar-right">
          <button className="demo-launch" onClick={runDemoMode} disabled={demoRunning}>
            <Rocket size={15} /> {demoRunning ? "Running Demo" : "Run Demo"}
          </button>
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
           <button className={activeTab === "replay" ? "tab active" : "tab"} onClick={() => setActiveTab("replay")}><Activity size={17} /> Replay</button>
           <button className={activeTab === "rams" ? "tab active" : "tab"} onClick={() => setActiveTab("rams")}><ShieldCheck size={17} /> RAMS</button>
           <button className={activeTab === "decisions" ? "tab active" : "tab"} onClick={() => setActiveTab("decisions")}><Zap size={17} /> Decisions</button>
           <button className={activeTab === "command" ? "tab active command-tab" : "tab command-tab"} onClick={() => setActiveTab("command")}><Radio size={17} /> Command Center</button>
         </nav>

        {notice && (
          <div className="notice">
            <div><Zap size={17} /> {notice}</div>
            <button onClick={() => setNotice(null)}><X size={17} /></button>
          </div>
        )}

        {demoMode && (
          <section className="demo-console panel span-two">
            <div className="demo-console-head">
              <div>
                <span className="section-kicker">FINAL DEMO MODE</span>
                <h2>TDOS end-to-end demonstration</h2>
                <p>One run drives the complete operational workflow from scenario execution to digital twin replay and maintenance intelligence.</p>
              </div>
              <button className="icon-button" onClick={() => setDemoMode(false)} aria-label="Close demo panel"><X size={17} /></button>
            </div>
            <div className="demo-steps">
              {["Configure", "Create simulation", "Run engine", "Load intelligence", "Ready"].map((label, index) => {
                const step = index + 1;
                const complete = demoStage >= step;
                const current = demoStage === step && demoRunning;
                return (
                  <div className={`demo-step ${complete ? "complete" : ""} ${current ? "current" : ""}`} key={label}>
                    <div className="demo-step-icon">{complete ? <Check size={14} /> : step}</div>
                    <span>{label}</span>
                  </div>
                );
              })}
            </div>
            {!demoRunning && demoStage === 5 && (
              <div className="demo-ready">
                <ListChecks size={18} />
                <span><strong>Demo ready.</strong> Use the navigation above to walk through the complete TDOS workflow.</span>
              </div>
            )}
          </section>
        )}

        {activeTab === "command" && (
          <CommandCenter
            results={results}
            assets={assets}
          />
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

            <div className="panel span-two scenario-lab-panel">
              <div className="panel-head">
                <div>
                  <span className="section-kicker">03 · SCENARIO LAB</span>
                  <h2>Build the operating environment</h2>
                  <p className="scenario-lab-subtitle">Configure independent stressors, timing, probability and asset impact before the simulation begins.</p>
                </div>
                <div className="scenario-lab-count">{selectedScenarios.length}/12 configured</div>
              </div>

              <div className="scenario-library">
                <div className="scenario-library-head">
                  <span>AVAILABLE STRESSORS</span>
                  <small>Select a scenario to add it to the experiment.</small>
                </div>
                <div className="scenario-library-grid">
                  {SCENARIO_LIBRARY.map((definition) => {
                    const Icon = definition.icon;
                    const count = selectedScenarios.filter((scenario) => scenario.type === definition.name).length;
                    return (
                      <button
                        key={definition.name}
                        type="button"
                        className={`scenario-library-card ${count > 0 ? "configured" : ""}`}
                        disabled={selectedScenarios.length >= 12}
                        onClick={() => addScenario(definition.name)}
                      >
                        <div className="scenario-library-icon"><Icon size={18} /></div>
                        <div className="scenario-library-copy">
                          <strong>{definition.label}</strong>
                          <span>{definition.description}</span>
                        </div>
                        {count > 0 && <div className="scenario-library-badge">{count}</div>}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div className="configured-scenarios">
                <div className="configured-scenarios-head">
                  <div>
                    <span>CONFIGURED SCENARIOS</span>
                    <small>Each scenario can target different infrastructure and time windows.</small>
                  </div>
                  <strong>{selectedScenarios.length}</strong>
                </div>

                {selectedScenarios.length === 0 ? (
                  <div className="scenario-empty-state">
                    <Sparkles size={24} />
                    <strong>No scenarios configured</strong>
                    <span>Add a stressor above to begin building your simulation environment.</span>
                  </div>
                ) : (
                  <div className="configured-scenario-list">
                    {selectedScenarios.map((scenario, index) => {
                      const definition = SCENARIO_LIBRARY.find((item) => item.name === scenario.type);
                      const Icon = definition?.icon ?? AlertTriangle;
                      const endStep = Math.min(steps, scenario.start_step + scenario.duration);
                      return (
                        <div className={`configured-scenario ${scenario.enabled ? "" : "disabled"}`} key={scenario.scenario_id}>
                          <div className="configured-scenario-header">
                            <div className="configured-scenario-title">
                              <div className="scenario-number">{String(index + 1).padStart(2, "0")}</div>
                              <div className="configured-scenario-icon"><Icon size={17} /></div>
                              <div>
                                <strong>{scenario.name}</strong>
                                <span>{scenario.category} · {scenario.type}</span>
                              </div>
                            </div>
                            <div className="configured-scenario-actions">
                              <button
                                type="button"
                                className={scenario.enabled ? "scenario-toggle enabled" : "scenario-toggle"}
                                onClick={() => updateScenario(scenario.scenario_id, { enabled: !scenario.enabled })}
                              >
                                <span />{scenario.enabled ? "ENABLED" : "DISABLED"}
                              </button>
                              <button
                                type="button"
                                className="scenario-delete"
                                onClick={() => removeScenario(scenario.scenario_id)}
                                title="Remove scenario"
                              >
                                <Trash2 size={14} />
                              </button>
                            </div>
                          </div>

                          <div className="scenario-config-grid">
                            <label className="scenario-field">
                              <span>Scenario name</span>
                              <input value={scenario.name} onChange={(e) => updateScenario(scenario.scenario_id, { name: e.target.value })} />
                            </label>

                            <label className="scenario-field">
                              <span>Target asset</span>
                              <select
                                value={scenario.target_asset ?? ""}
                                onChange={(e) => {
                                  const value = e.target.value || null;
                                  updateScenario(scenario.scenario_id, {
                                    target_asset: value,
                                    affected_assets: value ? [value] : scenario.affected_assets,
                                  });
                                }}
                              >
                                <option value="">Entire railway</option>
                                {assets.map((asset) => <option key={asset.asset_id} value={asset.asset_id}>{asset.asset_name ?? asset.asset_id}</option>)}
                              </select>
                            </label>

                            <label className="scenario-field">
                              <span>Start step</span>
                              <input
                                type="number"
                                min={0}
                                max={Math.max(0, steps - 1)}
                                value={scenario.start_step}
                                onChange={(e) => updateScenario(scenario.scenario_id, { start_step: Math.min(Math.max(0, Number(e.target.value)), Math.max(0, steps - 1)) })}
                              />
                            </label>

                            <label className="scenario-field">
                              <span>Duration</span>
                              <input
                                type="number"
                                min={1}
                                max={Math.max(1, steps)}
                                value={scenario.duration}
                                onChange={(e) => updateScenario(scenario.scenario_id, { duration: Math.min(Math.max(1, Number(e.target.value)), Math.max(1, steps)) })}
                              />
                            </label>
                          </div>

                          <div className="scenario-slider-grid">
                            <div className="scenario-slider-block">
                              <div className="scenario-slider-label"><span>SEVERITY</span><strong>{Math.round(scenario.severity * 100)}%</strong></div>
                              <input type="range" min={0} max={100} value={Math.round(scenario.severity * 100)} onChange={(e) => updateScenario(scenario.scenario_id, { severity: Number(e.target.value) / 100 })} />
                              <small>Impact intensity</small>
                            </div>
                            <div className="scenario-slider-block">
                              <div className="scenario-slider-label"><span>OCCURRENCE PROBABILITY</span><strong>{Math.round(scenario.probability * 100)}%</strong></div>
                              <input type="range" min={0} max={100} value={Math.round(scenario.probability * 100)} onChange={(e) => updateScenario(scenario.scenario_id, { probability: Number(e.target.value) / 100 })} />
                              <small>Likelihood of occurrence</small>
                            </div>
                          </div>

                          <div className="scenario-assets-block">
                            <div className="scenario-assets-head"><span>AFFECTED ASSETS</span><small>{scenario.affected_assets.length} selected</small></div>
                            <div className="scenario-assets-list">
                              {assets.map((asset) => {
                                const active = scenario.affected_assets.includes(asset.asset_id);
                                return (
                                  <button
                                    key={asset.asset_id}
                                    type="button"
                                    className={active ? "scenario-asset-chip active" : "scenario-asset-chip"}
                                    onClick={() => toggleScenarioAsset(scenario.scenario_id, asset.asset_id)}
                                  >
                                    <span>{asset.asset_id}</span>
                                    {asset.asset_name && <small>{asset.asset_name}</small>}
                                    {active && <CheckCircle2 size={13} />}
                                  </button>
                                );
                              })}
                            </div>
                          </div>

                          <div className="scenario-timeline">
                            <div className="scenario-timeline-label"><span>SIMULATION WINDOW</span><strong>STEP {scenario.start_step} → {endStep}</strong></div>
                            <div className="scenario-timeline-track">
                              <div
                                className="scenario-timeline-fill"
                                style={{
                                  left: `${Math.min(100, (scenario.start_step / Math.max(1, steps)) * 100)}%`,
                                  width: `${Math.max(0, ((endStep - scenario.start_step) / Math.max(1, steps)) * 100)}%`,
                                }}
                              />
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}
              </div>

              <div className="scenario-lab-footer">
                 <div>
                   <strong>{selectedScenarios.filter((scenario) => scenario.enabled).length} active stressors</strong>
                   <span>The configured environment will be frozen into the simulation when created.</span>
                 </div>
                 <span className="scenario-lab-ready">Ready for the final simulation action below.</span>
               </div>
             </div>

             <div className="action-bar span-two">
              <div><strong>Ready to simulate?</strong><span>Configure your railway and launch a live TDOS run.</span></div>
              <div className="action-buttons">
                <button className="secondary-button" onClick={() => setActiveTab("overview")}>Cancel</button>
                <button className="primary-button create-button" disabled={loading} onClick={createSimulation}>{loading ? "Creating..." : "Create simulation"}</button>
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
                {selectedScenarios.filter((scenario) => scenario.enabled).length ? selectedScenarios.filter((scenario) => scenario.enabled).map((scenario) => (
                  <div className="active-scenario" key={scenario.scenario_id}>
                    <div className="tiny-icon"><AlertTriangle size={15} /></div>
                    <div>
                      <strong>{scenario.name}</strong>
                      <span>{Math.round(scenario.severity * 100)}% severity · {Math.round(scenario.probability * 100)}% probability · Step {scenario.start_step} → {Math.min(steps, scenario.start_step + scenario.duration)}</span>
                    </div>
                  </div>
                )) : <div className="empty-state">No active scenarios.</div>}
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
          <section className="content-grid results-page">
            <div className="panel span-two results-hero">
              <div className="results-hero-copy">
                <span className="section-kicker">FINAL OUTPUT</span>
                <h2>{results ? "Simulation intelligence" : "Simulation results"}</h2>
                <p>
                  {results
                    ? `TDOS completed ${results.simulation_steps} simulation steps and evaluated ${results.total_assets} railway assets.`
                    : "Run a TDOS simulation and the final analysis will appear here."}
                </p>
              </div>
              {results?.success && (
                <div className="success-chip">
                  <CheckCircle2 size={16} /> Completed successfully
                </div>
              )}
            </div>

            {!results ? (
              <div className="panel span-two">
                <div className="empty-large">
                  <BarChart3 size={40} />
                  <h3>No results yet</h3>
                  <p>Run a TDOS simulation and the final analysis will appear here.</p>
                  <button className="primary-button" onClick={() => setActiveTab("setup")}>Configure simulation</button>
                </div>
              </div>
            ) : (
              <>
                <MetricCard icon={<Gauge />} label="Average health" value={results.average_health_score.toFixed(1)} detail="Overall asset condition" tone="blue" />
                <MetricCard icon={<ShieldCheck />} label="Healthy assets" value={results.healthy_assets} detail={`${results.total_assets} assets evaluated`} tone="green" />
                <MetricCard icon={<TriangleAlert />} label="Needs attention" value={results.degraded_assets} detail="Degraded condition" tone="amber" />
                <MetricCard icon={<AlertTriangle />} label="Failed assets" value={results.failed_assets} detail="Critical condition" tone="red" />

                <div className="panel span-two">
                  <div className="panel-head">
                    <div><span className="section-kicker">AI OUTLOOK</span><h2>Predictive intelligence</h2></div>
                    <BrainCircuit size={20} className="accent-icon" />
                  </div>
                  {results.prediction ? (
                    <div
                      className="prediction-grid"
                      style={{
                        display: "grid",
                        gridTemplateColumns: "repeat(4, minmax(0, 1fr))",
                        gap: 24,
                        marginTop: 24,
                      }}
                    >
                      <div className="prediction-feature" style={{ display: "flex", flexDirection: "column", gap: 7, minWidth: 0 }}>
                        <span style={{ color: "#7d8789", fontSize: 10, lineHeight: 1.35 }}>Failure probability</span>
                        <strong style={{ display: "flex", alignItems: "baseline", gap: 2, fontFamily: "Manrope, sans-serif", fontSize: 28, lineHeight: 1, letterSpacing: "-.045em" }}>
                          {Math.round(results.prediction.failure_probability * 100)}
                          <small style={{ fontSize: 12, letterSpacing: 0 }}>%</small>
                        </strong>
                        <div className="prediction-track" style={{ marginTop: 4 }}>
                          <div style={{ width: `${Math.min(100, results.prediction.failure_probability * 100)}%` }} />
                        </div>
                      </div>

                      <div className="prediction-feature" style={{ display: "flex", flexDirection: "column", gap: 7, minWidth: 0 }}>
                        <span style={{ color: "#7d8789", fontSize: 10, lineHeight: 1.35 }}>Predicted health</span>
                        <strong style={{ display: "flex", alignItems: "baseline", gap: 3, fontFamily: "Manrope, sans-serif", fontSize: 28, lineHeight: 1, letterSpacing: "-.045em" }}>
                          {results.prediction.predicted_health_score.toFixed(1)}
                          <small style={{ fontSize: 12, letterSpacing: 0 }}>/100</small>
                        </strong>
                        <em style={{ color: "#9aa1a1", fontSize: 9, fontStyle: "normal", lineHeight: 1.4 }}>Projected asset condition</em>
                      </div>

                      <div className="prediction-feature" style={{ display: "flex", flexDirection: "column", gap: 7, minWidth: 0 }}>
                        <span style={{ color: "#7d8789", fontSize: 10, lineHeight: 1.35 }}>Remaining useful life</span>
                        <strong style={{ display: "flex", alignItems: "baseline", gap: 4, fontFamily: "Manrope, sans-serif", fontSize: 28, lineHeight: 1, letterSpacing: "-.045em" }}>
                          {results.prediction.remaining_useful_life_days}
                          <small style={{ fontSize: 11, letterSpacing: 0 }}>days</small>
                        </strong>
                        <em style={{ color: "#9aa1a1", fontSize: 9, fontStyle: "normal", lineHeight: 1.4 }}>Estimated operational life</em>
                      </div>

                      <div className="prediction-feature" style={{ display: "flex", flexDirection: "column", gap: 7, minWidth: 0 }}>
                        <span style={{ color: "#7d8789", fontSize: 10, lineHeight: 1.35 }}>Model confidence</span>
                        <strong style={{ display: "flex", alignItems: "baseline", gap: 2, fontFamily: "Manrope, sans-serif", fontSize: 28, lineHeight: 1, letterSpacing: "-.045em" }}>
                          {Math.round(results.prediction.confidence * 100)}
                          <small style={{ fontSize: 12, letterSpacing: 0 }}>%</small>
                        </strong>
                        <em style={{ color: "#9aa1a1", fontSize: 9, fontStyle: "normal", lineHeight: 1.4 }}>Prediction confidence</em>
                      </div>
                    </div>
                  ) : <div className="empty-state">Prediction outputs are unavailable for this run.</div>}
                </div>

                <div className="panel">
                  <div className="panel-head">
                    <div><span className="section-kicker">DIGITAL TWIN</span><h2>Live twin registry</h2></div>
                    <Layers3 size={20} className="accent-icon" />
                  </div>
                  <div
                    className="twin-summary"
                    style={{
                      display: "grid",
                      gridTemplateColumns: "auto minmax(0, 1fr)",
                      alignItems: "center",
                      gap: 22,
                      marginTop: 24,
                    }}
                  >
                    <div
                      className="twin-count"
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 3,
                        minWidth: 78,
                      }}
                    >
                      <strong style={{ fontFamily: "Manrope, sans-serif", fontSize: 30, lineHeight: 1, letterSpacing: "-.05em" }}>
                        {results.metadata?.digital_twins ?? results.total_assets}
                      </strong>
                      <span style={{ color: "#8b9293", fontSize: 9, textTransform: "uppercase", letterSpacing: ".07em", fontWeight: 800 }}>
                        active twins
                      </span>
                    </div>

                    <div
                      className="twin-copy"
                      style={{
                        display: "flex",
                        flexDirection: "column",
                        gap: 6,
                        minWidth: 0,
                        paddingLeft: 18,
                        borderLeft: "1px solid #eee9dd",
                      }}
                    >
                      <strong style={{ fontSize: 11, lineHeight: 1.3 }}>Asset states synchronized</strong>
                      <span style={{ color: "#8b9293", fontSize: 9, lineHeight: 1.5 }}>
                        Digital Twins tracked throughout the simulation run.
                      </span>
                    </div>
                  </div>
                </div>

                <div className="panel">
                  <div className="panel-head">
                    <div><span className="section-kicker">RUN METADATA</span><h2>Execution profile</h2></div>
                    <Activity size={20} className="accent-icon" />
                  </div>
                  <div
                    className="metadata-list"
                    style={{
                      display: "grid",
                      gap: 0,
                      marginTop: 24,
                    }}
                  >
                    <div style={{ display: "grid", gridTemplateColumns: "1fr auto", alignItems: "center", gap: 16, padding: "9px 0", borderBottom: "1px solid #eee9dd" }}>
                      <span style={{ color: "#8b9293", fontSize: 9 }}>Simulation ID</span>
                      <strong className="mono" style={{ fontSize: 9, textAlign: "right" }}>{results.simulation_id}</strong>
                    </div>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr auto", alignItems: "center", gap: 16, padding: "9px 0", borderBottom: "1px solid #eee9dd" }}>
                      <span style={{ color: "#8b9293", fontSize: 9 }}>Duration</span>
                      <strong style={{ fontSize: 10, textAlign: "right" }}>{results.duration_seconds.toFixed(2)} s</strong>
                    </div>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr auto", alignItems: "center", gap: 16, padding: "9px 0", borderBottom: "1px solid #eee9dd" }}>
                      <span style={{ color: "#8b9293", fontSize: 9 }}>Replay frames</span>
                      <strong style={{ fontSize: 10, textAlign: "right" }}>{results.metadata?.replay_frames ?? "—"}</strong>
                    </div>
                    <div style={{ display: "grid", gridTemplateColumns: "1fr auto", alignItems: "center", gap: 16, padding: "9px 0" }}>
                      <span style={{ color: "#8b9293", fontSize: 9 }}>Engine</span>
                      <strong style={{ maxWidth: 150, fontSize: 9, lineHeight: 1.3, textAlign: "right" }}>
                        {results.metadata?.engine ?? "TDOS"}
                      </strong>
                    </div>
                  </div>
                </div>

                <ReplayHealthChart
                  replay={replay}
                  selectedAssetId={selectedReplayAsset}
                  onAssetChange={setSelectedReplayAsset}
                  stepIndex={replayStep}
                  onStepChange={setReplayStep}
                  isPlaying={isReplayPlaying}
                  onPlayChange={setIsReplayPlaying}
                  replaySpeed={replaySpeed}
                  onReplaySpeedChange={setReplaySpeed}
                />

                <ReplayFleetChart replay={replay} stepIndex={replayStep} />

                <ReplayRiskPanel
                  replay={replay}
                  results={results}
                  stepIndex={replayStep}
                />

                <div className="panel span-two step2-complete-panel">
                  <div className="step2-complete-icon"><CheckCircle2 size={19} /></div>
                  <div>
                    <span className="section-kicker">ANALYTICS WORKSPACE</span>
                    <h2>Simulation intelligence complete</h2>
                    <p>
                      TDOS now connects final results, real replay history, fleet comparison,
                      degradation analysis, and interactive playback in one operational view.
                    </p>
                  </div>
                  <div className="step2-complete-stats">
                    <span><strong>{replay?.total_frames ?? 0}</strong> frames</span>
                    <span><strong>{results?.total_assets ?? 0}</strong> assets</span>
                    <span><strong>{results?.simulation_steps ?? 0}</strong> steps</span>
                  </div>
                </div>

                <div className="panel span-two">
                  <div className="panel-head">
                    <div><span className="section-kicker">ASSET ANALYSIS</span><h2>Infrastructure condition</h2></div>
                    <span className="small-status">{results.total_assets} assets</span>
                  </div>
                  <div className="result-table">
                    <div className="result-row result-head"><span>Asset</span><span>Health</span><span>Risk</span><span>Maintenance</span><span>State</span></div>
                    {(results.asset_results ?? []).map((asset) => {
                      const sourceAsset = assets.find((item) => item.asset_id === asset.asset_id);
                      return (
                        <div className="result-row" key={asset.asset_id}>
                          <span className="asset-result-name">
                            <strong>{sourceAsset?.asset_name ?? asset.asset_id}</strong>
                            <small>{asset.asset_id}{sourceAsset?.asset_type ? ` · ${sourceAsset.asset_type}` : ""}</small>
                          </span>
                          <span><HealthPill score={asset.health_score} /></span>
                          <span className="risk">{asset.predicted_risk}</span>
                          <span className={asset.maintenance_required ? "warn-text" : "good-text"}>{asset.maintenance_required ? "Required" : "Clear"}</span>
                          <span>{asset.failed ? <span className="bad-text">FAILED</span> : <span className="good-text">OPERATIONAL</span>}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </>
            )}
          </section>
        )}

        {activeTab === "replay" && (
          <section className="content-grid replay-workspace">
            <div className="panel span-two replay-hero">
              <div>
                <span className="section-kicker">STEP 8 · DIGITAL TWIN REPLAY</span>
                <h1>Walk through the railway state, step by step.</h1>
                <p>Replay the recorded simulation as a temporal digital twin. Inspect asset health, fleet condition and risk at any point in the run.</p>
              </div>
              <div className="replay-hero-status"><strong>{replay?.total_frames ?? 0}</strong><span>recorded frames</span></div>
            </div>
            <div className="panel span-two replay-stage">
              <div className="replay-stage-head">
                <div><span className="section-kicker">TEMPORAL POSITION</span><h2>Simulation frame {replay ? replayStep + 1 : 0} / {replay?.total_frames ?? 0}</h2></div>
                <div className="replay-stage-meta"><span>{replay?.frames[replayStep]?.timestamp ? new Date(replay.frames[replayStep].timestamp).toLocaleTimeString() : "—"}</span><span>Step {replay?.frames[replayStep]?.step ?? 0}</span></div>
              </div>
              {replay ? (
                <>
                  <ReplayHealthChart replay={replay} selectedAssetId={selectedReplayAsset} onAssetChange={setSelectedReplayAsset} stepIndex={replayStep} onStepChange={setReplayStep} isPlaying={isReplayPlaying} onPlayChange={setIsReplayPlaying} replaySpeed={replaySpeed} onReplaySpeedChange={setReplaySpeed} />
                  <div className="replay-twin-grid">
                    <ReplayTwinInspector replay={replay} stepIndex={replayStep} selectedAssetId={selectedReplayAsset} />
                    <ReplayFleetChart replay={replay} stepIndex={replayStep} />
                  </div>
                  <ReplayRiskPanel replay={replay} results={results} stepIndex={replayStep} />
                </>
              ) : (
                <div className="empty-large"><Activity size={40} /><h3>No replay loaded</h3><p>Complete a simulation first. TDOS will automatically record the temporal state history.</p><button className="primary-button" onClick={() => setActiveTab("setup")}>Configure simulation</button></div>
              )}
            </div>
          </section>
        )}

        {activeTab === "rams" && (
          <RAMSPage rams={rams} onSetup={() => setActiveTab("setup")} />
        )}

        {activeTab === "decisions" && (
          <DecisionSupportPage decisions={decisions} whatIf={whatIf} scenarios={whatIfScenarios} onScenarioChange={updateWhatIfScenario} onAddScenario={addWhatIfScenario} onRemoveScenario={removeWhatIfScenario} onRunWhatIf={runWhatIf} whatIfRunning={whatIfRunning} />
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


function RAMSPage({ rams, onSetup }: { rams: RAMSResult | null; onSetup: () => void }) {
  if (!rams) {
    return (
      <section className="content-grid">
        <div className="panel span-two rams-empty">
          <div className="rams-empty-icon"><ShieldCheck size={28} /></div>
          <span className="section-kicker">RAMS INTELLIGENCE</span>
          <h2>No RAMS analysis yet</h2>
          <p>Complete a TDOS simulation first. RAMS will evaluate Reliability, Availability, Maintainability and Safety from the recorded simulation outputs.</p>
          <button className="primary-button" onClick={onSetup}>Configure simulation</button>
        </div>
      </section>
    );
  }

  const components = [
    { key: "reliability", label: "Reliability", score: rams.fleet.reliability_score, icon: ShieldCheck, description: "Probability of remaining failure-free" },
    { key: "availability", label: "Availability", score: rams.fleet.availability_score, icon: Activity, description: "Observed operational uptime" },
    { key: "maintainability", label: "Maintainability", score: rams.fleet.maintainability_score, icon: RotateCcw, description: "Maintenance-readiness proxy" },
    { key: "safety", label: "Safety", score: rams.fleet.safety_score, icon: TriangleAlert, description: "Risk and asset criticality" },
  ];

  const sortedAssets = [...rams.assets].sort((a, b) => a.rams_score - b.rams_score);

  return (
    <section className="content-grid rams-page">
      <div className="panel span-two rams-hero">
        <div className="rams-hero-copy">
          <span className="section-kicker">STEP 3 · RAMS INTELLIGENCE</span>
          <h2>Reliability. Availability. Maintainability. Safety.</h2>
          <p>{rams.methodology}</p>
        </div>
        <div className="rams-score-orb">
          <strong>{Math.round(rams.fleet.rams_score)}</strong>
          <span>RAMS SCORE</span>
          <em>{rams.fleet.rams_grade}</em>
        </div>
      </div>

      <div className="panel span-two">
        <div className="panel-head">
          <div><span className="section-kicker">RAMS BREAKDOWN</span><h2>Fleet performance</h2></div>
          <span className="small-status">Weighted index</span>
        </div>
        <div className="rams-component-grid">
          {components.map((item) => {
            const Icon = item.icon;
            return (
              <div className="rams-component" key={item.key}>
                <div className="rams-component-top">
                  <div className="rams-component-icon"><Icon size={17} /></div>
                  <div>
                    <strong>{item.label}</strong>
                    <span>{item.description}</span>
                  </div>
                  <b>{Math.round(item.score)}</b>
                </div>
                <div className="rams-score-track"><div style={{ width: `${item.score}%` }} /></div>
              </div>
            );
          })}
        </div>
      </div>

      <MetricCard icon={<TriangleAlert />} label="Critical assets" value={rams.fleet.critical_assets} detail="Highest safety criticality" tone="red" />
      <MetricCard icon={<Zap />} label="Immediate maintenance" value={rams.fleet.immediate_maintenance} detail="Requires immediate action" tone="amber" />
      <MetricCard icon={<Activity />} label="High priority" value={rams.fleet.high_priority_maintenance} detail="Priority intervention" tone="blue" />
      <MetricCard icon={<ShieldCheck />} label="Fleet availability" value={`${rams.fleet.fleet_operational_availability_percent.toFixed(1)}%`} detail="Observed replay uptime" tone="green" />

      <div className="panel span-two">
        <div className="panel-head">
          <div><span className="section-kicker">ASSET RAMS RANKING</span><h2>Maintenance decision queue</h2></div>
          <span className="small-status">{rams.assets.length} assets</span>
        </div>
        <div className="rams-table">
          <div className="rams-table-row rams-table-head"><span>Asset</span><span>RAMS</span><span>Reliability</span><span>Availability</span><span>Safety</span><span>Priority</span></div>
          {sortedAssets.map((asset) => (
            <div className="rams-table-row" key={asset.asset_id}>
              <span className="rams-asset-cell"><strong>{asset.asset_name}</strong><small>{asset.asset_id} · {asset.asset_type}</small></span>
              <span className="rams-score-cell"><strong>{Math.round(asset.rams_score)}</strong><small>{asset.rams_grade}</small></span>
              <span>{Math.round(asset.reliability.score)}</span>
              <span>{Math.round(asset.availability.score)}%</span>
              <span>{Math.round(asset.safety.score)}</span>
              <span><span className={`rams-priority rams-priority-${asset.maintenance_priority.toLowerCase()}`}>{asset.maintenance_priority}</span></span>
            </div>
          ))}
        </div>
      </div>

      <div className="panel span-two rams-methodology">
        <div className="panel-head"><div><span className="section-kicker">ENGINEERING BASIS</span><h2>How TDOS calculates RAMS</h2></div><Info size={19} className="accent-icon" /></div>
        <div className="rams-method-grid">
          <div><strong>Reliability · 30%</strong><span>100 × (1 − predicted failure probability).</span></div>
          <div><strong>Availability · 25%</strong><span>Percentage of recorded replay snapshots in an operational state.</span></div>
          <div><strong>Maintainability · 20%</strong><span>Health + RUL maintenance-readiness proxy; not an MTTR measurement.</span></div>
          <div><strong>Safety · 25%</strong><span>Predicted failure risk + health degradation + asset-type criticality.</span></div>
        </div>
      </div>
    </section>
  );
}

function DecisionSupportPage({
  decisions,
  whatIf,
  scenarios,
  onScenarioChange,
  onAddScenario,
  onRemoveScenario,
  onRunWhatIf,
  whatIfRunning = false,
}: {
  decisions: DecisionResult | null;
  whatIf: WhatIfBatchResult | null;
  scenarios: WhatIfScenario[];
  onScenarioChange: (id: string, patch: Partial<WhatIfScenario>) => void;
  onAddScenario: () => void;
  onRemoveScenario: (id: string) => void;
  onRunWhatIf: () => void | Promise<void>;
  whatIfRunning?: boolean;
}) {
  if (!decisions) return <section className="content-grid"><div className="panel span-two decision-empty"><div className="decision-empty-icon"><Zap size={28} /></div><span className="section-kicker">STEP 4 · DECISION SUPPORT</span><h2>No decision analysis yet</h2><p>Complete a simulation to generate explainable maintenance recommendations.</p></div></section>;
  const priorityClass = (p:string) => `decision-priority decision-${p.toLowerCase()}`;
  return <section className="content-grid decision-page">
    <div className="panel span-two decision-hero">
      <div><span className="section-kicker">STEP 4 · DECISION SUPPORT</span><h2>From simulation insight to operator action.</h2><p>{decisions.methodology}</p></div>
      <div className="decision-summary"><div><strong>{decisions.summary.critical}</strong><span>critical</span></div><div><strong>{decisions.summary.high}</strong><span>high</span></div><div><strong>{decisions.summary.medium}</strong><span>planned</span></div></div>
    </div>
    <MetricCard icon={<TriangleAlert />} label="Immediate actions" value={decisions.summary.immediate_actions} detail="Operator attention now" tone="red" />
    <MetricCard icon={<Zap />} label="Planned actions" value={decisions.summary.planned_actions} detail="Within maintenance window" tone="amber" />
    <MetricCard icon={<Activity />} label="Decision items" value={decisions.decisions.length} detail="Assets assessed" tone="blue" />
    <MetricCard icon={<ShieldCheck />} label="Low priority" value={decisions.summary.low} detail="Routine monitoring" tone="green" />
    <div className="panel span-two"><div className="panel-head"><div><span className="section-kicker">MAINTENANCE QUEUE</span><h2>Recommended actions</h2></div><span className="small-status">Explainable rules</span></div>
      <div className="decision-list">{decisions.decisions.map((d)=><div className="decision-card" key={d.asset_id}><div className="decision-card-main"><div className="decision-asset"><strong>{d.asset_name}</strong><small>{d.asset_id} · {d.asset_type}</small></div><span className={priorityClass(d.priority)}>{d.priority}</span><div className="decision-action"><strong>{d.action}</strong><span>{d.reason}</span></div><div className="decision-timing">{d.timing}</div></div><div className="decision-metrics"><span>Health <b>{d.health_score.toFixed(1)}</b></span><span>RAMS <b>{Math.round(d.rams_score)}</b></span><span>Failure <b>{(d.failure_probability*100).toFixed(1)}%</b></span><span>RUL <b>{d.remaining_useful_life_days}d</b></span></div></div>)}</div>
    </div>
    <div className="panel span-two">
      <div className="panel-head"><div><span className="section-kicker">MAINTENANCE WHAT-IF</span><h2>Compare multiple intervention scenarios</h2></div><RotateCcw size={19} className="accent-icon" /></div>
      <p className="whatif-intro">Build several independent maintenance strategies, then compare their projected effect without changing the completed simulation.</p>
      <div className="whatif-scenario-list">
        {scenarios.map((scenario, index) => (
          <div className="whatif-scenario-card" key={scenario.id}>
            <div className="whatif-scenario-head">
              <div><span className="scenario-number">{String(index + 1).padStart(2, "0")}</span><strong>{scenario.name}</strong></div>
              {scenarios.length > 1 && <button className="whatif-remove" onClick={() => onRemoveScenario(scenario.id)} title="Remove scenario"><Trash2 size={14} /></button>}
            </div>
            <div className="whatif-scenario-fields">
              <label>Scenario name<input value={scenario.name} onChange={e=>onScenarioChange(scenario.id,{name:e.target.value})} /></label>
              <label>Asset<select value={scenario.asset_id} onChange={e=>onScenarioChange(scenario.id,{asset_id:e.target.value})}>{decisions.decisions.map(d=><option key={d.asset_id} value={d.asset_id}>{d.asset_name}</option>)}</select></label>
              <label>Health recovery<input type="number" min="0" max="50" step="1" value={scenario.health_recovery} onChange={e=>onScenarioChange(scenario.id,{health_recovery:Number(e.target.value)})} /></label>
              <label>Degradation reduction %<input type="number" min="0" max="100" step="5" value={scenario.degradation_reduction_percent} onChange={e=>onScenarioChange(scenario.id,{degradation_reduction_percent:Number(e.target.value)})} /></label>
            </div>
          </div>
        ))}
      </div>
      <div className="whatif-actions">
        <button className="secondary-button" onClick={onAddScenario} disabled={scenarios.length >= 12}><Plus size={14} /> Add scenario</button>
        <span>{scenarios.length}/12 scenarios</span>
        <button className="primary-button compare-button" onClick={onRunWhatIf} disabled={!scenarios.length || whatIfRunning}><FlaskConical size={15} /> {whatIfRunning ? "Comparing…" : "Compare scenarios"}</button>
      </div>
      {whatIf && <div className="whatif-comparison"><div className="whatif-comparison-head"><div><span className="section-kicker">SCENARIO COMPARISON</span><h3>{whatIf.scenario_count} intervention outcomes</h3></div></div><div className="whatif-result-grid">{whatIf.scenarios.map((item)=><div className="whatif-result" key={item.scenario_id ?? item.asset_id}><div className="whatif-result-title"><strong>{item.scenario_name ?? item.asset_name}</strong><small>{item.asset_name}</small></div><div><span>BEFORE</span><strong>{Math.round(item.before.rams_score)}</strong><small>{item.before.priority}</small></div><ChevronRight size={18}/><div><span>AFTER</span><strong>{Math.round(item.after.rams_score)}</strong><small>{item.after.priority}</small></div><div className="whatif-deltas"><span>Health <b>+{item.changes.health_score.toFixed(1)}</b></span><span>RAMS <b>+{item.changes.rams_score.toFixed(1)}</b></span><span>Failure <b>{(item.changes.failure_probability*100).toFixed(1)} pts</b></span><span>RUL <b>+{item.changes.remaining_useful_life_days} days</b></span></div></div>)}</div></div>}
    </div>
  </section>;
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

function ReplayHealthChart({
  replay,
  selectedAssetId,
  onAssetChange,
  stepIndex,
  onStepChange,
  isPlaying,
  onPlayChange,
  replaySpeed,
  onReplaySpeedChange,
}: {
  replay: ReplayResponse | null;
  selectedAssetId: string;
  onAssetChange: (value: string) => void;
  stepIndex: number;
  onStepChange: (value: number) => void;
  isPlaying: boolean;
  onPlayChange: (value: boolean) => void;
  replaySpeed: number;
  onReplaySpeedChange: (value: number) => void;
}) {
  const width = 860;
  const height = 300;
  const pad = { left: 48, right: 22, top: 28, bottom: 42 };

  const assets = replay?.frames[0]?.assets ?? [];
  const selected = selectedAssetId || assets[0]?.asset_id || "";
  const points = (replay?.frames ?? [])
    .map((frame, index) => {
      const asset = frame.assets.find((item) => item.asset_id === selected);
      return asset ? { step: frame.step, health: asset.health_score, index } : null;
    })
    .filter((point): point is { step: number; health: number; index: number } => point !== null);

  const currentFrame = replay?.frames[stepIndex];
  const currentAsset = currentFrame?.assets.find((item) => item.asset_id === selected);
  const minHealth = Math.min(0, ...points.map((p) => p.health));
  const maxHealth = Math.max(100, ...points.map((p) => p.health));
  const range = Math.max(1, maxHealth - minHealth);

  const x = (index: number) =>
    pad.left + (points.length <= 1 ? 0 : (index / (points.length - 1)) * (width - pad.left - pad.right));
  const y = (health: number) =>
    pad.top + ((maxHealth - health) / range) * (height - pad.top - pad.bottom);

  const path = points.map((point, index) => `${index === 0 ? "M" : "L"} ${x(index).toFixed(2)} ${y(point.health).toFixed(2)}`).join(" ");
  const currentPointIndex = points.findIndex((point) => point.index === stepIndex);
  const currentPoint = currentPointIndex >= 0 ? points[currentPointIndex] : points[points.length - 1];

  if (!replay || !replay.frames.length) {
    return (
      <div className="panel span-two">
        <div className="panel-head">
          <div><span className="section-kicker">SIMULATION ANALYTICS</span><h2>Health trajectory</h2></div>
        </div>
        <div className="empty-state">Replay data is not available yet. Complete a simulation to generate the health timeline.</div>
      </div>
    );
  }

  return (
    <div className="panel span-two">
      <div className="panel-head">
        <div>
          <span className="section-kicker">SIMULATION ANALYTICS</span>
          <h2>Health trajectory</h2>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <select
            value={selected}
            onChange={(event) => onAssetChange(event.target.value)}
            style={{
              border: "1px solid #e8e2d5",
              borderRadius: 9,
              background: "#fffdf8",
              padding: "8px 30px 8px 10px",
              color: "#3d484b",
              fontSize: 11,
              fontWeight: 700,
              outline: "none",
            }}
          >
            {assets.map((asset) => (
              <option key={asset.asset_id} value={asset.asset_id}>
                {asset.asset_name ?? asset.asset_id}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "minmax(0, 1fr) 150px", gap: 18, alignItems: "stretch" }}>
        <div className="analytics-chart-shell" style={{ minWidth: 0, border: "1px solid #eee9dd", borderRadius: 15, background: "#fffdf9", padding: "8px 8px 0" }}>
          <svg viewBox={`0 0 ${width} ${height}`} width="100%" role="img" aria-label="Asset health trajectory">
            {[100, 90, 80, 70, 60].map((value) => (
              <g key={value}>
                <line x1={pad.left} x2={width - pad.right} y1={y(value)} y2={y(value)} stroke="#eee9dd" strokeDasharray="4 5" />
                <text x={pad.left - 10} y={y(value) + 4} textAnchor="end" fontSize="10" fill="#9aa1a1">{value}</text>
              </g>
            ))}
            <line x1={pad.left} x2={width - pad.right} y1={height - pad.bottom} y2={height - pad.bottom} stroke="#ded8ca" />
            {points.length > 1 && (
              <>
                <path d={path} fill="none" stroke="#e9a82f" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round" />
                <path
                  d={`${path} L ${x(points.length - 1)} ${height - pad.bottom} L ${x(0)} ${height - pad.bottom} Z`}
                  fill="#f8e7ae"
                  opacity="0.28"
                  stroke="none"
                />
              </>
            )}
            {currentPoint && (
              <>
                <line
                  x1={x(currentPointIndex >= 0 ? currentPointIndex : points.length - 1)}
                  x2={x(currentPointIndex >= 0 ? currentPointIndex : points.length - 1)}
                  y1={pad.top}
                  y2={height - pad.bottom}
                  stroke="#c9b36d"
                  strokeDasharray="5 5"
                />
                <circle
                  cx={x(currentPointIndex >= 0 ? currentPointIndex : points.length - 1)}
                  cy={y(currentPoint.health)}
                  r="6"
                  fill="#fffdf9"
                  stroke="#e9a82f"
                  strokeWidth="3"
                />
              </>
            )}
            {[0, Math.floor((points.length - 1) / 2), points.length - 1].filter((v, i, a) => a.indexOf(v) === i).map((index) => (
              <text key={index} x={x(index)} y={height - 14} textAnchor="middle" fontSize="10" fill="#9aa1a1">
                Step {points[index]?.step}
              </text>
            ))}
          </svg>
        </div>

        <div style={{ borderRadius: 15, background: "#fff7d8", padding: 16, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
          <div>
            <span style={{ display: "block", fontSize: 9, fontWeight: 800, letterSpacing: ".09em", color: "#9a813e" }}>CURRENT STATE</span>
            <strong style={{ display: "block", marginTop: 7, fontFamily: "Manrope, sans-serif", fontSize: 30, letterSpacing: "-.05em", color: "#5e4c1b" }}>
              {currentAsset?.health_score.toFixed(1) ?? "—"}
            </strong>
            <span style={{ fontSize: 10, color: "#9a813e" }}>health / 100</span>
          </div>
          <div style={{ display: "grid", gap: 9, marginTop: 18 }}>
            <div><span style={{ display: "block", color: "#9a813e", fontSize: 9, textTransform: "uppercase" }}>Step</span><strong style={{ fontSize: 12 }}>{currentFrame?.step ?? "—"} / {replay.total_frames}</strong></div>
            <div><span style={{ display: "block", color: "#9a813e", fontSize: 9, textTransform: "uppercase" }}>State</span><strong style={{ fontSize: 12 }}>{currentAsset?.failed ? "FAILED" : currentAsset?.under_maintenance ? "MAINTENANCE" : "OPERATIONAL"}</strong></div>
          </div>
        </div>
      </div>

      <div className="replay-controls">
        <button
          className="replay-control replay-primary replay-main-action"
          title={isPlaying ? "Pause replay" : "Play replay"}
          onClick={() => {
            if (stepIndex >= replay.frames.length - 1) onStepChange(0);
            onPlayChange(!isPlaying);
          }}
        >
          {isPlaying ? <Pause size={15} /> : <Play size={15} />}
          {isPlaying ? "Pause" : "Play"}
        </button>

        <button
          className="replay-control replay-restart"
          title="Restart replay"
          onClick={() => {
            onPlayChange(false);
            onStepChange(0);
          }}
        >
          <RotateCcw size={14} />
          Restart
        </button>

        <button
          className="icon-button"
          title="Previous step"
          disabled={stepIndex <= 0}
          onClick={() => {
            onPlayChange(false);
            onStepChange(Math.max(0, stepIndex - 1));
          }}
        >
          ◀
        </button>

        <input
          type="range"
          min={0}
          max={Math.max(0, replay.frames.length - 1)}
          value={Math.min(stepIndex, Math.max(0, replay.frames.length - 1))}
          onChange={(event) => {
            onPlayChange(false);
            onStepChange(Number(event.target.value));
          }}
          style={{ flex: 1, accentColor: "#e9a82f" }}
          aria-label="Replay step"
        />

        <button
          className="icon-button"
          title="Next step"
          disabled={stepIndex >= replay.frames.length - 1}
          onClick={() => {
            onPlayChange(false);
            onStepChange(Math.min(replay.frames.length - 1, stepIndex + 1));
          }}
        >
          ▶
        </button>

        <select
          className="replay-speed"
          value={replaySpeed}
          onChange={(event) => onReplaySpeedChange(Number(event.target.value))}
          aria-label="Replay speed"
        >
          <option value={0.5}>0.5×</option>
          <option value={1}>1×</option>
          <option value={2}>2×</option>
          <option value={4}>4×</option>
        </select>

        <span className="replay-step-label">
          Step {currentFrame?.step ?? "—"} / {replay.total_frames}
        </span>
      </div>
    </div>
  );
}

function ReplayFleetChart({
  replay,
  stepIndex,
}: {
  replay: ReplayResponse | null;
  stepIndex: number;
}) {
  const width = 860;
  const height = 310;
  const pad = { left: 48, right: 22, top: 34, bottom: 44 };

  const assets = replay?.frames[0]?.assets ?? [];
  const palette = ["#e9a82f", "#4d9c8d", "#6c7edc", "#d9775b", "#8b6fb3", "#4e879f"];

  const series = assets.map((asset, assetIndex) => {
    const points = (replay?.frames ?? []).map((frame, index) => {
      const current = frame.assets.find((item) => item.asset_id === asset.asset_id);
      return current ? { step: frame.step, health: current.health_score, index } : null;
    }).filter((point): point is { step: number; health: number; index: number } => point !== null);

    return {
      asset,
      points,
      stroke: palette[assetIndex % palette.length],
    };
  });

  const x = (index: number) =>
    pad.left + ((index / Math.max(1, (replay?.frames.length ?? 1) - 1)) * (width - pad.left - pad.right));

  const y = (health: number) =>
    pad.top + ((100 - Math.max(0, Math.min(100, health))) / 100) * (height - pad.top - pad.bottom);

  if (!replay || !replay.frames.length || !assets.length) {
    return (
      <div className="panel span-two">
        <div className="panel-head">
          <div><span className="section-kicker">FLEET ANALYTICS</span><h2>Asset comparison</h2></div>
        </div>
        <div className="empty-state">Complete a simulation to compare asset health trajectories.</div>
      </div>
    );
  }

  const currentFrame = replay.frames[Math.min(stepIndex, replay.frames.length - 1)];
  const currentValues = assets.map((asset) => currentFrame?.assets.find((item) => item.asset_id === asset.asset_id));

  return (
    <div className="panel span-two">
      <div className="panel-head">
        <div>
          <span className="section-kicker">FLEET ANALYTICS</span>
          <h2>Asset comparison</h2>
        </div>
        <span className="small-status">Step {currentFrame?.step ?? "—"}</span>
      </div>

      <div className="analytics-chart-shell" style={{ border: "1px solid #eee9dd", borderRadius: 15, background: "#fffdf9", padding: "8px 8px 0" }}>
        <svg viewBox={`0 0 ${width} ${height}`} width="100%" role="img" aria-label="Comparative asset health trajectories">
          {[100, 80, 60, 40, 20, 0].map((value) => (
            <g key={value}>
              <line
                x1={pad.left}
                x2={width - pad.right}
                y1={y(value)}
                y2={y(value)}
                stroke="#eee9dd"
                strokeDasharray="4 5"
              />
              <text x={pad.left - 10} y={y(value) + 4} textAnchor="end" fontSize="10" fill="#9aa1a1">
                {value}
              </text>
            </g>
          ))}

          {series.map((item) => {
            const path = item.points
              .map((point, index) => `${index === 0 ? "M" : "L"} ${x(point.index).toFixed(2)} ${y(point.health).toFixed(2)}`)
              .join(" ");

            return (
              <path
                key={item.asset.asset_id}
                d={path}
                fill="none"
                stroke={item.stroke}
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
                opacity="0.9"
              />
            );
          })}

          <line
            x1={x(Math.min(stepIndex, replay.frames.length - 1))}
            x2={x(Math.min(stepIndex, replay.frames.length - 1))}
            y1={pad.top}
            y2={height - pad.bottom}
            stroke="#c9b36d"
            strokeDasharray="5 5"
          />

          {currentValues.map((asset, index) => asset ? (
            <circle
              key={asset.asset_id}
              cx={x(Math.min(stepIndex, replay.frames.length - 1))}
              cy={y(asset.health_score)}
              r="5"
              fill="#fffdf9"
              stroke={palette[index % palette.length]}
              strokeWidth="3"
            />
          ) : null)}

          {[0, Math.floor((replay.frames.length - 1) / 2), replay.frames.length - 1]
            .filter((value, index, array) => array.indexOf(value) === index)
            .map((index) => (
              <text key={index} x={x(index)} y={height - 14} textAnchor="middle" fontSize="10" fill="#9aa1a1">
                Step {replay.frames[index]?.step}
              </text>
            ))}
        </svg>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(190px, 1fr))", gap: 10, marginTop: 14 }}>
        {assets.map((asset, index) => {
          const current = currentValues[index];
          return (
            <div
              key={asset.asset_id}
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: 10,
                padding: "11px 13px",
                border: "1px solid #eee9dd",
                borderRadius: 12,
                background: "#fffdf9",
              }}
            >
              <div style={{ minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 7 }}>
                  <span style={{ width: 8, height: 8, borderRadius: "50%", background: palette[index % palette.length], flexShrink: 0 }} />
                  <strong style={{ fontSize: 10, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
                    {asset.asset_name ?? asset.asset_id}
                  </strong>
                </div>
                <span style={{ display: "block", marginTop: 3, color: "#9aa1a1", fontSize: 9 }}>{asset.asset_id}</span>
              </div>
              <strong style={{ fontFamily: "Manrope, sans-serif", fontSize: 17, letterSpacing: "-.04em" }}>
                {current?.health_score.toFixed(1) ?? "—"}
              </strong>
            </div>
          );
        })}
      </div>
    </div>
  );
}

function ReplayRiskPanel({
  replay,
  results,
  stepIndex,
}: {
  replay: ReplayResponse | null;
  results: Results | null;
  stepIndex: number;
}) {
  if (!replay || !replay.frames.length) {
    return null;
  }

  const firstFrame = replay.frames[0];
  const currentFrame = replay.frames[Math.min(stepIndex, replay.frames.length - 1)];
  const finalFrame = replay.frames[replay.frames.length - 1];

  const rows = firstFrame.assets.map((initialAsset) => {
    const currentAsset = currentFrame?.assets.find((asset) => asset.asset_id === initialAsset.asset_id);
    const finalAsset = finalFrame?.assets.find((asset) => asset.asset_id === initialAsset.asset_id);
    const resultAsset = results?.asset_results?.find((asset) => asset.asset_id === initialAsset.asset_id);

    const healthDrop = Math.max(0, initialAsset.health_score - (currentAsset?.health_score ?? initialAsset.health_score));
    const projectedDrop = Math.max(0, initialAsset.health_score - (finalAsset?.health_score ?? initialAsset.health_score));
    const rate = currentAsset?.degradation_rate ?? initialAsset.degradation_rate ?? 0;

    const severity =
      rate >= 0.10 || healthDrop >= 8 ? "HIGH" :
      rate >= 0.06 || healthDrop >= 4 ? "MODERATE" :
      "LOW";

    const severityClass =
      severity === "HIGH" ? "risk-high" :
      severity === "MODERATE" ? "risk-moderate" :
      "risk-low";

    return {
      asset: initialAsset,
      current: currentAsset,
      result: resultAsset,
      healthDrop,
      projectedDrop,
      rate,
      severity,
      severityClass,
    };
  });

  const highestRisk = [...rows].sort((a, b) => {
    const score = (row: typeof rows[number]) =>
      row.rate * 100 + row.healthDrop * 2 + (row.result?.maintenance_required ? 15 : 0) + (row.result?.failed ? 100 : 0);
    return score(b) - score(a);
  })[0];

  return (
    <div className="panel span-two risk-intelligence-panel">
      <div className="panel-head">
        <div>
          <span className="section-kicker">RISK INTELLIGENCE</span>
          <h2>Degradation & risk profile</h2>
        </div>
        <span className="small-status">Step {currentFrame?.step ?? "—"} / {replay.total_frames}</span>
      </div>

      <div className="risk-callout">
        <div className="risk-callout-icon"><TriangleAlert size={18} /></div>
        <div>
          <strong>
            {highestRisk ? `${highestRisk.asset.asset_name} shows the highest degradation pressure.` : "Risk profile available."}
          </strong>
          <span>
            {highestRisk
              ? `${highestRisk.rate.toFixed(2)} health points/step · ${highestRisk.healthDrop.toFixed(1)} points lost by the current step.`
              : "Replay data is available for analysis."}
          </span>
        </div>
      </div>

      <div className="risk-table">
        <div className="risk-row risk-head">
          <span>Asset</span>
          <span>Health loss</span>
          <span>Degradation</span>
          <span>Projected loss</span>
          <span>Risk</span>
          <span>Final state</span>
        </div>

        {rows.map((row) => (
          <div className="risk-row" key={row.asset.asset_id}>
            <span className="risk-asset">
              <strong>{row.asset.asset_name ?? row.asset.asset_id}</strong>
              <small>{row.asset.asset_id} · {row.asset.asset_type}</small>
            </span>
            <span className="risk-number">
              <strong>{row.healthDrop.toFixed(1)}</strong>
              <small>pts</small>
            </span>
            <span className="risk-rate">
              <div className="rate-bar">
                <div style={{ width: `${Math.min(100, (row.rate / 0.15) * 100)}%` }} />
              </div>
              <small>{row.rate.toFixed(2)} / step</small>
            </span>
            <span className="risk-number">
              <strong>{row.projectedDrop.toFixed(1)}</strong>
              <small>pts</small>
            </span>
            <span><span className={`risk-badge ${row.severityClass}`}>{row.result?.predicted_risk ?? row.severity}</span></span>
            <span className={row.result?.failed ? "bad-text" : row.result?.maintenance_required ? "warn-text" : "good-text"}>
              {row.result?.failed ? "FAILED" : row.result?.maintenance_required ? "MAINTENANCE" : "OPERATIONAL"}
            </span>
          </div>
        ))}
      </div>

      <div className="risk-footnote">
        <span><Info size={13} /> Degradation is derived from the recorded replay state and asset degradation rate. Final risk uses the simulation prediction output.</span>
      </div>
    </div>
  );
}

function ReplayTwinInspector({ replay, stepIndex, selectedAssetId }: { replay: ReplayResponse; stepIndex: number; selectedAssetId: string }) {
  const frame = replay.frames[stepIndex] ?? replay.frames[replay.frames.length - 1];
  const asset = frame?.assets.find((item) => item.asset_id === selectedAssetId) ?? frame?.assets[0];
  if (!asset) return null;
  const health = asset.health_score;
  const state = asset.failed ? "FAILED" : asset.under_maintenance ? "MAINTENANCE" : health < 60 ? "DEGRADED" : "OPERATIONAL";
  const tone = asset.failed ? "bad" : health < 60 ? "warn" : "good";
  return (
    <div className="panel replay-twin-inspector">
      <div className="panel-head"><div><span className="section-kicker">DIGITAL TWIN STATE</span><h2>Live asset snapshot</h2></div><Layers3 size={20} className="accent-icon" /></div>
      <div className="twin-identity"><div className={`twin-state-dot ${tone}`} /><div><strong>{asset.asset_name ?? asset.asset_id}</strong><span>{asset.asset_id} · {asset.asset_type}</span></div><span className={`replay-state-pill ${tone}`}>{state}</span></div>
      <div className="twin-health-readout"><strong>{health.toFixed(1)}</strong><span>/ 100 health</span></div>
      <div className="twin-health-bar"><div style={{ width: `${Math.max(0, Math.min(100, health))}%` }} /></div>
      <div className="twin-facts"><div><span>Latitude</span><strong>{asset.latitude.toFixed(4)}</strong></div><div><span>Longitude</span><strong>{asset.longitude.toFixed(4)}</strong></div><div><span>Age</span><strong>{asset.age_days} days</strong></div><div><span>Degradation</span><strong>{asset.degradation_rate.toFixed(2)} / step</strong></div></div>
    </div>
  );
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