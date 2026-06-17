import { useState } from 'react'
import styles from './BulletsTab.module.css'

function extractBullets(text) {
  const lines = text.split('\n').map(l => l.trim()).filter(Boolean)
  return lines.filter(l =>
    l.startsWith('-') || l.startsWith('•') || l.startsWith('*') || /^\d+\./.test(l)
  ).map(l => l.replace(/^[-•*]\s*/, '').replace(/^\d+\.\s*/, '').trim())
    .filter(l => l.length > 20)
    .slice(0, 15)
}

export default function BulletsTab({ rawText }) {
  const detected = extractBullets(rawText)
  const [bullets, setBullets] = useState(detected.join('\n'))
  const [rewrites, setRewrites] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleRewrite = async () => {
    const list = bullets.split('\n').map(b => b.trim()).filter(Boolean)
    if (!list.length) return
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/rewrite-bullets', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bullets: list }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed')
      setRewrites(data.rewrites)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <div className="card">
        <h2 className={styles.sectionTitle}>
          <span className={styles.dot} />
          Resume Bullet Points
        </h2>
        <p className={styles.hint}>
          Auto-detected from your resume. Edit or add more below.
        </p>
        <textarea
          className={styles.textarea}
          value={bullets}
          onChange={e => setBullets(e.target.value)}
          rows={8}
          placeholder="Paste bullet points here, one per line..."
        />
        {error && <p className={styles.error}>{error}</p>}
        <button
          className={`btn-primary ${styles.rewriteBtn}`}
          onClick={handleRewrite}
          disabled={loading || !bullets.trim()}
        >
          {loading ? <><span className="spinner" /> Rewriting with Gemini…</> : '✦ Rewrite with AI'}
        </button>
      </div>

      {rewrites && (
        <div className={styles.results}>
          {rewrites.map((r, i) => (
            <div key={i} className={`card ${styles.rewriteCard} fade-up`}>
              <div className={styles.original}>
                <span className={styles.label}>Original</span>
                <p>{r.original}</p>
              </div>
              <div className={styles.arrow}>↓</div>
              <div className={styles.rewritten}>
                <span className={styles.label} style={{ color: 'var(--accent3)' }}>Rewritten</span>
                <p>{r.rewritten}</p>
              </div>
              {r.tip && (
                <div className={styles.tip}>
                  <span className={styles.tipIcon}>💡</span>
                  <span>{r.tip}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}