import { useState, useRef } from 'react'
import styles from './UploadPage.module.css'

export default function UploadPage({ onDone }) {
  const [file, setFile] = useState(null)
  const [dragging, setDragging] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const inputRef = useRef()

  const handleFile = (f) => {
    if (f && f.type === 'application/pdf') {
      setFile(f)
      setError('')
    } else {
      setError('Only PDF files are supported.')
    }
  }

  const handleDrop = (e) => {
    e.preventDefault()
    setDragging(false)
    handleFile(e.dataTransfer.files[0])
  }

  const handleSubmit = async () => {
    if (!file) return
    setLoading(true)
    setError('')
    try {
      const form = new FormData()
      form.append('resume', file)
      const res = await fetch('/upload', { method: 'POST', body: form })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Upload failed')
      onDone(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.bg} aria-hidden />

      <header className={styles.header}>
        <span className={styles.logo}>ResumeIQ</span>
        <span className={styles.badge}>ML + Gemini</span>
      </header>

      <main className={styles.main}>
        <div className={`${styles.hero} fade-up`}>
          <h1 className={styles.title}>
            Decode your<br />
            <span className={styles.titleAccent}>resume.</span>
          </h1>
          <p className={styles.subtitle}>
            Upload your PDF — get skill extraction, role predictions,<br />
            bullet rewrites, and JD match scoring.
          </p>
        </div>

        <div
          className={`${styles.dropzone} ${dragging ? styles.dragging : ''} ${file ? styles.hasFile : ''} fade-up`}
          style={{ animationDelay: '0.1s' }}
          onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => inputRef.current.click()}
        >
          <input
            ref={inputRef}
            type="file"
            accept=".pdf"
            style={{ display: 'none' }}
            onChange={(e) => handleFile(e.target.files[0])}
          />
          {file ? (
            <div className={styles.fileInfo}>
              <span className={styles.fileIcon}>📄</span>
              <span className={styles.fileName}>{file.name}</span>
              <span className={styles.fileSize}>{(file.size / 1024).toFixed(1)} KB</span>
            </div>
          ) : (
            <div className={styles.dropContent}>
              <div className={styles.uploadIcon}>↑</div>
              <p className={styles.dropText}>Drop your resume PDF here</p>
              <p className={styles.dropSub}>or click to browse</p>
            </div>
          )}
        </div>

        {error && <p className={`${styles.error} fade-up`}>{error}</p>}

        <button
          className={`btn-primary ${styles.analyzeBtn}`}
          onClick={handleSubmit}
          disabled={!file || loading}
          style={{ animationDelay: '0.2s' }}
        >
          {loading ? <><span className="spinner" /> Analyzing…</> : 'Analyze Resume →'}
        </button>

        <div className={`${styles.features} fade-up`} style={{ animationDelay: '0.3s' }}>
          {['Skill Extraction', 'Role Prediction', 'Bullet Rewrites', 'JD Matching'].map(f => (
            <span key={f} className="tag">{f}</span>
          ))}
        </div>
      </main>
    </div>
  )
}