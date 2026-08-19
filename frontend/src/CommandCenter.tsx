import { useMemo } from "react";
import {
  Activity,
  ArrowUpRight,
  CheckCircle2,
  Clock3,
  Gauge,
  ShieldAlert,
  Wrench,
  Zap,
  Radio,
  TrainFront,
  CircleAlert,
} from "lucide-react";

export type CommandCenterAsset = {
  asset_id: string;
  asset_name?: string;
  asset_type?: string;
  health_score: number;
  degradation_rate?: number;
  predicted_risk?: string;
  maintenance_required?: boolean;
  failed?: boolean;
};

export type CommandCenterResults = {
  simulation_id: string;
  simulation_name: string;
  simulation_steps: number;
  total_assets: number;
  healthy_assets: number;
  degraded_assets: number;
  failed_assets: number;
  average_health_score: number;

  prediction?: {
    failure_probability: number;
    remaining_useful_life_days: number;
    predicted_health_score: number;
    confidence: number;
  } | null;

  asset_results?: CommandCenterAsset[];

  metadata?: Record<string, string | undefined>;
};

type Priority = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW";

type Decision = CommandCenterAsset & {
  priority: Priority;
  action: string;
  timing: string;
  reason: string;
  riskScore: number;
};

function priorityFor(
  asset: CommandCenterAsset,
  failureProbability: number,
): Priority {
  const risk = (asset.predicted_risk ?? "").toUpperCase();

  if (
    asset.failed ||
    asset.health_score < 40 ||
    failureProbability >= 0.5 ||
    risk === "CRITICAL"
  ) {
    return "CRITICAL";
  }

  if (
    asset.health_score < 60 ||
    failureProbability >= 0.35 ||
    asset.maintenance_required ||
    risk === "HIGH"
  ) {
    return "HIGH";
  }

  if (asset.health_score < 80 || risk === "MEDIUM") {
    return "MEDIUM";
  }

  return "LOW";
}

function actionFor(priority: Priority, asset: CommandCenterAsset) {
  if (priority === "CRITICAL") {
    return asset.failed
      ? "Isolate asset and initiate emergency intervention."
      : "Perform immediate detailed inspection.";
  }

  if (priority === "HIGH") {
    return "Schedule priority maintenance and inspection.";
  }

  if (priority === "MEDIUM") {
    return "Increase inspection frequency.";
  }

  return "Continue routine condition monitoring.";
}

function timingFor(priority: Priority) {
  if (priority === "CRITICAL") return "NOW";
  if (priority === "HIGH") return "< 7 DAYS";
  if (priority === "MEDIUM") return "< 30 DAYS";
  return "ROUTINE";
}

function reasonFor(
  asset: CommandCenterAsset,
  priority: Priority,
) {
  const reasons: string[] = [];

  if (asset.health_score < 60) {
    reasons.push(`Health ${asset.health_score.toFixed(1)}`);
  }

  if ((asset.degradation_rate ?? 0) >= 0.1) {
    reasons.push("Elevated degradation");
  }

  if (asset.maintenance_required) {
    reasons.push("Maintenance required");
  }

  if (asset.failed) {
    reasons.push("Asset failure");
  }

  if (
    ["HIGH", "CRITICAL"].includes(
      (asset.predicted_risk ?? "").toUpperCase(),
    )
  ) {
    reasons.push(`${asset.predicted_risk} predicted risk`);
  }

  if (reasons.length === 0) {
    return priority === "LOW"
      ? "Condition remains within normal operating range."
      : "Combined condition indicators require attention.";
  }

  return reasons.join(" · ");
}

function priorityRank(priority: Priority) {
  return {
    CRITICAL: 0,
    HIGH: 1,
    MEDIUM: 2,
    LOW: 3,
  }[priority];
}

function priorityClass(priority: Priority) {
  return `cc-priority cc-priority-${priority.toLowerCase()}`;
}

function healthClass(score: number) {
  if (score < 40) return "cc-health-critical";
  if (score < 60) return "cc-health-warning";
  if (score < 80) return "cc-health-watch";
  return "cc-health-good";
}

export default function CommandCenter({
  results,
  assets,
}: {
  results: CommandCenterResults | null;
  assets: CommandCenterAsset[];
}) {
  const decisions = useMemo<Decision[]>(() => {
    if (!results) return [];

    const assetMap = new Map(
      assets.map((asset) => [asset.asset_id, asset]),
    );

    const failureProbability =
      results.prediction?.failure_probability ?? 0;

    return (results.asset_results ?? assets)
      .map((resultAsset) => {
        const merged = {
          ...assetMap.get(resultAsset.asset_id),
          ...resultAsset,
        };

        const priority = priorityFor(
          merged,
          failureProbability,
        );

        const riskScore = Math.min(
          100,
          Math.max(
            failureProbability * 100,
            100 - merged.health_score,
            merged.failed ? 100 : 0,
          ),
        );

        return {
          ...merged,
          priority,
          action: actionFor(priority, merged),
          timing: timingFor(priority),
          reason: reasonFor(merged, priority),
          riskScore,
        };
      })
      .sort(
        (a, b) =>
          priorityRank(a.priority) -
            priorityRank(b.priority) ||
          b.riskScore - a.riskScore,
      );
  }, [results, assets]);

  if (!results) {
    return (
      <section className="content-grid cc-page">
        <div className="panel span-two cc-empty">
          <Radio size={30} />

          <span className="section-kicker">
            STEP 5 · OPERATIONS COMMAND
          </span>

          <h2>Command center awaiting simulation data</h2>

          <p>
            Run a TDOS simulation to populate the operational
            picture, asset priorities and recommended maintenance
            actions.
          </p>
        </div>
      </section>
    );
  }

  const critical = decisions.filter(
    (item) => item.priority === "CRITICAL",
  ).length;

  const high = decisions.filter(
    (item) => item.priority === "HIGH",
  ).length;

  const medium = decisions.filter(
    (item) => item.priority === "MEDIUM",
  ).length;

  const averageRisk = decisions.length
    ? decisions.reduce(
        (sum, item) => sum + item.riskScore,
        0,
      ) / decisions.length
    : 0;

  const commandState = critical
    ? "CRITICAL"
    : high
      ? "PRIORITY"
      : medium
        ? "MONITOR"
        : "STABLE";

  const commandStateClass = critical
    ? "critical"
    : high
      ? "priority"
      : medium
        ? "monitor"
        : "stable";

  return (
    <section className="content-grid cc-page">

      {/* ======================================================
          COMMAND HEADER
      ====================================================== */}

      <div className="panel span-two cc-command-header">

        <div className="cc-command-left">

          <div className="cc-command-kicker">
            <span className="cc-live-dot" />
            LIVE OPERATIONS
            <span className="cc-command-divider" />
            TDOS COMMAND DECK
          </div>

          <h1>
            Railway infrastructure
            <span> command center.</span>
          </h1>

          <p>
            Simulation intelligence translated into
            operational priorities, intervention windows
            and infrastructure decisions.
          </p>

          <div className="cc-command-meta">

            <div>
              <span>RUN</span>
              <strong className="mono">
                {results.simulation_id}
              </strong>
            </div>

            <div>
              <span>STEPS</span>
              <strong>{results.simulation_steps}</strong>
            </div>

            <div>
              <span>ASSETS</span>
              <strong>{results.total_assets}</strong>
            </div>

          </div>

        </div>

        <div className="cc-command-status">

          <div className="cc-status-ring">
            <div>
              <span>NETWORK</span>
              <strong>
                {results.average_health_score.toFixed(1)}
              </strong>
              <small>HEALTH</small>
            </div>
          </div>

          <div className={`cc-command-state ${commandStateClass}`}>
            <span />
            {commandState}
          </div>

        </div>

      </div>


      {/* ======================================================
          OPERATIONAL STRIP
      ====================================================== */}

      <div className="cc-operation-strip span-two">

        <div className="cc-operation-item critical">
          <div className="cc-operation-icon">
            <ShieldAlert size={19} />
          </div>

          <div>
            <span>CRITICAL</span>
            <strong>{critical}</strong>
            <small>Immediate intervention</small>
          </div>
        </div>

        <div className="cc-operation-item high">
          <div className="cc-operation-icon">
            <Wrench size={19} />
          </div>

          <div>
            <span>HIGH PRIORITY</span>
            <strong>{high}</strong>
            <small>Maintenance queue</small>
          </div>
        </div>

        <div className="cc-operation-item monitor">
          <div className="cc-operation-icon">
            <Activity size={19} />
          </div>

          <div>
            <span>MONITORING</span>
            <strong>{medium}</strong>
            <small>Increased inspection</small>
          </div>
        </div>

        <div className="cc-operation-item stable">
          <div className="cc-operation-icon">
            <TrainFront size={19} />
          </div>

          <div>
            <span>HEALTHY</span>
            <strong>{results.healthy_assets}</strong>
            <small>Operational assets</small>
          </div>
        </div>

      </div>


      {/* ======================================================
          PRIORITY QUEUE
      ====================================================== */}

      <div className="panel span-two cc-priority-panel">

        <div className="cc-section-header">

          <div>
            <span className="section-kicker">
              ACTIVE PRIORITIES
            </span>

            <h2>Intervention queue</h2>

            <p>
              Assets ranked by operational consequence and
              predicted deterioration.
            </p>
          </div>

          <div className="cc-queue-count">
            <strong>{decisions.length}</strong>
            <span>ASSETS ASSESSED</span>
          </div>

        </div>


        <div className="cc-decision-list">

          {decisions.map((asset, index) => (

            <div
              className="cc-decision-card"
              key={asset.asset_id}
            >

              <div className="cc-rank">
                {String(index + 1).padStart(2, "0")}
              </div>


              <div className="cc-asset-identity">

                <div className="cc-asset-heading">

                  <div>
                    <strong>
                      {asset.asset_name ??
                        asset.asset_id}
                    </strong>

                    <span>
                      {asset.asset_id}
                      {asset.asset_type
                        ? ` · ${asset.asset_type}`
                        : ""}
                    </span>
                  </div>

                  <span
                    className={priorityClass(
                      asset.priority,
                    )}
                  >
                    {asset.priority}
                  </span>

                </div>


                <div className="cc-action-line">

                  {asset.priority === "CRITICAL" ? (
                    <CircleAlert size={16} />
                  ) : (
                    <Wrench size={16} />
                  )}

                  <div>
                    <strong>{asset.action}</strong>
                    <span>{asset.reason}</span>
                  </div>

                </div>

              </div>


              <div className="cc-asset-health">

                <span>HEALTH</span>

                <strong
                  className={healthClass(
                    asset.health_score,
                  )}
                >
                  {asset.health_score.toFixed(1)}
                </strong>

                <div className="cc-health-bar">
                  <i
                    style={{
                      width: `${Math.max(
                        0,
                        Math.min(
                          100,
                          asset.health_score,
                        ),
                      )}%`,
                    }}
                  />
                </div>

              </div>


              <div className="cc-asset-risk">

                <span>RISK INDEX</span>

                <strong>
                  {asset.riskScore.toFixed(0)}
                </strong>

                <small>
                  {asset.predicted_risk ??
                    "NORMAL"}
                </small>

              </div>


              <div className="cc-asset-timing">

                <span>INTERVENTION</span>

                <strong>{asset.timing}</strong>

                <ArrowUpRight size={15} />

              </div>

            </div>

          ))}

        </div>

      </div>


      {/* ======================================================
          NETWORK STATE
      ====================================================== */}

      <div className="panel cc-network-panel">

        <div className="cc-section-header compact">

          <div>
            <span className="section-kicker">
              NETWORK PROFILE
            </span>

            <h2>Infrastructure state</h2>
          </div>

          <Activity
            size={20}
            className="accent-icon"
          />

        </div>


        <div className="cc-network-map">

          <div className="cc-track-line">
            <i />
            <i />
            <i />
          </div>

          <div className="cc-track-label">
            <span>NETWORK CONDITION</span>
            <strong>
              {results.average_health_score.toFixed(1)}
              <small>/100</small>
            </strong>
          </div>

        </div>


        <div className="cc-state-list">

          <div>
            <span>
              <i className="green-dot" />
              Healthy
            </span>
            <strong>{results.healthy_assets}</strong>
          </div>

          <div>
            <span>
              <i className="amber-dot" />
              Degraded
            </span>
            <strong>{results.degraded_assets}</strong>
          </div>

          <div>
            <span>
              <i className="red-dot" />
              Failed
            </span>
            <strong>{results.failed_assets}</strong>
          </div>

        </div>

      </div>


      {/* ======================================================
          OPERATOR FOCUS
      ====================================================== */}

      <div className="panel cc-focus-panel">

        <div className="cc-section-header compact">

          <div>
            <span className="section-kicker">
              OPERATOR WINDOW
            </span>

            <h2>Recommended focus</h2>
          </div>

          <Clock3
            size={20}
            className="accent-icon"
          />

        </div>


        <div
          className={`cc-focus-card ${commandStateClass}`}
        >

          <div className="cc-focus-icon">
            <Zap size={20} />
          </div>

          <div>

            <span>NEXT ACTION</span>

            <strong>
              {critical
                ? "Resolve critical assets first."
                : high
                  ? "Schedule high-priority maintenance."
                  : medium
                    ? "Increase inspection frequency."
                    : "Continue routine monitoring."}
            </strong>

            <p>
              {critical
                ? `${critical} asset(s) require immediate operational attention.`
                : high
                  ? `${high} high-priority asset(s) are waiting for intervention.`
                  : medium
                    ? `${medium} asset(s) should enter an increased inspection cycle.`
                    : "No urgent intervention is currently indicated."}
            </p>

          </div>

        </div>


        <div className="cc-focus-metric">

          <div>
            <span>AVERAGE RISK</span>
            <strong>
              {averageRisk.toFixed(0)}
            </strong>
          </div>

          <div>
            <span>FAILURE PROBABILITY</span>
            <strong>
              {Math.round(
                (results.prediction
                  ?.failure_probability ?? 0) * 100,
              )}
              %
            </strong>
          </div>

          <div>
            <span>MODEL CONFIDENCE</span>
            <strong>
              {Math.round(
                (results.prediction?.confidence ?? 0) *
                  100,
              )}
              %
            </strong>
          </div>

        </div>

      </div>


      {/* ======================================================
          DIGITAL TWIN / RUN INTELLIGENCE
      ====================================================== */}

      <div className="panel cc-intelligence-panel">

        <div className="cc-section-header compact">

          <div>
            <span className="section-kicker">
              DIGITAL TWIN
            </span>

            <h2>Simulation state</h2>
          </div>

          <Gauge
            size={20}
            className="accent-icon"
          />

        </div>


        <div className="cc-twin-status">

          <div className="cc-twin-number">
            <strong>
              {results.metadata?.digital_twins ??
                results.total_assets}
            </strong>

            <span>ACTIVE TWINS</span>
          </div>

          <div className="cc-twin-copy">
            <strong>
              Asset states synchronized
            </strong>

            <span>
              Digital Twins tracked throughout the
              simulation run.
            </span>
          </div>

        </div>


        <div className="cc-run-grid">

          <div>
            <span>REPLAY</span>
            <strong>
              {results.metadata?.replay_frames ??
                "—"}
            </strong>
            <small>frames</small>
          </div>

          <div>
            <span>DURATION</span>
            <strong>
              {results.metadata?.duration_seconds ??
                "—"}
            </strong>
            <small>seconds</small>
          </div>

          <div>
            <span>ENGINE</span>
            <strong>TDOS</strong>
            <small>simulation core</small>
          </div>

        </div>

      </div>

    </section>
  );
}