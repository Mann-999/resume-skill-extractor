import { useState } from 'react'
import SkillsTab from '../components/SkillsTab.jsx'
import RolesTab from '../components/RolesTab.jsx'
import BulletsTab from '../components/BulletsTab.jsx'
import JDMatchTab from '../components/JDMatchTab.jsx'
import styles from './ResultsPage.module.css'

const TABS = ['Skills', 'Roles', 'Bullet Rewrites', 'JD Match']

export default function ResultsPage({ data, onReset }) {
  const [activeTab, setActiveTab] = useState('Skills')
  const [downloading, setDownloading] = useState(false)

  const handleDownload = async () => {
    setDownloading(true)
    try {
      const res = await fetch('/generate-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          skills: data.skills,
          predicted_roles: data.predicted_roles,
          summary: data.summary,
          reasoning: data.reasoning,
        }),
      })
      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = 'resume_report.pdf'
      a.click()
      URL.revokeObjectURL(url)
    } catch (e) {
      alert('Failed to download report.')
    } finally {
      setDownloading(false)
    }
  }

  return (
    <div className={styles.page}>
      <div className={styles.bg} aria-hidden />

      <header className={styles.header}>
        <button className="btn-ghost" onClick={onReset}>← New Resume</button>
        <span className={styles.logo}>ResumeIQ</span>
        <button className="btn-primary" onClick={handleDownload} disabled={downloading}>
          {downloading ? <><span className="spinner" /> Generating…</> : '↓ PDF Report'}
        </button>
      </header>

      <div className={`${styles.summary} fade-up`}>
        <p className={styles.summaryText}>{data.summary}</p>
      </div>

      <nav className={`${styles.tabs} fade-up`} style={{ animationDelay: '0.05s' }}>
        {TABS.map(tab => (
          <button
            key={tab}
            className={`${styles.tab} ${activeTab === tab ? styles.tabActive : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      <main className={`${styles.content} fade-up`} style={{ animationDelay: '0.1s' }}>
        {activeTab === 'Skills' && <SkillsTab skills={data.skills} />}
        {activeTab === 'Roles' && <RolesTab roles={data.predicted_roles} reasoning={data.reasoning} />}
        {activeTab === 'Bullet Rewrites' && <BulletsTab rawText={data.raw_text} />}
        {activeTab === 'JD Match' && <JDMatchTab rawText={data.raw_text} />}
      </main>
    </div>
  )
}