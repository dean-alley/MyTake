import { useState } from 'react'
import ProcessForm from './components/ProcessForm'
import ResultView from './components/ResultView'
import ContentList from './components/ContentList'
import './App.css'

function App() {
  const [currentView, setCurrentView] = useState('process') // 'process' or 'history'
  const [currentResult, setCurrentResult] = useState(null)

  const handleProcessComplete = (result) => {
    setCurrentResult(result)
  }

  const handleViewContent = (content) => {
    setCurrentResult(content)
    setCurrentView('process')
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>MyTake</h1>
          <p className="tagline">Turn links into understanding — in your voice</p>
        </div>
        <nav className="nav-tabs">
          <button
            className={currentView === 'process' ? 'active' : ''}
            onClick={() => setCurrentView('process')}
          >
            Process
          </button>
          <button
            className={currentView === 'history' ? 'active' : ''}
            onClick={() => setCurrentView('history')}
          >
            History
          </button>
        </nav>
      </header>

      <main className="app-main">
        {currentView === 'process' ? (
          <div className="process-view">
            <ProcessForm onComplete={handleProcessComplete} />
            {currentResult && <ResultView result={currentResult} />}
          </div>
        ) : (
          <ContentList onViewContent={handleViewContent} />
        )}
      </main>

      <footer className="app-footer">
        <p>MyTake - A thinking amplifier, not a content farm</p>
      </footer>
    </div>
  )
}

export default App
