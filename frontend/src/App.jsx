import { useState } from 'react'
import ProcessForm from './components/ProcessForm'
import ResultView from './components/ResultView'
import ContentList from './components/ContentList'
import StatsView from './components/StatsView'
import './App.css'

const VIEWS = ['process', 'history', 'stats']

function App() {
  const [currentView, setCurrentView] = useState('process')
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
          {VIEWS.map(view => (
            <button
              key={view}
              className={currentView === view ? 'active' : ''}
              onClick={() => setCurrentView(view)}
            >
              {view.charAt(0).toUpperCase() + view.slice(1)}
            </button>
          ))}
        </nav>
      </header>

      <main className="app-main">
        {currentView === 'process' && (
          <div className="process-view">
            <ProcessForm onComplete={handleProcessComplete} />
            {currentResult && <ResultView result={currentResult} />}
          </div>
        )}
        {currentView === 'history' && (
          <ContentList onViewContent={handleViewContent} />
        )}
        {currentView === 'stats' && (
          <StatsView />
        )}
      </main>

      <footer className="app-footer">
        <p>MyTake — a thinking amplifier, not a content farm</p>
      </footer>
    </div>
  )
}

export default App
