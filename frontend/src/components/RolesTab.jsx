import styles from './RolesTab.module.css'

export default function RolesTab({ roles, reasoning }) {
  return (
    <div className={styles.container}>
      <div className="card">
        <h2 className={styles.sectionTitle}>
          <span className={styles.dot} />
          Career Match Predictions
        </h2>
        <div className={styles.roles}>
          {roles.map((role, i) => (
            <div key={role.role} className={styles.roleRow}>
              <div className={styles.roleHeader}>
                <span className={styles.roleRank}>#{i + 1}</span>
                <span className={styles.roleName}>{role.role}</span>
                <span className={styles.roleScore}>{role.confidence}%</span>
              </div>
              <div className={styles.barTrack}>
                <div
                  className={styles.barFill}
                  style={{
                    width: `${role.confidence}%`,
                    background: i === 0
                      ? 'var(--accent)'
                      : i === 1
                        ? 'var(--accent2)'
                        : 'var(--accent3)'
                  }}
                />
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="card">
        <h2 className={styles.sectionTitle}>
          <span className={styles.dot} style={{ background: 'var(--accent3)' }} />
          Prediction Reasoning
        </h2>
        <p className={styles.reasoning}>{reasoning}</p>
      </div>
    </div>
  )
}