import { useState } from 'react'
import UploadPage from './pages/UploadPage.jsx'
import ResultsPage from './pages/ResultsPage.jsx'

export default function App() {
  const [analysisData, setAnalysisData] = useState(null)

  const handleAnalysisDone = (data) => setAnalysisData(data)
  const handleReset = () => setAnalysisData(null)

  return analysisData
    ? <ResultsPage data={analysisData} onReset={handleReset} />
    : <UploadPage onDone={handleAnalysisDone} />
}