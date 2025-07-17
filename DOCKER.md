# Situ8 Platform Docker Implementation

## Overview

The Situ8 platform now features a comprehensive Docker implementation that provides:

- **Consistent Development Environment**: Identical environments across all developer machines
- **Production-Ready Containers**: Optimized Docker images for AWS ECS deployment
- **Multi-Tenant Architecture**: Container-based tenant isolation and routing
- **Scalable Infrastructure**: Auto-scaling ECS services with load balancing
- **CI/CD Integration**: Automated Docker builds and deployments via GitHub Actions

## Quick Start

### Prerequisites

- Docker Desktop installed and running
- Node.js 20+ (for local development without Docker)
- Git access to the repository

### Development Environment

Start the complete development stack:

```bash
# Easy way - using helper script
./docker-dev.sh dev

# Or using docker-compose directly
docker-compose --profile dev up -d
```

This starts:
- PostgreSQL database on port 5432
- API server on port 5000 (with hot-reload)
- Admin portal on port 3000 (with hot-reload)
- Customer portal on port 3001 (with hot-reload)

### Production Testing

Test the production-like environment:

```bash
# Start production containers
./docker-dev.sh prod

# Or using docker-compose directly
docker-compose --profile prod up -d
```

This starts:
- PostgreSQL database
- API server (compiled, production-ready)
- Admin portal on port 8080 (nginx-served)
- Customer portal on port 8081 (nginx-served)
- Load balancer on port 80

## Architecture

### Container Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Admin Portal   │    │ Customer Portal │    │   API Server    │
│  (React/Nginx)  │    │  (React/Nginx)  │    │   (Node.js)     │
│  Port: 8080     │    │  Port: 8081     │    │   Port: 5000    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
                    ┌─────────────────┐
                    │   PostgreSQL    │
                    │  Port: 5432     │
                    └─────────────────┘
```

### Multi-Tenant Routing

The platform supports multiple tenants through:

1. **Subdomain Routing**: `admin.situ8.ai`, `canary.situ8.ai`, `{customer}.situ8.ai`
2. **Header-Based Routing**: `X-Tenant` header for development
3. **Port-Based Routing**: Different ports for local development

## Docker Images

### API Image (`situ8-api`)

- **Base**: Node.js 20 Alpine
- **Multi-stage build**: Separate build and runtime stages
- **Security**: Non-root user, minimal attack surface
- **Size**: ~150MB (optimized)
- **Health checks**: Built-in health monitoring

Key features:
- TypeScript compilation during build
- Production-only dependencies in final image
- Database migration support
- Proper signal handling with dumb-init

### Frontend Image (`situ8-frontend`)

- **Base**: Nginx 1.25 Alpine
- **Multi-stage build**: React build + Nginx serving
- **Security**: Non-root user, security headers
- **Size**: ~50MB (optimized)
- **Features**: SPA routing, gzip compression

Key features:
- Environment-specific builds (admin/customer)
- Nginx configuration for multi-tenant routing
- Security headers (CORS, CSP, etc.)
- Browser caching optimization

## Development Workflows

### Using Helper Scripts

The `docker-dev.sh` script provides convenient commands:

```bash
# Start development environment
./docker-dev.sh dev

# Start production-like testing
./docker-dev.sh prod

# Build all images
./docker-dev.sh build

# Run comprehensive tests
./docker-dev.sh test

# Clean up everything
./docker-dev.sh clean

# View logs
./docker-dev.sh logs

# Open shell in API container
./docker-dev.sh shell-api

# Show help
./docker-dev.sh help
```

### Manual Docker Commands

For API development:
```bash
# Build API image
cd api && docker build -t situ8-api .

# Run API container
docker run -p 5000:5000 --env-file .env.local situ8-api

# Run with development mount
docker run -p 5000:5000 -v $(pwd)/src:/app/src situ8-api:dev
```

For Frontend development:
```bash
# Build frontend image
cd portals && docker build -t situ8-frontend .

# Run production frontend
docker run -p 8080:80 situ8-frontend

# Run development frontend with hot-reload
docker run -p 3000:3000 -v $(pwd)/src:/app/src situ8-frontend:dev
```

### NPM Scripts

Both `api/` and `portals/` directories include Docker-specific npm scripts:

```bash
# In api/ directory
npm run docker:build      # Build production image
npm run docker:build:dev  # Build development image
npm run docker:run        # Run production container
npm run docker:test       # Run tests in container
npm run docker:shell      # Open shell in container

# In portals/ directory
npm run docker:build:admin     # Build admin portal
npm run docker:build:customer  # Build customer portal
npm run docker:run:dev         # Run development server
npm run docker:test            # Run tests in container
```

## Production Deployment

### AWS ECS Deployment

The platform deploys to AWS ECS with:

- **Fargate**: Serverless containers
- **Auto Scaling**: CPU/Memory-based scaling
- **Load Balancing**: Application Load Balancer
- **Service Discovery**: ECS service mesh
- **Container Registry**: Amazon ECR

Deployment is handled automatically via GitHub Actions when pushing to the `main` branch.

### Terraform Configuration

ECS deployment is enabled by default:

```hcl
# In terraform/variables.tf
variable "enable_ecs" {
  description = "Enable ECS deployment"
  type        = bool
  default     = true  # Docker deployment is now default
}
```

### GitHub Actions Workflow

The `.github/workflows/docker-deploy.yml` workflow:

1. **Validates** infrastructure and runs tests
2. **Builds** API and Frontend Docker images
3. **Pushes** images to Amazon ECR
4. **Deploys** to ECS services
5. **Validates** deployment health

## Configuration

### Environment Variables

#### API Container
- `NODE_ENV`: production/development
- `PORT`: 5000 (default)
- `DB_HOST`: Database hostname
- `DB_PORT`: Database port
- `DB_USERNAME`: Database user
- `DB_PASSWORD`: Database password
- `JWT_SECRET`: JWT signing secret
- `ALLOWED_ORIGINS`: CORS origins

#### Frontend Container
- `REACT_APP_API_URL`: API endpoint URL
- `REACT_APP_BUILD_TARGET`: admin/customer

### Build Arguments

Frontend supports build-time configuration:

```bash
docker build \
  --build-arg REACT_APP_API_URL=https://api.situ8.ai/api/v1 \
  --build-arg REACT_APP_BUILD_TARGET=admin \
  -t situ8-frontend:admin .
```

## Testing

### Comprehensive Testing

Run the complete test suite:

```bash
./test-docker-stack.sh
```

This tests:
- Docker image builds
- Development environment functionality
- Production environment functionality
- Resource usage and performance
- Security and vulnerability scanning (if tools available)

### Individual Tests

```bash
# Test API build only
cd api && docker build -t situ8-api:test .

# Test frontend build only
cd portals && docker build -t situ8-frontend:test .

# Test specific environment
docker-compose --profile dev up -d
docker-compose --profile prod up -d
```

## Troubleshooting

### Common Issues

1. **Port conflicts**: Make sure ports 3000, 3001, 5000, 8080, 8081 are available
2. **Docker not running**: Ensure Docker Desktop is started
3. **Build failures**: Check `.dockerignore` files and dependencies
4. **Permission issues**: On Linux, ensure proper Docker permissions

### Debugging Commands

```bash
# View container logs
docker-compose logs [service-name]

# Check container status
docker-compose ps

# Inspect container
docker inspect [container-name]

# Open shell in running container
docker-compose exec [service-name] sh

# Check Docker system resources
docker system df
docker system events
```

### Log Analysis

```bash
# Real-time logs from all services
docker-compose logs -f

# Logs from specific service
docker-compose logs -f api

# Last 100 lines from API
docker-compose logs --tail 100 api
```

## Performance and Optimization

### Image Optimization

- **Multi-stage builds**: Separate build and runtime environments
- **Layer caching**: Optimized Dockerfile layer ordering
- **Minimal base images**: Alpine Linux for smaller footprint
- **.dockerignore**: Exclude unnecessary files from build context

### Resource Usage

Typical resource usage:
- **API Container**: ~200MB RAM, ~0.1 CPU
- **Frontend Container**: ~50MB RAM, ~0.05 CPU
- **Database Container**: ~150MB RAM, ~0.1 CPU

### Scaling Configuration

ECS auto-scaling triggers:
- CPU utilization > 70%
- Memory utilization > 80%
- Custom metrics available

## Security

### Container Security

- **Non-root users**: All containers run as unprivileged users
- **Minimal attack surface**: Only necessary packages installed
- **Security headers**: Nginx configured with security headers
- **Network isolation**: Containers communicate through Docker networks

### Vulnerability Scanning

If available, the testing script uses:
- **Docker Scout**: Built-in Docker security scanning
- **Trivy**: Open-source vulnerability scanner

### Best Practices Implemented

- Secrets management via environment variables
- Read-only filesystem where possible
- Resource limits and health checks
- Proper signal handling for graceful shutdowns

## Migration from EC2

The platform has migrated from EC2-based deployment to containerized ECS deployment:

### Benefits

- **Consistency**: Identical environments across dev/staging/prod
- **Scalability**: Automatic scaling based on demand
- **Cost Efficiency**: Pay only for resources used
- **Deployment Speed**: Faster deployments with container updates
- **Rollback Capability**: Easy rollbacks with ECS task definitions

### Backward Compatibility

The existing EC2 infrastructure remains available but is disabled by default. To re-enable EC2 deployment:

```hcl
# In terraform/variables.tf
variable "enable_ecs" {
  default = false  # Disables ECS, enables EC2
}
```

## Support and Maintenance

### Regular Tasks

- **Image Updates**: Rebuild images monthly for security updates
- **Dependency Updates**: Update Node.js and base images
- **Resource Monitoring**: Monitor container resource usage
- **Log Rotation**: Ensure log rotation is configured
- **Backup Verification**: Test database backup/restore procedures

### Monitoring

Production monitoring includes:
- Container health checks
- Resource utilization metrics
- Application performance monitoring
- Log aggregation and analysis

For support, refer to the main project documentation or contact the development team.