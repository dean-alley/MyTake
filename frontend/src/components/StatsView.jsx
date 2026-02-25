import { useState, useEffect } from 'react'
import './StatsView.css'

function StatCard({ label, value, sub }) {
  return (
    <div className="stat-card">
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
      {sub && <div className="stat-sub">{sub}</div>}
    </div>
  )
}

function StatsView() {
  const [overview, setOverview] = useState(null)
  const [insights, setInsights] = useState(null)
  const [voicePerf, setVoicePerf] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    async function fetchAll() {
      try {
        const [ov, ins, vp] = await Promise.all([
          fetch('/api/analytics/overview').then(r => r.json()),
          fetch('/api/analytics/content-insights').then(r => r.json()),
          fetch('/api/analytics/voice-performance').then(r => r.json()),
        ])
        setOverview(ov)
        setInsights(ins)
        setVoicePerf(vp)
      } catch (e) {
        setError(e.message)
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [])

  if (loading) return <div className="stats-loading">Loading analytics…</div>
  if (error)   return <div className="stats-error">Error: {error}</div>
  if (!overview || overview.total_items === 0) {
    return (
      <div className="stats-empty">
        <h2>No data yet</h2>
        <p>Process some content first and check back here.</p>
      </div>
    )
  }

  const vf = overview.voice_feedback
  const ps = overview.processing_stats

  return (
    <div className="stats-view">
      <h2>Analytics</h2>

      {/* top-level numbers */}
      <div className="stat-grid">
        <StatCard label="Items processed" value={overview.total_items} />
        <StatCard
          label="Avg processing time"
          value={`${ps.average_time_seconds}s`}
          sub={`${ps.min_time_seconds}s – ${ps.max_time_seconds}s`}
        />
        <StatCard
          label="Voice feedback"
          value={vf.total || 0}
          sub={vf.accuracy_percentage != null ? `${vf.accuracy_percentage}% positive` : 'none yet'}
        />
        {insights && (
          <StatCard
            label="Avg input length"
            value={`${insights.input_word_stats?.average || '—'} words`}
          />
        )}
      </div>

      {/* content types */}
      <section className="stats-section">
        <h3>Content Types</h3>
        <div className="bar-group">
          {Object.entries(overview.content_type_distribution).map(([type, count]) => (
            <div key={type} className="bar-row">
              <span className="bar-label">{type}</span>
              <div className="bar-track">
                <div
                  className="bar-fill"
                  style={{ width: `${(count / overview.total_items) * 100}%` }}
                />
              </div>
              <span className="bar-count">{count}</span>
            </div>
          ))}
        </div>
      </section>

      {/* output section word counts */}
      {insights?.average_output_words && (
        <section className="stats-section">
          <h3>Average Output Length (words)</h3>
          <div className="bar-group">
            {Object.entries(insights.average_output_words).map(([section, avg]) => {
              const label = section
                .replace('what_they_said_', 'They said — ')
                .replace('what_i_say_', "I'd say — ")
              const max = Math.max(...Object.values(insights.average_output_words))
              return (
                <div key={section} className="bar-row">
                  <span className="bar-label">{label}</span>
                  <div className="bar-track">
                    <div className="bar-fill" style={{ width: `${(avg / max) * 100}%` }} />
                  </div>
                  <span className="bar-count">{avg}</span>
                </div>
              )
            })}
          </div>
        </section>
      )}

      {/* voice performance */}
      {voicePerf?.section_performance && (
        <section className="stats-section">
          <h3>Voice Accuracy by Section</h3>
          <div className="bar-group">
            {Object.entries(voicePerf.section_performance).map(([section, stats]) => {
              const label = section
                .replace('what_i_say_simple', "I'd say — simple")
                .replace('what_i_say_deep', "I'd say — deep")
              return (
                <div key={section} className="bar-row">
                  <span className="bar-label">{label}</span>
                  <div className="bar-track">
                    <div
                      className="bar-fill green"
                      style={{ width: `${stats.accuracy_percentage}%` }}
                    />
                  </div>
                  <span className="bar-count">{stats.accuracy_percentage}%</span>
                </div>
              )
            })}
          </div>
        </section>
      )}

      {/* top keywords */}
      {insights?.top_keywords?.length > 0 && (
        <section className="stats-section">
          <h3>Top Keywords</h3>
          <div className="keyword-cloud">
            {insights.top_keywords.map(({ word, count }) => (
              <span key={word} className="keyword-tag">
                {word} <em>{count}</em>
              </span>
            ))}
          </div>
        </section>
      )}

      {/* recent items */}
      <section className="stats-section">
        <h3>Recent Items</h3>
        <table className="recent-table">
          <thead>
            <tr><th>ID</th><th>Type</th><th>Title</th><th>Time</th></tr>
          </thead>
          <tbody>
            {overview.recent_items.map(item => (
              <tr key={item.id}>
                <td>{item.id}</td>
                <td><span className="source-badge small">{item.source_type}</span></td>
                <td>{item.title}</td>
                <td>{item.processing_time_seconds}s</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  )
}

export default StatsView
