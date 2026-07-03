---
name: react-page-builder
description: Use this skill when building or scaffolding a new React page or component for this project. Trigger on requests like "build a page", "create a new screen", "add a settings page", "create a React component", or "scaffold a feature". Follow the project's folder structure, React best practices, styling conventions, and accessibility requirements.
---

# React Page Builder

## Folder structure

Every new page should be created under:

```
src/pages/<PageName>/
├── index.jsx          # Exports the page component
├── <PageName>.jsx     # Main React component (optional if using index.jsx only)
├── <PageName>.module.css   # Component-specific styles
├── hooks.js           # Optional custom hooks for the page
├── constants.js       # Optional constants
├── utils.js           # Optional helper functions
└── components/        # Child components specific to this page
```

Reusable UI components belong under:

```
src/components/
```

Shared hooks belong under:

```
src/hooks/
```

Shared utilities belong under:

```
src/utils/
```

Do not place business logic directly inside JSX when it can be extracted into hooks or utility functions.

---

# React coding standards

- Use React Functional Components only.
- Use Hooks (`useState`, `useEffect`, `useMemo`, `useCallback`, `useRef`) where appropriate.
- Never use class components.
- Keep components focused on a single responsibility.
- Prefer composition over inheritance.
- Extract repeated UI into reusable components.
- Avoid unnecessary prop drilling. Use Context only for shared application state.
- Do not mutate state directly.
- Use immutable update patterns.

---

# Styling rules

- Use CSS Modules (`*.module.css`) unless the project specifies another styling solution.
- Never use inline styles unless dynamically required.
- Never place `<style>` blocks inside JSX.
- Reuse existing design tokens from the project.

Example:

```
var(--color-primary)
var(--spacing-md)
var(--font-size-lg)
```

Do not hardcode:

- Hex colors
- Font sizes
- Spacing values
- Border radius values

unless explicitly instructed.

Use meaningful class names following BEM or the project's existing naming convention.

---

# Component guidelines

Prefer components smaller than 200 lines.

Split large pages into reusable sections.

Example:

```
SettingsPage
 ├── ProfileSection
 ├── NotificationSection
 ├── SecuritySection
 └── FooterActions
```

Avoid deeply nested JSX.

---

# Accessibility baseline (non-negotiable)

Every component must be keyboard accessible.

Requirements:

- Semantic HTML whenever possible.
- Every input has an associated label.
- Every icon-only button has an `aria-label`.
- Focus indicators must remain visible.
- Buttons must be actual `<button>` elements.
- Links must be actual `<a>` elements.
- Use `aria-expanded`, `aria-pressed`, `aria-selected`, `aria-current`, and other ARIA attributes where appropriate.
- Forms must expose validation errors to screen readers.
- Color alone must never indicate state.
- Meet WCAG AA contrast requirements.

---

# State management

Use local component state whenever possible.

```
useState
```

For derived state:

```
useMemo
```

For side effects:

```
useEffect
```

For complex page logic:

Create a custom hook.

Example:

```
useSettingsPage()
```

Do not introduce Redux, Zustand, MobX, or any additional state library unless the existing project already uses it.

Shared application state should use the project's existing Context or state management solution.

---

# Event handling

Use React event handlers.

Example:

```
onClick
onChange
onSubmit
onKeyDown
```

Never manipulate the DOM directly using:

```
document.getElementById()
querySelector()
innerHTML
```

unless absolutely unavoidable.

Use refs instead.

---

# Forms

Use controlled components.

Example:

```
value={value}
onChange={handleChange}
```

Validate user input before submission.

Disable submit buttons while requests are pending.

Show loading indicators during async operations.

Display user-friendly validation messages.

---

# API calls

Place API logic in:

```
src/services/
```

or

```
src/api/
```

Never place fetch logic directly inside JSX.

Use async/await.

Handle:

- loading
- success
- empty
- error

states.

Always catch errors.

---

# Save / Submit actions

Any Save or Submit action must:

- Disable the action button while processing.
- Show a loading spinner or progress indicator.
- Prevent duplicate submissions.
- Display success or failure notifications using the project's notification utility.
- Refresh local state after successful updates if needed.

---

# Performance guidelines

Use:

- React.memo
- useMemo
- useCallback

only when they provide measurable benefits.

Lazy load large pages using:

```
React.lazy()
Suspense
```

Avoid unnecessary re-renders.

Provide stable keys for lists.

Never use array index as key unless the list is static.

---

# File naming

Components:

```
UserProfile.jsx
NotificationCard.jsx
SettingsPage.jsx
```

Hooks:

```
useAuth.js
useSettings.js
```

Utilities:

```
dateUtils.js
formatCurrency.js
```

CSS Modules:

```
SettingsPage.module.css
```

---

# Code quality

Always:

- Keep components readable.
- Use descriptive variable names.
- Remove dead code.
- Remove unused imports.
- Prefer early returns over nested conditions.
- Avoid duplicated logic.
- Add comments only where the intent is not obvious.

---

# Expected output

Whenever asked to build a page or component:

- Create the complete folder structure.
- Generate production-quality React components.
- Use modern React patterns.
- Follow accessibility requirements.
- Include loading and error states where applicable.
- Write clean, maintainable, reusable code.
- Follow the project's existing architecture and naming conventions.