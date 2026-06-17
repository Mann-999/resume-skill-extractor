import { useState } from 'react'
import styles from './JDMatchTab.module.css'

const EMPTY_JD = { title: '', description: '' }

export default function JDMatchTab({ rawText }) {
  const [jds, setJds] = useState([{ ...EMPTY_JD }, { ...EMPTY_JD }])
  const [matches, setMatches] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const updateJD = (i, field, val) => {
    setJds(prev => prev.map((jd, idx) => idx === i ? { ...jd, [field]: val } : jd))
  }

  const addJD = () => setJds(prev => [...prev, { ...EMPTY_JD }])
  const removeJD = (i) => setJds(prev => prev.filter((_, idx) => idx !== i))

  const handleMatch = async () => {
    const valid = jds.filter(jd => jd.title.trim() && jd.description.trim())
    if (!valid.length) { setError('Add at least one complete JD.'); return }
    setLoading(true)
    setError('')
    try {
      const res = await fetch('/match-jds', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_text: rawText, job_descriptions: valid }),
      })
      const data = await res.json()
      if (!res.ok) throw new Error(data.error || 'Failed')
      setMatches(data.matches)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const scoreColor = (score) => {
    if (score >= 75) return 'var(--accent3)'
    if (score >= 50) return 'var(--accent)'
    return 'var(--accent2)'
  }

  return (
    <div className={styles.container}>
      <div className="card">
        <h2 className={styles.sectionTitle}>
          <span className={styles.dot} />
          Job Descriptions
        </h2>
        <p className={styles.hint}>Paste JDs below. Your resume will be ranked against all of them.</p>

        <div className={styles.jdList}>
          {jds.map((jd, i) => (
            <div key={i} className={styles.jdItem}>
              <div className={styles.jdHeader}>
                <span className={styles.jdNum}>JD {i + 1}</span>
                {jds.length > 1 && (
                  <button className={styles.removeBtn} onClick={() => removeJD(i)}>✕</button>
                )}
              </div>
              <input
                className={styles.titleInput}
                placeholder="Job title (e.g. Software Engineer at Google)"
                value={jd.title}
                onChange={e => updateJD(i, 'title', e.target.value)}
              />
              <textarea
                className={styles.jdTextarea}
                placeholder="Paste the full job description here..."
                value={jd.description}
                onChange={e => updateJD(i, 'description', e.target.value)}
                rows={5}
              />
            </div>
          ))}
        </div>

        <div className={styles.jdActions}>
          <button className="btn-ghost" onClick={addJD}>+ Add JD</button>
          <button
            className="btn-primary"
            onClick={handleMatch}
            disabled={loading}
            style={{ display: 'flex', alignItems: 'center', gap: '8px' }}
          >
            {loading ? <><span className="spinner" /> Matching…</> : '⚡ Match & Rank'}
          </button>
        </div>

        {error && <p className={styles.error}>{error}</p>}
      </div>

      {matches && (
        <div className={styles.results}>
          <h3 className={styles.resultsTitle}>Ranked Results</h3>
          {matches.map((m, i) => (
            <div key={i} className={`card ${styles.matchCard} fade-up`}>
              <div className={styles.matchTop}>
                <div className={styles.matchLeft}>
                  <span className={styles.matchRank}>#{i + 1}</span>
                  <span className={styles.matchTitle}>{m.title}</span>
                </div>
                <span className={styles.matchScore} style={{ color: scoreColor(m.match_score) }}>
                  {m.match_score}%
                </span>
              </div>

              <div className={styles.scoreBar}>
                <div
                  className={styles.scoreBarFill}
                  style={{ width: `${m.match_score}%`, background: scoreColor(m.match_score) }}
                />
              </div>

              <p className={styles.verdict}>{m.verdict}</p>

              <div className={styles.skillsRow}>
                <div className={styles.skillGroup}>
                  <span className={styles.skillLabel}>Matched</span>
                  <div className={styles.skillTags}>
                    {(m.matched_skills || []).map(s => (
                      <span key={s} className="tag green">{s}</span>
                    ))}
                  </div>
                </div>
                <div className={styles.skillGroup}>
                  <span className={styles.skillLabel}>Missing</span>
                  <div className={styles.skillTags}>
                    {(m.missing_skills || []).map(s => (
                      <span key={s} className="tag soft">{s}</span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}