import PageShell from '../../components/PageShell';
import StatCard from '../../components/StatCard';
import Tag from '../../components/Tag';
import { events, guestSegments } from '../../data/mockData';
import styles from './EventsPage.module.css';

export default function EventsPage() {
  return (
    <PageShell
      title="Elegant planning for every service"
      subtitle="Track each event at a glance, compare guest mix, and move from concept to menu without losing sight of budget or coverage."
      actions={
        <>
          <button className={styles.primaryButton} type="button">
            New event
          </button>
          <button className={styles.secondaryButton} type="button">
            View menu library
          </button>
        </>
      }
    >
      <section className={styles.statsGrid} aria-label="Event summary metrics">
        <StatCard label="Active events" value="12" detail="Three services are in final review." tone="mint" />
        <StatCard label="Guests tracked" value="304" detail="Dietary preferences captured across all events." tone="sand" />
        <StatCard label="Menu coverage" value="96%" detail="Most events already have a balanced menu mix." tone="berry" />
        <StatCard label="Avg. cost per head" value="$28" detail="Projected from confirmed dishes and guest counts." tone="sky" />
      </section>

      <section className={styles.layout}>
        <div className={styles.mainColumn}>
          <div className={styles.sectionHeader}>
            <div>
              <p className={styles.sectionKicker}>Upcoming calendar</p>
              <h2>Events that feel ready before the first tasting</h2>
            </div>
            <Tag tone="accent">Responsive overview</Tag>
          </div>

          <div className={styles.eventGrid}>
            {events.map((event) => (
              <article key={event.id} className={styles.eventCard}>
                <div className={styles.eventTopRow}>
                  <div>
                    <p className={styles.eventDate}>{event.date}</p>
                    <h3>{event.name}</h3>
                  </div>
                  <Tag tone={event.status === 'Ready' ? 'success' : event.status === 'Needs review' ? 'warning' : 'accent'}>
                    {event.status}
                  </Tag>
                </div>

                <p className={styles.eventVenue}>{event.venue}</p>

                <dl className={styles.eventStats}>
                  <div>
                    <dt>Guests</dt>
                    <dd>{event.guestCount}</dd>
                  </div>
                  <div>
                    <dt>Menu items</dt>
                    <dd>{event.menuCount}</dd>
                  </div>
                  <div>
                    <dt>Priority</dt>
                    <dd>{event.accent}</dd>
                  </div>
                </dl>

                <div className={styles.progressBar} aria-hidden="true">
                  <span style={{ width: `${Math.min(100, event.guestCount)}%` }} />
                </div>
              </article>
            ))}
          </div>
        </div>

        <aside className={styles.sideColumn}>
          <section className={styles.sidePanel}>
            <div className={styles.sectionHeader}>
              <div>
                <p className={styles.sectionKicker}>Guest mix</p>
                <h2>Coverage by dietary segment</h2>
              </div>
            </div>

            <div className={styles.segmentList}>
              {guestSegments.map((segment) => (
                <div key={segment.label} className={styles.segmentRow}>
                  <div>
                    <strong>{segment.label}</strong>
                    <p>{segment.value} guests</p>
                  </div>
                  <Tag tone={segment.tone}>{segment.label}</Tag>
                </div>
              ))}
            </div>
          </section>

          <section className={styles.sidePanelAlt}>
            <p className={styles.sectionKicker}>Workflow</p>
            <h3>Quick next steps</h3>
            <ol className={styles.stepList}>
              <li>Review the guest count for each service.</li>
              <li>Balance vegetarian and gluten-free options.</li>
              <li>Confirm the menu before generating totals.</li>
            </ol>
          </section>
        </aside>
      </section>
    </PageShell>
  );
}