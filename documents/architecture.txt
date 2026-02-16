┌───────────────────────────────┐
│           Browser             │
│  HTML / CSS / JavaScript      │
│  - Station map/list UI        │
│  - Weather forecast UI        │
│  - Product & checkout UI      │
│  - Borrow/Return actions      │
└───────────────┬───────────────┘
                │ HTTPS (REST API, JSON)
                ▼
┌───────────────────────────────┐
│             Flask             │
│  Blueprints / Modules:        │
│  1) auth/users                │
│  2) stations (availability)   │
│  3) weather (forecast)        │
│  4) products/orders/payments  │
│  5) rentals (borrow/return)   │
│                               │
│  Cross-cutting:               │
│  - Validation (expire_date)   │
│  - Transaction + locking      │
│  - Error handling             │
│  - Logging/Audit              │
└───────────────┬───────────────┘
                │ SQLAlchemy or PyMySQL
                ▼
┌───────────────────────────────┐
│             MySQL             │
│  Tables: stations, users,     │
│  products, weather, orders,   │
│  (+ rentals / station_events) │
└───────────────────────────────┘
