import { useState } from 'react'
import ReactMarkdown from 'react-markdown'
import './ResultView.css'

function ResultView({ result }) {
  const [activeSection, setActiveSection] = useState('what_i_say_simple')
  const [showFeedback, setShowFeedback] = useState(false)

  const sections = [
    { key: 'what_they_said_simple', label: 'What they said — simple' },
    { key: 'what_they_said_deep', label: 'What they said — deep' },
    { key: 'what_i_say_simple', label: "What I'd say — simple" },
    { key: 'what_i_say_deep', label: "What I'd say — deep" },
  ]

  const handleFeedback = async (soundsLikeMe) => {
    if (!activeSection.startsWith('what_i_say')) {
      alert('Feedback is only available for "What I\'d say" sections')
      return
    }

    try {
      await fetch('/api/feedback', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          content_id: result.id,
          section: activeSection,
          sounds_like_me: soundsLikeMe
        })
      })
      setShowFeedback(true)
      setTimeout(() => setShowFeedback(false), 3000)
    } catch (err) {
      console.error('Failed to submit feedback:', err)
    }
  }

  return (
    <div className="result-view">
      <div className="result-header">
        <h2>{result.title}</h2>
        <div className="result-meta">
          <span className="source-badge">{result.source_type}</span>
          {result.url && (
            <a href={result.url} target="_blank" rel="noopener noreferrer" className="source-link">
              View Original
            </a>
          )}
          <span className="processing-time">
            {result.processing_time_seconds?.toFixed(1)}s
          </span>
        </div>
      </div>

      <div className="section-tabs">
        {sections.map(section => (
          <button
            key={section.key}
            className={activeSection === section.key ? 'active' : ''}
            onClick={() => setActiveSection(section.key)}
          >
            {section.label}
          </button>
        ))}
      </div>

      <div className="section-content">
        <ReactMarkdown>
          {result[activeSection] || 'No content available'}
        </ReactMarkdown>
      </div>

      {activeSection.startsWith('what_i_say') && (
        <div className="feedback-section">
          <p className="feedback-prompt">Does this sound like you?</p>
          <div className="feedback-buttons">
            <button onClick={() => handleFeedback(true)} className="feedback-yes">
              Yes, sounds like me
            </button>
            <button onClick={() => handleFeedback(false)} className="feedback-no">
              No, doesn't sound like me
            </button>
          </div>
          {showFeedback && (
            <p className="feedback-thanks">Thanks! This helps improve your voice profile.</p>
          )}
        </div>
      )}

      {result.markdown_path && (
        <div className="markdown-info">
          <p>Saved to: <code>{result.markdown_path}</code></p>
        </div>
      )}
    </div>
  )
}

export default ResultView
