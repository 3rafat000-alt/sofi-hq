# SAKK Flutter Web Interface — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development or executing-plans to implement this plan task-by-task.

**Goal:** Build the SAKK Flutter Web interface — 9 screens with sidebar navigation, RTL Arabic, dark-mode-only theme, accessibility (WCAG 2.2 AA), and live API integration.

**Architecture:** The existing mobile Flutter project (`projects/sakk/mobile/`) already contains ALL business logic, models, repositories, and API client. We extend it with a web-specific shell (sidebar nav) and responsive page adapters. The data layer is shared; only the presentation shell differs between mobile and web.

**Tech Stack:** Flutter 3.44.1 · Dart 3.12.1 · Riverpod · go_router · Dio · IBM Plex Sans Arabic · design-tokens/tokens.json (W3C DTCG)

**Spec:** `projects/sakk/brain/openapi-spec.yaml` (73 endpoints) · `projects/sakk/brain/design-tokens/tokens.json` (frozen) · `projects/sakk/brain/hi-fi-mockups/` (frozen) · `projects/sakk/brain/brand-guidelines.md`

## Global Constraints
- Dark-mode-only: ink-950 #121212 bg · paper #EAEAEA text · neon-500 #00E676 accent
- RTL Arabic throughout (Directionality + textDirection)
- WCAG 2.2 AA: skip links, focus indicators, keyboard nav, ARIA semantics
- Law 10: all work on main tree (no worktrees)
- Law 4: `file:line` evidence for every deliverable
- Law INT-0004: DFR gate OPEN — code execution permitted
- Reuse existing `AppColors`, `AppTheme`, `AppSizes`, models, and repositories from mobile

---

## File Structure

### New files to create (inside `projects/sakk/mobile/lib/`):

```
web/
├── shell/
│   ├── web_shell.dart              — Responsive shell: sidebar on desktop, bottom nav on mobile
│   ├── web_sidebar.dart            — RTL sidebar with nav items, collapse, user profile
│   └── web_top_bar.dart            — Top bar with search, notifications bell, user menu
├── pages/
│   ├── web_dashboard_page.dart     — Dashboard adapted for desktop (grid layout)
│   ├── web_login_page.dart         — Login centered card on desktop
│   ├── web_register_page.dart      — Register centered card on desktop
│   ├── web_wallets_page.dart       — Wallets grid layout
│   ├── web_transactions_page.dart  — Transactions table layout
│   ├── web_transfer_page.dart      — Transfer form with sidebar summary
│   ├── web_cards_page.dart         — Cards management with table view
│   ├── web_kyc_page.dart           — KYC steps with progress
│   └── web_profile_page.dart       — Profile settings form
└── widgets/
    ├── web_responsive.dart         — Breakpoint detection + responsive layout builder
    ├── web_data_table.dart         — Reusable styled data table
    ├── web_stat_card.dart          — Stat card widget for dashboard
    └── web_empty_state.dart        — Empty state widget
```

### Files to modify:
- `mobile/lib/core/router/app_router.dart` — Add web-aware routing (detect platform)
- `mobile/lib/main.dart` — Web bootstrap (skip mobile-only services)

---

## Tasks

### Task 1: Responsive Breakpoint System + Web Shell Skeleton
**Files:**
- Create: `lib/web/widgets/web_responsive.dart`
- Create: `lib/web/shell/web_shell.dart`
- Create: `lib/web/shell/web_sidebar.dart`
- Create: `lib/web/shell/web_top_bar.dart`

**Interfaces:**
- Consumes: `AppColors`, `AppSizes`, `AppTheme` from `core/theme/`
- Produces: `WebResponsive.isDesktop(context)`, `WebShell` widget, `WebSidebar` widget

- [ ] Create `web/widgets/web_responsive.dart` with `WebResponsive` class that wraps `LayoutBuilder` to detect breakpoints:
  - Desktop: width >= 1024px
  - Tablet: 768px <= width < 1024px
  - Mobile: width < 768px

- [ ] Create `web/shell/web_sidebar.dart` — RTL sidebar:
  - Width: 260px expanded, 72px collapsed
  - Items: Dashboard, Wallets, Cards, Transactions, Transfers, KYC, Profile, Settings, Logout
  - Active item highlighted with neon-500 left border + neonSoft bg
  - Logo "صكّ" at top
  - Collapse/expand button at bottom
  - All text Arabic, RTL layout (right-to-left sidebar items)
  - Accessibility: semantic labels, keyboard focusable

- [ ] Create `web/shell/web_top_bar.dart` — Top bar:
  - Height: 64px
  - Search input (placeholder: "بحث...")
  - Notification bell icon with badge
  - User avatar + name dropdown
  - Background: ink-950 with hairline bottom border

- [ ] Create `lib/web/shell/web_shell.dart` — Composes sidebar + top bar + child content:
  ```dart
  class WebShell extends StatelessWidget {
    final Widget child;
    const WebShell({super.key, required this.child});
    // Layout: Row [Sidebar, Column [TopBar, Expanded(child)]]
  }
  ```

- [ ] Verify: `flutter build web --release` completes without errors
- [ ] Commit

### Task 2: Web Router Integration
**Files:**
- Modify: `lib/core/router/app_router.dart`

**Interfaces:**
- Consumes: `WebShell`, `WebResponsive`
- Produces: `webShellRoute` (ShellRoute for web)

- [ ] Add a `WebShellRoute` that wraps authenticated pages in `WebShell` when `kIsWeb` is true
- [ ] Keep existing mobile `MainShell` for non-web platforms
- [ ] Platform detection: `import 'package:flutter/foundation.dart' show kIsWeb;`
- [ ] Route mapping: each page gets its web equivalent via `WebShellRoute`
- [ ] Verify: `flutter run -d chrome` loads with sidebar shell
- [ ] Commit

### Task 3: Web Login Page
**Files:**
- Create: `lib/web/pages/web_login_page.dart`

**Interfaces:**
- Consumes: `authRepositoryProvider`, `AppColors`, `AppSizes`
- Produces: Login page widget (centered card, dark bg, RTL)

- [ ] Create centered login card on dark background (#121212):
  - Max width: 420px, centered horizontally and vertically
  - SAKK logo/title "صكّ" above the form
  - Email field, password field with show/hide toggle
  - "تذكرني" checkbox
  - Login button (neon-500, full width)
  - "نسيت كلمة المرور؟" link
  - "ليس لديك حساب؟ سجّل الآن" link
  - All Arabic text, RTL layout
- [ ] Wire to existing `authRepositoryProvider.login()`
- [ ] Error handling: show SnackBar with error message
- [ ] Loading state: button shows CircularProgressIndicator
- [ ] Accessibility: labels on all fields, focus order, skip link
- [ ] Verify: page renders correctly in Chrome
- [ ] Commit

### Task 4: Web Register Page
**Files:**
- Create: `lib/web/pages/web_register_page.dart`

**Interfaces:**
- Consumes: `authRepositoryProvider`, `AppColors`, `AppSizes`
- Produces: Register page widget

- [ ] Centered register card (max-width: 420px):
  - Fields: name, email, phone, password, confirm password
  - "أوافق على الشروط والأحكام" checkbox
  - Register button (neon-500)
  - "لديك حساب بالفعل؟ سجّل الدخول" link
- [ ] Form validation: email regex, password min 8 chars, passwords match
- [ ] Wire to existing auth flow
- [ ] Accessibility + RTL
- [ ] Commit

### Task 5: Web Dashboard Page
**Files:**
- Create: `lib/web/pages/web_dashboard_page.dart`
- Create: `lib/web/widgets/web_stat_card.dart`

**Interfaces:**
- Consumes: `walletsProvider`, `recentTransactionsProvider` from existing providers
- Produces: Dashboard widget with stat cards grid + activity table

- [ ] Create `web_stat_card.dart`: Dark card (#1B1B1B) with label (paper-muted), value (paper), icon (neon for positive)
- [ ] Dashboard layout:
  - Top row: 4 stat cards (Total Balance, Active Cards, Recent Transactions, KYC Status)
  - Middle: Wallets horizontal scroll with currency cards
  - Bottom: Recent transactions table (desktop table format)
- [ ] Responsive: 4 columns desktop → 2 tablet → 1 mobile
- [ ] All data from existing Riverpod providers
- [ ] Empty states for each section
- [ ] Accessibility
- [ ] Commit

### Task 6: Web Wallets Page
**Files:**
- Create: `lib/web/pages/web_wallets_page.dart`

**Interfaces:**
- Consumes: `walletsProvider`
- Produces: Wallets grid layout

- [ ] Grid of wallet cards (3 columns desktop, 2 tablet, 1 mobile)
- [ ] Each card: currency flag, name, balance (large), available balance, pending balance
- [ ] "إيداع" and "سحب" action buttons per card
- [ ] "محفظة جديدة" button (neon-500 accent)
- [ ] Total balance summary bar at top
- [ ] Commit

### Task 7: Web Transactions Page
**Files:**
- Create: `lib/web/pages/web_transactions_page.dart`
- Create: `lib/web/widgets/web_data_table.dart`

**Interfaces:**
- Consumes: `transactionsProvider`
- Produces: Transactions table with filters

- [ ] Create `web_data_table.dart`: Styled DataTable matching dark theme
  - Header: ink-lighter bg, paper text
  - Rows: alternating surface/surfaceCard
  - Hover: neonSoft highlight
  - RTL text alignment
- [ ] Transactions table columns: Date, Type, Amount, Fee, Status, Actions
- [ ] Filter bar: date range, type dropdown, status dropdown, search
- [ ] Pagination: "عرض المزيد" button
- [ ] Row click → transaction detail dialog or page
- [ ] Status chips: completed=neon, pending=gold, failed=error, cancelled=textSecondary
- [ ] Commit

### Task 8: Web Transfer Page
**Files:**
- Create: `lib/web/pages/web_transfer_page.dart`

**Interfaces:**
- Consumes: `walletsProvider`, `authRepositoryProvider`
- Produces: Transfer form page

- [ ] Two-column layout:
  - Right (main): Transfer form (recipient, amount, currency, note)
  - Left (summary): Transfer summary card (amount, fee, exchange rate, total)
- [ ] Recipient search: by email, phone, or username with autocomplete
- [ ] Amount input with currency selector
- [ ] Fee calculation before confirmation
- [ ] "تأكيد التحويل" button with password confirmation dialog
- [ ] Success/failure result page
- [ ] Commit

### Task 9: Web Cards Page
**Files:**
- Create: `lib/web/pages/web_cards_page.dart`

**Interfaces:**
- Consumes: `cardsProvider`
- Produces: Cards management page

- [ ] Cards grid (2 columns desktop)
- [ ] Each card: virtual card visual (dark gradient), last 4 digits, status chip, balance
- [ ] Card actions: Freeze, Unfreeze, Cancel, View Details
- [ ] "طلب بطاقة جديدة" button
- [ ] Card details modal: full card info, transaction history
- [ ] Empty state: "لا توجد بطاقات" with CTA
- [ ] Commit

### Task 10: Web KYC Page
**Files:**
- Create: `lib/web/pages/web_kyc_page.dart`

**Interfaces:**
- Consumes: KYC repository providers
- Produces: KYC steps page

- [ ] Three-column progress indicator (Basic → Medium → Full)
- [ ] Current level highlighted with neon
- [ ] Upload zone: drag & drop area for documents
- [ ] Document type selector (ID card, passport, proof of address)
- [ ] Status display: pending, approved, rejected (with reason)
- [ ] Resubmit flow for rejected documents
- [ ] Commit

### Task 11: Web Profile Page
**Files:**
- Create: `lib/web/pages/web_profile_page.dart`

**Interfaces:**
- Consumes: user auth data
- Produces: Profile settings form

- [ ] Two-column layout: avatar + info (right), form (left)
- [ ] Fields: name, email, phone, date of birth
- [ ] Change password section
- [ ] Notification preferences toggles
- [ ] Account deletion link
- [ ] Save button with loading state
- [ ] Commit

### Task 12: Accessibility + Final Polish
**Files:**
- Modify: all web page files

**Interfaces:**
- Consumes: all created pages
- Produces: WCAG 2.2 AA compliant pages

- [ ] Add skip-to-content link on every page
- [ ] Ensure all interactive elements have focus indicators (neon-500 ring)
- [ ] Add Semantics labels to all widgets (Arabic)
- [ ] Verify keyboard navigation works (Tab order)
- [ ] Test with screen reader semantics
- [ ] Verify RTL layout on all pages
- [ ] Run `flutter analyze` — zero errors
- [ ] Run `flutter build web --release` — succeeds
- [ ] Commit

### Task 13: Performance + Build Verification
**Files:**
- Modify: `lib/main.dart` (web-specific bootstrap)

**Interfaces:**
- Consumes: all web pages
- Produces: Optimized web build

- [ ] Skip mobile-only services on web (FCM, local auth, secure storage)
- [ ] Web bootstrap: skip `Hive.initFlutter()` if not needed
- [ ] Lazy load pages (deferred components)
- [ ] Verify bundle size < 5MB
- [ ] Lighthouse audit: Performance > 80, Accessibility > 90
- [ ] Commit
