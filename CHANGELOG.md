# CryptoPrism ETL Dashboard - Changelog

All notable changes to this project will be documented in this file.

## [1.2.0] - 2025-10-26

### Added
- **Deployment Support**: Added `.python-version` file specifying Python 3.11 for Streamlit Cloud
- **Pipeline Monitoring**: Enhanced data pipeline monitoring page with comprehensive stage tracking

### Fixed
- **Import Errors**: Resolved missing pandas import in `utils/helpers.py`
  - Fixed "name 'pd' is not defined" error in `cleanup_dataframe_for_display` function
  - Added explicit pandas import for datetime type checking operations
- **Function Imports**: Fixed missing `styled_metric_card` import in `pages/pipeline_monitor.py`
  - Resolved undefined function error in recent updates dashboard

### Changed
- **Dependency Management**: Pinned all package versions in `requirements.txt` for stable deployment
  - Streamlit 1.32.0 (was >=1.28.0)
  - Pandas 2.2.0 (was >=1.5.0)
  - Plotly 5.19.0 (was >=5.17.0)
  - SQLAlchemy 2.0.25 (was >=2.0.0)
  - Added explicit numpy 1.26.3 dependency
- **Deployment**: Improved Streamlit Cloud compatibility with pinned dependencies

### Technical Improvements
- Enhanced error handling for pipeline monitoring operations
- Improved module import organization across dashboard pages
- Standardized dependency versions to prevent installation conflicts

## [1.1.3] - 2025-01-10

### Added
- **Documentation**: Created comprehensive CLAUDE.md file for future Claude Code instances
  - Essential development commands and Docker deployment procedures
  - Detailed architecture overview covering service layer and configuration patterns
  - Critical integration points and technical constraint documentation
  - Development notes including datetime handling patterns

### Fixed
- **Timeline Visualization**: Resolved persistent datetime operand type errors in timeline charts
  - Enhanced datetime conversion with robust error handling using `errors='coerce'`
  - Added timezone normalization for consistent datetime processing
  - Improved null value validation and data cleanup before visualization
- **Chart Rendering**: Replaced problematic px.timeline charts with clean table views
  - Eliminated "unsupported operand type(s) for +: 'int' and 'datetime.datetime'" errors
  - Maintained all ETL job information display without visualization errors
  - Improved user experience with reliable data presentation

### Technical Improvements
- Enhanced datetime handling patterns throughout the application
- Improved error handling with fallback table views for failed chart rendering
- Added data validation and type coercion for robust datetime operations

## [1.1.2] - 2025-01-10

### Changed
- **UI Enhancement**: Removed all emojis from dashboard interface for professional appearance
  - Cleaned up main dashboard status indicators and metrics displays
  - Removed emojis from database connection status messages
  - Updated performance tracking displays to use text-only format

### Fixed
- **Database Connectivity**: Resolved statement_timeout parameter corruption causing connection failures
  - Fixed malformed timeout values in database query execution
  - Improved timeout handling and error recovery in database service
  - Added proper fallback mechanisms for configuration value parsing

### Technical Improvements
- Enhanced database service error handling and timeout management
- Improved configuration value validation and type safety
- Streamlined query execution without custom timeout complications

## [1.1.1] - 2025-01-09

### Added
- Initial CryptoPrism ETL Dashboard release
- Comprehensive database monitoring and analytics platform
- Real-time ETL pipeline monitoring
- Advanced data quality validation and reporting
- Interactive cryptocurrency trading analytics
- Multi-database support and optimization tools