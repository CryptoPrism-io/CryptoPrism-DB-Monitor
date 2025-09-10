# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Common Commands

### Development
```bash
# Run dashboard (primary development command)
streamlit run app/streamlit_app.py --server.port 8501

# Alternative ports if 8501 is occupied
streamlit run app/streamlit_app.py --server.port 8502

# Full setup from scratch
python setup_dashboard.py

# Install dependencies
pip install -r requirements.txt
```

### Docker Deployment
```bash
# Production deployment
cd docker
docker-compose -f docker-compose.dashboard.yml up -d

# View logs
docker-compose logs cryptoprism-dashboard
```

### Database Setup
```bash
# Initialize ETL tracking tables
psql -h your_host -U your_user -d your_db -f sql/etl_tracking_setup.sql
```

## Architecture Overview

This is a **Streamlit-based monitoring dashboard** for CryptoPrism's ETL operations and database infrastructure. The architecture follows a modular design pattern with clear separation of concerns.

### Core Architecture Patterns

1. **Configuration-Driven**: The `config/settings.py` module provides centralized configuration management using environment variables with sensible defaults. Database connections, caching TTLs, and authentication settings are all configurable via `.env` files.

2. **Service Layer Pattern**: The `services/database_service.py` implements a singleton database service with connection pooling, caching, and health monitoring. This is the **single point** for all database interactions across the application.

3. **Component-Based UI**: The `components/ui_components.py` provides reusable UI components (layouts, charts, data displays) that maintain consistent styling and behavior across all dashboard pages.

4. **Page-Based Routing**: Streamlit's native multipage architecture is used, with each page in `pages/` handling specific monitoring aspects (overview, performance, business signals, etc.).

### Critical Integration Points

- **Database Service Integration**: All pages import and use the global `db_service` instance from `services/database_service.py`. This service handles connection pooling, query execution, and error handling.

- **Configuration Management**: The `config` module is imported globally and provides database connection strings, caching settings, and feature flags. Changes to `.env` require application restart.

- **CryptoPrism Utilities Integration**: The dashboard integrates with external CryptoPrism utilities located in `crypto_db_utils/` for validation, optimization, and schema analysis functions.

### Key Technical Constraints

- **PostgreSQL-Specific**: The application is built specifically for PostgreSQL databases with CryptoPrism's schema (tables like `etl_runs`, `etl_job_stats`, etc.).

- **Read-Only Operations**: The dashboard performs only SELECT operations for safety. All monitoring is non-intrusive.

- **Datetime Handling**: The codebase has specific patterns for handling timezone-aware datetime objects. Use `pd.to_datetime(utc=True).dt.tz_localize(None)` for consistency and `errors='coerce'` for robustness.

- **Caching Strategy**: Streamlit's `@st.cache_data` and `@st.cache_resource` decorators are used extensively with TTL settings from the configuration module.

## Environment Configuration

The `.env` file is **required** and must contain:
- Database connection parameters (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT)
- DASHBOARD_PASSWORD for authentication
- Optional Slack webhook for alerts
- Performance tuning parameters (cache TTLs, query timeouts)

Copy `.env.example` to `.env` and configure for your environment.

## Development Notes

- **No Timeline Charts**: Timeline/Gantt charts using `px.timeline` have been intentionally removed due to persistent datetime operand errors. Use table views instead.

- **Error Handling Pattern**: Database operations use try-catch blocks with fallback to default/empty data structures. UI components gracefully handle empty datasets.

- **Authentication**: The dashboard uses simple password-based authentication via Streamlit's session state. The password is configured in the environment.

- **Modular Page Structure**: Each page follows the pattern: data loading functions, rendering functions, and a main page function that orchestrates the display.

- **Performance Optimization**: The `DatabaseService` class implements connection pooling, query timeouts, and result caching to handle production workloads efficiently.