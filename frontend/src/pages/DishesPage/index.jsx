import { useMemo, useState } from 'react';
import PageShell from '../../components/PageShell';
import Tag from '../../components/Tag';
import { dishes } from '../../data/mockData';
import styles from './DishesPage.module.css';

const filters = ['All', 'Vegetarian', 'Vegan', 'Gluten-free'];

export default function DishesPage() {
  const [activeFilter, setActiveFilter] = useState('All');

  const visibleDishes = useMemo(() => {
    if (activeFilter === 'All') {
      return dishes;
    }

    return dishes.filter((dish) => dish.tags.includes(activeFilter.toLowerCase()));
  }, [activeFilter]);

  return (
    <PageShell
      title="A polished dish library with room to breathe"
      subtitle="Review signature dishes, inspect allergen coverage, and keep ingredient choices readable on desktops, tablets, and phones."
      actions={
        <>
          <button className={styles.primaryButton} type="button">
            Add dish
          </button>
          <button className={styles.secondaryButton} type="button">
            Add ingredient
          </button>
        </>
      }
    >
      <section className={styles.topBar} aria-label="Dish filters">
        <div className={styles.filterGroup}>
          {filters.map((filter) => (
            <button
              key={filter}
              className={`${styles.filterButton} ${activeFilter === filter ? styles.filterButtonActive : ''}`}
              type="button"
              aria-pressed={activeFilter === filter}
              onClick={() => setActiveFilter(filter)}
            >
              {filter}
            </button>
          ))}
        </div>
        <p className={styles.resultCount}>{visibleDishes.length} dishes shown</p>
      </section>

      <section className={styles.layout}>
        <div className={styles.libraryGrid}>
          {visibleDishes.map((dish) => (
            <article key={dish.id} className={styles.dishCard}>
              <div className={styles.cardHeader}>
                <div>
                  <p className={styles.category}>{dish.category}</p>
                  <h2>{dish.name}</h2>
                </div>
                <Tag tone="accent">${dish.cost} / head</Tag>
              </div>

              <p className={styles.description}>{dish.description}</p>

              <div className={styles.tagRow}>
                {dish.tags.map((tag) => (
                  <Tag key={tag}>{tag}</Tag>
                ))}
              </div>

              <div className={styles.splitRow}>
                <div>
                  <p className={styles.subheading}>Ingredients</p>
                  <ul className={styles.inlineList}>
                    {dish.ingredients.map((ingredient) => (
                      <li key={ingredient}>{ingredient}</li>
                    ))}
                  </ul>
                </div>
                <div>
                  <p className={styles.subheading}>Allergen tags</p>
                  <div className={styles.tagRow}>
                    {dish.allergens.map((allergen) => (
                      <Tag key={allergen} tone="warning">
                        {allergen}
                      </Tag>
                    ))}
                  </div>
                </div>
              </div>
            </article>
          ))}
        </div>

        <aside className={styles.sidePanel}>
          <section className={styles.ingredientStudio}>
            <p className={styles.panelKicker}>Ingredient studio</p>
            <h3>Keep tags explicit and easy to scan</h3>

            <label className={styles.field}>
              <span>Ingredient name</span>
              <input type="text" defaultValue="Charred fennel" />
            </label>

            <fieldset className={styles.fieldset}>
              <legend>Allergen tags</legend>
              <div className={styles.checkGrid}>
                {['meat', 'dairy', 'eggs', 'honey', 'gluten', 'nuts'].map((tag) => (
                  <label key={tag} className={styles.checkItem}>
                    <input type="checkbox" defaultChecked={tag === 'gluten'} />
                    <span>{tag}</span>
                  </label>
                ))}
              </div>
            </fieldset>

            <button className={styles.saveButton} type="button">
              Save ingredient
            </button>
          </section>

          <section className={styles.noteCard}>
            <p className={styles.panelKicker}>Presentation</p>
            <h3>Designed to stay readable across screen sizes</h3>
            <p>
              Cards compress into a single column on smaller displays so names, tags, and allergen markers never feel cramped.
            </p>
          </section>
        </aside>
      </section>
    </PageShell>
  );
}