import { useState, useEffect } from 'react'
import './ContentList.css'

function ContentList({ onViewContent }) {
  const [content, setContent] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchContent()
  }, [])

  const fetchContent = async () => {
    try {
      const response = await fetch('/api/content')
      if (!response.ok) {
        throw new Error('Failed to fetch content')
      }
      const data = await response.json()
      setContent(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading history...</div>
  }

  if (error) {
    return <div className="error">Error: {error}</div>
  }

  if (content.length === 0) {
    return (
      <div className="empty-state">
        <h2>No content yet</h2>
        <p>Process your first URL or text to get started!</p>
      </div>
    )
  }

  return (
    <div className="content-list">
      <h2>Your MyTakes</h2>
      <div className="content-grid">
        {content.map(item => (
          <div key={item.id} className="content-card">
            <div className="card-header">
              <h3>{item.title}</h3>
              <span className="source-badge">{item.source_type}</span>
            </div>
            <div className="card-meta">
              <span className="date">
                {new Date(item.created_at).toLocaleDateString()}
              </span>
              {item.processing_time_seconds && (
                <span className="processing-time">
                  {item.processing_time_seconds.toFixed(1)}s
                </span>
              )}
            </div>
            <div className="card-preview">
              {item.what_i_say_simple.substring(0, 150)}...
            </div>
            <button
              onClick={() => onViewContent(item)}
              className="view-button"
            >
              View Full Take
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default ContentList
