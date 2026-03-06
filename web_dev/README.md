# Web Development Module - Django/React Framework

## Overview

The `web_dev` module provides a modern web-based interface for IMDASH workflow execution and result visualization. This module may be developmented in the future and contains a Django REST Framework backend with React frontend for remote job submission and monitoring.

## Status: In Development

**⚠️ Important**: The web development components are in architectural development. Interfaces, data models, and feature implementations are subject to change. The information below describes the current design state and planned functionality.

## Architecture

### Technology Stack

- **Backend**: Django REST Framework (Python 3.9+)
  - RESTful API for job submission and monitoring
  - Asynchronous task processing with Celery
  - PostgreSQL/SQLite database for job state
  - Redis for caching and message brokering

- **Frontend**: React with TypeScript
  - Modern UI for workflow configuration
  - Real-time job status monitoring
  - Interactive result visualization
  - WebSocket support for live updates

- **Infrastructure**: Docker Compose
  - Multi-container orchestration
  - Service isolation (Django, React, Redis, Postgres)
  - Local development and cloud deployment
  - Environment-based configuration

### Service Architecture

```
┌────────────────┐
│   Web Browser  │
└────────┬───────┘
         │ HTTP/WebSocket
         ↓
┌────────────────────┐       ┌──────────────┐
│   React Frontend   │──────→│  Django DRF  │
└────────────────────┘       │   Backend    │
                             └──────┬───────┘
         ┌───────────────────────────┼──────────────────────┐
         ↓                           ↓                      ↓
    ┌─────────┐            ┌──────────────┐        ┌────────────┐
    │ Celery  │            │  PostgreSQL  │        │   Redis    │
    │ (Tasks) │            │ (Database)   │        │ (Caching)  │
    └─────────┘            └──────────────┘        └────────────┘
         ↓ 
    ┌──────────────┐
    │ Singularity  │
    │ (Container)  │
    └──────────────┘
```

## Directory Structure

### Backend (Django REST Framework)

**`drf/backend/`** - Django application directory

```
drf/backend/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── docker-compose.yml           # Container orchestration
├── Dockerfile                   # Backend image specification
├── .env.example                 # Environment variables template
│
├── imdash_api/                  # Main Django app
│   ├── models.py               # Job and workflow models
│   ├── views.py                # API views and endpoints
│   ├── serializers.py          # Request/response serializers
│   ├── urls.py                 # URL routing
│   ├── permissions.py          # Authentication/authorization
│   ├── tasks.py                # Celery async tasks
│   └── admin.py                # Django admin configuration
│
├── config/                      # Django settings
│   ├── settings.py             # Main configuration
│   ├── wsgi.py                 # Application entry point
│   └── production.py           # Production overrides (if exists)
│
└── static/                      # Static files (CSS, JS, images)
```

### Frontend (React)

**`drf/backend/react_app_1/`** - React application directory

```
react_app_1/
├── public/                      # Static HTML and assets
│   └── index.html              # React mounting point
├── src/
│   ├── App.tsx                 # Root component
│   ├── index.tsx               # React entry point
│   ├── components/             # Reusable components
│   │   ├── WorkflowConfig.tsx  # Workflow configuration form
│   │   ├── JobMonitor.tsx      # Job status monitoring
│   │   ├── ResultViewer.tsx    # Result visualization
│   │   └── Navigation.tsx      # Header and routing
│   ├── pages/                  # Page components
│   │   ├── Dashboard.tsx       # Main dashboard
│   │   ├── SubmitJob.tsx       # Job submission interface
│   │   └── Results.tsx         # Results browsing
│   ├── api/                    # API client
│   │   └── client.ts           # Axios/Fetch configuration
│   ├── types/                  # TypeScript interfaces
│   │   └── index.ts            # API type definitions
│   └── styles/                 # CSS/SCSS
│       └── App.css             # Global styles
├── package.json                # NPM dependencies
├── tsconfig.json               # TypeScript configuration
├── Dockerfile                  # Frontend image specification
└── README.md                   # Frontend-specific documentation
```

## Core Features (Current Implementation Status)

### Job Submission API (In Development)

**Endpoint**: `POST /api/jobs/`

Submit IMDASH workflow for execution:

```json
{
  "name": "SampleAnalysis_2024_01_15",
  "experiment_type": "Single",
  "tools": ["PW", "MZ", "AC"],
  "configuration": {
    "calibrant_file": "/calibrants.txt",
    "mzml_data": "/path/to/data",
    "features_output": "/path/to/output"
  },
  "compute_resource": "cluster",
  "priority": "normal"
}
```

**Response**: Job ID and submission confirmation

### Job Monitoring (In Development)

**Endpoint**: `GET /api/jobs/{job_id}/status`

Retrieve real-time job execution status:

```json
{
  "job_id": "abc123def456",
  "status": "running",
  "progress": 45,
  "current_tool": "MZmine",
  "start_time": "2024-01-15T10:30:00Z",
  "estimated_completion": "2024-01-15T12:45:00Z",
  "log_entries": [
    "Started at 10:30:00",
    "ProteoWizard conversion 100% complete",
    "MZmine feature detection 45% complete"
  ]
}
```

### Result Retrieval (In Development)

**Endpoint**: `GET /api/jobs/{job_id}/results`

Retrieve completed analysis results:

```json
{
  "job_id": "abc123def456",
  "status": "completed",
  "results": {
    "features_csv": "https://api.example.com/download/abc123_features.csv",
    "annotated_features": "https://api.example.com/download/abc123_annotated.csv",
    "quality_metrics": {
      "features_detected": 450,
      "features_annotated": 420,
      "annotation_rate": 0.933
    }
  }
}
```

### Result Visualization (In Development)

Interactive visualization of analysis results:
- Feature intensity heatmaps
- CCS distribution plots
- Mass accuracy histograms
- Feature overlap Venn diagrams
- Time-series analysis trends

## API Endpoints (Planned)

### Job Management

```
POST   /api/jobs/                    # Submit new job
GET    /api/jobs/                    # List jobs
GET    /api/jobs/{id}/               # Job details
GET    /api/jobs/{id}/status         # Current status
GET    /api/jobs/{id}/logs           # Job logs
DELETE /api/jobs/{id}/               # Cancel job
GET    /api/jobs/{id}/results        # Download results
```

### Workflow Templates

```
GET    /api/templates/               # List workflow templates
GET    /api/templates/{id}           # Template details
POST   /api/templates/               # Create custom template (admin)
```

### User Management

```
POST   /api/auth/register            # User registration
POST   /api/auth/login               # User authentication
POST   /api/auth/logout              # Logout
GET    /api/users/me                 # Current user info
POST   /api/users/                   # User creation (admin)
```

### System Status

```
GET    /api/status/                  # System health check
GET    /api/config/                  # Available tools/resources
```

## Development Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Node.js 16+ (for React development)
- Git

### Local Development

```bash
# Clone repository
git clone https://github.com/your-org/imdash.git
cd ion-mob-ms/web_dev/drf

# Create .env file from template
cp .env.example .env

# Start services with Docker Compose
docker-compose up -d

# Backend available at: http://localhost:8000
# Frontend available at: http://localhost:3000
```

### Database Setup

```bash
# Initialize database (in Django container)
docker-compose exec web python manage.py migrate

# Create superuser for admin
docker-compose exec web python manage.py createsuperuser

# Access admin panel: http://localhost:8000/admin
```

### React Development

```bash
# Install dependencies
cd drf/backend/react_app_1
npm install

# Start development server (with Docker Compose)
docker-compose up react

# Or local development (for faster iterating)
npm start
```

## Running Services

### Docker Compose Services

```yaml
services:
  web:          # Django REST API backend
  react:        # React frontend
  postgres:     # PostgreSQL database
  redis:        # Redis cache/message broker
  celery:       # Async task processing
```

### Service Status

```bash
# Check all services
docker-compose ps

# View logs
docker-compose logs -f web          # Django logs
docker-compose logs -f react        # React logs
docker-compose logs -f celery       # Task processing logs
```

### Service Management

```bash
# Stop services
docker-compose down

# Restart specific service
docker-compose restart web

# View service configuration
docker-compose config
```

## Authentication and Authorization

### Planned Implementation

- JWT token-based authentication
- Role-based access control (RBAC)
- User groups for multi-tenant support
- API key authentication for programmatic access

### Typical Flow

```
User Login
    ↓
JWT Token Generation
    ↓
API Requests with Bearer Token
    ↓
Permission Verification
    ↓
Request Processing/Response
```

## Asynchronous Processing

### Celery Task Queue

Long-running IMDASH workflows use Celery for:
- Job execution in background
- Real-time progress updates
- Result persistence
- Error handling and retries
- Log aggregation

### Task Lifetime

```
Job Submitted
    ↓
Task Queued (Redis)
    ↓
Worker Picks Up Task
    ↓
Execution in Container (Singularity/Docker)
    ↓
Progress Update (via WebSocket)
    ↓
Result Storage
    ↓
Status Complete
```

## WebSocket Connection (Planned)

Real-time job monitoring via WebSocket:

```javascript
// Client-side (React)
const ws = new WebSocket('ws://localhost:8000/ws/jobs/abc123/');

ws.onmessage = (event) => {
  const status = JSON.parse(event.data);
  console.log(`Progress: ${status.progress}%`);
  console.log(`Log: ${status.log_entry}`);
  updateUI(status);
};
```

## Environment Configuration

### .env Variables

```bash
# Django settings
DEBUG=False                  # Production: False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# Database
DATABASE_URL=postgresql://user:pass@postgres:5432/imdash
REDIS_URL=redis://redis:6379/0

# JWT settings
JWT_SECRET=your-jwt-secret
JWT_ALGORITHM=HS256

# IMDASH paths
IMDASH_SINGULARITY_IMAGE=/path/to/pipeline.sif
IMDASH_OUTPUT_DIRECTORY=/var/imdash_results

# File upload
FILE_UPLOAD_MAX_SIZE=5GB
```

## Testing

### Backend Tests

```bash
# Run Django tests
docker-compose exec web python manage.py test

# Run with coverage
docker-compose exec web coverage run --source='.' manage.py test
docker-compose exec web coverage report
```

### Frontend Tests

```bash
# Run React tests
cd drf/backend/react_app_1
npm test

# Run with coverage
npm test -- --coverage
```

## Deployment

### Production Deployment

For production use:

1. **Set DEBUG=False** in .env
2. **Configure SECRET_KEY** (generate new)
3. **Set ALLOWED_HOSTS** to production domain
4. **Use PostgreSQL** (not SQLite)
5. **Configure HTTPS/SSL** (nginx reverse proxy)
6. **Enable CORS** for frontend domain
7. **Set up backup** strategy for database

### Docker Hub Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Push to registry
docker tag imdash-web:latest your-registry/imdash-web:latest
docker push your-registry/imdash-web:latest

# Deploy to cloud
# (specific instructions depend on platform)
```

## Known Limitations and TODOs

- [ ] Authentication system not fully implemented
- [ ] WebSocket connection needs Channels library integration
- [ ] Result download streaming not yet implemented
- [ ] Admin dashboard for job management incomplete
- [ ] Advanced filtering/querying of results not ready
- [ ] Integration testing with actual Singularity execution pending
- [ ] Performance optimization for large result sets pending
- [ ] Mobile responsive design refinement needed

## Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL service
docker-compose ps postgres

# Verify connection string in .env
# Test connection
docker-compose exec web python -c \
  "from django.db import connection; connection.ensure_connection()"
```

### Django Static Files Not Loading

```bash
# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Verify nginx configuration serves /static/* correctly
```

### React Build Failures

```bash
# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm package-lock.json
npm install

# Check TypeScript errors
npm run type-check
```

### WebSocket Connection Issues

```bash
# Ensure Redis is running
docker-compose ps redis

# Check WebSocket proxy configuration
docker-compose ps nginx  # If using nginx proxy
```

## Related Modules

- **CLI Module**: Command-line workflows this web interface simplifies
- **HPC Module**: Backend execution uses similar Singularity containers
- **Docker Module**: Container definitions used by web backend
- **Test Data**: Sample workflows for UI testing

## Development Roadmap

**Stage One**:
- Complete job submission API
- Implement real-time status updates
- Basic result visualization
- User authentication

**Stage Two**:
- Advanced permission system
- Result dataset management
- Workflow template customization
- Performance optimization

**Stage Three**:
- Federated execution (multiple clusters)
- Advanced analytics and reporting
- Community plugin system

## Contributing

When modifying web components:

1. Test both backend and frontend locally
2. Update API documentation in docstrings
3. Add unit tests for new features
4. Update this README with significant changes
5. Reference GitHub issues in commits

## Notes

- **Status**: This module is a candidate for future development
- **Feedback**: Report issues and feature requests on project tracker
- **Performance**: Local Docker Compose suitable for development; production requires optimization
- **Security**: Review environment variables before production deployment
- **Scaling**: Current design supports single-node; clustering requires architectural changes
