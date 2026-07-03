import { useEffect, useState } from 'react';
import EventsPage from './pages/EventsPage';
import DishesPage from './pages/DishesPage';
import EventDetailPage from './pages/EventDetailPage';
import styles from './App.module.css';

const pages = {
  events: EventsPage,
  dishes: DishesPage,
  detail: EventDetailPage,
};

function getRouteFromHash() {
  const hash = window.location.hash.replace('#', '').trim();
  return pages[hash] ? hash : 'events';
}

export default function App() {
  const [route, setRoute] = useState(getRouteFromHash);

  useEffect(() => {
    const handleHashChange = () => setRoute(getRouteFromHash());
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const ActivePage = pages[route];

  return (
    <div className={styles.appShell}>
      <header className={styles.topBar}>
        <div>
          <p className={styles.brand}>Event Catering Calculator</p>
          <p className={styles.tagline}>Elegant planning screens for modern service teams.</p>
        </div>

        <nav className={styles.nav} aria-label="Primary">
          <a className={route === 'events' ? styles.navLinkActive : styles.navLink} href="#events">
            Events
          </a>
          <a className={route === 'dishes' ? styles.navLinkActive : styles.navLink} href="#dishes">
            Dishes
          </a>
          <a className={route === 'detail' ? styles.navLinkActive : styles.navLink} href="#detail">
            Event detail
          </a>
        </nav>
      </header>

      <main className={styles.main}>
        <ActivePage />
      </main>
    </div>
  );
}