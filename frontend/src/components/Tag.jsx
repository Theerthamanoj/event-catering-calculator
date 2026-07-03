import styles from './Tag.module.css';

export default function Tag({ children, tone = 'neutral' }) {
  return <span className={`${styles.tag} ${styles[tone]}`}>{children}</span>;
}