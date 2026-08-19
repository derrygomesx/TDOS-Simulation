import {
  Activity,
  ArrowDownRight,
  ArrowRight,
  ArrowUpRight,
  CheckCircle2,
  FlaskConical,
  Gauge,
  Plus,
  RotateCcw,
  ShieldCheck,
  Sparkles,
  Trash2,
  TrendingDown,
  TrendingUp,
  Wrench,
  X,
  Zap,
} from "lucide-react";

type Decision = {
  asset_id: string;
  asset_name: string;
  asset_type: string;
  priority: string;
  action: string;
  timing: string;
  reason: string;
  health_score: number;
  rams_score: number;
  failure_probability: number;
  remaining_useful_life_days: number;
  criticality: string;
  maintenance_required: boolean;
  factors: Record<string, number>;
};

type DecisionResult = {
  simulation_id: string;
  simulation_name: string;
  methodology: string;
  summary: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    immediate_actions: number;
    planned_actions: number;
  };
  decisions: Decision[];
};

type WhatIfScenario = {
  id: string;
  name: string;
  asset_id: string;
  health_recovery: number;
  degradation_reduction_percent: number;
};

type WhatIfResult = {
  asset_id: string;
  asset_name: string;

  intervention: {
    health_recovery: number;
    degradation_reduction_percent: number;
  };

  before: Decision;
  after: Decision;

  changes: {
    health_score: number;
    rams_score: number;
    failure_probability: number;
    remaining_useful_life_days: number;
  };

  scenario_id?: string;
  scenario_name?: string;
};

type WhatIfBatchResult = {
  simulation_id: string;
  scenario_count: number;
  scenarios: WhatIfResult[];
};

type Props = {
  decisions: DecisionResult | null;
  whatIf: WhatIfBatchResult | null;
  scenarios: WhatIfScenario[];

  onScenarioChange: (
    id: string,
    patch: Partial<WhatIfScenario>,
  ) => void;

  onAddScenario: () => void;

  onRemoveScenario: (id: string) => void;

  onRunWhatIf: () => void | Promise<void>;
};

function deltaClass(value: number, inverse = false) {
  const positive = inverse ? value < 0 : value > 0;

  if (Math.abs(value) < 0.001) {
    return "wil-delta-neutral";
  }

  return positive
    ? "wil-delta-good"
    : "wil-delta-bad";
}

function formatSigned(value: number, digits = 1) {
  if (Math.abs(value) < 0.001) {
    return "0";
  }

  return `${value > 0 ? "+" : ""}${value.toFixed(digits)}`;
}

function priorityClass(priority: string) {
  return `wil-priority wil-priority-${priority.toLowerCase()}`;
}

function scoreScenario(result: WhatIfResult) {
  const healthGain = Math.max(0, result.changes.health_score);
  const ramsGain = Math.max(0, result.changes.rams_score);

  const failureReduction = Math.max(
    0,
    -result.changes.failure_probability * 100,
  );

  const rulGain = Math.max(
    0,
    result.changes.remaining_useful_life_days,
  );

  return (
    healthGain * 0.35 +
    ramsGain * 0.35 +
    failureReduction * 0.2 +
    Math.min(100, rulGain) * 0.1
  );
}

export default function WhatIfLab({
  decisions,
  whatIf,
  scenarios,
  onScenarioChange,
  onAddScenario,
  onRemoveScenario,
  onRunWhatIf,
}: Props) {
  if (!decisions) {
    return (
      <section className="content-grid wil-page">
        <div className="panel span-two wil-empty">
          <div className="wil-empty-icon">
            <FlaskConical size={30} />
          </div>

          <span className="section-kicker">
            STEP 6 · WHAT-IF LAB
          </span>

          <h2>
            Simulation intelligence,
            before the decision.
          </h2>

          <p>
            Complete a TDOS simulation first. The What-If
            Lab will let you test maintenance strategies
            against the resulting asset intelligence.
          </p>
        </div>
      </section>
    );
  }

  const rankedResults = [...(whatIf?.scenarios ?? [])]
    .map((result) => ({
      ...result,
      scenarioScore: scoreScenario(result),
    }))
    .sort(
      (a, b) =>
        b.scenarioScore - a.scenarioScore,
    );

  const bestScenario = rankedResults[0] ?? null;

  const totalHealthGain = rankedResults.reduce(
    (sum, item) =>
      sum + item.changes.health_score,
    0,
  );

  const totalRamsGain = rankedResults.reduce(
    (sum, item) =>
      sum + item.changes.rams_score,
    0,
  );

  const totalFailureReduction = rankedResults.reduce(
    (sum, item) =>
      sum -
      item.changes.failure_probability * 100,
    0,
  );

  return (
    <section className="content-grid wil-page">

      {/* ======================================================
          HERO
      ====================================================== */}

      <div className="panel span-two wil-hero">

        <div className="wil-hero-copy">

          <div className="wil-kicker">
            <span className="wil-pulse" />
            STEP 6 · DECISION EXPERIMENTATION
          </div>

          <h1>
            Test the intervention
            <span> before touching the railway.</span>
          </h1>

          <p>
            Build several maintenance strategies,
            run them against the completed TDOS
            intelligence, and compare the projected
            operational outcome.
          </p>

          <div className="wil-hero-meta">

            <div>
              <span>SIMULATION</span>
              <strong className="mono">
                {decisions.simulation_id}
              </strong>
            </div>

            <div>
              <span>ASSETS</span>
              <strong>
                {decisions.decisions.length}
              </strong>
            </div>

            <div>
              <span>STRATEGIES</span>
              <strong>
                {scenarios.length}
              </strong>
            </div>

          </div>

        </div>

        <div className="wil-hero-orb">
          <div className="wil-orb-ring one" />
          <div className="wil-orb-ring two" />
          <FlaskConical size={54} />
        </div>

      </div>


      {/* ======================================================
          RESULT SUMMARY
      ====================================================== */}

      {whatIf && rankedResults.length > 0 && (
        <div className="wil-summary span-two">

          <div className="wil-summary-card">

            <Activity size={18} />

            <div>
              <span>PROJECTED HEALTH GAIN</span>
              <strong className={deltaClass(totalHealthGain)}>
                {formatSigned(totalHealthGain)}
              </strong>
            </div>

          </div>

          <div className="wil-summary-card">

            <ShieldCheck size={18} />

            <div>
              <span>RAMS IMPROVEMENT</span>
              <strong className={deltaClass(totalRamsGain)}>
                {formatSigned(totalRamsGain)}
              </strong>
            </div>

          </div>

          <div className="wil-summary-card">

            <TrendingDown size={18} />

            <div>
              <span>FAILURE RISK REDUCTION</span>
              <strong className={deltaClass(totalFailureReduction)}>
                {formatSigned(totalFailureReduction)}%
              </strong>
            </div>

          </div>

          <div className="wil-summary-card">

            <Zap size={18} />

            <div>
              <span>BEST STRATEGY</span>
              <strong>
                {bestScenario
                  ? bestScenario.scenario_name ??
                    "Scenario"
                  : "—"}
              </strong>
            </div>

          </div>

        </div>
      )}


      {/* ======================================================
          SCENARIO BUILDER
      ====================================================== */}

      <div className="panel span-two wil-builder">

        <div className="wil-section-head">

          <div>
            <span className="section-kicker">
              SCENARIO BUILDER
            </span>

            <h2>
              Maintenance strategy stack
            </h2>

            <p>
              Create multiple independent
              intervention strategies and compare
              them in a single run.
            </p>
          </div>

          <div className="wil-builder-actions">

            <span className="wil-count">
              {scenarios.length}/12
            </span>

            <button
              className="ghost-button"
              onClick={onAddScenario}
              disabled={scenarios.length >= 12}
            >
              <Plus size={15} />
              Add strategy
            </button>

          </div>

        </div>


        {scenarios.length === 0 ? (
          <div className="wil-no-scenarios">

            <Sparkles size={23} />

            <strong>
              No maintenance strategies configured.
            </strong>

            <span>
              Add a strategy to begin the experiment.
            </span>

            <button
              className="primary-button"
              onClick={onAddScenario}
            >
              <Plus size={15} />
              Create strategy
            </button>

          </div>
        ) : (

          <div className="wil-scenario-stack">

            {scenarios.map((scenario, index) => {

              const selectedAsset =
                decisions.decisions.find(
                  (asset) =>
                    asset.asset_id ===
                    scenario.asset_id,
                );

              return (
                <div
                  className="wil-scenario-card"
                  key={scenario.id}
                >

                  <div className="wil-scenario-index">
                    {String(index + 1).padStart(2, "0")}
                  </div>


                  <div className="wil-scenario-main">

                    <div className="wil-scenario-title">

                      <div>

                        <input
                          className="wil-name-input"
                          value={scenario.name}
                          onChange={(event) =>
                            onScenarioChange(
                              scenario.id,
                              {
                                name:
                                  event.target.value,
                              },
                            )
                          }
                        />

                        <span>
                          MAINTENANCE STRATEGY
                        </span>

                      </div>

                      <button
                        className="wil-remove"
                        onClick={() =>
                          onRemoveScenario(
                            scenario.id,
                          )
                        }
                        aria-label="Remove strategy"
                      >
                        <Trash2 size={15} />
                      </button>

                    </div>


                    <div className="wil-scenario-grid">

                      <label>
                        <span>TARGET ASSET</span>

                        <select
                          value={scenario.asset_id}
                          onChange={(event) =>
                            onScenarioChange(
                              scenario.id,
                              {
                                asset_id:
                                  event.target.value,
                              },
                            )
                          }
                        >
                          {decisions.decisions.map(
                            (asset) => (
                              <option
                                key={asset.asset_id}
                                value={asset.asset_id}
                              >
                                {asset.asset_name}
                                {" · "}
                                {asset.asset_id}
                              </option>
                            ),
                          )}
                        </select>

                        <small>
                          {selectedAsset?.asset_type ??
                            "INFRASTRUCTURE"}
                        </small>
                      </label>


                      <label>
                        <div className="wil-range-label">
                          <span>
                            HEALTH RECOVERY
                          </span>

                          <strong>
                            +{scenario.health_recovery}
                          </strong>
                        </div>

                        <input
                          className="wil-range"
                          type="range"
                          min={0}
                          max={50}
                          step={1}
                          value={
                            scenario.health_recovery
                          }
                          onChange={(event) =>
                            onScenarioChange(
                              scenario.id,
                              {
                                health_recovery:
                                  Number(
                                    event.target.value,
                                  ),
                              },
                            )
                          }
                        />

                        <small>
                          Maximum simulated recovery:
                          +50 points
                        </small>
                      </label>


                      <label>
                        <div className="wil-range-label">
                          <span>
                            DEGRADATION REDUCTION
                          </span>

                          <strong>
                            {
                              scenario.degradation_reduction_percent
                            }
                            %
                          </strong>
                        </div>

                        <input
                          className="wil-range"
                          type="range"
                          min={0}
                          max={100}
                          step={5}
                          value={
                            scenario.degradation_reduction_percent
                          }
                          onChange={(event) =>
                            onScenarioChange(
                              scenario.id,
                              {
                                degradation_reduction_percent:
                                  Number(
                                    event.target.value,
                                  ),
                              },
                            )
                          }
                        />

                        <small>
                          Simulated reduction in
                          degradation rate
                        </small>
                      </label>

                    </div>

                  </div>

                </div>
              );
            })}

          </div>
        )}


        <div className="wil-run-bar">

          <div>

            <div className="wil-run-status">
              <span />
              NON-DESTRUCTIVE EXPERIMENT
            </div>

            <p>
              The completed simulation remains
              unchanged. TDOS evaluates each strategy
              independently against the same baseline.
            </p>

          </div>

          <button
            className="primary-button wil-run-button"
            disabled={!scenarios.length}
            onClick={onRunWhatIf}
          >
            <FlaskConical size={17} />
            Run What-If Lab
          </button>

        </div>

      </div>


      {/* ======================================================
          BEST STRATEGY
      ====================================================== */}

      {bestScenario && (
        <div className="panel span-two wil-best">

          <div className="wil-best-icon">
            <CheckCircle2 size={24} />
          </div>

          <div className="wil-best-copy">

            <span className="section-kicker">
              RECOMMENDED EXPERIMENT
            </span>

            <h2>
              {bestScenario.scenario_name ??
                "Best strategy"}
            </h2>

            <p>
              Based on projected health recovery,
              RAMS improvement, failure-risk reduction
              and remaining useful life extension.
            </p>

          </div>

          <div className="wil-best-action">

            <span>
              PROJECTED HEALTH
            </span>

            <strong>
              {bestScenario.after.health_score.toFixed(
                1,
              )}
            </strong>

            <small>
              from{" "}
              {bestScenario.before.health_score.toFixed(
                1,
              )}
            </small>

          </div>

        </div>
      )}


      {/* ======================================================
          COMPARISON
      ====================================================== */}

      <div className="panel span-two wil-results">

        <div className="wil-section-head">

          <div>
            <span className="section-kicker">
              SCENARIO COMPARISON
            </span>

            <h2>
              Before → projected after
            </h2>

            <p>
              Compare the operational consequences of
              every maintenance strategy.
            </p>
          </div>

          {whatIf && (
            <span className="wil-result-badge">
              {whatIf.scenario_count} evaluated
            </span>
          )}

        </div>


        {!whatIf ||
        !whatIf.scenarios.length ? (

          <div className="wil-results-empty">

            <Gauge size={27} />

            <strong>
              No experiment results yet.
            </strong>

            <span>
              Configure your strategies above and
              run the lab.
            </span>

          </div>

        ) : (

          <div className="wil-results-list">

            {rankedResults.map(
              (result, index) => {

                const healthDelta =
                  result.changes.health_score;

                const ramsDelta =
                  result.changes.rams_score;

                const failureDelta =
                  result.changes.failure_probability *
                  100;

                const rulDelta =
                  result.changes
                    .remaining_useful_life_days;

                return (
                  <div
                    className={`wil-result-card ${
                      index === 0
                        ? "wil-result-best"
                        : ""
                    }`}
                    key={
                      result.scenario_id ??
                      `${result.asset_id}-${index}`
                    }
                  >

                    <div className="wil-result-rank">

                      {index === 0 ? (
                        <Sparkles size={16} />
                      ) : (
                        String(index + 1).padStart(
                          2,
                          "0",
                        )
                      )}

                    </div>


                    <div className="wil-result-identity">

                      <div className="wil-result-title">

                        <strong>
                          {result.scenario_name ??
                            "Maintenance strategy"}
                        </strong>

                        {index === 0 && (
                          <span className="wil-best-pill">
                            BEST PROJECTED OUTCOME
                          </span>
                        )}

                      </div>

                      <span>
                        {result.asset_name}
                        {" · "}
                        {result.asset_id}
                      </span>

                      <div className="wil-priority-transition">

                        <span
                          className={priorityClass(
                            result.before.priority,
                          )}
                        >
                          {result.before.priority}
                        </span>

                        <ArrowRight size={14} />

                        <span
                          className={priorityClass(
                            result.after.priority,
                          )}
                        >
                          {result.after.priority}
                        </span>

                      </div>

                    </div>


                    <div className="wil-result-metrics">

                      <div>
                        <span>HEALTH</span>

                        <strong>
                          {result.before.health_score.toFixed(
                            1,
                          )}
                        </strong>

                        <ArrowRight size={12} />

                        <strong>
                          {result.after.health_score.toFixed(
                            1,
                          )}
                        </strong>

                        <small
                          className={deltaClass(
                            healthDelta,
                          )}
                        >
                          {formatSigned(
                            healthDelta,
                          )}
                        </small>
                      </div>


                      <div>
                        <span>RAMS</span>

                        <strong>
                          {result.before.rams_score.toFixed(
                            1,
                          )}
                        </strong>

                        <ArrowRight size={12} />

                        <strong>
                          {result.after.rams_score.toFixed(
                            1,
                          )}
                        </strong>

                        <small
                          className={deltaClass(
                            ramsDelta,
                          )}
                        >
                          {formatSigned(
                            ramsDelta,
                          )}
                        </small>
                      </div>


                      <div>
                        <span>FAILURE RISK</span>

                        <strong>
                          {(
                            result.before
                              .failure_probability *
                            100
                          ).toFixed(1)}
                          %
                        </strong>

                        <ArrowRight size={12} />

                        <strong>
                          {(
                            result.after
                              .failure_probability *
                            100
                          ).toFixed(1)}
                          %
                        </strong>

                        <small
                          className={deltaClass(
                            failureDelta,
                            true,
                          )}
                        >
                          {formatSigned(
                            failureDelta,
                          )}
                          %
                        </small>
                      </div>


                      <div>
                        <span>RUL</span>

                        <strong>
                          {
                            result.before
                              .remaining_useful_life_days
                          }
                          d
                        </strong>

                        <ArrowRight size={12} />

                        <strong>
                          {
                            result.after
                              .remaining_useful_life_days
                          }
                          d
                        </strong>

                        <small
                          className={deltaClass(
                            rulDelta,
                          )}
                        >
                          {formatSigned(
                            rulDelta,
                            0,
                          )}
                          d
                        </small>
                      </div>

                    </div>


                    <div className="wil-result-action">

                      <Wrench size={15} />

                      <div>
                        <span>PROJECTED ACTION</span>

                        <strong>
                          {result.after.action}
                        </strong>

                        <small>
                          {result.after.timing}
                        </small>
                      </div>

                    </div>

                  </div>
                );
              },
            )}

          </div>

        )}

      </div>


      {/* ======================================================
          EXPLANATION
      ====================================================== */}

      <div className="panel span-two wil-explanation">

        <div className="wil-explanation-icon">
          <RotateCcw size={19} />
        </div>

        <div>

          <span className="section-kicker">
            HOW THE LAB WORKS
          </span>

          <h3>
            Same baseline. Different intervention.
          </h3>

          <p>
            Each strategy is evaluated independently
            using the completed RAMS and decision-support
            state. The experiment does not mutate the
            original simulation or asset state.
          </p>

        </div>

        <div className="wil-method-flow">

          <span>BASELINE</span>
          <ArrowRight size={14} />
          <span>INTERVENTION</span>
          <ArrowRight size={14} />
          <span>PROJECTED STATE</span>

        </div>

      </div>

    </section>
  );
}