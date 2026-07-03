import styles from './StatCard.module.css';

export default function StatCard({ label, value, detail, tone = 'neutral' }) {
  return (
    <article className={`${styles.card} ${styles[tone]}`}>
      <p className={styles.label}>{label}</p>
      <strong className={styles.value}>{value}</strong>
      {detail ? <p className={styles.detail}>{detail}</p> : null}
    </article>
  );
}