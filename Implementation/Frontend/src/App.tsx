import { type ReactNode, useEffect, useMemo, useState } from "react";

import "./styles.css";

type AssessmentStatus =
  | "draft"
  | "submitted"
  | "scored"
  | "recommendations_generated"
  | "reviewed"
  | "reported";

type CapabilityScore = {
  capability: string;
  score: number;
  maturity_level: number;
  confidence: number;
};

type Recommendation = {
  recommendation_id: string;
  title: string;
  description: string;
  priority: string;
  priority_score: number;
  confidence: number;
  confidence_label: string;
  risk_score: number;
  risk_label: string;
  expected_business_return: Record<string, unknown>;
  expected_life_return: Record<string, unknown>;
  human_time_required: Record<string, unknown>;
  triggered_capabilities: string[];
  capability_score_ids?: string[];
  supporting_evidence_ids?: string[];
  rationale: Record<string, unknown>;
  calculation_trace: Record<string, unknown>;
  recommended_execution_path: string;
};

type DashboardData = {
  source: "api" | "demo";
  businessName: string;
  assessmentStatus: AssessmentStatus;
  progressPercent: number;
  overallScore: number;
  overallConfidence: number;
  scoredAt: string;
  capabilityScores: CapabilityScore[];
  recommendations: Recommendation[];
  recentActivity: string[];
};

type IconName =
  | "dashboard"
  | "businesses"
  | "assessments"
  | "scores"
  | "recommendations"
  | "settings"
  | "businessReturn"
  | "lifeReturn"
  | "humanTime"
  | "confidence";

const demoCapabilities: CapabilityScore[] = [
  { capability: "Human Signature", score: 84, maturity_level: 4, confidence: 0.86 },
  { capability: "Knowledge Assets", score: 62, maturity_level: 3, confidence: 0.78 },
  { capability: "Podcast Assets", score: 74, maturity_level: 3, confidence: 0.82 },
  { capability: "Trust", score: 78, maturity_level: 4, confidence: 0.8 },
  { capability: "Business Systems", score: 48, maturity_level: 2, confidence: 0.74 },
  { capability: "AI Leverage", score: 55, maturity_level: 2, confidence: 0.72 },
  { capability: "Business Return", score: 58, maturity_level: 2, confidence: 0.77 },
  { capability: "Life Return", score: 67, maturity_level: 3, confidence: 0.79 },
];

const demoRecommendations: Recommendation[] = [
  {
    recommendation_id: "demo-knowledge-library",
    title: "Build a reusable knowledge library",
    description: "Turn founder expertise into structured assets that support content and delivery.",
    priority: "High",
    priority_score: 87,
    confidence: 0.82,
    confidence_label: "High",
    risk_score: 0.26,
    risk_label: "Low",
    expected_business_return: { score: 82, label: "High" },
    expected_life_return: { score: 74, label: "Good" },
    human_time_required: { estimated_hours_required: { min: 8, max: 14 } },
    triggered_capabilities: ["Knowledge Assets", "Business Systems"],
    rationale: { why_generated: "Knowledge Assets and Business Systems constrain repeatability." },
    calculation_trace: { source: "Demo data; use ?assessmentId=<id> for Core v1 API data." },
    recommended_execution_path: "DIY",
  },
  {
    recommendation_id: "demo-automation",
    title: "Automate one recurring delivery workflow",
    description: "Reduce founder dependency by standardizing a high-frequency operational process.",
    priority: "High",
    priority_score: 81,
    confidence: 0.76,
    confidence_label: "Medium",
    risk_score: 0.34,
    risk_label: "Medium",
    expected_business_return: { score: 76, label: "Good" },
    expected_life_return: { score: 84, label: "High" },
    human_time_required: { estimated_hours_required: { min: 6, max: 10 } },
    triggered_capabilities: ["Business Systems", "AI Leverage", "Life Return"],
    rationale: { why_generated: "Business Systems and AI Leverage show practical improvement potential." },
    calculation_trace: { source: "Demo data; use ?assessmentId=<id> for Core v1 API data." },
    recommended_execution_path: "DWY",
  },
  {
    recommendation_id: "demo-content-system",
    title: "Create a podcast-to-trust content system",
    description: "Convert podcast assets into repeatable trust-building touchpoints.",
    priority: "Medium",
    priority_score: 72,
    confidence: 0.79,
    confidence_label: "Medium",
    risk_score: 0.22,
    risk_label: "Low",
    expected_business_return: { score: 79, label: "Good" },
    expected_life_return: { score: 68, label: "Good" },
    human_time_required: { estimated_hours_required: { min: 5, max: 9 } },
    triggered_capabilities: ["Podcast Assets", "Trust"],
    rationale: { why_generated: "Podcast Assets are healthy enough to become a stronger trust engine." },
    calculation_trace: { source: "Demo data; use ?assessmentId=<id> for Core v1 API data." },
    recommended_execution_path: "DIY",
  },
];

const demoDashboard: DashboardData = {
  source: "demo",
  businessName: "CreatingReorganized",
  assessmentStatus: "recommendations_generated",
  progressPercent: 100,
  overallScore: 66,
  overallConfidence: 0.79,
  scoredAt: "Demo assessment",
  capabilityScores: demoCapabilities,
  recommendations: demoRecommendations,
  recentActivity: [
    "Demo assessment scored",
    "Demo recommendations generated",
    "Evidence trace available per capability",
  ],
};

const apiBaseUrl = import.meta.env.VITE_PBOS_API_BASE_URL ?? "/api/v1";

function formatPercent(value: number) {
  return `${Math.round(value * 100)}%`;
}

function statusLabel(status: AssessmentStatus) {
  return status.replace(/_/g, " ");
}

function scoreTone(score: number) {
  if (score >= 85) return "excellent";
  if (score >= 70) return "good";
  if (score >= 50) return "attention";
  return "critical";
}

function getNumericScore(value: Record<string, unknown>) {
  const score = value.score;
  return typeof score === "number" ? score : undefined;
}

function getHours(value: Record<string, unknown>) {
  const estimate = value.estimated_hours_required;
  if (
    estimate &&
    typeof estimate === "object" &&
    "min" in estimate &&
    "max" in estimate &&
    typeof estimate.min === "number" &&
    typeof estimate.max === "number"
  ) {
    return `${estimate.min}-${estimate.max}h`;
  }
  return "Trace";
}

function getHourEstimate(value: Record<string, unknown>) {
  const estimate = value.estimated_hours_required;
  if (
    estimate &&
    typeof estimate === "object" &&
    "min" in estimate &&
    "max" in estimate &&
    typeof estimate.min === "number" &&
    typeof estimate.max === "number"
  ) {
    return estimate;
  }
  return undefined;
}

function average(values: number[]) {
  if (values.length === 0) return 0;
  return Math.round(values.reduce((sum, value) => sum + value, 0) / values.length);
}

function humanTimeSummary(recommendations: Recommendation[]) {
  const estimates = recommendations
    .map((recommendation) => getHourEstimate(recommendation.human_time_required))
    .filter((estimate): estimate is { min: number; max: number } => Boolean(estimate));

  if (estimates.length === 0) return "Trace";

  const min = estimates.reduce((sum, estimate) => sum + estimate.min, 0);
  const max = estimates.reduce((sum, estimate) => sum + estimate.max, 0);
  return `${min}-${max}h`;
}

async function getJson<T>(path: string): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`);
  if (!response.ok) {
    throw new Error(`Request failed: ${path}`);
  }
  return response.json() as Promise<T>;
}

function useDashboardData() {
  const [data, setData] = useState<DashboardData>(demoDashboard);
  const [error, setError] = useState<string | null>(null);
  const assessmentId = new URLSearchParams(window.location.search).get("assessmentId");

  useEffect(() => {
    if (!assessmentId) return;

    let cancelled = false;

    async function loadDashboardData() {
      try {
        const [assessment, progress, scores, recommendations] = await Promise.all([
          getJson<{
            status: AssessmentStatus;
            completed_at: string | null;
            created_at: string;
          }>(`/assessments/${assessmentId}`),
          getJson<{ percent_complete: number }>(`/assessments/${assessmentId}/progress`),
          getJson<{
            overall_score: number;
            overall_confidence: number;
            scored_at: string;
            capability_scores: CapabilityScore[];
          }>(`/assessments/${assessmentId}/scores`),
          getJson<Recommendation[]>(`/assessments/${assessmentId}/recommendations`).catch(
            () => [] as Recommendation[],
          ),
        ]);

        if (cancelled) return;

        setData({
          source: "api",
          businessName: "PBOS Founder Dashboard",
          assessmentStatus: assessment.status,
          progressPercent: progress.percent_complete,
          overallScore: Math.round(scores.overall_score),
          overallConfidence: scores.overall_confidence,
          scoredAt: new Date(scores.scored_at).toLocaleString(),
          capabilityScores: scores.capability_scores,
          recommendations,
          recentActivity: [
            `Assessment ${statusLabel(assessment.status)}`,
            `Scored ${new Date(scores.scored_at).toLocaleString()}`,
            `${recommendations.length} recommendations available`,
          ],
        });
        setError(null);
      } catch {
        if (!cancelled) {
          setData(demoDashboard);
          setError("Core v1 data could not be loaded. Showing labeled demo data.");
        }
      }
    }

    void loadDashboardData();

    return () => {
      cancelled = true;
    };
  }, [assessmentId]);

  return { data, error, assessmentId };
}

function RadarPlaceholder({ capabilities }: { capabilities: CapabilityScore[] }) {
  const points = capabilities
    .map((capability, index) => {
      const angle = (Math.PI * 2 * index) / capabilities.length - Math.PI / 2;
      const radius = 22 + (capability.score / 100) * 78;
      return `${110 + Math.cos(angle) * radius},${110 + Math.sin(angle) * radius}`;
    })
    .join(" ");

  return (
    <div className="radar-card" aria-label="Capability radar chart">
      <svg viewBox="0 0 220 220" role="img" aria-label="Radar chart of capability scores">
        <circle cx="110" cy="110" r="94" />
        <circle cx="110" cy="110" r="62" />
        <circle cx="110" cy="110" r="31" />
        {capabilities.map((_, index) => {
          const angle = (Math.PI * 2 * index) / capabilities.length - Math.PI / 2;
          return (
            <line
              key={index}
              x1="110"
              y1="110"
              x2={110 + Math.cos(angle) * 96}
              y2={110 + Math.sin(angle) * 96}
            />
          );
        })}
        <polygon points={points} />
      </svg>
    </div>
  );
}

function SvgIcon({ name }: { name: IconName }) {
  const paths: Record<IconName, ReactNode> = {
    dashboard: (
      <>
        <rect x="3" y="3" width="7" height="8" rx="1.5" />
        <rect x="14" y="3" width="7" height="5" rx="1.5" />
        <rect x="14" y="12" width="7" height="9" rx="1.5" />
        <rect x="3" y="15" width="7" height="6" rx="1.5" />
      </>
    ),
    businesses: (
      <>
        <path d="M4 21V5a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v16" />
        <path d="M16 8h2a2 2 0 0 1 2 2v11" />
        <path d="M8 7h4M8 11h4M8 15h4" />
      </>
    ),
    assessments: (
      <>
        <path d="M8 4h8l2 2v15H6V6l2-2Z" />
        <path d="M9 10h6M9 14h6M9 18h3" />
      </>
    ),
    scores: (
      <>
        <path d="M4 19V5" />
        <path d="M4 19h16" />
        <path d="M8 16v-5M12 16V8M16 16v-9" />
      </>
    ),
    recommendations: (
      <>
        <path d="M12 3a7 7 0 0 0-4 12.74V19h8v-3.26A7 7 0 0 0 12 3Z" />
        <path d="M9 22h6" />
        <path d="M10 11l1.5 1.5L15 9" />
      </>
    ),
    settings: (
      <>
        <circle cx="12" cy="12" r="3" />
        <path d="M19.4 15a8.1 8.1 0 0 0 .1-1.2 8.1 8.1 0 0 0-.1-1.2l2-1.5-2-3.5-2.4 1a8 8 0 0 0-2-1.1L14.7 5h-5.4L9 7.5a8 8 0 0 0-2 1.1l-2.4-1-2 3.5 2 1.5a8.1 8.1 0 0 0-.1 1.2 8.1 8.1 0 0 0 .1 1.2l-2 1.5 2 3.5 2.4-1a8 8 0 0 0 2 1.1l.3 2.5h5.4l.3-2.5a8 8 0 0 0 2-1.1l2.4 1 2-3.5-2-1.5Z" />
      </>
    ),
    businessReturn: (
      <>
        <path d="M4 19V5" />
        <path d="M4 19h16" />
        <path d="m7 15 4-4 3 3 5-7" />
        <path d="M16 7h3v3" />
      </>
    ),
    lifeReturn: (
      <>
        <path d="M12 21s-7-4.5-9-10a5 5 0 0 1 8-5 5 5 0 0 1 8 5c-2 5.5-9 10-9 10Z" />
        <path d="M8 12h2l1-2 2 5 1-3h2" />
      </>
    ),
    humanTime: (
      <>
        <circle cx="12" cy="12" r="8" />
        <path d="M12 8v5l3 2" />
      </>
    ),
    confidence: (
      <>
        <path d="M12 3 4 6v6c0 5 3.4 8 8 9 4.6-1 8-4 8-9V6l-8-3Z" />
        <path d="m8.5 12 2.2 2.2L15.8 9" />
      </>
    ),
  };

  return (
    <svg className="icon" viewBox="0 0 24 24" aria-hidden="true">
      {paths[name]}
    </svg>
  );
}

function MetricCard({
  title,
  value,
  detail,
  icon,
  tone = "neutral",
}: {
  title: string;
  value: string;
  detail: string;
  icon?: IconName;
  tone?: "neutral" | "excellent" | "good" | "attention" | "critical";
}) {
  return (
    <section className={`metric-card metric-card--${tone}`}>
      <div className="metric-card__header">
        {icon && <SvgIcon name={icon} />}
        <p>{title}</p>
      </div>
      <strong>{value}</strong>
      <span>{detail}</span>
    </section>
  );
}

export function App() {
  const { data, error, assessmentId } = useDashboardData();
  const [selectedRecommendation, setSelectedRecommendation] = useState<Recommendation | null>(null);

  const strongest = useMemo(
    () => [...data.capabilityScores].sort((first, second) => second.score - first.score)[0],
    [data.capabilityScores],
  );
  const weakest = useMemo(
    () => [...data.capabilityScores].sort((first, second) => first.score - second.score)[0],
    [data.capabilityScores],
  );
  const topRecommendations = useMemo(
    () =>
      [...data.recommendations]
        .sort((first, second) => second.priority_score - first.priority_score)
        .slice(0, 3),
    [data.recommendations],
  );
  const businessReturn = average(
    data.recommendations
      .map((recommendation) => getNumericScore(recommendation.expected_business_return))
      .filter((score): score is number => typeof score === "number"),
  );
  const lifeReturn = average(
    data.recommendations
      .map((recommendation) => getNumericScore(recommendation.expected_life_return))
      .filter((score): score is number => typeof score === "number"),
  );
  const humanTime = humanTimeSummary(data.recommendations);
  const navItems: { label: string; icon: IconName }[] = [
    { label: "Dashboard", icon: "dashboard" },
    { label: "Businesses", icon: "businesses" },
    { label: "Assessments", icon: "assessments" },
    { label: "Scores", icon: "scores" },
    { label: "Recommendations", icon: "recommendations" },
    { label: "Settings", icon: "settings" },
  ];

  return (
    <main className="founder-dashboard" aria-label="Founder Dashboard">
      <aside className="sidebar">
        <div className="sidebar__brand">
          <img
            className="sidebar__logo"
            src="/creatingreorganized-logo.svg"
            alt="CreatingReorganized"
          />
          <p>Podcast Business Operating System</p>
        </div>
        <nav aria-label="Primary navigation">
          {navItems.map((item) => (
            <a className={item.label === "Dashboard" ? "active" : undefined} href="#" key={item.label}>
              <SvgIcon name={item.icon} />
              {item.label}
            </a>
          ))}
        </nav>
      </aside>

      <section className="dashboard-content">
        <header className="topbar">
          <div>
            <p className="eyebrow">Founder Dashboard</p>
            <h1>{data.businessName}</h1>
          </div>
          <div className="topbar__meta">
            <span className="status-pill">{statusLabel(data.assessmentStatus)}</span>
            <span>{data.scoredAt}</span>
          </div>
        </header>

        {(data.source === "demo" || error) && (
          <div className="demo-banner" role="status">
            {error ?? "Demo data: add ?assessmentId=<id> to load PBHS Core v1 assessment data."}
          </div>
        )}

        <section className="hero-grid" aria-label="Business health summary">
          <section className={`score-hero score-hero--${scoreTone(data.overallScore)}`}>
            <p>Overall PBHS Score</p>
            <div>
              <strong>{data.overallScore}</strong>
              <span>/100</span>
            </div>
            <small>Confidence {formatPercent(data.overallConfidence)}</small>
          </section>
          <MetricCard
            title="Business Return"
            value={businessReturn ? `${businessReturn}` : "Trace"}
            detail="Expected return from recommendations"
            icon="businessReturn"
            tone={businessReturn ? scoreTone(businessReturn) : "neutral"}
          />
          <MetricCard
            title="Life Return"
            value={lifeReturn ? `${lifeReturn}` : "Trace"}
            detail="Founder-life value from recommendations"
            icon="lifeReturn"
            tone={lifeReturn ? scoreTone(lifeReturn) : "neutral"}
          />
          <MetricCard
            title="Human Time"
            value={humanTime}
            detail="Estimated time across recommendations"
            icon="humanTime"
            tone="attention"
          />
          <MetricCard
            title="Confidence"
            value={formatPercent(data.overallConfidence)}
            detail="Evidence-backed certainty"
            icon="confidence"
            tone="good"
          />
        </section>

        <section className="insight-grid">
          <section className="panel panel--wide">
            <div className="panel__header">
              <div>
                <p className="eyebrow">Capability Pattern</p>
                <h2>Radar overview</h2>
              </div>
              <span>8 capabilities</span>
            </div>
            <RadarPlaceholder capabilities={data.capabilityScores} />
          </section>

          <section className="signal-stack">
            <MetricCard
              title="Weakest Capability"
              value={weakest?.capability ?? "Unavailable"}
              detail={weakest ? `${weakest.score}/100, confidence ${formatPercent(weakest.confidence)}` : ""}
              tone={weakest ? scoreTone(weakest.score) : "neutral"}
            />
            <MetricCard
              title="Strongest Capability"
              value={strongest?.capability ?? "Unavailable"}
              detail={
                strongest ? `${strongest.score}/100, confidence ${formatPercent(strongest.confidence)}` : ""
              }
              tone={strongest ? scoreTone(strongest.score) : "neutral"}
            />
          </section>
        </section>

        <section className="panel">
          <div className="panel__header">
            <div>
              <p className="eyebrow">Capability Scores</p>
              <h2>Operating health</h2>
            </div>
          </div>
          <div className="capability-grid">
            {data.capabilityScores.map((capability) => (
              <article
                className={`capability-card capability-card--${scoreTone(capability.score)}`}
                key={capability.capability}
              >
                <div>
                  <h3>{capability.capability}</h3>
                  <span>Maturity {capability.maturity_level}</span>
                </div>
                <strong>{Math.round(capability.score)}</strong>
                <div className="progress-track">
                  <div
                    className={`progress-fill progress-fill--${scoreTone(capability.score)}`}
                    style={{ width: `${capability.score}%` }}
                  />
                </div>
                <small>Confidence {formatPercent(capability.confidence)}</small>
              </article>
            ))}
          </div>
        </section>

        <section className="bottom-grid">
          <section className="panel">
            <div className="panel__header">
              <div>
                <p className="eyebrow">Top 3</p>
                <h2>Latest recommendations</h2>
              </div>
            </div>
            <div className="recommendation-list">
              {topRecommendations.map((recommendation) => (
                <button
                  className="recommendation-row"
                  key={recommendation.recommendation_id}
                  onClick={() => setSelectedRecommendation(recommendation)}
                  type="button"
                >
                  <span>
                    <strong>{recommendation.title}</strong>
                    <small>
                      {recommendation.priority} priority | {recommendation.recommended_execution_path}
                    </small>
                  </span>
                  <span>{Math.round(recommendation.priority_score)}</span>
                </button>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="panel__header">
              <div>
                <p className="eyebrow">Founder Load</p>
                <h2>Human time</h2>
              </div>
            </div>
            <div className="time-stack">
              {topRecommendations.map((recommendation) => (
                <div key={recommendation.recommendation_id}>
                  <span>{recommendation.title}</span>
                  <strong>{getHours(recommendation.human_time_required)}</strong>
                </div>
              ))}
            </div>
          </section>

          <section className="panel">
            <div className="panel__header">
              <div>
                <p className="eyebrow">Activity</p>
                <h2>Recent activity</h2>
              </div>
            </div>
            <ol className="activity-list">
              {data.recentActivity.map((item) => (
                <li key={item}>{item}</li>
              ))}
              {!assessmentId && <li>API activity appears when an assessment is loaded.</li>}
            </ol>
          </section>
        </section>
      </section>

      {selectedRecommendation && (
        <aside className="detail-panel" aria-label="Recommendation detail">
          <button type="button" onClick={() => setSelectedRecommendation(null)}>
            Close
          </button>
          <p className="eyebrow">Recommendation Detail</p>
          <h2>{selectedRecommendation.title}</h2>
          <p>{selectedRecommendation.description}</p>
          <dl>
            <div>
              <dt>Priority</dt>
              <dd>
                {selectedRecommendation.priority} ({Math.round(selectedRecommendation.priority_score)})
              </dd>
            </div>
            <div>
              <dt>Business Return</dt>
              <dd>{JSON.stringify(selectedRecommendation.expected_business_return)}</dd>
            </div>
            <div>
              <dt>Life Return</dt>
              <dd>{JSON.stringify(selectedRecommendation.expected_life_return)}</dd>
            </div>
            <div>
              <dt>Human Time</dt>
              <dd>{JSON.stringify(selectedRecommendation.human_time_required)}</dd>
            </div>
            <div>
              <dt>Confidence</dt>
              <dd>
                {selectedRecommendation.confidence_label} ({formatPercent(selectedRecommendation.confidence)})
              </dd>
            </div>
            <div>
              <dt>Risk</dt>
              <dd>
                {selectedRecommendation.risk_label} ({formatPercent(selectedRecommendation.risk_score)})
              </dd>
            </div>
            <div>
              <dt>Evidence</dt>
              <dd>
                Triggered capabilities: {selectedRecommendation.triggered_capabilities.join(", ")}
                <br />
                Evidence IDs: {selectedRecommendation.supporting_evidence_ids?.join(", ") ?? "Unavailable"}
                <br />
                Capability score IDs: {selectedRecommendation.capability_score_ids?.join(", ") ?? "Unavailable"}
              </dd>
            </div>
            <div>
              <dt>Rationale</dt>
              <dd>{JSON.stringify(selectedRecommendation.rationale)}</dd>
            </div>
            <div>
              <dt>Calculation Trace</dt>
              <dd>{JSON.stringify(selectedRecommendation.calculation_trace)}</dd>
            </div>
          </dl>
        </aside>
      )}
    </main>
  );
}
