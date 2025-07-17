# Task List v1.1 - Activities Module Implementation (Frontend-First Approach)

## Overview
This document tracks the implementation of the Activities module using a frontend-first approach. By building the UI components first with mock data, we can iterate quickly on user experience before implementing complex backend logic.

**Last Updated**: 2025-01-11
**Current Phase**: Frontend Development
**Approach**: Frontend-First with Mock Data

## Key Advantages of Frontend-First
- Rapid visual feedback and iteration
- Clarify requirements through UI prototyping
- Use existing alert endpoints as temporary backend
- Parallel development once UI is approved
- Better stakeholder engagement with visual progress

## Task Categories

### PHASE 1: Frontend Foundation & Mock Data [PRIORITY 1]

#### 1.1 Mock Data Setup
- [ ] **TASK-001**: Create activity mock data generator
  - Generate realistic activity data for all types
  - Include various statuses and timestamps
  - Create mock tags and locations
  - Export as JSON for easy import
  
- [ ] **TASK-002**: Create mock API service
  - Simulate CRUD operations with local storage
  - Add artificial delays for realism
  - Include mock error scenarios
  - Support pagination and filtering

#### 1.2 Core Components
- [ ] **TASK-003**: Create ActivityCard component
  - Display activity type with icon (🚨🔍⚠️🔧🚫👁️📸)
  - Show title, description preview
  - Status badge (detecting/responding/investigating/resolved)
  - Location info (building, floor, zone)
  - Timestamp with relative time
  - Priority indicator for critical activities
  
- [ ] **TASK-004**: Create ActivityList component
  - Grid/List view toggle
  - Bulk selection with checkboxes
  - Pagination controls
  - Empty state design
  - Loading skeleton screens
  - Iceberg view indicator (showing X of Y activities)
  
- [ ] **TASK-005**: Create ActivityTypeIcon component
  - Icon mapping for each activity type
  - Color coding by priority/type
  - Animated states for active activities
  - Tooltip with type description

#### 1.3 Activity Management Page
- [ ] **TASK-006**: Update Activities page structure
  - Replace current Alerts page content
  - Add page header with statistics
  - Implement responsive layout
  - Add breadcrumb navigation
  
- [ ] **TASK-007**: Create ActivityFilters component
  - Type filter (multi-select checkboxes)
  - Status filter dropdown
  - Date range picker
  - Location selector
  - Tag search input
  - Clear all filters button
  - Save filter presets
  
- [ ] **TASK-008**: Create ActivityStats component
  - Total activities count
  - Breakdown by type (pie chart)
  - Status distribution
  - Response time metrics
  - Trend indicators (↑↓)

### PHASE 2: Activity Details & Forms [PRIORITY 1]

#### 2.1 Detail Views
- [ ] **TASK-009**: Create ActivityDetailModal component
  - Full activity information display
  - Timeline of status changes
  - Related incidents section
  - Assigned personnel list
  - Location map preview
  - Media attachments viewer
  - Action buttons (update status, assign, escalate)
  
- [ ] **TASK-010**: Create ActivityTimeline component
  - Visual status progression
  - Timestamp for each change
  - User who made changes
  - Comments/notes per status
  - Estimated time remaining

#### 2.2 Creation & Editing
- [ ] **TASK-011**: Create ActivityForm component
  - Type selector with descriptions
  - Title and description fields
  - Location picker (hierarchical)
  - Tag input with suggestions
  - Confidence slider (for integration activities)
  - Media upload area
  - Save as draft option
  
- [ ] **TASK-012**: Create LocationPicker component
  - Building → Floor → Zone hierarchy
  - Search functionality
  - Recent locations
  - Map-based selection (optional)
  - GPS coordinate input
  
- [ ] **TASK-013**: Create TagInput component
  - Auto-complete from existing tags
  - Category:value format validation
  - Color-coded tag chips
  - Remove tags with X
  - Suggest tags based on activity type

### PHASE 3: Real-time Features & Interactions [PRIORITY 2]

#### 3.1 Live Updates
- [ ] **TASK-014**: Create ActivityNotification component
  - Toast notifications for new activities
  - Priority-based styling
  - Sound alerts for critical types
  - Quick action buttons
  - Auto-dismiss timer
  
- [ ] **TASK-015**: Implement real-time activity updates
  - Simulate WebSocket with mock data
  - Update list automatically
  - Show update indicators
  - Conflict resolution UI
  
- [ ] **TASK-016**: Create ActivityStream component
  - Continuous scrolling feed
  - New activity indicators
  - Compact card design
  - Type filtering toggles
  - Pause/resume updates

#### 3.2 Bulk Operations
- [ ] **TASK-017**: Create BulkActions component
  - Tag multiple activities
  - Change status in bulk
  - Create incident from selected
  - Export selected activities
  - Assign to user in bulk

### PHASE 4: Command Center Integration [PRIORITY 2]

#### 4.1 Dashboard Widgets
- [ ] **TASK-018**: Create ActivityStreamWidget
  - Compact view for command center
  - Configurable size
  - Priority filtering
  - Quick create button
  - Minimal UI design
  
- [ ] **TASK-019**: Create ActivityMapWidget
  - Plot activities on floor plan
  - Activity type icons
  - Cluster nearby activities
  - Click for quick details
  - Heat map option

#### 4.2 Mobile Responsiveness
- [ ] **TASK-020**: Optimize components for mobile
  - Touch-friendly controls
  - Swipe actions
  - Responsive layouts
  - Offline capability
  - Progressive web app features

### PHASE 5: Backend API Implementation [PRIORITY 1]

#### 5.1 Database & Models
- [ ] **TASK-021**: Create Activity model
  - Define schema based on frontend needs
  - Add indexes for performance
  - Set up relationships
  
- [ ] **TASK-022**: Create database migrations
  - Activities table
  - Activity_tags junction table
  - Update incidents table

#### 5.2 API Endpoints
- [ ] **TASK-023**: Implement Activity CRUD endpoints
  - GET /api/v1/activities (with filters)
  - POST /api/v1/activities
  - PATCH /api/v1/activities/:id
  - DELETE /api/v1/activities/:id
  
- [ ] **TASK-024**: Create validation middleware
  - Request body validation
  - Type and status validation
  - Permission checking
  
- [ ] **TASK-025**: Implement Auto-Incident Engine
  - Rule evaluation logic
  - Incident creation
  - Notification triggers

### PHASE 6: Integration Layer [PRIORITY 2]

#### 6.1 External System Webhooks
- [ ] **TASK-026**: Create webhook receivers
  - Ambient.ai endpoint
  - Lenel endpoint
  - Generic sensor endpoint
  
- [ ] **TASK-027**: Build activity mappers
  - Transform external events to activities
  - Calculate confidence scores
  - Apply auto-tagging

#### 6.2 Real-time Infrastructure
- [ ] **TASK-028**: Implement WebSocket server
  - Activity broadcasts
  - User subscriptions
  - Connection management
  
- [ ] **TASK-029**: Create notification service
  - Email notifications
  - SMS for critical
  - Push notifications

### PHASE 7: Testing & Polish [PRIORITY 3]

#### 7.1 Testing
- [ ] **TASK-030**: Write component tests
  - Unit tests for each component
  - Integration tests for workflows
  - Visual regression tests
  
- [ ] **TASK-031**: Create E2E tests
  - Activity creation flow
  - Filter and search
  - Bulk operations

#### 7.2 Documentation
- [ ] **TASK-032**: Document component APIs
  - Props documentation
  - Usage examples
  - Storybook stories
  
- [ ] **TASK-033**: Create user guides
  - Activity management guide
  - Integration setup
  - Best practices

## Implementation Order

### Week 1-2: Foundation
1. Mock data setup (TASK-001, 002)
2. Core components (TASK-003, 004, 005)
3. Basic page structure (TASK-006)

### Week 3-4: Full UI
1. Filters and stats (TASK-007, 008)
2. Detail views (TASK-009, 010)
3. Forms (TASK-011, 012, 013)

### Week 5-6: Interactivity
1. Real-time features (TASK-014, 015, 016)
2. Bulk operations (TASK-017)
3. Command center widgets (TASK-018, 019)

### Week 7-8: Backend
1. Database setup (TASK-021, 022)
2. API implementation (TASK-023, 024, 025)
3. Connect frontend to real API

### Week 9-10: Integration & Polish
1. External webhooks (TASK-026, 027)
2. Real-time infrastructure (TASK-028, 029)
3. Testing and documentation

## Progress Tracking

### Completed Tasks
- None yet (Initial creation)

### In Progress
- Setting up frontend structure

### Blocked Tasks
- None currently

## Quick Reference

### Component Hierarchy
```
Activities (page)
├── ActivityStats
├── ActivityFilters
├── ActivityList
│   └── ActivityCard
├── ActivityDetailModal
│   └── ActivityTimeline
└── ActivityForm
    ├── LocationPicker
    └── TagInput
```

### Mock Data Structure
```javascript
{
  id: "ACT-0001",
  type: "medical",
  title: "Medical emergency in Building A",
  description: "Person collapsed near entrance",
  status: "responding",
  location: {
    building: "A",
    floor: "1",
    zone: "Lobby"
  },
  tags: ["urgent:critical", "location:entrance"],
  confidence: 95,
  trigger_type: "human",
  created_at: "2024-01-11T10:30:00Z",
  created_by: { id: 1, name: "John Smith" }
}
```

### Activity Types & Icons
- `patrol` 🔍 - Routine patrol
- `alert` ⚠️ - System alert
- `medical` 🚨 - Medical emergency
- `security-breach` 🚫 - Security violation
- `property-damage` 🔧 - Property damage
- `bol-event` 👁️ - BOL match
- `evidence` 📸 - Evidence collection