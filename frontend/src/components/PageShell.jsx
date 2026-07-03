import styles from './PageShell.module.css';

export default function PageShell({ title, subtitle, actions, children }) {
  return (
    <section className={styles.shell}>
      <header className={styles.hero}>
        <div>
          <p className={styles.kicker}>Event catering control room</p>
          <h1>{title}</h1>
          <p className={styles.subtitle}>{subtitle}</p>
        </div>
        {actions ? <div className={styles.actions}>{actions}</div> : null}
      </header>
      <div className={styles.content}>{children}</div>
    </section>
  );
}