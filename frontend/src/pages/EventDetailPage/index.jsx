import { useState } from 'react';
import PageShell from '../../components/PageShell';
import Tag from '../../components/Tag';
import { eventDetail } from '../../data/mockData';
import styles from './EventDetailPage.module.css';

export default function EventDetailPage() {
  const [activeTab, setActiveTab] = useState('Guests');

  return (
    <PageShell
      title={eventDetail.name}
      subtitle={`${eventDetail.date} · ${eventDetail.venue} · ${eventDetail.guestCount} guests · Budget ${eventDetail.budget}`}
      actions={
        <>
          <button className={styles.primaryButton} type="button">
            Run calculation
          </button>
          <button className={styles.secondaryButton} type="button">
            Share event
          </button>
        </>
      }
    >
      <section className={styles.summaryStrip} aria-label="Event summary">
        <Tag tone="accent">Live planning</Tag>
        <Tag tone="success">Coverage balanced</Tag>
        <Tag tone="warning">1 menu item needs a gluten swap</Tag>
        <Tag tone="muted">All content is mock UI only</Tag>
      </section>

      <div className={styles.tabBar} role="tablist" aria-label="Event sections">
        {eventDetail.tabs.map((tab) => (
          <button
            key={tab}
            type="button"
            className={`${styles.tabButton} ${activeTab === tab ? styles.tabButtonActive : ''}`}
            aria-selected={activeTab === tab}
            role="tab"
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === 'Guests' ? <GuestsPanel /> : null}
      {activeTab === 'Menu' ? <MenuPanel /> : null}
      {activeTab === 'Results' ? <ResultsPanel /> : null}
    </PageShell>
  );
}

function GuestsPanel() {
  return (
    <section className={styles.panelGrid}>
      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <div>
            <p className={styles.kicker}>Guest roster</p>
            <h2>Readable at a glance</h2>
          </div>
          <Tag tone="accent">4 sampled guests</Tag>
        </div>

        <div className={styles.guestList}>
          {eventDetail.guests.map((guest) => (
            <article key={guest.name} className={styles.guestRow}>
              <div>
                <strong>{guest.name}</strong>
                <p>Special handling applies to this guest profile.</p>
              </div>
              <div className={styles.tagRow}>
                {guest.tags.map((tag) => (
                  <Tag key={tag}>{tag}</Tag>
                ))}
              </div>
            </article>
          ))}
        </div>
      </div>

      <aside className={styles.sideCard}>
        <p className={styles.kicker}>Add guest</p>
        <label className={styles.field}>
          <span>Name</span>
          <input type="text" defaultValue="New guest" />
        </label>
        <fieldset className={styles.fieldset}>
          <legend>Dietary tags</legend>
          <div className={styles.checkGrid}>
            {['vegetarian', 'vegan', 'gluten-free', 'nut allergy'].map((tag) => (
              <label key={tag} className={styles.checkItem}>
                <input type="checkbox" defaultChecked={tag === 'gluten-free'} />
                <span>{tag}</span>
              </label>
            ))}
          </div>
        </fieldset>
        <button className={styles.saveButton} type="button">
          Save guest
        </button>
      </aside>
    </section>
  );
}

function MenuPanel() {
  return (
    <section className={styles.panelGrid}>
      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <div>
            <p className={styles.kicker}>Selected menu</p>
            <h2>Items currently assigned to the event</h2>
          </div>
        </div>

        <div className={styles.menuGrid}>
          {eventDetail.menu.map((dish) => (
            <article key={dish.id} className={styles.menuCard}>
              <div className={styles.menuTopRow}>
                <div>
                  <p className={styles.menuCategory}>{dish.category}</p>
                  <strong>{dish.name}</strong>
                </div>
                <Tag tone="accent">${dish.cost} / head</Tag>
              </div>
              <p>{dish.description}</p>
              <div className={styles.tagRow}>
                {dish.tags.map((tag) => (
                  <Tag key={tag}>{tag}</Tag>
                ))}
              </div>
            </article>
          ))}
        </div>
      </div>

      <aside className={styles.sideCard}>
        <p className={styles.kicker}>Menu builder</p>
        <p className={styles.sideText}>
          Use the wider canvas for high-level dish selection, then move into results when the mix feels balanced.
        </p>
        <div className={styles.metricStack}>
          <Tag tone="success">8 planned portions per guest group</Tag>
          <Tag tone="warning">1 allergen mismatch flagged</Tag>
          <Tag tone="accent">Responsive cards</Tag>
        </div>
      </aside>
    </section>
  );
}

function ResultsPanel() {
  return (
    <section className={styles.panelGrid}>
      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <div>
            <p className={styles.kicker}>Calculation results</p>
            <h2>Distribution, totals, and flags</h2>
          </div>
          <Tag tone="success">Ready to present</Tag>
        </div>

        <div className={styles.resultTable} role="table" aria-label="Catering calculation results">
          <div className={styles.resultHead} role="row">
            <span role="columnheader">Dish</span>
            <span role="columnheader">Quantity</span>
            <span role="columnheader">Total</span>
            <span role="columnheader">Flag</span>
          </div>
          {eventDetail.results.map((row) => (
            <div key={row.dish} className={styles.resultRow} role="row">
              <strong role="cell">{row.dish}</strong>
              <span role="cell">{row.quantity}</span>
              <span role="cell">{row.total}</span>
              <span role="cell">{row.flag}</span>
            </div>
          ))}
        </div>
      </div>

      <aside className={styles.sideCard}>
        <p className={styles.kicker}>Cost matrix</p>
        <div className={styles.metricStack}>
          {eventDetail.costBreakdown.map((row) => (
            <div key={row.label} className={styles.breakdownRow}>
              <span>{row.label}</span>
              <strong>{row.value}</strong>
            </div>
          ))}
        </div>
      </aside>
    </section>
  );
}