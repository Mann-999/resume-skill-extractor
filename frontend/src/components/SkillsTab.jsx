import styles from './SkillsTab.module.css'

export default function SkillsTab({ skills }) {
  const technical = skills?.technical || []
  const soft = skills?.soft || []

  return (
    <div className={styles.container}>
      <div className="card">
        <h2 className={styles.sectionTitle}>
          <span className={styles.dot} style={{ background: 'var(--accent)' }} />
          Technical Skills
          <span className={styles.count}>{technical.length}</span>
        </h2>
        <div className={styles.tagCloud}>
          {technical.length > 0
            ? technical.map(s => <span key={s} className="tag tech">{s}</span>)
            : <span className={styles.empty}>No technical skills found.</span>}
        </div>
      </div>

      <div className="card">
        <h2 className={styles.sectionTitle}>
          <span className={styles.dot} style={{ background: 'var(--accent2)' }} />
          Soft Skills
          <span className={styles.count}>{soft.length}</span>
        </h2>
        <div className={styles.tagCloud}>
          {soft.length > 0
            ? soft.map(s => <span key={s} className="tag soft">{s}</span>)
            : <span className={styles.empty}>No soft skills found.</span>}
        </div>
      </div>
    </div>
  )
}