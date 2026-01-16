import { useState } from 'react'
import './ProcessForm.css'

function ProcessForm({ onComplete }) {
  const [inputData, setInputData] = useState('')
  const [sourceType, setSourceType] = useState('auto')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!inputData.trim()) {
      setError('Please enter a URL or text')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/process', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input_data: inputData,
          source_type: sourceType
        })
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.detail || 'Processing failed')
      }

      const result = await response.json()
      onComplete(result)
      setInputData('')
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="process-form">
      <h2>Process Content</h2>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="input-data">URL or Text</label>
          <textarea
            id="input-data"
            value={inputData}
            onChange={(e) => setInputData(e.target.value)}
            placeholder="Paste a YouTube or TikTok URL, or enter text directly..."
            rows="4"
            disabled={loading}
          />
        </div>

        <div className="form-group">
          <label htmlFor="source-type">Source Type</label>
          <select
            id="source-type"
            value={sourceType}
            onChange={(e) => setSourceType(e.target.value)}
            disabled={loading}
          >
            <option value="auto">Auto-detect</option>
            <option value="youtube">YouTube</option>
            <option value="tiktok">TikTok</option>
            <option value="text">Plain Text</option>
          </select>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <button type="submit" disabled={loading} className="submit-button">
          {loading ? 'Processing...' : 'Process'}
        </button>
      </form>

      {loading && (
        <div className="loading-indicator">
          <div className="spinner"></div>
          <p>Extracting content and generating your MyTake...</p>
          <p className="loading-hint">This may take 30-60 seconds</p>
        </div>
      )}
    </div>
  )
}

export default ProcessForm
