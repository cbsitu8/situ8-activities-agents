# Situ8 FSD - AI-Assisted MVP Edition v0.1

## **📆 Version History**

| Version | Date | Changes |
|---------|------|---------|
| v0.0 | Original | Initial FSD with Activity-first architecture |
| v0.1 | Current | Enhanced Case Management with AI insights, Full Reports & Analytics, Global AI Assistant |

### **🆕 New in v0.1**
- **Enhanced Case Management**: AI-powered insights, automated timelines, smart incident suggestions
- **Reports & Analytics**: Comprehensive reporting suite replacing basic daily reports
- **Global AI Assistant**: Expanded Orchestr8 with natural language processing across all modules

---

## **📌 1. Overview**

Situ8 is a comprehensive security operations platform designed to unify all security events through a single **Activity-first architecture**. Every event - from routine patrols to critical emergencies - enters the system as an Activity, creating one searchable, intelligent stream of security data. This Functional Specification Document (FSD) serves as the single source of truth for the MVP implementation, featuring Orchestr8 AI as the intelligent assistant for activity management and communication via integrated platforms.

### **1.1 📋 Document Purpose**

- Define exact platform behavior for developer implementation of the Activity-first system
- Establish Security Command Center as the operational interface for activity monitoring
- Specify how all events become Activities before any other processing
- Provide comprehensive activity routing and auto-incident creation rules
- Detail specialized AI contexts that analyze activity patterns
- Enable seamless flow from Activities → Incidents → Cases
- Establish clear role-based permissions for activity management
- Specify data relationships, validation rules, and tag taxonomy
- Provide API contract expectations for activity creation
- Enable future iterations through prompt-based editing

### **1.2 🎯 V0 Scope Principles**

- **Activity-First** – Every event enters as an Activity, no exceptions
- **Unified Stream** – Single searchable stream replaces scattered logs
- **Intelligent Routing** – Auto-incident rules based on activity type and context
- **Command Center First** – Real-time activity monitoring as primary interface
- **Human + System Input** – Radio, manual entry, and all integrations create Activities
- **Smart Tagging** – Activities are automatically tagged for search and routing
- **AI-Enhanced** – Triple AI system analyzes activity patterns
- **Core functionality only** – Advanced features in future versions
- **Data integrity focus** – Complete audit trail of all activities

### **1.3 🏗️ Platform Architecture Overview**

```
Situ8 Activity-First Architecture:

                    ┌─────────────────────────────────────┐
                    │        ACTIVITY INPUT LAYER         │
                    │    ├─ Human Triggers (Radio/UI)    │
                    │    ├─ Integration Triggers         │
                    │    ├─ Auto-Tagging Engine          │
                    │    └─ Activity Type Classification │
                    └─────────────────┬───────────────────┘
                                      │
                                      ▼
                    ┌─────────────────────────────────────┐
                    │      ACTIVITY PROCESSING ENGINE     │
                    │    ├─ Status: detecting → resolved │
                    │    ├─ Auto-Incident Rules          │
                    │    ├─ Tag-Based Routing            │
                    │    └─ AI Pattern Analysis          │
                    └─────────────────┬───────────────────┘
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        │                             │                             │
        ▼                             ▼                             ▼
┌───────────────────┐       ┌─────────────────┐         ┌─────────────────┐
│  STAYS ACTIVITY   │       │ BECOMES INCIDENT │         │ LINKS TO EXISTING│
│ ├─ Patrol logs    │       │ ├─ Medical emergency     │ ├─ Related activity
│ ├─ Routine checks │       │ ├─ Security breach       │ ├─ Evidence added
│ └─ Archived       │       │ └─ Property damage       │ └─ Updates status
└───────────────────┘       └─────────────────┘         └─────────────────┘

                           SECURITY COMMAND CENTER
                    ┌─────────────────────────────────────────────────────────────────┐
                    │                    PRIMARY INTERFACE                             │
                    ├─────────────────────────────────────────────────────────────────┤
                    │  Activity Stream │ Active Incidents │ Guard Status │ Map View*   │
                    │  ├─ Live feed    │ ├─ Grouped activities │ ├─ Locations │ ├─ Guards    │
                    │  ├─ Type filters │ ├─ Response tracking  │ ├─ Dispatch  │ ├─ Incidents │
                    │  ├─ Tag search   │ ├─ Auto-escalation    │ ├─ Comms     │ ├─ Zones     │
                    │  └─ Status flow  │ └─ Case creation      │ └─ Resources │ └─ *Optional │
                    └─────────────────────────────────────────────────────────────────┘
```

### **1.4 🤖 MVP AI Architecture**

```
MVP AI Architecture with Orchestr8:

┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORCHESTR8 AI SYSTEM (MVP)                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🤖 ORCHESTR8 (Operational AI)                                              │
│  ├─ Activity creation from voice/text     Powered by:                      │
│  ├─ Simple categorization                 • GPT-4.0 mini (cost-efficient)  │
│  ├─ Basic summaries                       • OpenAI Whisper (transcription) │
│  ├─ Status updates                        • N8N workflow orchestration     │
│  └─ Operational guidance                                                    │
│                                                                             │
│  Future Versions:                                                           │
│  • Investig8 (Pattern Analysis)                                            │
│  • Coordin8 (Resource Optimization)                                        │
│                                                                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                      ACTIVITY PROCESSING ENGINE                             │
│  ├─ Voice memo → Activity conversion                                        │
│  ├─ Auto-incident rule application                                         │
│  ├─ Basic tag generation                                                    │
│  └─ Status tracking                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **1.5 🔄 Activity Processing & Integration Stack**

| **Input Source** | **Creates Activity Type** | **Auto-Incident Rules** | **Command Center Display** |
|------------------|---------------------------|-------------------------|----------------------------|
| **📻 Radio (Human)** | All types based on speech | Type-specific rules | Real-time in Activity Stream |
| **📱 Manual UI (Human)** | All types via form | Type-specific rules | Immediate update |
| **🎥 Ambient.ai** | `alert`, `security-breach` | Confidence > 80% or after-hours | Video + Activity correlation |
| **🚪 Lenel Access** | `alert`, `security-breach` | After-hours = auto-incident | Door status + Activity |
| **🔊 Sensors** | `alert`, `property-damage` | Confidence > 75% | Location map + Activity |
| **👁️ BOL System** | `bol-event` | Always creates incident | Priority alert + Activity |

**Activity Type Auto-Incident Rules:**

| **Activity Type** | **Auto-Incident Logic** | **Supervisor Override** |
|-------------------|-------------------------|-------------------------|
| `medical` | ALWAYS create incident | Can add notes, cannot dismiss |
| `security-breach` | ALWAYS create incident | Can downgrade after review |
| `bol-event` | ALWAYS create incident | Cannot dismiss active BOL |
| `alert` | IF confidence > 80% OR after-hours | Can dismiss if false positive |
| `property-damage` | IF confidence > 75% | Can dismiss if minor |
| `patrol` | NEVER auto-incident | Can manually elevate |
| `evidence` | NEVER auto-incident | Links to existing incident |

## **🔖 2. Table of Contents**

### **2.1 📑 Comprehensive Navigation**

**🆕 Quick Links to New v0.1 Features:**
- [AI-Powered Case Insights](#738-ai-powered-case-insights-v01-enhancement)
- [Full Reports & Analytics](#76-reports--analytics)
- [Global AI Assistant](#7105-global-ai-assistant-enhancement-v01)

**📚 Complete Document Structure:**

1. **[📌 Overview](#1-overview)**
   - 1.1 [📋 Document Purpose](#11-document-purpose)
   - 1.2 [🎯 V0 Scope Principles](#12-v0-scope-principles)
   - 1.3 [🏗️ Platform Architecture Overview](#13-platform-architecture-overview)
   - 1.4 [🤖 MVP AI Architecture](#14-mvp-ai-architecture)
   - 1.5 [🔄 Activity Processing & Integration Stack](#15-activity-processing--integration-stack)

2. **[🔖 Table of Contents](#2-table-of-contents)** *(You are here)*

3. **[🖼️ System Interface Mockups](#3-system-interface-mockups)** 🆕
   - 3.1 Security Command Center Dashboard
   - 3.2 Activity Management Interface
   - 3.3 Case Management with AI Insights
   - 3.4 Reports & Analytics Center
   - 3.5 Global AI Assistant

4. **[📊 Module & Features Summary](#4-module--features-summary)** 🆕
   - Complete feature matrix
   - v0.1 enhancements highlighted

5. **[👤 User Roles](#5-user-roles)**
   - 7.1 [🎭 Role Definitions](#71-role-definitions)
   - 7.2 [🎛️ Command Center Role Matrix](#72-command-center-role-matrix)
   - 7.3 [🏢 Platform Admin Role](#73-platform-admin-role)
   - 7.4 [📊 Detailed Permissions Matrix](#74-detailed-permissions-matrix)
   - 7.5 [🔐 Session Management](#75-session-management)

6. **[🌐 Global Functional Rules](#6-global-functional-rules)**
   - 6.1 [🌍 Universal Behaviors](#61-universal-behaviors)
   - 6.2 [🔗 Enhanced Linking Rules](#62-enhanced-linking-rules)
   - 6.3 [🏔️ Activity Filtering Rules](#63-activity-filtering-rules)
   - 6.4 [📍 Location Data Requirements](#64-location-data-requirements)

7. **[📄 Page-Level Functional Specifications](#7-page-level-functional-specifications)**
   
   **7.1 [📋 Activity Management](#71-activity-management)**
   - 7.1.1 Activity System Architecture
   - 7.1.2 Enhanced Activity Processing
   - 7.1.3 Enhanced Activity Interface
   - 7.1.4 Activity Cards
   - 7.1.5 Enhanced Activity Workflow
   - 7.1.6 Activity Filtering - Iceberg Approach
   - 7.1.7 Manual Activity Creation
   - 7.1.8 Integration Activity Processing
   - 7.1.9 Tag Management Interface
   - 7.1.10 Activity Analytics Dashboard
   
   **7.2 [📋 Incident Management](#72-incident-management)**
   - 7.2.1 Command Center Integration
   - 7.2.2 Enhanced Multi-Location Architecture
   - 7.2.3 Enhanced Incident Management Interface
   - 7.2.4 Enhanced Incident Creation
   - 7.2.5 Enhanced Incident Detail View
   - 7.2.6 Enhanced Incident Workflow
   
   **7.3 [📁 Case Management](#73-case-management)** ✨ *Enhanced in v0.1*
   - 7.3.1 Strategic Layer Integration
   - 7.3.2 Oracle AI Integration
   - 7.3.3 Enhanced Case List Interface
   - 7.3.4 Enhanced Case Creation
   - 7.3.5 Enhanced Case Detail View
   - 7.3.6 Enhanced Case Workflow
   - 7.3.7 Case Status Progression
   - 7.3.8 🆕 AI-Powered Case Insights
   - 7.3.9 🆕 Automated Case Timeline
   - 7.3.10 🆕 Smart Incident Suggestions
   
   **7.4 [👥 User Management](#74-user-management)**
   - 7.4.1 Multi-Location User Matrix
   - 7.4.2 Enhanced User Creation/Edit
   - 7.4.3 Location Access Management
   - 7.4.4 Command Center Access Configuration
   - 7.4.5 Real-Time Activity Coordination
   - 7.4.6 User Performance Analytics
   - 7.4.7 Special User Management Behaviors
   
   **7.5 [🔍 Global Search](#75-global-search)**
   - 7.5.1 Global Search Interface
   - 7.5.2 Real-Time Search Results
   - 7.5.3 AI-Enhanced Search Intelligence
   - 7.5.4 Enhanced Saved Searches
   - 7.5.5 Search Analytics
   
   **7.6 [📊 Reports & Analytics](#76-reports--analytics)** 🆕 *Completely Enhanced in v0.1*
   - 7.6.1 Pre-Built Reports Library
   - 7.6.2 Custom Report Builder
   - 7.6.3 Report Queue & Management
   - 7.6.4 Report Features & Permissions
   
   **7.7 [⚙️ Settings & Configuration](#77-settings--configuration)**
   - 7.7.1 Organization Settings
   - 7.7.2 Security Settings
   - 7.7.3 Activity Type Configuration
   - 7.7.4 Tag Management
   - 7.7.5 Integrations Page
   - 7.7.6 Notification Settings
   - 7.7.7 AI Configuration
   
   **7.8 [👁️ BOL Management](#78-bol-management)**
   - 7.8.1 Multi-Site BOL Dashboard
   - 7.8.2 Enhanced BOL Creation
   - 7.8.3 Oracle-Enhanced BOL Intelligence
   - 7.8.4 Real-Time BOL Activity Matching
   - 7.8.5 Cross-Site BOL Activity Coordination
   - 7.8.6 Enhanced BOL Resolution
   
   **7.9 [📝 Passdowns](#79-passdowns)**
   - 7.9.1 Passdown Dashboard with Activities
   - 7.9.2 Enhanced Passdown Creation
   - 7.9.3 Activity-Based Passdown Intelligence
   - 7.9.4 Cross-Site Activity Coordination
   - 7.9.5 Enhanced Passdown Detail
   
   **7.10 [🤖 Orchestr8 AI Assistant](#710-orchestr8-ai-assistant)** ✨ *Enhanced in v0.1*
   - 7.10.1 Orchestr8 AI Architecture
   - 7.10.2 Orchestr8 AI Interface
   - 7.10.3 MVP Task Capabilities
   - 7.10.4 AI Permissions & Limits
   - 7.10.5 🆕 Global AI Assistant Enhancement
   
   **7.11 [📋 Audit Logs](#711-audit-logs)**
   - 7.11.1 Activity-Enhanced Audit Architecture
   - 7.11.2 Activity-Specific Audit Events
   - 7.11.3 Auto-Incident Decision Logging
   - 7.11.4 Tag Operation Auditing
   - 7.11.5 Activity Audit Analytics
   
   **7.12 [🏢 Location Management](#712-location-management)**
   - 7.12.1 Activity-Enhanced Location Structure
   - 7.12.2 Activity-Based Location Configuration
   - 7.12.3 Activity-Based Resource Allocation
   - 7.12.4 Cross-Site Activity Coordination
   - 7.12.5 Activity-Based Security Policies
   - 7.12.6 Location Activity Analytics
   
   **7.13 [💬 In-App Messaging](#713-in-app-messaging)** *(Deprecated)*
   
   **7.14 [🎥 Ambient.ai Integration](#714-ambientai-integration)**
   - 7.14.1 GIF Preview Feature
   - 7.14.2 Integration Specifications
   - 7.14.3 Alert Processing Workflow
   - 7.14.4 Configuration Settings
   
   **7.15 [🚪 Lenel Access Control Integration](#715-lenel-access-control-integration)**
   - 7.15.1 Badge Correlation Engine
   - 7.15.2 Integration Specifications
   - 7.15.3 PII Data Management
   - 7.15.4 Correlation Workflow
   
   **7.16 [📱 Communication Platforms](#716-communication-platforms)**
   - 7.16.1 Telegram Integration
   - 7.16.2 N8N Workflow Orchestration
   - 7.16.3 Modular Architecture
   - 7.16.4 Future Platform Support
   
   **7.17 [🗺️ Map-Based Visualization](#717-map-based-visualization)**
   - 7.17.1 Guard Tracking
   - 7.17.2 Incident Visualization
   - 7.17.3 Map Controls
   - 7.17.4 Location Data Requirements
   - 7.17.5 Configuration Options

8. **[🆕 Summary of v0.1 Enhancements](#8-summary-of-v01-enhancements)**

9. **[📚 Implementation Guide](#9-implementation-guide)**

---

## **🖼️ 3. System Interface Mockups**

### **3.1 Security Command Center Dashboard**

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ SITU8 SECURITY COMMAND CENTER                          🔔 3  👤 Admin  ⚙️  🚪 Logout │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│ ┌─────────────────────┬─────────────────────┬────────────────────┬──────────────┐ │
│ │  ACTIVITY STREAM    │  ACTIVE INCIDENTS   │   GUARD STATUS     │   MAP VIEW   │ │
│ │  ════════════════   │  ════════════════   │   ════════════     │   ════════   │ │
│ │                     │                     │                    │              │ │
│ │ 🚨 Medical Emergency│ 🔴 INC-0234 (3 act) │ 👮 12/15 On Duty   │ [Interactive │ │
│ │    Building A       │    Medical - Bldg A │ 🟢 Johnson - A1    │     Map      │ │
│ │    2 min ago        │    Responding       │ 🟢 Wilson - B2     │   Showing    │ │
│ │                     │                     │ 🟡 Garcia - Break  │   Guards &   │ │
│ │ ⚠️ Door Forced      │ 🟠 INC-0232 (1 act) │                    │  Incidents]  │ │
│ │    Loading Dock     │    Security Breach  │ 📊 Response Stats  │              │ │
│ │    5 min ago        │    Investigating    │ Avg Time: 2.3 min  │ 📍 Site A    │ │
│ │                     │                     │                    │ 🔴 2 Active  │ │
│ │ 🔍 Patrol Complete  │ 🟡 INC-0230 (2 act) │ 📞 Dispatch        │ 👮 5 Guards  │ │
│ │    Zone C           │    Suspicious Person│ [Quick Dispatch]   │              │ │
│ │    12 min ago       │    Monitoring       │                    │              │ │
│ │                     │                     │                    │              │ │
│ │ [View All ▼]        │ [+ Create Incident] │ [Guard Details]    │ [Full Map]   │ │
│ └─────────────────────┴─────────────────────┴────────────────────┴──────────────┘ │
│                                                                                    │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🤖 AI INSIGHTS                                          [Expand] [Settings]   │ │
│ ├──────────────────────────────────────────────────────────────────────────────┤ │
│ │ • Pattern Detected: 3 similar incidents in Building A this week              │ │
│ │ • Recommendation: Increase patrols in Building A 02:00-04:00                 │ │
│ │ • Alert: Guard coverage below minimum in Zone D                              │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│ [📋 Activities] [🚨 Incidents] [📁 Cases] [📊 Reports] [👁️ BOLs] [📝 Passdowns] │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### **3.2 Activity Management Page**

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ 📋 ACTIVITY MANAGEMENT                                 🔔 3  👤 Admin  ⚙️  🚪 Logout │
├────────────────────────────────────────────────────────────────────────────────────┤
│ Filters: [All Types ▼] [All Triggers ▼] [All Statuses ▼] [Today ▼]               │
│ Search: [🔍 Search by tags, title, description...]          [+ Create Activity]    │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│ ⚡ Quick Stats: 234 Total | 12 Detecting | 8 Responding | 3 Investigating         │
│                                                                                    │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ □ │ ID       │ Type      │ Title              │ Status      │ Location │ Time │ │
│ ├───┼──────────┼───────────┼────────────────────┼─────────────┼──────────┼──────┤ │
│ │ □ │ ACT-0456 │ 🚨Medical │ Unconscious person │ Responding  │ Bldg A   │ 2m   │ │
│ │ □ │ ACT-0455 │ ⚠️Alert   │ Door held open     │ Detecting   │ Bldg B   │ 5m   │ │
│ │ □ │ ACT-0454 │ 🔍Patrol  │ Zone C complete    │ Resolved    │ Zone C   │ 12m  │ │
│ │ □ │ ACT-0453 │ 🏚️Damage  │ Broken window      │ Investigating│ Bldg A  │ 1h   │ │
│ │ □ │ ACT-0452 │ 📸Evidence│ Photos uploaded    │ Resolved    │ Bldg A   │ 2h   │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
│                                                                                    │
│ Bulk Actions: [🏷️ Tag Selected] [🚨 Create Incident] [📤 Export]                  │
│                                                                                    │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🏔️ ACTIVITY ICEBERG                                   ○ Smart ● All          │ │
│ ├──────────────────────────────────────────────────────────────────────────────┤ │
│ │ Showing top 10% critical activities. 210 routine activities hidden.          │ │
│ │ [Show Hidden Activities] [Configure Filters]                                 │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### **3.3 Case Management with AI Insights (v0.1)**

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ 📁 CASE MANAGEMENT                                     🔔 3  👤 Admin  ⚙️  🚪 Logout │
├────────────────────────────────────────────────────────────────────────────────────┤
│ CASE-2024-0123: Coordinated Theft Ring Investigation              Status: ACTIVE   │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│ [📊 Overview] [🕐 Timeline] [📎 Evidence] [👥 Team] [🤖 AI Insights] [📝 Notes]    │
│                                                                                    │
│ ┌─────────────────────────────┬──────────────────────────────────────────────────┐ │
│ │ 🤖 AI CASE INSIGHTS 🆕      │ 📊 CASE DETAILS                                  │ │
│ ├─────────────────────────────┼──────────────────────────────────────────────────┤ │
│ │ Pattern Analysis:           │ Lead: Det. Johnson                               │ │
│ │ • 78% occur 02:00-04:00 AM │ Team: Wilson, Garcia                             │ │
│ │ • Entry via loading dock   │ Priority: HIGH                                   │ │
│ │ • Cameras disabled first   │ Activities: 47                                   │ │
│ │                             │ Incidents: 6                                     │ │
│ │ Risk Score: 85/100 🔴       │ Locations: Building A, B                         │ │
│ │                             │                                                  │ │
│ │ Recommendations:            │ Related Cases:                                   │ │
│ │ 1. Increase dock patrols    │ • CASE-2023-0892 (87% match)                    │ │
│ │ 2. Review night shift logs  │ • CASE-2023-0645 (73% match)                    │ │
│ │ 3. Check vehicle sightings  │                                                  │ │
│ │                             │                                                  │ │
│ │ [View Full Analysis]        │ [Update Case] [Generate Report]                  │ │
│ └─────────────────────────────┴──────────────────────────────────────────────────┘ │
│                                                                                    │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🕐 AUTOMATED TIMELINE 🆕                                    [Filter] [Export] │ │
│ ├──────────────────────────────────────────────────────────────────────────────┤ │
│ │ 2024-01-10 02:15 | 🔍 Patrol reports suspicious vehicle (ACT-0234)          │ │
│ │ 2024-01-10 02:45 | ⚠️ Door sensor triggered at loading dock (ACT-0237)      │ │
│ │ 2024-01-10 02:47 | 🚨 Multiple cameras disabled (ACT-0238)                  │ │
│ │ 2024-01-10 03:15 | 🏚️ Inventory missing - $45,000 (ACT-0241)               │ │
│ │ 2024-01-11 09:30 | 📸 Security footage recovered (ACT-0256)                 │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### **3.4 Reports & Analytics Center (v0.1)**

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ 📊 REPORTS & ANALYTICS CENTER 🆕                       🔔 3  👤 Admin  ⚙️  🚪 Logout │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│ [📚 Pre-Built Reports] [🔨 Custom Builder] [📋 My Reports] [⏰ Scheduled] [📈 Queue] │
│                                                                                    │
│ ┌─────────────────────────────┬──────────────────────────────────────────────────┐ │
│ │ 📚 PRE-BUILT REPORTS        │ 🔨 CUSTOM REPORT BUILDER                         │ │
│ ├─────────────────────────────┼──────────────────────────────────────────────────┤ │
│ │ 📅 Daily Activity Summary   │ Step 1: Select Data Sources                      │ │
│ │    Last: 2 hours ago        │ ☑ Activities  ☑ Incidents  ☐ Cases  ☐ Users    │ │
│ │    [Run] [Schedule] [View]  │                                                  │ │
│ │                             │ Step 2: Choose Fields (Drag & Drop)             │ │
│ │ 📈 Weekly Incident Report   │ Available:        Selected:                      │ │
│ │    Last: Monday             │ • Type           • Date                          │ │
│ │    [Run] [Schedule] [View]  │ • Status         • Type                          │ │
│ │                             │ • Location       • Location                      │ │
│ │ 📊 Monthly Case Metrics     │ • Tags           • Response Time                 │ │
│ │    Last: 1st of month       │                                                  │ │
│ │    [Run] [Schedule] [View]  │ Step 3: Set Filters                              │ │
│ │                             │ Date: [Last 30 Days ▼]                          │ │
│ │ 👥 User Activity Report     │ Location: [All ▼]                                │ │
│ │ ⏱️ Response Time Analysis   │                                                  │ │
│ │ 🤖 AI Usage Report          │ [Preview] [Save & Run] [Schedule]                │ │
│ └─────────────────────────────┴──────────────────────────────────────────────────┘ │
│                                                                                    │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ 📈 REPORT QUEUE                                                               │ │
│ ├──────────────────────────────────────────────────────────────────────────────┤ │
│ │ 🔄 Monthly Case Metrics - Progress: ████████░░ 78% (Est: 1 min)             │ │
│ │ ✅ Daily Activity Summary - Complete (Download)                              │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────┘
```

### **3.5 Global AI Assistant Interface (v0.1)**

```
┌────────────────────────────────────────────────────────────────────────────────────┐
│ Any Page in Situ8...                                   🔔 3  👤 Admin  ⚙️  🚪 Logout │
├────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                    │
│ [Regular page content...]                                                          │
│                                                                                    │
│                                                              ┌─────────────────┐   │
│                                                              │ 🤖 AI Assistant │   │
│                                                              │ ═══════════════ │   │
│                                                              │                 │   │
│                                                              │ How can I help? │   │
│                                                              │                 │   │
│                                                              │ Quick Actions:  │   │
│                                                              │ 🔍 Search       │   │
│                                                              │ 📋 Create       │   │
│                                                              │ 📊 Report       │   │
│                                                              │                 │   │
│                                                              │ [Minimize] [?]  │   │
│                                                              └─────────────────┘   │
│                                                                                    │
│ ┌──────────────────────────────────────────────────────────────────────────────┐ │
│ │ 💬 AI ASSISTANT - EXPANDED VIEW 🆕                         [─] [×]          │ │
│ ├──────────────────────────────────────────────────────────────────────────────┤ │
│ │ Current Context: Case Management > CASE-2024-0123                            │ │
│ ├──────────────────────────────────────────────────────────────────────────────┤ │
│ │ You: Show me all medical incidents from last week                           │ │
│ │                                                                              │ │
│ │ AI: I found 3 medical incidents from last week:                             │ │
│ │     • INC-0234 - Person unconscious (Building A) - Resolved                 │ │
│ │     • INC-0267 - Slip and fall (Parking Lot) - Resolved                    │ │
│ │     • INC-0289 - Allergic reaction (Cafeteria) - Resolved                  │ │
│ │                                                                              │ │
│ │     Would you like to view details or create a report?                      │ │
│ │                                                                              │ │
│ │ [View INC-0234] [View All] [Create Report] [New Search]                     │ │
│ ├──────────────────────────────────────────────────────────────────────────────┤ │
│ │ Type your question or command... (Ctrl+K)                    [Send] [Clear] │ │
│ └──────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────┘
```

---

## **📊 4. Module & Features Summary**

### **4.1 Complete Feature Matrix**

| Module | Purpose | Key Features | v0.1 Enhancements |
|--------|---------|--------------|-------------------|
| **📋 Activity Management** | Central event capture system | • All events enter as activities<br>• Auto-tagging & routing<br>• Iceberg filtering<br>• Status workflow | - |
| **📋 Incident Management** | Operational response coordination | • Auto-creation from activities<br>• Multi-location support<br>• Response tracking<br>• Command center integration | - |
| **📁 Case Management** | Strategic investigation platform | • Incident grouping<br>• Evidence management<br>• Team coordination<br>• Cross-site support | 🆕 AI insights<br>🆕 Auto timeline<br>🆕 Smart suggestions |
| **👥 User Management** | Personnel administration | • Role-based access<br>• Location assignments<br>• Performance tracking<br>• Activity analytics | - |
| **🔍 Global Search** | Universal data discovery | • Natural language<br>• AI-enhanced<br>• Saved searches<br>• Analytics | - |
| **📊 Reports & Analytics** | Data analysis & reporting | • Daily summaries only (v0.0) | 🆕 6 report types<br>🆕 Custom builder<br>🆕 Queue system<br>🆕 Multi-format export |
| **⚙️ Settings** | System configuration | • Organization settings<br>• Security policies<br>• Tag management<br>• AI configuration | - |
| **👁️ BOL Management** | Be-on-lookout alerts | • Multi-site distribution<br>• Real-time matching<br>• Photo support<br>• Auto-expiration | - |
| **📝 Passdowns** | Shift communication | • Activity summaries<br>• Cross-site coordination<br>• Read receipts<br>• AI drafting | - |
| **🤖 AI Assistant** | Intelligent automation | • Operational support<br>• Voice processing<br>• Basic commands | 🆕 Global availability<br>🆕 Natural language<br>🆕 Context awareness<br>🆕 Action confirmation |
| **📋 Audit Logs** | Compliance tracking | • Complete trail<br>• Activity auditing<br>• Tag operations<br>• Analytics | - |
| **🏢 Location Management** | Site administration | • Hierarchical structure<br>• Resource allocation<br>• Cross-site coordination | - |
| **🎥 Ambient.ai** | Video analytics | • GIF previews<br>• Alert creation<br>• Confidence scoring | - |
| **🚪 Lenel Access** | Door control integration | • Badge correlation<br>• Alert generation<br>• PII management | - |
| **📱 Communications** | Multi-channel messaging | • Telegram integration<br>• Voice memos<br>• N8N workflows | - |
| **🗺️ Map Visualization** | Geographic display | • Guard tracking<br>• Incident mapping<br>• Real-time updates | - |

### **4.2 v0.1 Enhancement Summary**

**🎯 Three Major Enhancements:**

1. **Case Management AI** - Transform investigations with pattern analysis, automated timelines, and intelligent suggestions
2. **Full Reporting Suite** - Replace basic daily reports with comprehensive analytics, custom builders, and scheduled distribution  
3. **Global AI Assistant** - Expand from operational-only to system-wide natural language interface

**✨ Key Benefits:**
- Faster case resolution through AI insights
- Data-driven decision making with advanced reports
- Improved productivity with natural language commands
- Maintained activity → incident → case workflow integrity

---

## **5. RBAC Preview for Activity-First System**

### **Core Permission Changes (Section 5 Preview)**

**Activity Management Permissions Matrix:**

| **Function** | **🔴 Admin** | **🟠 Supervisor** | **🟢 Officer** |
|--------------|--------------|-------------------|----------------|
| **View Activities** | ✅ All types, all locations | ✅ All types, assigned locations | ✅ All types, current location |
| **Create Activities** | ✅ All types | ✅ All types | ✅ All types |
| **Modify Activity Type** | ✅ | ✅ | ✅ (with audit log) |
| **Add Activity Tags** | ✅ Unlimited | ✅ Up to 15 tags | ✅ Up to 10 tags |
| **Remove Activity Tags** | ✅ Any tag | ✅ Own + non-routing tags | ✅ Own tags only |
| **Dismiss Auto-Incidents** | ✅ | ✅ | ❌ |
| **Delete Activities** | ✅ (soft delete) | ❌ | ❌ |
| **Link Activities to Incidents** | ✅ | ✅ | ✅ Suggest only |
| **Change Activity Status** | ✅ Any status | ✅ Any status | ✅ Limited progression |

**Key Permission Principles:**

1. **Creation Freedom**: All roles can create any activity type - the system handles urgency through auto-incident rules
2. **Modification Transparency**: Officers can modify activity types but all changes are audited
3. **Supervisor Review**: Only Supervisors+ can dismiss auto-created incidents, providing oversight
4. **No Deletion**: Only Admins can soft-delete; Officers and Supervisors cannot delete to maintain audit trail

**Tag Permission Hierarchy:**

- **System Tags** (read-only): `trigger:*`, `time:*`, `location:*`, `confidence:*`
- **Admin Tags**: Can create categories, modify any tag
- **Supervisor Tags**: Can add `priority:*`, `status:*`, cannot modify routing tags
- **Officer Tags**: Can add descriptive tags only, no routing tags

---

## **👤 5. User Roles**

### **7.1 🎭 Role Definitions**

| **Role** | **🎯 Primary Function** | **🔐 Access Level** | **🎛️ Command Center Access** |
|----------|-------------------------|---------------------|------------------------------|
| **🔴 Admin** | System administration & oversight | Full platform access | Full command center + layout configuration |
| **🟠 Supervisor** | Operational management & activity oversight | Extended operational access | Full command center (read-only layout) |
| **🟢 Officer** | Field operations & activity monitoring | Basic operational access | Simplified command center view |

### **7.2 🎛️ Command Center Role Matrix**

| **Command Center Function** | **🔴 Admin** | **🟠 Supervisor** | **🟢 Officer** |
|----------------------------|--------------|-------------------|----------------|
| **📋 Activity Stream Access** | ✅ Full control | ✅ View + acknowledge | ✅ View + acknowledge |
| **🔴 Activity Management** | ✅ All actions | ✅ Acknowledge/escalate/dismiss | ✅ Acknowledge/escalate |
| **🗺️ Map View Access** | ✅ Full map features | ✅ View guards + incidents | ✅ View current zone |
| **📍 Guard Tracking** | ✅ All guards | ✅ Assigned guards | ✅ Self + zone guards |
| **👥 Guard Coordination** | ✅ Full dispatch | ✅ Coordinate shifts | ✅ Check-in only |
| **🚪 Door Control** | ✅ Override all | ✅ Emergency override | ✅ Status view |
| **🎨 Layout Configuration** | ✅ Full customization | ❌ Preset layouts only | ❌ Preset layouts only |
| **📊 Multi-Site View** | ✅ All locations | ✅ Assigned locations | ✅ Current location |
| **🤖 AI Context Access** | ✅ Orchestr8 (full features) | ✅ Orchestr8 (operational) | ✅ Orchestr8 (basic) |
| **⚡ Emergency Protocols** | ✅ Initiate/override | ✅ Initiate assigned | ✅ Follow protocols |

### **7.3 🏢 Platform Admin Role**

**System Administration (Internal IT Use Only)**

| **Capability** | **Description** | **V0 Status** |
|----------------|-----------------|---------------|
| **Multi-tenant Management** | Organization and location hierarchy | ✅ Available |
| **Cross-Site Coordination** | Global event correlation and resource sharing | ✅ Available |
| **Infrastructure Monitoring** | System health across all locations | ✅ Available |
| **Command Center Deployment** | Deploy and configure command centers per location | ✅ Available |
| **AI Context Management** | Configure specialized AI contexts per location | ✅ Available |
| **Integration Orchestration** | Manage integrations across sites | ✅ Available |

### **7.4 📊 Detailed Permissions Matrix**

| **Function** | **🔴 Admin** | **🟠 Supervisor** | **🟢 Officer** |
|--------------|--------------|-------------------|----------------|
| **🎛️ COMMAND CENTER** | | | |
| Access Command Center | ✅ Full interface | ✅ Full interface | ✅ Simplified view |
| Configure Layouts | ✅ All layouts | ❌ Preset only | ❌ Preset only |
| Multi-Location View | ✅ All locations | ✅ Assigned locations | ✅ Current location |
| Map View Toggle | ✅ On/Off/Configure | ✅ On/Off | ✅ View only |
| Guard Tracking on Map | ✅ All guards | ✅ Assigned guards | ✅ Zone guards |
| Incident Display on Map | ✅ All incidents | ✅ All incidents | ✅ Zone incidents |
| Video Wall Control | ✅ Full control | ✅ View + basic | ✅ View only |
| **📋 ACTIVITIES** | | | |
| View Activities | ✅ All locations | ✅ Assigned locations | ✅ Current location |
| Create Activities | ✅ All types | ✅ All types | ✅ All types |
| Modify Activity Type | ✅ | ✅ | ✅ With audit log |
| Add Activity Tags | ✅ Unlimited | ✅ Up to 15 | ✅ Up to 10 |
| Remove Activity Tags | ✅ Any tag | ✅ Non-system tags | ✅ Own tags only |
| Change Activity Status | ✅ Any transition | ✅ Any transition | ✅ Forward only |
| Delete Activities | ✅ Soft delete | ❌ | ❌ |
| Dismiss Auto-Incidents | ✅ | ✅ | ❌ |
| Bulk Activity Actions | ✅ | ✅ | ❌ |
| **📋 INCIDENTS** | | | |
| View Incidents | ✅ All locations | ✅ Assigned/All locations | ✅ Current location |
| Create Incidents | ✅ | ✅ | ✅ |
| Edit Incidents | ✅ All | ✅ Assigned | ✅ Own |
| Delete Incidents | ✅ | ❌ | ❌ |
| Multi-Location Incidents | ✅ Create/manage | ✅ View/escalate | ✅ View assigned |
| **📁 CASES** | | | |
| View Cases | ✅ All locations | ✅ Assigned/All locations | ✅ Assigned |
| Create Cases | ✅ | ✅ | ❌ |
| Edit Cases | ✅ All | ✅ Assigned | ❌ |
| Close Cases | ✅ | ✅ | ❌ |
| Delete Cases | ✅ | ❌ | ❌ |
| Cross-Site Cases | ✅ Full management | ✅ Coordinate assigned | ❌ |
| **👁️ BOLs** | | | |
| View BOLs | ✅ All locations | ✅ All locations | ✅ Current location |
| Create BOLs | ✅ | ✅ | ❌ |
| Edit BOLs | ✅ All | ✅ All | ❌ |
| Multi-Location BOLs | ✅ Create/distribute | ✅ Create/distribute | ❌ |
| **📝 PASSDOWNS** | | | |
| View Passdowns | ✅ All locations | ✅ Assigned locations | ✅ Current location |
| Create Passdowns | ✅ | ✅ | ✅ |
| Edit Passdowns | ✅ All | ✅ Assigned | ✅ Own |
| Cross-Site Passdowns | ✅ All | ✅ Coordinate | ✅ Receive |
| **👥 GUARD COORDINATION** | | | |
| View Guard Status | ✅ All locations | ✅ Assigned locations | ✅ Current location |
| Dispatch Guards | ✅ All locations | ✅ Assigned locations | ❌ |
| Emergency Coordination | ✅ Cross-site | ✅ Local + escalate | ✅ Check-in |
| **📊 REPORTS** | | | |
| Generate Reports | ✅ All locations | ✅ Assigned locations | ❌ |
| Export Data | ✅ All locations | ✅ Assigned locations | ❌ |
| Cross-Site Analytics | ✅ | ✅ | ❌ |
| **🤖 AI ASSISTANCE** | | | |
| Access Orchestr8 | ✅ | ✅ | ✅ |
| AI Feature Level | Full | Operational | Basic |
| Voice Processing | ✅ | ✅ | ✅ |
| Report Generation | ✅ | ✅ | ❌ |
| AI Configuration | ✅ | ❌ | ❌ |
| **🏢 LOCATION MANAGEMENT** | | | |
| View Locations | ✅ All | ✅ Assigned | ✅ Current |
| Manage Locations | ✅ | ❌ | ❌ |
| Configure Integrations | ✅ | ❌ | ❌ |
| **📋 AUDIT LOGS** | | | |
| View Audit Logs | ✅ All locations | ❌ | ❌ |
| Export Audit Logs | ✅ All locations | ❌ | ❌ |
| Filter Audit Logs | ✅ All locations | ❌ | ❌ |
| **⚙️ ADMINISTRATION** | | | |
| User Management | ✅ All locations | ❌ | ❌ |
| System Settings | ✅ All locations | ❌ | ❌ |
| Multi-Location Config | ✅ | ❌ | ❌ |

### **7.5 🔐 Session Management**

| **Parameter** | **Value** | **Location Context** |
|---------------|-----------|----------------------|
| **Session Duration** | 8 hours active | Location context preserved |
| **Idle Timeout** | 1 hour | Warning at 55 minutes with location |
| **Concurrent Sessions** | Single session per user | Cross-location session management |
| **Re-authentication Required** | Sensitive operations | Multi-location operations require re-auth |
| **Location Switching** | Instant | Permissions recalculated per location |
| **Emergency Override** | Admin/Supervisor only | Cross-site emergency access |

## **🌐 6. Global Functional Rules**

### **6.1 🌍 Universal Behaviors**

#### **4.1.1 📝 Enhanced Audit Logging**

| **Aspect** | **Specification** | **Multi-Location Enhancement** |
|------------|-------------------|-------------------------------|
| **Logged Operations** | All CREATE, UPDATE, DELETE actions + Command Center operations | Location context and cross-site operations |
| **Log Contents** | Actor, Action, Target, Timestamp, IP Address, Before/After values | Location ID, Cross-site correlation IDs |
| **Retention Period** | Permanent retention | Per-location and global retention policies |
| **User Interface** | Admin-only audit logs page with search and export | Multi-location filtering and cross-site search |
| **Real-time Logging** | Command Center operations logged immediately | Live audit stream in Command Center |
| **Emergency Operations** | Critical operations auto-escalated | Cross-site emergency coordination tracking |

#### **4.1.2 🕐 Enhanced Timestamps**

| **Aspect** | **Specification** | **Multi-Location Enhancement** |
|------------|-------------------|-------------------------------|
| **Required Fields** | created_at, updated_at on all entities | location_timestamp, timezone_context |
| **Storage Format** | UTC timezone | UTC with location timezone metadata |
| **Display Format** | User's configured timezone | Location-aware timezone display |
| **Format Standard** | ISO 8601 (YYYY-MM-DDTHH:mm:ss.sssZ) | Enhanced with location timezone suffix |
| **Real-time Sync** | WebSocket timestamp synchronization | Cross-location time coordination |
| **Emergency Timestamps** | High-precision timestamps for critical events | Coordinated emergency response timing |

#### **4.1.3 🗑️ Enhanced Soft Deletion**

| **Aspect** | **Specification** | **Multi-Location Enhancement** |
|------------|-------------------|-------------------------------|
| **Delete Method** | Soft delete only (no hard deletes in V0) | Location-aware soft deletion |
| **Implementation** | deleted_at timestamp field | deleted_at + location_context |
| **Query Behavior** | Deleted items excluded from normal queries | Location-scoped deletion filtering |
| **Recovery** | Admin can view/restore with explicit filter | Cross-location recovery permissions |
| **Cross-Site Impact** | Deletion affects related cross-site entities | Coordinated multi-location cleanup |

#### **4.1.4 ✅ Enhanced Field Validation**

| **Validation Type** | **Rules** | **Multi-Location Enhancement** |
|---------------------|-----------|-------------------------------|
| **Execution** | Client-side AND server-side | Location-aware validation rules |
| **Required Fields** | Cannot be empty strings or whitespace | Location-specific required fields |
| **Email Format** | RFC 5322 compliant | Multi-domain organization support |
| **Phone Format** | E.164 format storage | Location-specific number formatting |
| **Location Fields** | Hierarchical location validation | Organization → Region → Site → Building |
| **Cross-Site References** | Validation for multi-location entities | Verify cross-site entity existence |
| **Activity Fields** | Type, trigger, status validation | Activity-specific validation rules |
| **Tag Format** | category:value, lowercase, no spaces | Tag category restrictions by role |

#### **4.1.5 ⚠️ Enhanced Error Handling**

| **Error Type** | **Handling Method** | **Multi-Location Enhancement** |
|----------------|---------------------|-------------------------------|
| **User Errors** | Friendly messages displayed | Location-specific error context |
| **Technical Errors** | Logged internally, generic message to user | Cross-site error correlation |
| **Validation Errors** | Inline form display | Location-aware validation messages |
| **System Errors** | Generic message with incident ID | Multi-location incident tracking |
| **Integration Errors** | Per-integration error handling | Location-specific integration status |
| **Emergency Errors** | Priority escalation and notification | Cross-site emergency protocols |

#### **4.1.6 🔍 Enhanced Search Behavior**

| **Feature** | **Specification** | **Multi-Location Enhancement** |
|-------------|-------------------|-------------------------------|
| **Case Sensitivity** | Case-insensitive by default | Location-aware case handling |
| **Matching** | Partial string matching enabled | Cross-site fuzzy matching |
| **Special Characters** | Automatically escaped | Multi-language character support |
| **Result Limit** | 100 items maximum (pagination required) | Location-scoped result limiting |
| **Cross-Site Search** | Global search across locations | Permission-based location filtering |
| **Real-time Search** | Live search in Command Center | WebSocket-powered instant results |
| **Tag Search** | Search by tag with category:value format | Tag-based activity filtering |

#### **4.1.7 📤 Enhanced Data Export**

| **Feature** | **Specification** | **Multi-Location Enhancement** |
|-------------|-------------------|-------------------------------|
| **Availability** | All list views | Location-scoped export permissions |
| **Filter Respect** | Exports honor current filters | Location and cross-site filtering |
| **Column Selection** | Visible columns only | Location-specific column visibility |
| **Row Limit** | Maximum 10,000 rows per export | Per-location and aggregate limits |
| **Cross-Site Export** | Multi-location data consolidation | Unified cross-site reporting |
| **Real-time Export** | Live data export from Command Center | Current operational state export |

#### **4.1.8 🤖 Enhanced AI Interaction Rules**

| **Rule** | **Implementation** | **Multi-Location Enhancement** |
|----------|-------------------|-------------------------------|
| **Context Isolation** | Each user has isolated AI sessions per context | Location-aware AI context switching |
| **Context Retention** | Last 10 messages per session | Location history preservation |
| **Action Confirmation** | Required for all data modifications | Cross-site operation confirmation |
| **Rate Limiting** | 100/hour Officers, 200/hour Supervisors, unlimited Admin | Location-based rate limiting |
| **Permission Inheritance** | AI actions limited by user's role permissions | Location permission enforcement |
| **Single Context Access** | Orchestr8 (Operational AI only in MVP) | Future: additional contexts |
| **Cross-Site Correlation** | AI analysis across multiple locations | Global pattern recognition |
| **Emergency AI Priority** | Priority processing during emergencies | Cross-site emergency coordination |

#### **4.1.9 🏢 Location Management Rules**

| **Rule** | **Implementation** | **Purpose** |
|----------|-------------------|-------------|
| **Hierarchical Structure** | Organization → Region → Site → Building → Zone → Asset | Logical organization structure |
| **Permission Inheritance** | Permissions flow down hierarchy | Simplified access management |
| **Location Switching** | Users can switch context between assigned locations | Operational flexibility |
| **Cross-Site Operations** | Specific permissions for multi-location operations | Coordinated security response |
| **Emergency Protocols** | Override permissions during emergencies | Crisis management capability |
| **Resource Sharing** | Coordinated resource allocation across sites | Mutual aid and support |

#### **4.1.10 🔄 Real-Time Operation Rules**

| **Rule** | **Implementation** | **Purpose** |
|----------|-------------------|-------------|
| **WebSocket Connections** | Persistent connections for real-time updates | Live operational awareness |
| **Event Prioritization** | Critical events bypass normal queuing | Emergency response capability |
| **Cross-Site Synchronization** | Events synchronized across all relevant locations | Coordinated situational awareness |
| **Failover Handling** | Automatic failover to backup systems | System reliability |
| **Rate Limiting** | Real-time event throttling per user role | Performance management |
| **Session Management** | Real-time session validation | Security and access control |

#### **4.1.11 📋 Activity Processing Rules**

| **Rule Category** | **Implementation** | **Details** |
|-------------------|-------------------|-------------|
| **Activity Types** | Enum validation | `patrol`, `alert`, `medical`, `security-breach`, `property-damage`, `bol-event`, `evidence` |
| **Trigger Types** | Binary validation | `human` or `integration` only |
| **Status Flow** | State machine | `detecting` → `responding` → `investigating` → `resolved` |
| **Tag Format** | Regex validation | `^[a-z0-9-]+:[a-z0-9-]+$` (category:value) |
| **Auto-Incident Rules** | Type-based logic | See detailed rules in section 4.1.11.1 |
| **Archive Policy** | Time-based | TBD: 14-30 days in active database |
| **Confidence Scores** | Integer 0-100 | Required for integration triggers |

##### **4.1.11.1 Auto-Incident Creation Rules**

```javascript
// Auto-Incident Decision Engine
const AUTO_INCIDENT_RULES = {
  // Always create incident
  'medical': { 
    create: 'always', 
    dismissible: false,
    priority: 'critical' 
  },
  'security-breach': { 
    create: 'always', 
    dismissible: true,
    priority: 'high' 
  },
  'bol-event': { 
    create: 'always', 
    dismissible: false,
    priority: 'high' 
  },
  
  // Conditional creation
  'alert': { 
    create: 'conditional',
    conditions: [
      { field: 'confidence', operator: '>', value: 80 },
      { field: 'tags', contains: 'time:after-hours' }
    ],
    dismissible: true,
    priority: 'medium' 
  },
  'property-damage': { 
    create: 'conditional',
    conditions: [
      { field: 'confidence', operator: '>', value: 75 }
    ],
    dismissible: true,
    priority: 'medium' 
  },
  
  // Never create incident
  'patrol': { 
    create: 'never' 
  },
  'evidence': { 
    create: 'never' 
  }
};
```

### **6.2 🔗 Enhanced Linking Rules**

#### **4.2.1 Enhanced Entity Relationships**

| **Relationship** | **Rule** | **Multi-Location Enhancement** |
|------------------|----------|-------------------------------|
| **Activities → Incidents** | Activities can exist without incidents | Cross-location activity grouping |
| **Incidents → Cases** | Incidents can exist without cases | Multi-location case coordination |
| **Activities → Cases** | Only through incidents (except evidence type) | Evidence can link directly to cases |
| **BOLs → Activities** | BOL creates activity of type `bol-event` | Cross-site BOL activity distribution |
| **Passdowns → Multiple** | Passdowns can reference activities/incidents/cases | Multi-location passdown coordination |
| **AI Sessions → User** | One user can have many AI sessions | Location-aware AI context sessions |
| **AI Actions → Entities** | AI actions create audit trails on all affected entities | Cross-site AI operation tracking |
| **Locations → All Entities** | All entities have location context | Hierarchical location relationships |
| **Guards → Locations** | Guards assigned to specific locations | Cross-site guard coordination |
| **Integrations → Locations** | Integration configurations per location | Location-specific system integration |

#### **4.2.2 Enhanced Cascade Rules**

| **Action** | **Effect** | **Multi-Location Impact** |
|------------|------------|--------------------------|
| **Delete Case** | Does NOT delete linked incidents | Preserves cross-location incident references |
| **Delete Incident** | Does NOT delete activities | Activities retain history |
| **Archive Activity** | Removes from active views | Historical data preserved |
| **Deactivate User** | Requires reassignment of owned items, terminates AI sessions | Cross-location ownership transfer |
| **Deactivate Location** | Requires entity migration to active location | Coordinated location shutdown |
| **Emergency Override** | Temporarily bypasses normal cascade rules | Crisis management flexibility |

#### **4.2.3 Enhanced Status Transitions**

| **Rule** | **Implementation** | **Multi-Location Enhancement** |
|----------|-------------------|-------------------------------|
| **Automation** | Workflow engine automates specific transitions | Cross-site workflow coordination |
| **Logging** | All transitions create audit log | Location-aware transition tracking |
| **Restrictions** | Some transitions restricted by role | Location-specific transition permissions |
| **Cross-Site Sync** | Status changes synchronized across locations | Coordinated state management |
| **Emergency Escalation** | Automated escalation during emergencies | Cross-site emergency coordination |
| **Real-time Updates** | Status changes pushed via WebSocket | Live operational state updates |

### **6.3 🏔️ Activity Filtering Rules**

#### **4.3.1 Iceberg Filtering Engine**

| **Rule Category** | **Implementation** | **Purpose** |
|-------------------|-------------------|-------------|
| **Visibility Scoring** | Algorithm assigns 0-100 score to each activity | Surface only relevant activities |
| **Role-Based Thresholds** | Officers: 70+, Supervisors: 50+, Admins: 0+ | Progressive information access |
| **Dynamic Adjustments** | Scores adjust based on age, status, confidence | Keep view current and relevant |
| **Override Capability** | Users can drill down to see hidden activities | Maintain full audit trail |
| **Performance Optimization** | Filter at query level, not UI level | Efficient database operations |

#### **4.3.2 Activity Prioritization Matrix**

| **Activity Type** | **Base Score** | **Modifiers** | **Typical Visibility** |
|-------------------|----------------|---------------|------------------------|
| medical | 100 | None | Always visible |
| security-breach | 95 | +5 if multiple locations | Always visible |
| bol-event | 90 | +10 if recent sighting | Always visible |
| alert | 50 | +20 if confidence >80%, +15 if after-hours | Conditional |
| property-damage | 40 | +20 if high value, -20 if resolved | Conditional |
| patrol | 10 | +10 if anomaly detected, -5 if completed | Usually hidden |
| evidence | 5 | +50 if linked to active case | Usually hidden |

### **6.4 📍 Location Data Requirements**

#### **4.4.1 Location Fields for Activities**

| **Field** | **Required** | **Format** | **Usage** |
|-----------|--------------|------------|-----------|
| location_id | Yes | UUID | Primary location reference |
| building | Yes | String | Building identifier |
| floor | Conditional | String | Required for indoor activities |
| zone | Yes | String | Security zone designation |
| coordinates | Conditional | {lat, lng} | For map display, GPS activities |
| landmark | Optional | String | Additional reference point |
| accuracy | Conditional | Number (meters) | GPS accuracy indicator |

#### **4.4.2 Guard Location Tracking**

| **Requirement** | **Specification** | **Privacy Consideration** |
|-----------------|-------------------|---------------------------|
| **Update Frequency** | 30 seconds when on duty | No tracking during breaks |
| **Location Source** | GPS, WiFi triangulation, manual check-in | User can select privacy mode |
| **Data Retention** | Last 100 positions per guard | Older data aggregated |
| **Map Display** | Real-time position with status | Show last known if signal lost |
| **Incident Assignment** | Auto-suggest nearest available guard | Consider zone assignments |

#### **4.4.3 Integration Location Data**

| **Integration** | **Location Data Provided** | **Mapping Required** |
|-----------------|---------------------------|---------------------|
| Ambient.ai | Camera location → zone/building | Camera ID to location mapping |
| Lenel | Door location → exact position | Door ID to coordinates |
| Telegram | User's assigned location | User ID to location |
| Sensors | Pre-configured positions | Sensor ID to location |

## **📄 7. Page-Level Functional Specifications**

### **7.1 📋 Activity Management**

**🎯 Purpose**: Central system for all security event capture, processing, and intelligent routing through the Activity-first architecture

#### **7.1.1 🏗️ Activity System Architecture**

**Entry Points**
- **Primary:** Command Center Activity Stream (real-time)
- **Secondary:** /activities dedicated page
- **Direct:** /activities/[ACTIVITY_ID] from notifications
- **Cross-Reference:** From incident/case activity links
- **Emergency:** Emergency mode activity prioritization
- **API:** WebSocket real-time activity subscriptions

#### **7.1.2 📡 Enhanced Activity Processing**

**Activity Creation Sources**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          ACTIVITY INPUT SOURCES                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ HUMAN TRIGGERS                        │ INTEGRATION TRIGGERS                │
├───────────────────────────────────────┼─────────────────────────────────────┤
│ 📻 Radio Communications               │ 🎥 Ambient.ai (Video Analytics)     │
│    └─ Speech-to-text via N8N         │    └─ Weapon/Person/Vehicle detect  │
│ 📱 Manual UI Entry                    │ 🚪 Lenel (Access Control)           │
│    └─ Web/Mobile forms               │    └─ Door forced/held/tailgate     │
│ 💬 Telegram (Backup)                  │ 🔊 Sensors (Environmental)          │
│    └─ Temporary radio substitute     │    └─ Glass break/motion/fire       │
│                                       │ 🌡️ HVAC/Fire Systems                │
│                                       │    └─ Temperature/smoke alerts      │
└─────────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ACTIVITY PROCESSING ENGINE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Create Activity Entity                                                   │
│ 2. Auto-tagging (location, time, trigger)                                  │
│ 3. AI Type Detection (if not specified)                                    │
│ 4. Auto-Incident Rule Evaluation                                           │
│ 5. Route to Command Center / Notifications                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.1.3 📊 Enhanced Activity Interface**

**Activity List View**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              ACTIVITY MANAGEMENT                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Filters: [All Types ▼] [All Triggers ▼] [All Statuses ▼] [Today ▼]        │
│ Search: [🔍 Search by tags, title, description...]          [+ Create New]  │
├─────────────────────────────────────────────────────────────────────────────┤
│ □ │ ID          │ Type     │ Title                │ Status      │ Actions  │
├───┼─────────────┼──────────┼──────────────────────┼─────────────┼──────────┤
│ □ │ ACT-2024-   │ 🚨Medical│ Person unconscious   │ Responding  │ [👁️][✏️] │
│   │ 0234        │          │ Building A           │ → INC-0089  │ [🔗][🏷️] │
├───┼─────────────┼──────────┼──────────────────────┼─────────────┼──────────┤
│ □ │ ACT-2024-   │ 🔍Patrol │ Sector 3 complete    │ Resolved    │ [👁️][✏️] │
│   │ 0233        │          │ All clear            │ No incident │ [📋][🏷️] │
├───┼─────────────┼──────────┼──────────────────────┼─────────────┼──────────┤
│ □ │ ACT-2024-   │ ⚠️Alert  │ Door forced B-12     │ Detecting   │ [👁️][✏️] │
│   │ 0232        │          │ Confidence: 89%      │ Evaluating  │ [🚨][🏷️] │
└───┴─────────────┴──────────┴──────────────────────┴─────────────┴──────────┘
│ Showing 1-20 of 234 activities         [← Previous] [1] 2 3 ... 12 [Next →] │
│ Bulk Actions: [🏷️ Tag Selected] [🚨 Create Incident] [📤 Export]           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Column Specifications**

| **Column** | **Description** | **Sortable** | **Searchable** |
|------------|-----------------|--------------|----------------|
| **ID** | Unique activity identifier | ✅ | ✅ |
| **Type** | Activity type with icon | ✅ | ✅ |
| **Title** | Brief activity summary | ✅ | ✅ |
| **Status** | Current activity status | ✅ | ✅ |
| **Location** | Hierarchical location | ✅ | ✅ |
| **Created** | Timestamp with timezone | ✅ | ✅ |
| **Trigger** | Human/Integration | ✅ | ✅ |
| **Tags** | All applied tags | ❌ | ✅ |

#### **7.1.4 📋 Activity Cards**

**Standard Activity Card**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 ACTIVITY: ACT-2024-0234                          Status: RESPONDING      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Type: 🚨 Medical Emergency          Trigger: Human (Radio)                  │
│ Title: Person unconscious - Building A                                      │
│ Created: 2024-01-15 14:23:15 PST   By: Officer Johnson                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Description:                                                                │
│ "Caller reports person collapsed in Building A lobby. Not breathing,        │
│ starting CPR. Need paramedics immediately."                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Location: Site A → Building A → Floor 1 → Lobby                            │
│ GPS: 37.4419° N, 122.1430° W                                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Tags: [trigger:human] [location:building-a] [time:business-hours]          │
│       [priority:critical] [dept:medical] [weather:clear]                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Auto-Incident: ✅ Created INC-2024-0089 (Medical always creates incident)  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Related Activities: ACT-0235 (CPR started), ACT-0238 (Area cleared)        │
│ Assigned To: Officer Garcia     Response Time: 1.8 minutes                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Actions: [Update Status] [Add Evidence] [Link Activity] [View Incident]    │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Integration Activity Card**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ 📋 ACTIVITY: ACT-2024-0245                          Status: DETECTING       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Type: ⚠️ Alert                      Trigger: Integration (Ambient.ai)       │
│ Title: Tailgating detected - Main entrance                                 │
│ Created: 2024-01-15 14:25:32 PST   Confidence: 86%                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ AI Analysis:                                                                │
│ • 2 people detected, only 1 badge scan                                     │
│ • Behavior anomaly confidence: 86%                                         │
│ • Camera: CAM-MAIN-01                                                      │
│ • Video clip available                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🎥 [View Video Clip] 📸 [View Snapshot] 🔍 [Enhance Analysis]              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Tags: [trigger:integration] [integration_type:ambient_ai]                   │
│       [location:main-entrance] [time:after-hours] [confidence:86]          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Auto-Incident: ⏳ Evaluating... (86% > 80% threshold + after-hours)        │
│ Decision in: 3 seconds                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🤖 Orchestr8: "Tailgating after hours suggests unauthorized access attempt. │
│               Recommend immediate guard dispatch to main entrance."          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Actions: [Force Incident] [Dismiss] [Assign Guard] [Update Confidence]     │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.1.5 🔄 Enhanced Activity Workflow**

**Activity Status Progression**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ACTIVITY STATUS WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  DETECTING ──────> RESPONDING ──────> INVESTIGATING ──────> RESOLVED       │
│      │                  │                    │                   │          │
│      │                  │                    └───────────────────┘          │
│      │                  └────────────────────────────────────────┘          │
│      └───────────────────────────────────────────────────────────────┘          │
│                                                                             │
│  Status Rules:                                                              │
│  • Forward progression only for Officers                                    │
│  • Supervisors/Admins can move backwards                                   │
│  • Some types skip stages (patrol: detecting → resolved)                   │
│  • Evidence type created in 'resolved' status                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Status Transition Matrix**

| **From Status** | **To Status** | **Allowed By** | **Conditions** |
|-----------------|---------------|----------------|----------------|
| detecting | responding | All roles | Activity acknowledged |
| detecting | resolved | All roles | No response needed |
| responding | investigating | All roles | Detailed review needed |
| responding | resolved | All roles | Response complete |
| investigating | resolved | All roles | Investigation complete |
| resolved | any | Admin/Supervisor | Reopening with reason |

#### **7.1.6 🏔️ Activity Filtering - Iceberg Approach**

**Core Philosophy**
- **Problem**: Too many activities flooding the system (access grants, routine patrols, resolved items)
- **Solution**: Surface only the top 10% of activities that need attention
- **Metaphor**: Like an iceberg - most activities stay below the surface, critical ones rise to the top

**Activity Visibility Rules by Role**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ACTIVITY ICEBERG VISUALIZATION                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   VISIBLE LAYER (Top 10%)                                                   │
│   ═══════════════════════                                                   │
│   🚨 Critical Activities    │ • Medical emergencies                         │
│   ⚠️  High Priority         │ • Security breaches                          │
│   🔔 Alerts Needing Action  │ • BOL events                                │
│                             │ • High-confidence alerts                      │
│   ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─           │
│                                                                             │
│   HIDDEN LAYER (Bottom 90%)                                                 │
│   ─────────────────────────                                                 │
│   📋 Routine Activities     │ • Completed patrols                          │
│   ✅ Resolved Items         │ • Access grants                             │
│   📊 Low Priority           │ • Resolved activities                       │
│                             │ • Low-confidence alerts                      │
│                                                                             │
│   [Show Hidden Activities]  │ Available on demand                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Filtering Rules by Role**

| **Role** | **Default View** | **Hidden Activities** | **Override Capability** |
|----------|------------------|-----------------------|-------------------------|
| **Officer** | Critical in their zone only | All routine/resolved | Can view own activities |
| **Supervisor** | All critical across zones | Routine patrols, resolved | Full drill-down access |
| **Admin** | Everything configurable | None (sees all) | Can modify filter rules |

**Activity Scoring Algorithm**

```javascript
// Activity visibility scoring (0-100)
function calculateActivityScore(activity) {
  let score = 0;
  
  // Type-based scoring
  const typeScores = {
    'medical': 100,           // Always visible
    'security-breach': 95,    // Always visible
    'bol-event': 90,         // Always visible
    'alert': 50,             // Conditional
    'property-damage': 40,   // Conditional
    'patrol': 10,            // Usually hidden
    'evidence': 5            // Usually hidden
  };
  
  score += typeScores[activity.type] || 0;
  
  // Modifiers
  if (activity.confidence > 80) score += 20;
  if (activity.tags.includes('time:after-hours')) score += 15;
  if (activity.status === 'detecting') score += 10;
  if (activity.status === 'resolved') score -= 30;
  if (activity.age > '24h') score -= 20;
  
  return Math.min(100, Math.max(0, score));
}

// Only show activities with score > threshold
const VISIBILITY_THRESHOLD = {
  officer: 70,      // Only high-priority items
  supervisor: 50,   // Medium and high priority
  admin: 0          // Everything
};
```

**Dynamic Filtering Controls**

```
Activity Filter Panel:
┌─────────────────────────────────────────────────────────────────────────┐
│ Quick Filters:  [🔴 Critical Only] [⚠️ Needs Action] [📍 My Zone]      │
│                                                                         │
│ Advanced:       Confidence: [>70% ▼]  Age: [<24h ▼]  Type: [All ▼]   │
│                                                                         │
│ Visibility:     ○ Smart Filter (Recommended)                           │
│                 ○ Show All Activities                                   │
│                 ● Custom Rules ────→ [Configure]                        │
└─────────────────────────────────────────────────────────────────────────┘
```

#### **7.1.7 ➕ Manual Activity Creation**

**Activity Creation Form**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CREATE NEW ACTIVITY                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Activity Type*    [Select Type ▼]                                          │
│                   ○ patrol - Routine security check                        │
│                   ○ alert - Security notification                          │
│                   ● medical - Medical emergency                            │
│                   ○ security-breach - Unauthorized access                  │
│                   ○ property-damage - Damage report                        │
│                   ○ bol-event - Be-on-lookout                             │
│                   ○ evidence - Supporting documentation                    │
│                                                                             │
│ ⚠️ Medical activities automatically create incidents                        │
│                                                                             │
│ Title*           [Person unconscious in Building A_____________________]   │
│                  0/100 characters                                           │
│                                                                             │
│ Description*     ┌─────────────────────────────────────────────────────┐   │
│                  │ Found person collapsed in Building A lobby.          │   │
│                  │ Not responsive. Starting CPR. Called paramedics.     │   │
│                  │                                                      │   │
│                  └─────────────────────────────────────────────────────┘   │
│                  45/5000 characters                                         │
│                                                                             │
│ Location*        [Site A ▼] [Building A ▼] [Floor 1 ▼] [Lobby ▼]          │
│                  📍 Use Current Location                                    │
│                                                                             │
│ Tags             [weather:clear] [shift:day] [+ Add tag]                   │
│                  Auto-tags: trigger:human, location:building-a,            │
│                             time:business-hours                             │
│                                                                             │
│ Evidence         [📎 Attach Files] [📷 Take Photo] [🎥 Add Video]          │
│                  Supported: JPG, PNG, PDF, MP4 (max 50MB)                  │
│                                                                             │
│ 🤖 Orchestr8: "Medical emergency will create high-priority incident and     │
│                dispatch nearest available guard automatically."              │
│                                                                             │
│ [Create Activity] [Create & Add Another] [Cancel]                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.1.7 🔌 Integration Activity Processing**

**Integration Configuration**

| **Integration** | **Activity Types** | **Confidence Calculation** | **Auto-Incident Threshold** |
|-----------------|-------------------|----------------------------|----------------------------|
| **Ambient.ai** | alert, security-breach | AI model confidence | >80% or after-hours |
| **Lenel** | alert, security-breach | 100% forced, 90% held | After-hours always |
| **Sensors** | alert, property-damage | Sensor-specific | >75% confidence |
| **Fire/HVAC** | alert, property-damage | Severity-based | Critical always |

**Integration Webhook Format**
```json
{
  "source": "ambient_ai",
  "timestamp": "2024-01-15T14:25:32Z",
  "location": {
    "camera_id": "CAM-MAIN-01",
    "zone": "main-entrance",
    "building": "A",
    "site": "headquarters"
  },
  "detection": {
    "type": "tailgating",
    "confidence": 86,
    "people_count": 2,
    "badge_scans": 1
  },
  "media": {
    "snapshot": "https://storage/snap_2024_4823.jpg",
    "video_clip": "https://storage/clip_2024_4823.mp4"
  }
}
```

#### **7.1.8 🏷️ Tag Management Interface**

**Tag Administration (Admin/Supervisor)**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            TAG MANAGEMENT                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ System Tags (Read-Only)              │ Custom Tags (Editable)              │
├──────────────────────────────────────┼─────────────────────────────────────┤
│ trigger:human                        │ dept:security (12 uses)            │
│ trigger:integration                  │ dept:facilities (8 uses)           │
│ time:business-hours                  │ dept:medical (3 uses)              │
│ time:after-hours                     │ weather:rain (45 uses)             │
│ location:* (auto-generated)          │ weather:clear (123 uses)           │
│ confidence:* (integration only)      │ event:concert (5 uses)             │
│ integration_type:* (system)          │ shift:day (234 uses)               │
│                                      │ shift:night (189 uses)             │
│                                      │                                     │
│                                      │ [+ Create New Tag Category]         │
└──────────────────────────────────────┴─────────────────────────────────────┘
│ Tag Rules:                                                                  │
│ • Format: category:value (lowercase, no spaces)                            │
│ • Officers: 10 tags max    • Supervisors: 15 tags max    • Admin: Unlimited│
│ • System tags cannot be modified or deleted                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.1.9 📊 Activity Analytics Dashboard**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ACTIVITY ANALYTICS - REAL TIME                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Last 24 Hours: 312 Activities    Auto-Incidents: 18    Manual: 247         │
├─────────────────────────────────────────────────────────────────────────────┤
│ BY TYPE                          │ BY STATUS                                │
│ ┌─────────────────────────────┐ │ ┌─────────────────────────────────────┐ │
│ │ Patrol      61% ████████    │ │ │ Resolved     78% ██████████         │ │
│ │ Alert       19% ███         │ │ │ Responding   12% ██                 │ │
│ │ Evidence     9% █           │ │ │ Investigating 7% █                  │ │
│ │ Property     5% █           │ │ │ Detecting     3% █                  │ │
│ │ Security     3% █           │ │ └─────────────────────────────────────┘ │
│ │ Medical      1% │           │ │                                           │
│ │ BOL          1% │           │ │ RESPONSE TIMES                          │
│ └─────────────────────────────┘ │ • Average: 3.2 minutes                  │
│                                  │ • Medical: 1.8 minutes                  │
│ TOP LOCATIONS                    │ • Security: 2.4 minutes                 │
│ • Building A: 134 activities     │ • Patrol: N/A                           │
│ • Building B: 98 activities      │                                         │
│ • Parking: 56 activities         │ AUTO-INCIDENT EFFECTIVENESS             │
│                                  │ • True Positives: 89%                  │
│ TOP TAGS                         │ • Dismissed: 11% (2 incidents)         │
│ #after-hours (67)                │ • Escalation Rate: 34%                 │
│ #weather:rain (45)               │                                         │
│ #shift:night (38)                │ [📊 Detailed Analytics] [📤 Export]     │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Activity Management**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | Yes - Activities are root entities, no parent required | [Activity System Architecture](#721-activity-system-architecture) |
| **Cardinality** | One activity can link to 0 or 1 incident | [Enhanced Activity Workflow](#725-enhanced-activity-workflow) |
| **Editable After Creation?** | Type and tags editable with audit, status forward-only for Officers | [Activity Cards](#724-activity-cards) |
| **Deletion/Archival Effects** | Soft delete only, archived after 14-30 days (TBD) | [Activity Processing Rules](#4111-activity-processing-rules) |
| **Mandatory Before Close?** | Status must be 'resolved' before archival | [Status Progression](#725-enhanced-activity-workflow) |
| **Audit-Trail Requirement?** | All activity changes logged including auto-incident decisions | [Enhanced Audit Logging](#411-enhanced-audit-logging) |
| **Edge-Case Handling** | Offline activity queueing, confidence threshold validation, tag limits enforced | [Integration Processing](#727-integration-activity-processing) |

**✔️ Logic Cross-check**: Activity Management serves as the foundation for all security events, with intelligent routing, comprehensive tagging, and seamless incident creation while maintaining full audit trails.

### **7.2 📋 Incident Management**

**🎯 Purpose**: Create, track, and coordinate security incidents as grouped collections of related activities requiring response

#### **7.2.1 🎛️ Command Center Integration**

**Real-Time Incident Coordination**
- Incidents appear in Command Center's operational tracking panel
- Auto-creation from activity rules with immediate notification
- Cross-site incident coordination and resource dispatch
- Real-time status updates across all locations
- Emergency incident protocols with Command Center override

**Incident Creation Workflows**

| **Creation Method** | **Integration** | **Multi-Location Support** |
|--------------------|-----------------|-----------------------------|
| **Auto-Created** | From activity rules (medical, security-breach, etc.) | Location inherited from activity |
| **Manual Grouping** | Select multiple related activities | Can span locations if justified |
| **Guard Report** | Mobile incident creation with activity link | GPS location validation |
| **Cross-Site Escalation** | Incident escalated from another location | Multi-site coordination protocols |
| **AI Recommendation** | Buddy/Oracle suggested incident creation | Pattern-based multi-site incidents |

#### **7.2.2 📍 Enhanced Multi-Location Architecture**

**Location-Aware Incident Structure**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       MULTI-LOCATION INCIDENT MATRIX                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ PRIMARY LOCATION     │ RELATED LOCATIONS      │ COORDINATION STATUS         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🏢 Site A-B1         │ 🏢 Site B-C2 (Related) │ ✅ Cross-site coordination  │
│ ├─ Main Incident     │ ├─ Supporting Response │ ├─ Guard Unit 7 (Site A)    │
│ ├─ Guard Unit 7      │ ├─ Resource Backup     │ ├─ Guard Unit 12 (Site B)   │
│ └─ Command Center    │ └─ Monitoring Support  │ └─ Shared video access      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🤖 AI COORDINATION: Oracle identified pattern across locations              │
│ 📞 COMMUNICATION: Cross-site teams coordinated via Everbridge              │
│ 🎥 VIDEO: Multi-location camera access shared                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Enhanced Location Fields**

| **Field** | **Enhancement** | **Multi-Location Support** |
|-----------|----------------|-----------------------------|
| **Primary Location** | Inherited from first activity | Required field with validation |
| **Related Locations** | Multi-select for cross-site incidents | Optional with coordination protocols |
| **GPS Coordinates** | From activity location data | Validation against known locations |
| **Location Context** | Business hours, security level, access restrictions | Location-specific incident procedures |
| **Cross-Site Impact** | Assessment of incident effects on other locations | Automated notification protocols |

#### **7.2.3 📊 Enhanced Incident Management Interface**

**Command Center Incident Panel**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ACTIVE INCIDENT TRACKING                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔴 CRITICAL INC-2024-0089 │ Medical Emergency B-A │ Activities: 4 │ 00:15  │
│ ├─ Auto-created from: ACT-2024-0234 (Person unconscious)                   │
│ ├─ Guard Unit 7 Responding │ ETA: 0:30 │ Paramedics: En route             │
│ └─ Latest Activity: "CPR in progress" (30 seconds ago)                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🟠 HIGH INC-2024-0090     │ Multi-Door Alerts B │ Activities: 3 │ 00:08    │
│ ├─ Manually grouped: Suspicious pattern detected                            │
│ ├─ Guard Unit 12 Investigating │ Supervisor notified                       │
│ └─ Latest Activity: "Checking all access points" (2 min ago)              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🟡 MEDIUM INC-2024-0088   │ BOL Match - Parking │ Activities: 2 │ 00:32    │
│ ├─ Auto-created from: ACT-2024-0231 (BOL event always creates incident)   │
│ ├─ Subject left premises │ License plate recorded                         │
│ └─ Status: Ready to close │ Awaiting supervisor review                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Enhanced Incident List View**

| **Column** | **Enhancement** | **Multi-Location Feature** |
|------------|----------------|-----------------------------|
| **🆔 ID** | Auto-generated with location prefix (A-2024-XXXX) | Location-aware ID generation |
| **📌 Title** | Generated from primary activity + enhancements | Location-specific templates |
| **🏢 Location** | Primary location display | Cross-site indicators |
| **🚦 Status** | Real-time status with activity count | Activity-driven progression |
| **⚡ Priority** | Inherited from activity type/priority | Location-based escalation |
| **👥 Response** | Assigned personnel and resources | Cross-site coordination |
| **📋 Activities** | Count and status breakdown | Expandable activity list |
| **⏱️ Duration** | Time since creation | Response time tracking |

#### **7.2.4 ➕ Enhanced Incident Creation**

**Auto-Creation from Activity**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AUTO-INCIDENT CREATION NOTIFICATION                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ ⚡ Incident Auto-Created: INC-2024-0089                                     │
│                                                                             │
│ Triggered By: ACT-2024-0234 (Medical Emergency)                            │
│ Rule: Medical activities always create incidents                           │
│ Priority: CRITICAL                                                          │
│ Location: Site A → Building A → Floor 1                                    │
│                                                                             │
│ Automatic Actions Taken:                                                    │
│ ✅ Guard Unit 7 dispatched (nearest available)                             │
│ ✅ Paramedics notified via Everbridge                                      │
│ ✅ Building A elevators held at ground floor                               │
│ ✅ Supervisor Martinez notified                                             │
│ ✅ Command Center alert activated                                           │
│                                                                             │
│ Your Role: PRIMARY RESPONDER                                               │
│                                                                             │
│ [View Incident] [Acknowledge] [Add Update]                                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Manual Activity Grouping**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CREATE INCIDENT FROM ACTIVITIES                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Select Related Activities:                                                  │
│                                                                             │
│ ☑ ACT-2024-0230 │ 14:19 │ Door forced - B-12    │ alert    │ Site B      │
│ ☑ ACT-2024-0232 │ 14:19 │ Motion detected - B-12│ alert    │ Site B      │
│ ☑ ACT-2024-0235 │ 14:20 │ Glass break - B-12    │ property │ Site B      │
│ ☐ ACT-2024-0233 │ 14:21 │ Patrol complete - A-3 │ patrol   │ Site A      │
│                           └─ Different location and type                    │
│                                                                             │
│ 🤖 Orchestr8: "3 activities at Building B-12 within 60 seconds suggest      │
│               coordinated breach attempt. Recommend HIGH priority."          │
│                                                                             │
│ Incident Title: [Suspected breach attempt - Building B-12_______________]  │
│                                                                             │
│ Priority: [HIGH ▼]           Type: [Security ▼]                           │
│                                                                             │
│ Justification*: [Multiple sensors triggered simultaneously at B-12,        │
│                  pattern suggests forced entry attempt_________________]    │
│                                                                             │
│ Initial Response:                                                           │
│ ☑ Dispatch nearest guard    ☑ Lock adjacent areas                        │
│ ☑ Notify supervisor         ☐ Contact law enforcement                    │
│                                                                             │
│ [Create Incident] [Cancel]                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.2.5 🔍 Enhanced Incident Detail View**

**Incident Dashboard with Activity Timeline**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ INCIDENT: INC-2024-0089 - Medical Emergency Building A                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Status: RESPONDING      Priority: CRITICAL      Created: Auto (Medical)     │
│ Assigned: Garcia, L.    Location: Building A    Duration: 00:24:35         │
├─────────────────────────────────────────────────────────────────────────────┤
│                          ACTIVITY TIMELINE                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 14:23:15 │ ACT-0234 │ 🚨 MEDICAL    │ "Person unconscious Floor 1"        │
│          │ trigger:human │ status:responding │ Created this incident       │
│          │ Officer Johnson via radio │ Auto-dispatch triggered             │
├─────────────────────────────────────────────────────────────────────────────┤
│ 14:23:47 │ ACT-0235 │ 🚨 MEDICAL    │ "Starting CPR"                     │
│          │ trigger:human │ status:responding │ Auto-linked                 │
│          │ Officer Johnson via radio │ Confidence: High                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 14:25:32 │ ACT-0238 │ 📎 EVIDENCE   │ "Floor 1 cleared for paramedics"  │
│          │ trigger:human │ status:resolved │ Manually linked              │
│          │ Officer Smith via UI │ Photo attached                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 14:28:19 │ ACT-0241 │ 🚨 MEDICAL    │ "Paramedics on scene"              │
│          │ trigger:human │ status:responding │ Auto-linked                 │
│          │ Officer Garcia via radio │ EMS taking over                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ [+ Add Activity] [Link Existing] [Create Evidence] [Update Status]         │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Incident Information Panel**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           INCIDENT INFORMATION                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Response Team:                      │ Resources Deployed:                   │
│ • Lead: Officer Garcia              │ • Guard Units: 7, 9                  │
│ • Support: Officer Smith            │ • Vehicles: SEC-03                   │
│ • Supervisor: Martinez (remote)     │ • Equipment: First aid kit #3        │
│ • External: City Paramedics         │ • Access: Elevators held             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Timeline:                           │ Communications:                       │
│ • Created: 14:23:15                 │ • Radio Channel: Emergency           │
│ • First Response: 14:23:47 (32s)    │ • Everbridge: Sent to 15 contacts    │
│ • On Scene: 14:24:45 (1m30s)        │ • Updates: Every 2 minutes           │
│ • EMS Arrival: 14:28:19 (5m04s)     │ • External: 911 called               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🤖 AI Assistance:                                                          │
│ Buddy: "Medical response within target time. Suggest preparing incident    │
│         report for OSHA compliance and scheduling debrief."                │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.2.6 🔄 Enhanced Incident Workflow**

**Activity-Driven Status Management**

| **Status** | **Triggered By** | **Required Activities** | **Available Actions** |
|------------|------------------|------------------------|----------------------|
| **New** | First activity linked | Min 1 activity in any status | Assign, acknowledge |
| **Assigned** | Personnel assigned | Activity acknowledgment | Update, add activities |
| **Responding** | Active response | Min 1 activity in 'responding' | Coordinate, escalate |
| **Investigating** | Detailed review | Activities being investigated | Add evidence, analyze |
| **Resolved** | All activities complete | All activities resolved | Close, create case |
| **Closed** | Final documentation | Resolution notes added | Reopen (with reason) |

**Cross-Activity Coordination**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ACTIVITY COORDINATION PANEL                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Add Activities to This Incident:                                           │
│                                                                             │
│ Recent Unlinked Activities:                                                │
│ ○ ACT-2024-0242 │ Evidence  │ "Medical kit used" │ 2 min ago │ [Link]    │
│ ○ ACT-2024-0243 │ Alert     │ "Crowd forming"   │ 3 min ago │ [Link]    │
│ ○ ACT-2024-0244 │ Patrol    │ "Area secured"    │ 5 min ago │ [Link]    │
│                                                                             │
│ 🤖 AI Suggestions:                                                         │
│ • ACT-0242 appears related (same location, evidence type)                  │
│ • ACT-0243 may be related (crowd response to medical incident)            │
│                                                                             │
│ Search for Activities: [🔍 By location, time, type, tags...]               │
│                                                                             │
│ [Link Selected] [Create New Activity] [Cancel]                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Supervisor Incident Dismissal**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     DISMISS AUTO-CREATED INCIDENT                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ ⚠️ Supervisor Action Required                                              │
│                                                                             │
│ Incident: INC-2024-0091                                                    │
│ Auto-created from: ACT-2024-0245 (Alert - Door sensor)                    │
│ Rule triggered: Alert with 89% confidence after hours                     │
│                                                                             │
│ Dismissal Reason*:                                                          │
│ ○ False positive - Equipment malfunction                                  │
│ ● Authorized activity - Maintenance work                                  │
│ ○ Environmental factor - Weather related                                  │
│ ○ Other: [_____________________________]                                   │
│                                                                             │
│ Additional Notes:                                                          │
│ [Scheduled maintenance on door B-12, work order #M-2024-0123.             │
│  Maintenance staff had proper authorization.]                              │
│                                                                             │
│ Impact of Dismissal:                                                       │
│ • Incident marked as "Dismissed - Authorized"                             │
│ • Activities remain for audit trail                                        │
│ • AI rules updated to reduce false positives                              │
│ • Notification sent to involved personnel                                 │
│                                                                             │
│ [Dismiss Incident] [Keep Active] [Request Review]                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Enhanced Incident Management**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | No - Incidents require at least one activity | [Command Center Integration](#731-command-center-integration) |
| **Cardinality** | One incident contains 1 to many activities | [Enhanced Multi-Location Architecture](#732-enhanced-multi-location-architecture) |
| **Editable After Creation?** | Yes - Status, assignments, linked activities | [Enhanced Interface](#733-enhanced-incident-management-interface) |
| **Deletion/Archival Effects** | Soft deletion only, activities preserved | [Enhanced Audit Logging](#411-enhanced-audit-logging) |
| **Mandatory Before Close?** | Resolution notes and all activities resolved | [Enhanced Workflow](#736-enhanced-incident-workflow) |
| **Audit-Trail Requirement?** | All changes logged including dismissals | [Supervisor Incident Dismissal](#736-enhanced-incident-workflow) |
| **Edge-Case Handling** | Multi-location conflicts, auto-creation rules, concurrent updates | [Activity-Driven Status Management](#736-enhanced-incident-workflow) |

**✔️ Logic Cross-check**: Enhanced Incident Management treats incidents as intelligent groupings of activities, with auto-creation rules, supervisor oversight, and comprehensive activity timeline tracking while maintaining full audit trails.

### **7.3 📁 Case Management**

**🎯 Purpose**: Strategic investigation management for complex security matters, building upon resolved incidents with activity evidence trails

#### **7.3.1 🎛️ Strategic Layer Integration**

**Activity to Case Workflow**
- Cases are created from resolved incidents (which contain activities)
- Evidence-type activities can be added directly to cases
- Oracle AI analyzes activity patterns across incidents for case building
- Command Center incidents seamlessly escalate to strategic investigations
- Real-time case status updates visible in Command Center
- Cross-site investigative team coordination

**Strategic vs Operational Distinction**

| **Layer** | **Focus** | **AI Context** | **Activity Relationship** |
|-----------|-----------|----------------|---------------------------|
| **Operational (Incidents)** | Real-time response to grouped activities | Buddy - immediate response | Direct activity management |
| **Strategic (Cases)** | Long-term investigation and pattern analysis | Oracle - investigative intelligence | Analyzes activity patterns |

#### **7.3.2 🔮 Oracle AI Integration**

**Enhanced Case Intelligence with Activity Analysis**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORACLE AI CASE INTELLIGENCE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔮 ACTIVITY PATTERN ANALYSIS:                                               │
│ "Analyzing 47 activities across 6 incidents reveals coordinated pattern:    │
│                                                                             │
│ • 12 security-breach activities at similar times (02:00-03:00)            │
│ • 8 property-damage activities following breach attempts                   │
│ • Same entry method across Sites A & B (door sensor bypass)               │
│ • Vehicle license ABC-123 in 4 separate patrol activities                 │
│                                                                             │
│ Confidence: 94% - Organized theft ring targeting electronics"              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔍 INVESTIGATIVE RECOMMENDATIONS:                                          │
│ • Review all patrol activities mentioning vehicle ABC-123                  │
│ • Cross-reference badge access logs during activity windows               │
│ • Interview guards who created patrol activities on those nights          │
│ • Check for similar activity patterns at other facilities                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📊 EVIDENCE CORRELATION:                                                    │
│ • 15 evidence-type activities contain relevant photos/videos              │
│ • Guard patrol activities show suspicious vehicle 2 weeks prior           │
│ • Similar activity patterns match CASE-2024-0187 (closed)                │
│ • Recommend consolidating incidents INC-0445, 0446, 0448, 0450           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Oracle AI Case Functions**

| **Function** | **Capability** | **Activity-Based Enhancement** |
|--------------|----------------|---------------------------------|
| **Pattern Recognition** | Identifies patterns across activities | Analyzes all activity types, not just alerts |
| **Evidence Analysis** | Correlates evidence-type activities | Links evidence activities to timeline |
| **Investigative Planning** | Suggests investigation strategies | Based on activity history and patterns |
| **Case Building** | Recommends incident consolidation | Groups incidents by activity patterns |
| **Threat Assessment** | Evaluates ongoing risks | Monitors new activities for pattern matches |

#### **7.3.3 📊 Enhanced Case List Interface**

**Multi-Location Case Overview**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ACTIVE CASE INVESTIGATIONS                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Filter: [All Types ▼] [All Priorities ▼] [My Cases ☑] [Active Only ☑]     │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔴 CASE-2024-0123 │ Coordinated Theft Ring │ Sites A, B │ Active          │
│ ├─ Lead: Det. Johnson │ Activities: 47 │ Incidents: 6 │ Oracle: 94%       │
│ ├─ Activity Types: security-breach (12), property-damage (8), patrol (23)  │
│ └─ Latest: New evidence activity added 2 hours ago                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🟠 CASE-2024-0124 │ Insider Threat Investigation │ Site A │ Active         │
│ ├─ Lead: Sup. Williams │ Activities: 23 │ Incidents: 3 │ Oracle: 87%      │
│ ├─ Activity Types: alert (15), bol-event (2), evidence (6)               │
│ └─ Status: Reviewing badge access patterns in activities                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🟡 CASE-2024-0125 │ Vandalism Pattern │ Site C │ Investigation            │
│ ├─ Lead: Off. Brown │ Activities: 18 │ Incidents: 4 │ Oracle: 76%         │
│ ├─ Activity Types: property-damage (10), patrol (5), evidence (3)        │
│ └─ Next: Interview witnesses from patrol activities                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Enhanced Case Columns**

| **Column** | **Enhancement** | **Activity Integration** |
|------------|----------------|-----------------------------|
| **🆔 Case ID** | Location-aware ID generation | Links to activity locations |
| **📌 Title** | Oracle AI suggested based on patterns | Derived from activity analysis |
| **📋 Activities** | Total count across all incidents | Breakdown by type shown |
| **🏢 Locations** | All locations from activities | Primary + secondary sites |
| **👥 Team** | Multi-location investigators | Based on activity locations |
| **🔮 Oracle Score** | Pattern confidence from activities | Updates as activities added |
| **📊 Evidence** | Count of evidence-type activities | Direct activity links |

#### **7.3.4 ➕ Enhanced Case Creation**

**Creating Case from Incidents with Activities**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CREATE CASE FROM INCIDENTS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Select Related Incidents (with Activity Summary):                          │
│                                                                             │
│ ☑ INC-2024-0445 │ Door Breach - Site A    │ 8 activities  │ Resolved     │
│   └─ Activities: security-breach (3), property-damage (2), evidence (3)    │
│ ☑ INC-2024-0446 │ Theft - Electronics      │ 5 activities  │ Resolved     │
│   └─ Activities: property-damage (3), patrol (1), evidence (1)            │
│ ☑ INC-2024-0448 │ Vehicle Surveillance     │ 12 activities │ Resolved     │
│   └─ Activities: patrol (8), alert (3), bol-event (1)                    │
│ ☐ INC-2024-0449 │ Medical Emergency        │ 4 activities  │ Resolved     │
│   └─ Different pattern - medical activities only                          │
│                                                                             │
│ 🔮 ORACLE ANALYSIS:                                                        │
│ "Pattern analysis of 25 activities suggests organized theft operation.     │
│ Vehicle ABC-123 appears in 6 patrol activities prior to incidents.        │
│ Recommend comprehensive investigation with focus on insider threat."       │
│                                                                             │
│ Case Title: [Organized Electronics Theft - Multi-Site Investigation_____]  │
│                                                                             │
│ Case Type: [Theft - Organized ▼]    Priority: [High ▼]                   │
│                                                                             │
│ Lead Investigator: [Det. Johnson ▼]  Support: [Off. Smith, Williams ▼]   │
│                                                                             │
│ Initial Investigation Plan:                                                │
│ ☑ Review all patrol activities mentioning vehicle                         │
│ ☑ Analyze badge access during incident windows                            │
│ ☑ Interview guards who reported suspicious activities                     │
│ ☐ Contact law enforcement for vehicle owner info                         │
│                                                                             │
│ [Create Case] [Save as Draft] [Cancel]                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.3.5 🔍 Enhanced Case Detail View**

**Case Dashboard with Activity Analysis**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ CASE: CASE-2024-0123 - Coordinated Theft Ring Investigation               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Status: ACTIVE INVESTIGATION    Priority: HIGH    Created: 2024-01-15      │
│ Lead: Det. Johnson              Locations: Site A (Primary), Site B        │
│ Oracle Score: 94%              Activities: 47     Incidents: 6            │
├─────────────────────────────────────────────────────────────────────────────┤
│                         ACTIVITY PATTERN TIMELINE                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📅 Date      │ 🕐 Time  │ Type          │ Description                     │
├──────────────┼──────────┼───────────────┼─────────────────────────────────┤
│ Jan 01       │ 23:45    │ 🔍 patrol     │ "Suspicious vehicle in lot"     │
│ Jan 01       │ 23:47    │ 🔍 patrol     │ "Vehicle ABC-123 noted"         │
│ Jan 08       │ 02:15    │ ⚠️ alert      │ "Motion after hours - B wing"   │
│ Jan 08       │ 02:18    │ 🚫 security   │ "Door forced - Electronics"     │
│ Jan 08       │ 02:45    │ 🔧 property   │ "Display cases damaged"         │
│ Jan 08       │ 03:15    │ 📎 evidence   │ "Security footage saved"        │
│ Jan 15       │ 02:22    │ 🚫 security   │ "Similar breach - Site B"       │
│              │          │               │ [View all 47 activities]        │
├──────────────┴──────────┴───────────────┴─────────────────────────────────┤
│ 🔮 Oracle Pattern Analysis:                                                │
│ • All breaches occur between 02:00-03:00 on Mondays                      │
│ • Vehicle ABC-123 spotted 24-48 hours before each incident               │
│ • Same entry method: door sensor bypass technique                        │
│ • Target: High-value electronics only                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Evidence Management Panel**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CASE EVIDENCE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Evidence Activities (15 total):                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📎 ACT-2024-0238 │ Security Footage    │ Added by: Smith   │ Jan 08      │
│   └─ Door breach captured, 2 suspects visible, 1 partial face             │
│ 📎 ACT-2024-0242 │ Vehicle Photo        │ Added by: Johnson │ Jan 08      │
│   └─ License plate ABC-123 clearly visible                                │
│ 📎 ACT-2024-0256 │ Damage Assessment    │ Added by: Brown   │ Jan 09      │
│   └─ $45,000 in stolen electronics documented                             │
│ 📎 ACT-2024-0289 │ Badge Access Log     │ Added by: System  │ Jan 15      │
│   └─ No authorized access during incident windows                         │
│                                                                             │
│ Additional Evidence Options:                                               │
│ [+ Add Evidence Activity] [Link Existing Activity] [Request Analysis]      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Chain of Custody: All evidence activities maintain full audit trail       │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Investigation Team & Tasks**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      INVESTIGATION TEAM & TASKS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Team Members:               │ Active Tasks:                                 │
│ 🎖️ Det. Johnson (Lead)     │ ☑ Review 23 patrol activities              │
│ 👮 Off. Smith (Site A)      │ ☐ Interview 5 guards who saw vehicle       │
│ 👮 Off. Williams (Site B)   │ ☐ Analyze badge patterns                   │
│ 🔍 Analyst Davis (Remote)   │ ⏳ Cross-reference with law enforcement    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Task Progress:                                                             │
│ ████████░░░░░░░░ 45% Complete (11 of 24 tasks)                           │
│                                                                             │
│ [+ Add Task] [Assign Task] [Update Progress] [Team Meeting]               │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.3.6 🔄 Enhanced Case Workflow**

**Case Status Progression**

| **Stage** | **Triggered By** | **Required Elements** | **Available Actions** |
|-----------|------------------|----------------------|----------------------|
| **Case Initiation** | Created from incidents | Min 1 incident with activities | Assign team, plan |
| **Evidence Collection** | Team assigned | Gathering evidence activities | Add evidence, analyze |
| **Investigation Planning** | Evidence reviewed | Investigation tasks created | Assign tasks, coordinate |
| **Active Investigation** | Tasks in progress | Team actively working | Update findings, add activities |
| **Case Resolution** | Investigation complete | All tasks resolved | Close case, final report |

**Adding Activities to Cases**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ADD ACTIVITY TO CASE                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Activity Type: [evidence ▼]                                                │
│                                                                             │
│ Title: [Witness statement - saw vehicle 3 times_______________________]    │
│                                                                             │
│ Description:                                                               │
│ [Guard Thompson reports seeing vehicle ABC-123 in parking lot on          │
│  Dec 28, Jan 1, and Jan 7 - always late evening. Seemed to be           │
│  photographing the building.]                                             │
│                                                                             │
│ Evidence Files: [📎 witness_statement_thompson.pdf] [+ Add More]          │
│                                                                             │
│ This activity will be:                                                    │
│ • Added to case CASE-2024-0123                                           │
│ • Marked as type 'evidence' with status 'resolved'                       │
│ • Linked to investigation timeline                                        │
│ • Included in Oracle pattern analysis                                    │
│                                                                             │
│ [Add to Case] [Cancel]                                                    │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Case Management**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | No - Cases require incidents (which contain activities) | [Strategic Layer Integration](#741-strategic-layer-integration) |
| **Cardinality** | One case can link to many incidents, each with many activities | [Oracle AI Integration](#742-oracle-ai-integration) |
| **Editable After Creation?** | Yes - Team, status, and evidence activities can be added | [Enhanced Case Detail View](#745-enhanced-case-detail-view) |
| **Deletion/Archival Effects** | Soft deletion preserves investigation history, activities remain | [Enhanced Audit Logging](#411-enhanced-audit-logging) |
| **Mandatory Before Close?** | Resolution summary and all tasks complete | [Enhanced Case Workflow](#746-enhanced-case-workflow) |
| **Audit-Trail Requirement?** | All case activities logged with full investigation trail | [Evidence Management Panel](#745-enhanced-case-detail-view) |
| **Edge-Case Handling** | Cross-site jurisdiction, evidence chain of custody, Oracle confidence thresholds | [Case Status Progression](#746-enhanced-case-workflow) |

**✔️ Logic Cross-check**: Case Management builds upon the activity foundation, using Oracle AI to analyze patterns across all activity types and create comprehensive investigations with full evidence trails.

#### **7.3.8 🆕 AI-Powered Case Insights (v0.1 Enhancement)**

**🎯 Purpose**: Provide intelligent analysis and recommendations for case investigations using AI pattern recognition

**AI Insights Panel**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AI CASE INSIGHTS - CASE-2024-0123                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🧠 PATTERN ANALYSIS                          Generated: 2 minutes ago       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Detected Patterns:                                                          │
│ • Time Pattern: 78% of activities occur between 02:00-04:00 AM            │
│ • Location Pattern: Entry always through loading dock (confidence: 92%)    │
│ • Behavioral Pattern: Suspect disables cameras before entry (5/6 times)   │
│ • Vehicle Pattern: Dark sedan spotted in 4 patrol activities              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🎯 RECOMMENDATIONS                           Priority: HIGH                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ 1. Increase patrols at loading dock 01:00-05:00 AM                        │
│ 2. Review employee access logs for night shift workers                     │
│ 3. Cross-reference vehicle sightings with parking lot cameras             │
│ 4. Interview guards who reported the dark sedan                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📊 RISK ASSESSMENT                                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Risk Score: 85/100 (Critical)                                              │
│ • Likelihood of recurrence: High                                           │
│ • Potential escalation: Medium                                             │
│ • Resource vulnerability: Loading dock security                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔗 SIMILAR CASES                                                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ CASE-2023-0892 (87% match) - Resolved: Employee theft ring                │
│ CASE-2023-0645 (73% match) - Resolved: External burglary crew             │
│ CASE-2024-0089 (69% match) - Active: Vandalism investigation              │
└─────────────────────────────────────────────────────────────────────────────┘
```

**API Integration**
- Endpoint: `GET /api/cases/{id}/insights`
- Updates: Real-time via WebSocket when new activities added
- Caching: 15-minute cache, invalidated on case updates

#### **7.3.9 🆕 Automated Case Timeline (v0.1 Enhancement)**

**🎯 Purpose**: Provide chronological visualization of all case-related activities

**Timeline View**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          CASE TIMELINE - CASE-2024-0123                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ [Activity View] [Incident View] [Evidence View] [All Events]               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-10 02:15:33                                                        │
│ ├─ 🔍 PATROL Activity (ACT-0234)                                          │
│ │  Officer reports suspicious vehicle in parking lot                       │
│ │  Location: Building A - Parking Lot                                     │
│ │  [View Details] [View Evidence]                                         │
│                                                                            │
│ 2024-01-10 02:45:12                                                        │
│ ├─ ⚠️ ALERT Activity (ACT-0237) → Created INC-0089                       │
│ │  Door sensor triggered - Loading dock forced entry                      │
│ │  Confidence: 95% | Integration: Lenel                                   │
│ │  [View Video] [View Details]                                           │
│                                                                            │
│ 2024-01-10 02:47:45                                                        │
│ ├─ 🚨 SECURITY-BREACH Activity (ACT-0238)                                 │
│ │  Multiple cameras disabled in sequence                                   │
│ │  AI Analysis: Deliberate pattern detected                               │
│ │  [View Analysis] [View Camera Locations]                                │
│                                                                            │
│ 2024-01-10 03:15:00                                                        │
│ ├─ 🏚️ PROPERTY-DAMAGE Activity (ACT-0241)                               │
│ │  Warehouse inventory reported missing                                    │
│ │  Estimated value: $45,000                                               │
│ │  [View Inventory List] [View Photos]                                   │
│                                                                            │
│ 2024-01-11 09:30:00                                                        │
│ ├─ 📸 EVIDENCE Activity (ACT-0256)                                        │
│ │  Security footage recovered from backup system                          │
│ │  Shows suspect vehicle license plate partially                          │
│ │  [View Footage] [Enhance Image]                                        │
└─────────────────────────────────────────────────────────────────────────────┘
│ Showing 5 of 47 total activities      [Load More] [Export Timeline]        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Timeline Features**
- Auto-aggregates all activities from linked incidents
- Filterable by activity type, date range, location
- Exportable as PDF/CSV for reports
- Real-time updates as new activities added

#### **7.3.10 🆕 Smart Incident Suggestions (v0.1 Enhancement)**

**🎯 Purpose**: AI-powered incident linking suggestions during case creation/editing

**Incident Suggestion Interface**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     SUGGESTED RELATED INCIDENTS                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Based on case description and existing incidents:                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ ☑ INC-2024-0089 (95% match)              Already Linked                   │
│   Door forced at loading dock - Building A                                 │
│   Activities: 12 | Status: Resolved                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ ☐ INC-2024-0087 (89% match)              🆕 Suggested                     │
│   Suspicious vehicle reported - Similar description                        │
│   Activities: 3 | Status: Resolved                                         │
│   AI Reasoning: "Same vehicle description, 2 hours before breach"          │
├─────────────────────────────────────────────────────────────────────────────┤
│ ☐ INC-2024-0084 (76% match)              🆕 Suggested                     │
│   Camera malfunction - Building A                                          │
│   Activities: 2 | Status: Investigating                                    │
│   AI Reasoning: "Camera disabled pattern matches case MO"                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ ☐ INC-2024-0079 (71% match)              🆕 Suggested                     │
│   Missing inventory report - Building B                                    │
│   Activities: 5 | Status: Resolved                                         │
│   AI Reasoning: "Similar items stolen, possible connection"                │
└─────────────────────────────────────────────────────────────────────────────┘
│ [Select All Relevant] [Link Selected] [Refresh Suggestions]                │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Suggestion Algorithm**
- Analyzes case title, description, and existing incidents
- Pattern matching on activity types, locations, times
- Confidence scoring based on multiple factors
- Updates suggestions as case details change

---

### **7.4 👥 User Management**

**🎯 Purpose**: Multi-location user administration with activity-based permissions and operational role management

#### **7.4.1 🌐 Multi-Location User Matrix**

**Enhanced User Overview with Activity Context**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         USER MANAGEMENT DASHBOARD                          │
├─────────────────────────────────────────────────────────────────────────────┤
│  👤 Active Users: 147    🏢 Locations: 12    📋 Activities Today: 892     │
├─────────────────────────────────────────────────────────────────────────────┤
│ User Name        │ Role          │ Locations     │ Activities │ Status    │
├──────────────────┼───────────────┼───────────────┼────────────┼───────────┤
│ Smith, John      │ 🔴 Admin      │ ✅ All (12)   │ 45 created │ 🟢 Active │
│ Johnson, Sarah   │ 🟠 Supervisor │ ✅ HQ, Ware(2)│ 123 created│ 🟢 Active │
│ Wilson, Mike     │ 🟢 Officer    │ ✅ Remote (1) │ 89 created │ 🟢 Active │
│ Davis, Karen     │ 🟢 Officer    │ ✅ HQ (1)     │ 67 created │ 🟡 Break  │
└──────────────────┴───────────────┴───────────────┴────────────┴───────────┘
│ Filters: [All Roles ▼] [All Locations ▼] [Active Only ☑]   [+ Create User] │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Table Columns Enhanced for Activities**

| **Column** | **Description** | **Activity Context** |
|------------|-----------------|----------------------|
| **👤 Name** | Full name | Links to activity history |
| **📧 Email** | Email address | Notification preferences |
| **🎭 Role** | Admin/Supervisor/Officer | Activity permissions |
| **🏢 Locations** | Site access | Where can create activities |
| **📋 Activities** | Activities created (24h) | Quick performance metric |
| **🚦 Status** | Current availability | Active/Break/Off-duty |
| **🕐 Last Activity** | Most recent activity created | Shows engagement |

#### **7.4.2 🏗️ Enhanced User Creation/Edit**

**User Form with Activity Permissions**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           CREATE/EDIT USER                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Basic Information:                                                          │
│ First Name*      [Mike_________________]                                   │
│ Last Name*       [Wilson_______________]                                    │
│ Email*           [mwilson@security.com_]                                   │
│ Phone            [(555) 123-4567_______]                                   │
│ Employee ID      [SEC-4782_____________]                                   │
│                                                                             │
│ Access Configuration:                                                       │
│ Primary Role*    [Officer ▼]                                               │
│ Home Location*   [Site A - HQ ▼]                                          │
│ Additional Sites [+ Add Location Access]                                   │
│                                                                             │
│ Activity Permissions:                                                      │
│ ☑ Create all activity types (standard for Officers)                       │
│ ☑ Modify activity type (with audit log)                                   │
│ ☑ Add tags (limit: 10 per activity)                                       │
│ ☐ Dismiss auto-incidents (Supervisor+ only)                               │
│ ☑ Link activities to incidents                                             │
│                                                                             │
│ Command Center Access:                                                      │
│ Interface Level  [Simplified View ▼]                                       │
│ Widget Access    ☑ Activity Stream  ☑ Video Wall  ☑ Guard Status         │
│                  ☐ System Health    ☐ Multi-Site   ☑ AI (Buddy)          │
│                                                                             │
│ Notification Settings:                                                      │
│ ☑ Email notifications for assigned incidents                               │
│ ☑ SMS for critical activities (medical, security-breach)                  │
│ ☑ Push notifications for BOL matches                                       │
│                                                                             │
│ [Save User] [Save & Create Another] [Cancel]                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.4.3 🏢 Location Access Management**

**User Location Assignment with Activity Context**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LOCATION ACCESS MANAGEMENT                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ User: Wilson, Mike (Officer)                                               │
│                                                                             │
│ Primary Location: Site A - HQ ✅                                           │
│ └─ Can create activities, view incidents, access Command Center            │
│                                                                             │
│ Additional Location Access:                                                │
│ ☐ Site B - Warehouse                                                      │
│    └─ Would enable: Activity creation, incident viewing                   │
│ ☐ Site C - Remote Office                                                  │
│    └─ Would enable: Activity creation, incident viewing                   │
│                                                                             │
│ Cross-Site Permissions:                                                    │
│ ☐ View activities from all assigned locations                             │
│ ☐ Create multi-location incidents (Supervisor approval required)          │
│ ☐ Access cross-site reports                                               │
│                                                                             │
│ Activity Creation by Location (Last 30 Days):                             │
│ Site A: 234 activities (89 patrol, 67 alert, 45 evidence, 33 other)      │
│                                                                             │
│ [Update Access] [View Activity History] [Cancel]                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.4.4 🎛️ Command Center Access Configuration**

**Activity-Focused Command Center Setup**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   COMMAND CENTER ACCESS CONFIGURATION                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ User: Wilson, Mike (Officer)                                               │
│                                                                             │
│ Interface Access Level: [Simplified View ▼]                                │
│                                                                             │
│ Available Widgets:                                                          │
│ ┌─────────────────────────┬─────────────────────────┐                     │
│ │ ✅ Activity Stream       │ Real-time activities    │                     │
│ │    • View all types      │ from current location   │                     │
│ │    • Create activities   │                         │                     │
│ │    • Basic filtering     │                         │                     │
│ ├─────────────────────────┼─────────────────────────┤                     │
│ │ ✅ Video Wall            │ Camera feeds from       │                     │
│ │    • View only           │ assigned areas          │                     │
│ │    • No PTZ control      │                         │                     │
│ ├─────────────────────────┼─────────────────────────┤                     │
│ │ ✅ Guard Status          │ Current location        │                     │
│ │    • View status         │ guards only             │                     │
│ │    • Check-in function   │                         │                     │
│ ├─────────────────────────┼─────────────────────────┤                     │
│ │ ✅ AI Assistant (Buddy)  │ Operational help with   │                     │
│ │    • Activity analysis   │ current activities      │                     │
│ │    • Response guidance   │                         │                     │
│ └─────────────────────────┴─────────────────────────┘                     │
│                                                                             │
│ Layout Preset: [Officer Standard ▼]                                        │
│                                                                             │
│ [Apply Settings] [Preview Layout] [Reset to Default]                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.4.5 👮 Real-Time Activity Coordination**

**User Activity Dashboard**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      USER ACTIVITY COORDINATION                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ Active Users at Site A                          Current Time: 14:35 PST     │
├─────────────────────────────────────────────────────────────────────────────┤
│ User Name      │ Status       │ Recent Activity         │ Response Time   │
├────────────────┼──────────────┼─────────────────────────┼─────────────────┤
│ Garcia, Ana    │ 🟢 Active    │ Created patrol activity │ 2 min ago       │
│                │              │ "Sector 3 complete"     │ Avg: 1.2 min    │
├────────────────┼──────────────┼─────────────────────────┼─────────────────┤
│ Johnson, Mark  │ 🟡 Responding│ Handling medical        │ Active now      │
│                │              │ INC-2024-0089          │ Avg: 1.8 min    │
├────────────────┼──────────────┼─────────────────────────┼─────────────────┤
│ Smith, Lisa    │ 🔴 Break     │ Last: evidence activity │ 15 min ago      │
│                │              │ "Photos uploaded"       │ Back at: 15:00  │
├────────────────┼──────────────┼─────────────────────────┼─────────────────┤
│ Davis, Tom     │ ⚫ Off Duty  │ Shift ended            │ 2 hours ago     │
│                │              │ Created 67 activities   │ Next: 22:00     │
└────────────────┴──────────────┴─────────────────────────┴─────────────────┘
│ Quick Actions: [View All Activities] [Export Report] [Shift Schedule]      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.4.6 📊 User Performance Analytics**

**Activity-Based Performance Metrics**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      USER PERFORMANCE ANALYTICS                             │
├─────────────────────────────────────────────────────────────────────────────┤
│ User: Wilson, Mike          Period: Last 30 Days          Role: Officer    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Activity Creation:                  │ Activity Quality:                     │
│ • Total: 892 activities            │ • Properly tagged: 98%               │
│ • Daily average: 29.7              │ • Complete descriptions: 94%         │
│ • By type:                         │ • Evidence attached: 87%             │
│   - Patrol: 523 (59%)              │ • Led to incidents: 12%              │
│   - Alert: 189 (21%)               │                                       │
│   - Evidence: 89 (10%)             │ Response Metrics:                     │
│   - Other: 91 (10%)                │ • Avg response time: 2.3 min         │
│                                    │ • Incident participation: 34         │
│ Peak Hours: 14:00-16:00            │ • Cases contributed to: 3            │
│ Peak Days: Tuesday, Thursday       │                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🏆 Achievements:                                                           │
│ • Fastest medical response (0.8 min)                                       │
│ • Most thorough patrol reports                                            │
│ • 100% activity tag compliance                                            │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.4.7 🎯 Special User Management Behaviors**

| **Behavior** | **Rule** | **Activity Impact** |
|--------------|----------|---------------------|
| **User Deactivation** | Cannot delete users | All created activities preserved |
| **Role Changes** | Immediate permission update | Historical activities unchanged |
| **Location Transfer** | Update primary location | Past activities retain original location |
| **Activity Ownership** | Activities linked to creator | Ownership cannot be changed |
| **Performance Tracking** | Based on activity metrics | Quality over quantity focus |

### **📋 V0 Logic Checklist - User Management**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | Yes - Users are top-level entities | [Multi-Location User Matrix](#741-multi-location-user-matrix) |
| **Cardinality** | One user → many activities, many locations | [User Creation/Edit](#742-enhanced-user-creationedit) |
| **Editable After Creation?** | Yes - All fields except email (unique identifier) | [Location Access Management](#743-location-access-management) |
| **Deletion/Archival Effects** | No deletion, only deactivation, activities preserved | [Special Behaviors](#747-special-user-management-behaviors) |
| **Mandatory Before Close?** | Must reassign active incidents before deactivation | [Real-Time Activity Coordination](#745-real-time-activity-coordination) |
| **Audit-Trail Requirement?** | All user changes logged, activity creation tracked | [User Performance Analytics](#746-user-performance-analytics) |
| **Edge-Case Handling** | Cannot deactivate last admin, activity ownership immutable | [Special Behaviors](#747-special-user-management-behaviors) |

**✔️ Logic Cross-check**: User Management integrates activity permissions throughout, tracking user performance through activity creation while maintaining security and audit requirements.

---

### **7.5 🔍 Global Search**

**🎯 Purpose**: Unified search across all activities, incidents, cases, and related entities with real-time updates

#### **7.5.1 🌐 Global Search Interface**

**Activity-Enhanced Search Interface**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          GLOBAL SEARCH COMMAND CENTER                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔍 Search: [vehicle ABC123 patrol activities]                   🤖 AI Mode │
│                                                                             │
│ 📍 Scope: [🌐 All Entities ▼] [🕐 Last 30 Days ▼] [📋 All Activities ▼]   │
│                                                                             │
│ 🎯 Quick Filters:                                                          │
│ [📋 Activities] [🚨 Incidents] [📁 Cases] [👁️ BOLs] [👤 Users]           │
│                                                                             │
│ Advanced Filters:                                                           │
│ Activity Type: [All ▼]  Trigger: [All ▼]  Status: [All ▼]  Tags: [____]  │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Search Syntax Examples**
```
Basic Searches:
• "vehicle ABC123" - Find all mentions across activities
• type:patrol - All patrol activities  
• trigger:human status:resolved - Human-created resolved activities
• tag:weather:rain - Activities tagged with rain

Advanced Searches:
• type:medical created:>2024-01-01 - Recent medical activities
• location:"Building A" AND (type:alert OR type:security-breach)
• confidence:>80 trigger:integration - High-confidence system alerts
• assigned:me status:responding - My active responses
```

#### **7.5.2 🎯 Real-Time Search Results**

**Live Search Results with Activities**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    SEARCH RESULTS - "vehicle ABC123"                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Found 23 results across all entities          🔄 Live updating: ON         │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📋 ACTIVITIES (17)                                                         │
│ ├─ ACT-2024-0156 │ patrol │ "Suspicious vehicle ABC123 in lot" │ Jan 01  │
│ ├─ ACT-2024-0189 │ patrol │ "ABC123 parked near loading dock" │ Jan 07  │
│ ├─ ACT-2024-0231 │ bol-event │ "BOLO issued for ABC123" │ Jan 08         │
│ └─ [Show 14 more activities]                                               │
│                                                                             │
│ 🚨 INCIDENTS (4)                                                           │
│ ├─ INC-2024-0445 │ "Theft investigation - vehicle involved" │ Active      │
│ │  └─ Contains 3 activities mentioning ABC123                             │
│ └─ [Show 3 more incidents]                                                 │
│                                                                             │
│ 📁 CASES (2)                                                               │
│ ├─ CASE-2024-0123 │ "Organized theft ring" │ Active Investigation        │
│ │  └─ Vehicle ABC123 identified in 6 patrol activities                    │
│ └─ CASE-2024-0098 │ "Previous incident" │ Closed                         │
│                                                                             │
│ 🤖 AI INSIGHT:                                                             │
│ "Vehicle ABC123 appears in patrol activities 24-48 hours before each      │
│ security incident. Pattern suggests reconnaissance behavior."              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.5.3 🧠 AI-Enhanced Search Intelligence**

**Oracle Search Analysis**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ORACLE SEARCH INTELLIGENCE                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ Natural Language Query: "Show all security problems last week at night"    │
│                                                                             │
│ 🤖 Oracle Translation:                                                     │
│ Searching for:                                                              │
│ • Activity types: alert, security-breach, property-damage                  │
│ • Time range: Last 7 days                                                  │
│ • Time filter: tag:time:after-hours                                        │
│ • Status: All (including resolved)                                         │
│                                                                             │
│ Found 34 matching activities:                                              │
│ • 23 alerts (18 auto-created incidents)                                   │
│ • 8 security-breach (all created incidents)                               │
│ • 3 property-damage (2 created incidents)                                 │
│                                                                             │
│ 📊 Pattern Analysis:                                                       │
│ • 71% occurred between 02:00-04:00                                        │
│ • Building B had 3x more than average                                     │
│ • Tuesday and Thursday show higher activity                               │
│                                                                             │
│ Suggested Refinements:                                                     │
│ [Focus on Building B] [Tuesday/Thursday only] [Add video evidence]        │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.5.4 💾 Enhanced Saved Searches**

**Activity-Focused Search Templates**

| **Template Name** | **Query** | **Use Case** |
|-------------------|-----------|--------------|
| **🚨 Active Emergencies** | `type:medical status:responding OR type:security-breach status:responding` | Current critical activities |
| **🔍 My Patrol Routes** | `type:patrol trigger:human created_by:me` | Personal patrol history |
| **⚠️ Unresolved Alerts** | `type:alert status:detecting confidence:>70` | Pending system alerts |
| **📎 Recent Evidence** | `type:evidence created:>today-7d` | Latest evidence activities |
| **👁️ BOL Monitoring** | `type:bol-event status:!resolved` | Active BOL activities |

**Custom Search Builder**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CREATE SAVED SEARCH                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Search Name: [Night Shift Security Review_____________________________]    │
│                                                                             │
│ Query Builder:                                                              │
│ Activity Types:  ☑ alert  ☑ security-breach  ☑ property-damage  ☐ patrol │
│ Triggers:        ☑ human  ☑ integration                                   │
│ Time Range:      [Last 24 hours ▼]                                        │
│ Additional:      ☑ After hours only  ☐ My activities only                 │
│                                                                             │
│ Advanced Query: [tag:time:after-hours AND (type:alert OR type:security)]  │
│                                                                             │
│ Notifications:                                                              │
│ ☑ Email me when new results match (max once per hour)                     │
│ ☑ Show in Command Center dashboard                                         │
│                                                                             │
│ Share With: [Supervisor team ▼]                                            │
│                                                                             │
│ [Save Search] [Test Query] [Cancel]                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.5.5 📊 Search Analytics**

**Search Usage Dashboard**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         SEARCH ANALYTICS                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Search Activity (Last 30 Days):                                           │
│                                                                             │
│ Total Searches: 3,847                      Top Search Terms:              │
│ Unique Users: 89                           1. type:patrol (523)           │
│ Avg Results: 34 per search                 2. vehicle plates (445)        │
│ AI-Assisted: 23%                           3. status:responding (398)     │
│                                            4. tag:weather:* (234)         │
│ By Entity Type:                            5. location:"Building A" (189) │
│ • Activities: 67%  ████████                                               │
│ • Incidents: 19%   ███                     Popular Saved Searches:        │
│ • Cases: 8%        █                       • Active Emergencies (45 users) │
│ • Users: 4%        █                       • Night Activity (34 users)    │
│ • BOLs: 2%         │                       • My Activities (89 users)     │
│                                                                             │
│ Search Performance:                                                         │
│ • Average response time: 0.3 seconds                                      │
│ • Cross-site searches: 34% of total                                       │
│ • Real-time updates active: 56% of searches                               │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Global Search**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | N/A - Search is a function, not an entity | [Global Search Interface](#751-global-search-interface) |
| **Cardinality** | One search → many results across all entity types | [Real-Time Search Results](#752-real-time-search-results) |
| **Editable After Creation?** | Saved searches can be edited by creator | [Enhanced Saved Searches](#754-enhanced-saved-searches) |
| **Deletion/Archival Effects** | Search history retained 90 days | [Search Analytics](#755-search-analytics) |
| **Mandatory Before Close?** | N/A - Searches execute immediately | N/A |
| **Audit-Trail Requirement?** | Search queries logged for security | [Search Analytics](#755-search-analytics) |
| **Edge-Case Handling** | Query validation, result limits, performance optimization | [AI-Enhanced Search](#753-ai-enhanced-search-intelligence) |

**✔️ Logic Cross-check**: Global Search provides unified access to all activities and related entities, with AI enhancement and real-time updates while respecting permissions.

---

### **7.6 📊 Reports & Analytics** 🆕 *(Enhanced in v0.1)*

**🎯 Purpose**: Comprehensive reporting system with pre-built reports, custom report builder, and automated distribution

#### **7.6.1 📚 Pre-Built Reports Library**

**Available Report Templates**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          REPORTS & ANALYTICS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📊 Pre-Built Reports              │ 🔨 Custom Reports                       │
├───────────────────────────────────┼─────────────────────────────────────────┤
│ 📅 Daily Activity Summary         │ [+ Create Custom Report]                │
│    Last run: 2 hours ago          │                                         │
│    [Run Now] [Schedule] [View]    │ Recent Custom Reports:                  │
│                                   │ • Weekend Security Analysis             │
│ 📈 Weekly Incident Report         │ • Building A Activity Patterns          │
│    Last run: Monday 08:00         │ • Response Time by Location             │
│    [Run Now] [Schedule] [View]    │                                         │
│                                   │ [View All Custom Reports]               │
│ 📊 Monthly Case Metrics           │                                         │
│    Last run: 1st of month         │                                         │
│    [Run Now] [Schedule] [View]    │                                         │
│                                   │                                         │
│ 👥 User Activity Report           │                                         │
│    Never run                      │                                         │
│    [Run Now] [Schedule] [View]    │                                         │
│                                   │                                         │
│ ⏱️ Response Time Analysis         │                                         │
│    Last run: Yesterday            │                                         │
│    [Run Now] [Schedule] [View]    │                                         │
│                                   │                                         │
│ 🤖 AI Usage Report                │                                         │
│    Last run: Last week            │                                         │
│    [Run Now] [Schedule] [View]    │                                         │
└───────────────────────────────────┴─────────────────────────────────────────┘
```

**Report Descriptions:**
- **Daily Activity Summary**: All activities, incidents, and cases from past 24 hours
- **Weekly Incident Report**: Incident trends, response times, resolution rates
- **Monthly Case Metrics**: Case closure rates, investigation duration, team performance
- **User Activity Report**: Individual user actions, login times, activity creation
- **Response Time Analysis**: Average response by type, location, time of day
- **AI Usage Report**: AI interactions, suggestions accepted/rejected, efficiency gains

#### **7.6.2 🔨 Custom Report Builder**

**Report Creation Wizard**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         CUSTOM REPORT BUILDER                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 1 of 4: Select Data Source                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Choose entities to include:                                                 │
│ ☑ Activities    ☑ Incidents    ☐ Cases    ☐ Users    ☐ BOLs              │
│                                                                             │
│ 🤖 AI Suggestion: "Based on your role, you might want to include Cases"     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 2 of 4: Select Fields                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Available Fields:              │ Selected Fields:                           │
│ ├─ Activity Type              │ ├─ Created Date                           │
│ ├─ Status                     │ ├─ Activity Type                          │
│ ├─ Location                   │ ├─ Location                               │
│ ├─ Created By                 │ ├─ Status                                 │
│ ├─ Tags                       │ └─ Response Time                          │
│ └─ [More Fields...]           │                                           │
│                               │ [↑] [↓] [Remove]                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 3 of 4: Set Filters                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Date Range: [Last 30 Days ▼]                                               │
│ Locations: [All My Locations ▼]                                            │
│ Activity Types: [All Types ▼]                                              │
│ Status: [All Statuses ▼]                                                   │
│                                                                             │
│ [+ Add Custom Filter]                                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Step 4 of 4: Output Options                                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Report Name: [Security Activity Analysis_______________]                    │
│ Format: ○ PDF  ● Excel  ○ CSV                                              │
│ Include Charts: ☑ Activity trends ☑ Location breakdown ☐ Time analysis     │
│                                                                             │
│ Schedule: ○ Run Once  ● Daily  ○ Weekly  ○ Monthly                        │
│ Send to: [john.doe@company.com; security-team@company.com]                 │
│                                                                             │
│ [Preview Report] [Save & Run] [Save Template]                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.6.3 📊 Report Queue & Management**

**Report Processing Queue**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            REPORT QUEUE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ Running Reports:                                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔄 Monthly Case Metrics          │ Progress: ████████░░ 78%                │
│    Started: 2 min ago            │ Est. Complete: 1 min                    │
│    Records: 15,234 of 19,543     │ [Cancel]                                │
├──────────────────────────────────┼─────────────────────────────────────────┤
│ ⏳ Response Time Analysis        │ Progress: ██░░░░░░░░ 23%                │
│    Started: 30 sec ago           │ Est. Complete: 3 min                    │
│    Records: 4,521 of 19,652      │ [Cancel]                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Completed Reports (Last 24 Hours):                                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ ✅ Daily Activity Summary        │ Completed: 08:00 AM                     │
│    Size: 2.4 MB (PDF)            │ [Download] [Email] [View]               │
├──────────────────────────────────┼─────────────────────────────────────────┤
│ ✅ Custom: Building A Analysis   │ Completed: Yesterday 16:45              │
│    Size: 856 KB (Excel)          │ [Download] [Email] [View]               │
└──────────────────────────────────┴─────────────────────────────────────────┘
│ [View All History] [Report Settings] [Clear Completed]                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.6.4 🎯 Report Features & Permissions**

**Advanced Report Features:**
- **Data Export Limits**: 10,000 rows for Excel/CSV, unlimited for PDF
- **Scheduled Reports**: Automatic generation and email distribution
- **Report Templates**: Save custom reports as reusable templates
- **AI Recommendations**: Suggests relevant fields and filters
- **Performance**: Large reports process asynchronously
- **Caching**: Frequently-run reports cached for 1 hour

**Report Permissions Matrix:**

| Feature | Admin | Supervisor | Officer |
|---------|-------|------------|----------|
| View Pre-built Reports | ✅ All data | ✅ Location filtered | ❌ |
| Create Custom Reports | ✅ | ✅ | ❌ |
| Schedule Reports | ✅ | ✅ | ❌ |
| Export Reports | ✅ All formats | ✅ All formats | ❌ |
| Share Reports | ✅ | ✅ Within team | ❌ |
| View Report History | ✅ All reports | ✅ Own reports | ❌ |

---

### **7.7 ⚙️ Settings & Configuration**

**🎯 Purpose**: System-wide configuration with activity management settings and multi-location support (Admin only)

#### **7.7.1 🏢 Organization Settings**

**Core Organization Configuration**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORGANIZATION SETTINGS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Organization Details:                                                       │
│ Name*            [ACME Security Corporation________________________]       │
│ Primary Contact* [admin@acmesecurity.com___________________________]       │
│ Phone           [(555) 123-4567____________________________________]       │
│ Time Zone       [Pacific Time (PST/PDT) ▼]                                │
│                                                                             │
│ Activity System Configuration:                                              │
│ Activity ID Format:     [ACT-YYYY-NNNNN]  Example: ACT-2024-00234        │
│ Activity Retention:     [30 ▼] days in active database                    │
│ Archive Policy:         [Permanent ▼] retention after archival            │
│                                                                             │
│ Business Hours:                                                             │
│ Monday-Friday:   [06:00] to [18:00]                                       │
│ Saturday-Sunday: [08:00] to [16:00]                                       │
│ After-Hours Tag: Applied automatically outside business hours              │
│                                                                             │
│ [Save Changes] [Reset to Defaults] [View Change History]                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.7.2 🔐 Security Settings**

**Activity Security Configuration**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SECURITY SETTINGS                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Password Policy:                                                            │
│ Minimum Length:        [12 ▼] characters                                   │
│ Complexity:            ☑ Uppercase  ☑ Lowercase  ☑ Numbers  ☑ Special     │
│ Expiration:            [90 ▼] days                                         │
│ Reuse Prevention:      Last [5 ▼] passwords                                │
│                                                                             │
│ Session Management:                                                         │
│ Session Timeout:       [60 ▼] minutes of inactivity                       │
│ Activity Draft Save:   [Every 30 seconds ▼]                               │
│ Concurrent Sessions:   [Single session per user ▼]                         │
│                                                                             │
│ Activity Permissions:                                                       │
│ ☑ All roles can create activities (recommended)                           │
│ ☑ Activity type modification requires audit log                            │
│ ☑ Supervisors can dismiss auto-created incidents                          │
│ ☐ Restrict evidence activities to Supervisors+ (not recommended)          │
│                                                                             │
│ [Update Security Settings] [View Security Audit Log]                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.7.3 📋 Activity Type Configuration**

**Activity Type Management**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ACTIVITY TYPE CONFIGURATION                          │
├─────────────────────────────────────────────────────────────────────────────┤
│ Standard Activity Types:                   Auto-Incident Rules:            │
├────────────────────────────────────────────┬───────────────────────────────┤
│ Type          │ Icon │ Status │ Incidents  │ Rule                          │
├───────────────┼──────┼────────┼────────────┼───────────────────────────────┤
│ patrol        │ 🔍   │ Active │ Never      │ No auto-creation              │
│ alert         │ ⚠️   │ Active │ Conditional│ If confidence > 80% OR        │
│               │      │        │            │ after-hours                   │
│ medical       │ 🚨   │ Active │ Always     │ Always create, no dismiss     │
│ security-     │ 🚫   │ Active │ Always     │ Always create, dismissible    │
│ breach        │      │        │            │                               │
│ property-     │ 🔧   │ Active │ Conditional│ If confidence > 75%           │
│ damage        │      │        │            │                               │
│ bol-event     │ 🎯   │ Active │ Always     │ Always create, no dismiss     │
│ evidence      │ 📎   │ Active │ Never      │ Links to existing only        │
├───────────────┴──────┴────────┴────────────┴───────────────────────────────┤
│ ⚠️ Warning: Modifying activity types affects the entire system             │
│                                                                             │
│ [Add Custom Type] [Edit Rules] [View Type Usage Statistics]               │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.7.4 🏷️ Tag Management**

**System Tag Configuration**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          TAG MANAGEMENT                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ System Tags (Automatic):              │ Custom Tag Categories:             │
├───────────────────────────────────────┼────────────────────────────────────┤
│ trigger:human                         │ dept:* (Routing)                   │
│ trigger:integration                   │   • dept:security                  │
│ time:business-hours                   │   • dept:facilities                │
│ time:after-hours                      │   • dept:medical                   │
│ location:[building-zone]              │   • dept:it                        │
│ confidence:[0-100]                    │                                    │
│ integration_type:[system]             │ weather:* (Environmental)          │
│ created:[timestamp]                   │   • weather:clear                  │
│                                       │   • weather:rain                   │
│ Tag Rules:                            │   • weather:snow                   │
│ • Format: category:value              │   • weather:fog                    │
│ • All lowercase                       │                                    │
│ • No spaces (use hyphens)            │ shift:* (Operational)              │
│ • Max 50 characters                   │   • shift:day                      │
│                                       │   • shift:evening                  │
│                                       │   • shift:night                    │
├───────────────────────────────────────┴────────────────────────────────────┤
│ Tag Limits by Role:                                                        │
│ • Officers: 10 tags per activity                                           │
│ • Supervisors: 15 tags per activity                                        │
│ • Admins: Unlimited                                                        │
│                                                                             │
│ [Add Category] [Edit Tags] [View Tag Usage] [Export Tag Report]           │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.7.5 🔌 Integrations Page**

**Integration Management Interface**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTEGRATIONS                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ 🎥 Ambient AI Integration                    Status: [Placeholder]         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Configuration:                                                              │
│ API Endpoint: [________________________________]                          │
│ API Key:      [********************************]                          │
│ Webhook URL:  [________________________________]                          │
│                                                                             │
│ [Test Connection] [Save Configuration]                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ 📻 Radio Integration                         Status: [Placeholder]         │
├─────────────────────────────────────────────────────────────────────────────┤
│ Configuration:                                                              │
│ Radio System: [________________________________]                           │
│ Channel ID:   [________________________________]                           │
│ Auth Token:   [********************************]                           │
│                                                                             │
│ [Test Connection] [Save Configuration]                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ [+ Add Integration] (Disabled - Future MVP Expansion)                      │
│                                                                             │
│ ℹ️ Additional integrations will be available in future updates             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.7.6 📧 Notification Settings**

**Activity Notification Configuration**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        NOTIFICATION SETTINGS                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Email Configuration:                                                        │
│ SMTP Server:     [smtp.acmesecurity.com___________________________]       │
│ Port:            [587] Security: [STARTTLS ▼]                             │
│ From Address:    [notifications@acmesecurity.com__________________]       │
│                                                                             │
│ Activity Notifications:                                                     │
│ ┌─────────────────────────┬────────────┬─────────┬───────┬──────────┐    │
│ │ Event                   │ Email      │ SMS     │ Push  │ In-App    │    │
│ ├─────────────────────────┼────────────┼─────────┼───────┼──────────┤    │
│ │ Medical Activity        │ ✅ All     │ ✅ All  │ ✅    │ ✅       │    │
│ │ Security Breach         │ ✅ All     │ ✅ Sup+ │ ✅    │ ✅       │    │
│ │ Auto-Incident Created   │ ✅ Assigned│ ❌      │ ✅    │ ✅       │    │
│ │ BOL Match              │ ✅ All     │ ✅ All  │ ✅    │ ✅       │    │
│ │ High Confidence Alert   │ ✅ Sup+    │ ❌      │ ✅    │ ✅       │    │
│ │ Evidence Added          │ ❌         │ ❌      │ ❌    │ ✅       │    │
│ └─────────────────────────┴────────────┴─────────┴───────┴──────────┘    │
│                                                                             │
│ Notification Rules:                                                         │
│ • Batch similar notifications: [5 minute window ▼]                        │
│ • Quiet hours: [22:00] to [06:00] (except critical)                      │
│ • Escalation: If no response in [15 ▼] minutes                           │
│                                                                             │
│ [Save Notification Settings] [Send Test Notification]                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.7.7 🤖 AI Configuration**

**AI Assistant Settings**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI ASSISTANT SETTINGS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Buddy (Operational AI):                                                    │
│ • Activity Analysis:      ✅ Enabled                                       │
│ • Response Suggestions:   ✅ Enabled                                       │
│ • Auto-Dispatch:         ☐ Disabled (requires human confirmation)         │
│ • Confidence Threshold:   [75%] for suggestions                           │
│                                                                             │
│ Oracle (Investigative AI):                                                 │
│ • Pattern Analysis:       ✅ Enabled                                       │
│ • Cross-Activity Links:   ✅ Enabled                                       │
│ • Case Recommendations:   ✅ Enabled                                       │
│ • Analysis Depth:        [Deep - All historical data ▼]                   │
│                                                                             │
│ Coordinator (Admin AI):                                                    │
│ • Resource Optimization:  ✅ Enabled                                       │
│ • Schedule Suggestions:   ✅ Enabled                                       │
│ • System Health Alerts:   ✅ Enabled                                       │
│ • Automation Level:      [Suggest only - no auto-execution ▼]            │
│                                                                             │
│ Rate Limits:                                                               │
│ • Officers:      [100/hour]                                                │
│ • Supervisors:   [200/hour]                                                │
│ • Admins:        [Unlimited]                                               │
│                                                                             │
│ [Update AI Settings] [View AI Usage Statistics]                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Settings & Configuration**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | Settings are system-level, no parent required | [Organization Settings](#771-organization-settings) |
| **Cardinality** | One configuration set per organization | [Security Settings](#772-security-settings) |
| **Editable After Creation?** | Yes - Admin only with full audit trail | [All Settings Sections](#77-settings--configuration) |
| **Deletion/Archival Effects** | Cannot delete, only modify settings | N/A |
| **Mandatory Before Close?** | N/A - Settings persist | N/A |
| **Audit-Trail Requirement?** | All configuration changes logged with before/after values | [All Settings Sections](#77-settings--configuration) |
| **Edge-Case Handling** | Validation on all inputs, safe defaults, rollback capability | [Integration Settings](#775-integration-settings) |

**✔️ Logic Cross-check**: Settings & Configuration provides comprehensive control over the activity-first system, with careful validation and audit trails for all changes.

---

### **7.8 👁️ BOL Management**

**🎯 Purpose**: Multi-location Be-On-the-Lookout coordination creating `bol-event` activities with real-time matching and cross-site intelligence

#### **7.8.1 📊 Multi-Site BOL Dashboard**

**Activity-Integrated BOL Management**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         COMMAND CENTER BOL DASHBOARD                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🚨 ACTIVE BOLS: 12        🎯 BOL ACTIVITIES TODAY: 45      📍 SITES: 8/12  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🔴 CRITICAL BOL ACTIVITIES (Real-time)                                     │
│ ├─ ACT-2024-0234: BOL Match - Vehicle ABC123 @ HQ (98% confidence)         │
│ ├─ ACT-2024-0235: BOL Creation - Wanted Person John Doe (All Sites)        │
│ └─ ACT-2024-0236: BOL Update - Suspect spotted @ Warehouse (In Progress)   │
│                                                                             │
│ 🟡 ACTIVE BOL MONITORING                                                   │
│ ├─ BOL-2024-0156: Person (3 activity matches in 24h)                      │
│ ├─ BOL-2024-0189: Vehicle (1 activity match today)                        │
│ └─ BOL-2024-0203: Equipment (0 matches, expires in 2 days)                │
│                                                                             │
│ 🔄 Activity Integration: [📋 View All BOL Activities] [🤖 Pattern Analysis] │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Enhanced BOL List View**

| **Column** | **Description** | **Activity Integration** | **Format** |
|------------|-----------------|--------------------------|------------|
| **🆔 BOL ID** | Unique identifier | Links to all related activities | BOL-YYYY-XXXX |
| **🏷️ Subject Type** | Person/Vehicle/Item/Pattern | Determines activity tags | Icon + Type |
| **📋 Activity Count** | Related bol-event activities | Real-time activity tracking | Count with trend |
| **⚡ Status** | Active/Matched/Expired | Based on activity status | Status + Activity link |
| **🎯 Last Match** | Most recent activity | Links to specific activity | Time + Location |
| **📍 Distribution** | Location coverage | Activity creation scope | Sites covered |
| **⏰ Expires** | Timezone-aware expiry | Auto-creates expiry activity | Countdown |

#### **7.8.2 ➕ Enhanced BOL Creation**

**BOL Creation with Auto-Activity**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      CREATE BOL (AUTO-ACTIVITY ENABLED)                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ ⚡ This will create a BOL and generate a 'bol-event' activity             │
│                                                                             │
│ Distribution Scope: [🌐 All Sites ▼]                                       │
│ Priority Level: [🔴 Critical ▼]                                           │
│ Subject Type: [👤 Person ▼]                                               │
│                                                                             │
│ 📋 Activity Generation Settings:                                           │
│ • Activity Type: bol-event (automatic)                                     │
│ • Initial Status: detecting                                                │
│ • Auto-Incident: ✅ Yes (BOL events always create incidents)              │
│ • Tags: Auto-generated based on BOL details                               │
│                                                                             │
│ 🤖 Oracle AI Assistance:                                                  │
│ "Creating this BOL will generate an activity and incident. Based on the   │
│ description, I recommend setting priority as Critical and including       │
│ these locations in distribution: Sites A, B, C (high traffic areas)."     │
│                                                                             │
│ [Create BOL & Activity] [Save as Draft] [Cancel]                          │
└─────────────────────────────────────────────────────────────────────────────┘
```

**BOL Activity Creation Flow**
1. User creates BOL with details
2. System automatically creates Activity:
   - Type: `bol-event`
   - Title: "[BOL Type]: [Subject Name/Description]"
   - Status: `detecting`
   - Tags: `trigger:human`, `bol:active`, `priority:[level]`
3. Auto-incident created per rules (BOL always creates incident)
4. Activity distributed to all specified locations
5. Real-time monitoring begins

#### **7.8.3 🧠 Oracle-Enhanced BOL Intelligence**

**BOL Activity Pattern Analysis**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ORACLE BOL ACTIVITY ANALYSIS                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ BOL-2024-0156: "Wanted Person - John Doe"                                  │
│ Activity Analysis: 23 bol-event activities in 7 days                       │
│                                                                             │
│ 🤖 Oracle Pattern Recognition:                                             │
│ • 15 patrol activities mention similar person (prior to BOL)              │
│ • 8 bol-event activities show cross-site movement pattern                 │
│ • Peak activity times: 14:00-16:00 (lunch hours)                         │
│ • Correlation with theft incidents: 89% confidence                        │
│                                                                             │
│ 📊 Activity-Based Insights:                                               │
│ • Most frequent locations: Building A entrance, Parking Lot C             │
│ • Associated vehicle from patrol activities: White sedan                  │
│ • Behavioral pattern: Avoids main security checkpoints                    │
│                                                                             │
│ 🎯 Recommended Actions:                                                    │
│ ✅ Review all patrol activities from past 30 days                        │
│ ✅ Create evidence activities for witness statements                      │
│ ✅ Enhance monitoring during identified peak times                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.8.4 🎯 Real-Time BOL Activity Matching**

**Activity-Based BOL Matching**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      REAL-TIME BOL ACTIVITY CREATION                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ ⚡ LIVE BOL MATCH DETECTED                                                 │
│                                                                             │
│ Creating Activity: ACT-2024-0567                                          │
│ Type: bol-event                                                            │
│ Title: "BOL Match: John Doe - 96% confidence"                             │
│ Status: detecting → responding (guard dispatched)                          │
│                                                                             │
│ Activity Details:                                                          │
│ • Trigger: integration (Ambient.ai facial recognition)                    │
│ • Confidence: 96%                                                         │
│ • Location: Site A - Building 1 - Main Entrance                          │
│ • Tags: trigger:integration, bol:match, confidence:96, priority:critical  │
│                                                                             │
│ Auto-Actions Taken:                                                        │
│ ✅ Incident created: INC-2024-0234 (auto-rule: bol-event = incident)     │
│ ✅ Guard Unit 7 dispatched                                                │
│ ✅ Adjacent cameras focused on subject                                    │
│ ✅ Cross-site alert issued                                                │
│                                                                             │
│ [View Activity] [Update BOL] [Add Evidence] [Close BOL]                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.8.5 🌐 Cross-Site BOL Activity Coordination**

**Multi-Location BOL Activity Flow**

| **BOL Event** | **Activity Created** | **Distribution** | **Auto-Incident** |
|---------------|---------------------|------------------|-------------------|
| **BOL Creation** | `bol-event` activity at creating site | All specified sites | Yes - Always |
| **BOL Match** | `bol-event` activity at detection site | Alert all sites | Yes - Always |
| **BOL Update** | `evidence` activity linked to BOL | Update subscribers | Links to existing |
| **BOL Expiry** | `bol-event` activity (status: resolved) | Notify all sites | Updates existing |

**Cross-Site Activity Coordination**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CROSS-SITE BOL ACTIVITY TRACKING                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ BOL-2024-0156 Activity Distribution (Last 24 Hours):                       │
│                                                                             │
│ 🏢 Site A: 5 activities                                                    │
│ ├─ ACT-0234: BOL creation (bol-event) - 08:00                            │
│ ├─ ACT-0267: Possible match (bol-event) - 10:30                          │
│ └─ ACT-0289: Confirmed sighting (bol-event) - 14:15                      │
│                                                                             │
│ 🏢 Site B: 2 activities                                                    │
│ ├─ ACT-0245: BOL received (bol-event) - 08:02                            │
│ └─ ACT-0291: Vehicle match (bol-event) - 14:45                           │
│                                                                             │
│ 🏢 Site C: 1 activity                                                      │
│ └─ ACT-0246: BOL acknowledged (bol-event) - 08:03                        │
│                                                                             │
│ Activity Pattern: Subject moving from Site A → Site B                     │
│ Oracle Confidence: 91% - Recommend Site B lockdown                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.8.6 📱 Enhanced BOL Resolution**

**BOL Resolution Creating Final Activity**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         BOL RESOLUTION WORKFLOW                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ BOL-2024-0156: "Wanted Person - John Doe"                                  │
│ Total Activities Generated: 14 bol-event, 6 evidence                       │
│                                                                             │
│ Resolution Type: [✅ Subject Located ▼]                                    │
│                                                                             │
│ Final Activity Creation:                                                    │
│ • Type: bol-event                                                         │
│ • Title: "BOL Resolved: Subject located and detained"                     │
│ • Status: resolved                                                        │
│ • Tags: trigger:human, bol:resolved, resolution:located                   │
│                                                                             │
│ Resolution Details: [Required - min 100 characters]                        │
│ "Subject located at Site B parking lot at 15:45. Local law enforcement    │
│ contacted and subject detained without incident. All sites notified."      │
│                                                                             │
│ Activity Links:                                                            │
│ • Links to Incident: INC-2024-0234                                       │
│ • Links to Case: CASE-2024-0089 (auto-created)                          │
│ • Evidence Activities: 6 photos, 2 videos, 3 witness statements          │
│                                                                             │
│ [Resolve BOL & Create Activity] [Cancel]                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - BOL Management**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | BOL creates `bol-event` activity automatically, no parent required | [Enhanced BOL Creation](#782-enhanced-bol-creation) |
| **Cardinality** | One BOL → many `bol-event` activities across multiple sites | [Cross-Site Coordination](#785-cross-site-bol-activity-coordination) |
| **Editable After Creation?** | BOL editable, creates new `evidence` activities for updates | [Oracle-Enhanced Intelligence](#783-oracle-enhanced-bol-intelligence) |
| **Deletion/Archival Effects** | No deletion, resolution creates final `bol-event` activity with status resolved | [Enhanced BOL Resolution](#786-enhanced-bol-resolution) |
| **Mandatory Before Close?** | Resolution details required, final activity must be created | [BOL Resolution Workflow](#786-enhanced-bol-resolution) |
| **Audit-Trail Requirement?** | All BOL actions create activities which are fully audited | [Real-Time BOL Matching](#784-real-time-bol-activity-matching) |
| **Edge-Case Handling** | Offline sites queue activities, confidence thresholds for auto-matching | [Activity Creation Flow](#782-enhanced-bol-creation) |

**✔️ Logic Cross-check**: BOL Management fully integrated with Activity-first architecture, creating `bol-event` activities for all BOL operations with complete audit trail.

---

### **7.9 📝 Passdowns**

**🎯 Purpose**: Shift communication and handover documentation with comprehensive activity summaries and cross-site coordination

#### **7.9.1 📊 Passdown Dashboard with Activities**

**Activity-Enhanced Passdown View**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COMMAND CENTER PASSDOWN DASHBOARD                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🕐 Current Shift: Day (06:00-14:00)     📋 Activities This Shift: 89      │
│ 📝 Passdowns Today: 23                  🔄 Unresolved Activities: 12      │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📋 SHIFT ACTIVITY SUMMARY                                                  │
│ ├─ Patrol Activities: 45 completed, 3 areas pending                       │
│ ├─ Alert Activities: 23 processed, 5 escalated to incidents               │
│ ├─ BOL Activities: 8 matches investigated, 1 confirmed                    │
│ └─ Evidence Activities: 12 added to ongoing cases                        │
│                                                                             │
│ 🚨 CRITICAL ACTIVITIES REQUIRING HANDOVER                                  │
│ ├─ ACT-2024-0567: Medical emergency - ongoing response                    │
│ ├─ ACT-2024-0568: Security breach - investigation in progress            │
│ └─ ACT-2024-0569: BOL match - awaiting law enforcement                   │
│                                                                             │
│ 🔄 Real-Time Updates: [📋 Activity Stream] [🤖 AI Summary] [📊 Stats]      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.9.2 ➕ Enhanced Passdown Creation with Activities**

**Activity-Integrated Passdown Form**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CREATE SHIFT PASSDOWN WITH ACTIVITIES                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ Shift: [🌅 Day Shift ▼] → [🌃 Evening Shift ▼]   Date: 2024-01-15         │
│                                                                             │
│ 📋 ACTIVITY SUMMARY (Auto-Generated)                                       │
│ Your shift processed 89 activities:                                        │
│ • Patrol: 45 ✅  • Alerts: 23 (5 → incidents)  • BOL: 8 (1 confirmed)    │
│                                                                             │
│ 🤖 Coordinator AI Activity Analysis:                                      │
│ "High activity shift with 23% increase over average. Key patterns:        │
│ • Increased alerts in Building B (investigate possible cause)             │
│ • 3 evidence activities added to CASE-2024-0089                          │
│ • All critical activities resolved except ACT-0569 (BOL match)"          │
│                                                                             │
│ Key Activities to Highlight:                                              │
│ ☑️ ACT-0567: Medical emergency resolved, follow-up needed                 │
│ ☑️ ACT-0569: Active BOL match, law enforcement en route                  │
│ ☐ ACT-0543: Patrol found damage in Zone C (add manually)                 │
│                                                                             │
│ Additional Notes:                                                          │
│ [Building B camera 5 offline - maintenance scheduled for 16:00________]    │
│                                                                             │
│ [Create Passdown] [Preview] [Add More Activities]                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.9.3 🤖 Activity-Based Passdown Intelligence**

**Coordinator AI Activity Summary**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    COORDINATOR PASSDOWN ACTIVITY ANALYSIS                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ Shift Activity Pattern Analysis:                                           │
│                                                                             │
│ 📊 ACTIVITY BREAKDOWN BY TYPE:                                            │
│ • Patrol: 45 activities (90% completion rate) ✅                          │
│ • Alert: 23 activities (5 escalated = 22% escalation rate) ⚠️            │
│ • Medical: 2 activities (both resolved within SLA) ✅                     │
│ • Security-breach: 1 activity (investigation ongoing) 🔄                  │
│ • BOL-event: 8 activities (1 confirmed match) 🎯                          │
│ • Evidence: 12 activities (supporting 3 cases) 📎                         │
│                                                                             │
│ 🔮 PATTERN INSIGHTS:                                                      │
│ • Alert clustering in Building B suggests systematic issue                 │
│ • Patrol activities show 15% increase in Zone C                          │
│ • Evidence collection rate improved by 30% this shift                     │
│                                                                             │
│ 📋 RECOMMENDED PASSDOWN PRIORITIES:                                       │
│ 1. Brief on ongoing BOL situation (ACT-0569)                             │
│ 2. Highlight Building B alert pattern for investigation                   │
│ 3. Ensure Zone C patrol coverage continues (damage found)                │
│ 4. Update on medical incident follow-up requirements                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.9.4 🌐 Cross-Site Activity Coordination**

**Multi-Location Activity Passdown**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CROSS-SITE ACTIVITY COORDINATION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🌐 MULTI-SITE ACTIVITY SUMMARY:                                           │
│                                                                             │
│ Site A (HQ): 134 activities                                                │
│ • High patrol activity (67 completed)                                      │
│ • 3 BOL-event activities related to corporate espionage case             │
│ • Resource sharing: Sent 2 guards to Site B                              │
│                                                                             │
│ Site B (Warehouse): 89 activities                                          │
│ • Alert spike in loading dock area (23 alerts)                           │
│ • Under investigation for systematic breach attempts                      │
│ • Received guard support from Site A                                      │
│                                                                             │
│ Site C (Remote): 45 activities                                             │
│ • Normal patrol patterns                                                  │
│ • 1 property-damage activity requiring follow-up                         │
│ • Stable operations                                                       │
│                                                                             │
│ 🔄 CROSS-SITE ACTIVITY LINKS:                                             │
│ • BOL-event activities suggest coordinated surveillance                   │
│ • Alert patterns at Site B may be related to Site A incidents           │
│ • Recommend enhanced monitoring at all sites                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.9.5 📱 Enhanced Passdown Detail with Activities**

**Activity-Rich Passdown View**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      PASSDOWN DETAIL WITH ACTIVITIES                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 📝 Passdown: PD-2024-1127-EVE-001                                         │
│ 📍 Coverage: All Sites | 🕐 Evening Shift (14:00-22:00 EST)               │
│ 👤 Author: Sarah Johnson (Supervisor, Site A)                             │
│                                                                             │
│ 📋 KEY ACTIVITIES FROM DAY SHIFT:                                         │
│                                                                             │
│ 🚨 Critical Activities:                                                   │
│ • ACT-0569 (bol-event): Active BOL match awaiting police                 │
│   Status: responding | Assigned: Officer Garcia                          │
│   Next: Law enforcement arrival expected 14:30                           │
│                                                                             │
│ • ACT-0567 (medical): Resolved but requires incident report              │
│   Status: resolved | Follow-up: Complete OSHA documentation             │
│                                                                             │
│ ⚠️ Patterns Requiring Attention:                                          │
│ • 23 alert activities in Building B (abnormal increase)                  │
│   Triggers: All integration-based from door sensors                      │
│   Action: Investigate potential sensor malfunction                       │
│                                                                             │
│ • Zone C patrol activities found property damage                         │
│   Evidence activities created: ACT-0588, ACT-0589                       │
│   Action: Insurance documentation needed                                  │
│                                                                             │
│ 📊 SHIFT STATISTICS:                                                      │
│ • Total Activities: 89 (↑23% from average)                              │
│ • Auto-Incidents: 8 created, 2 dismissed by supervisor                  │
│ • Response Times: Avg 2.3 min (within SLA)                              │
│                                                                             │
│ [View All Activities] [Print Report] [Add Comment]                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Passdowns**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | Yes - Passdowns reference activities but don't require specific ones | [Passdown Creation](#792-enhanced-passdown-creation-with-activities) |
| **Cardinality** | One passdown → many activities (referenced, not owned) | [Activity-Based Intelligence](#793-activity-based-passdown-intelligence) |
| **Editable After Creation?** | Yes - Author and supervisors can edit within 24 hours | Original rules maintained |
| **Deletion/Archival Effects** | No deletion, archived after 90 days, activity references preserved | Original rules maintained |
| **Mandatory Before Close?** | N/A - No close status, activity summaries auto-generated | [Cross-Site Coordination](#794-cross-site-activity-coordination) |
| **Audit-Trail Requirement?** | All changes logged, activity references tracked | Original audit rules maintained |
| **Edge-Case Handling** | Auto-generates activity summaries even if no manual content added | [Passdown Detail](#795-enhanced-passdown-detail-with-activities) |

**✔️ Logic Cross-check**: Passdowns fully integrated with Activity system, providing comprehensive shift handover with activity summaries and pattern analysis.

---

### **7.10 🤖 Orchestr8 AI Assistant** 🆕 *(Enhanced in v0.1)*

**🎯 Purpose**: Global AI assistant with natural language processing, available across all modules for enhanced productivity

#### **7.10.1 🧠 Orchestr8 AI Architecture**

**Technology Stack**
- **LLM**: GPT-4.0 mini (cost-efficient, fast responses)
- **Orchestration**: N8N workflow automation
- **Voice Processing**: OpenAI Whisper for transcription
- **Architecture**: Modular design for easy LLM switching

**Core Capabilities**
- Activity parsing and categorization from voice/text
- Simple report generation and summaries
- Basic pattern recognition
- Operational guidance and suggestions
- Natural language interaction

**Data Access Scope**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ORCHESTR8 AI DATA ACCESS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ ✅ Activities: Read activities from user's location                        │
│ ✅ Incidents: Read current incidents                                       │
│ ✅ Reports: Generate shift summaries                                       │
│ ✅ Patterns: Basic activity analysis                                       │
│ ❌ Complex Analysis: Reserved for future versions                          │
│ ❌ Cross-Site Data: Limited to current location                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.10.2 🤖 Orchestr8 AI Interface**

**AI Assistant Interface (MVP)**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       ORCHESTR8 AI ASSISTANT                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ 💬 Conversation:                                                           │
│                                                                             │
│ User: "What happened in Zone A today?"                                    │
│                                                                             │
│ 🤖 Orchestr8: "Zone A Activity Summary:                                   │
│                                                                             │
│ Today: 15 activities total                                                 │
│ - 12 patrols completed                                                    │
│ - 2 alerts (both resolved)                                                │
│ - 1 property damage report                                                │
│                                                                             │
│ The property damage was a broken window in Building 2."                   │
│                                                                             │
│ User: "Create activity for medical emergency in lobby"                    │
│                                                                             │
│ 🤖 Orchestr8: "Creating medical emergency activity:                       │
│ - Type: Medical                                                           │
│ - Location: Lobby                                                         │
│ - Status: Detecting                                                       │
│ - Auto-incident: Yes (medical always creates incident)                   │
│                                                                             │
│ Activity ACT-2024-0246 created.                                           │
│ Incident INC-2024-0091 auto-created."                                    │
│                                                                             │
│ [Type your message...]                                          [Send]     │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.10.3 📝 MVP Task Capabilities**

**Orchestr8 AI Task Automation (MVP)**

| **Task Category** | **Capabilities** | **Example Commands** |
|-------------------|------------------|---------------------|
| **Activity Creation** | Parse voice/text to create activities | "Broken window in Building 2" |
| **Simple Summaries** | Count activities by type/location | "How many patrols today?" |
| **Basic Search** | Find recent activities | "Show alerts from last hour" |
| **Status Updates** | Quick activity status changes | "Mark patrol complete" |
| **Voice Processing** | Transcribe voice memos via Telegram | Voice memo → Activity |

#### **7.10.4 🔐 AI Permissions & Limits**

#### **7.10.5 🆕 Global AI Assistant Enhancement (v0.1)**

**🎯 Purpose**: Expand Orchestr8 to be available everywhere with enhanced capabilities

**Floating Widget Interface**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          GLOBAL AI ASSISTANT                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ 🤖 Always Available:                                                        │
│ • Floating widget (bottom-right corner)                                    │
│ • Keyboard shortcut: Ctrl/Cmd + K                                         │
│ • Context menu integration                                                 │
│ • Persistent across navigation                                             │
│                                                                             │
│ 💬 Natural Language Commands:                                              │
│ User: "Show me all medical incidents from last week"                      │
│ AI: "Found 3 medical incidents. Here they are..."                         │
│     [INC-0234] [INC-0267] [INC-0289]                                      │
│                                                                             │
│ User: "Create a patrol activity for Building B"                           │
│ AI: "I'll create a patrol activity. Please confirm:"                      │
│     Type: Patrol                                                           │
│     Location: Building B                                                   │
│     [Confirm] [Modify] [Cancel]                                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Enhanced Natural Language Processing**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       COMMAND UNDERSTANDING                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Navigation Commands:                                                        │
│ • "Show me case 123" → Navigate to CASE-2024-0123                        │
│ • "Go to reports" → Navigate to Reports page                             │
│ • "Open user management" → Navigate to User Management                   │
│                                                                             │
│ Search Commands:                                                            │
│ • "Find all alerts in Building A" → Search with filters                  │
│ • "Show security breaches today" → Filtered activity list                │
│ • "Search for John Smith" → Global entity search                         │
│                                                                             │
│ Action Commands:                                                            │
│ • "Create incident for broken window" → Incident creation wizard         │
│ • "Add note to case 456" → Case update interface                         │
│ • "Generate daily report" → Report generation                            │
│                                                                             │
│ Analysis Commands:                                                          │
│ • "What patterns do you see?" → AI pattern analysis                      │
│ • "Summarize today's activities" → Quick summary                        │
│ • "Compare this week to last week" → Trend analysis                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Context Awareness System**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AI CONTEXT TRACKING                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ Current Context:                                                            │
│ • Page: Case Management                                                    │
│ • Entity: CASE-2024-0123                                                  │
│ • User: Supervisor Johnson                                                 │
│ • Location: Site A                                                         │
│                                                                             │
│ Available Actions:                                                          │
│ • Update case status                                                       │
│ • Add investigation notes                                                  │
│ • Link additional incidents                                                │
│ • Generate case report                                                     │
│ • View related activities                                                  │
│                                                                             │
│ Smart Suggestions:                                                          │
│ "I notice this case has 3 unreviewed activities. Would you like to        │
│  review them now?"                                                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Action Confirmation Framework**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ACTION CONFIRMATION                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ AI Action Request:                                                          │
│ "Create incident for medical emergency in Building C"                      │
│                                                                             │
│ Proposed Action:                                                            │
│ ┌─────────────────────────────────────────────────────────────┐            │
│ │ Create Incident:                                            │            │
│ │ • Type: Medical Emergency                                   │            │
│ │ • Location: Building C                                      │            │
│ │ • Priority: Critical (auto-set)                             │            │
│ │ • Auto-create: Yes (medical always creates incident)       │            │
│ │ • Assigned to: Nearest available guard                      │            │
│ └─────────────────────────────────────────────────────────────┘            │
│                                                                             │
│ [✓ Confirm & Execute] [✏️ Modify Details] [✗ Cancel]                       │
│                                                                             │
│ ⚠️ This action will create an incident and dispatch guards                 │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Quick Actions Menu**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         QUICK AI ACTIONS                                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ Frequently Used:                                                            │
│ 🔍 Search activities      📋 Create activity     📊 Generate report       │
│ 🚨 View incidents         📁 Open case           👥 Find user             │
│                                                                             │
│ Context Actions (Case Page):                                                │
│ 📝 Add case note          🔗 Link incident       📎 Attach evidence       │
│ 👤 Assign investigator    📊 Case insights       ⏰ Set reminder          │
└─────────────────────────────────────────────────────────────────────────────┘
```

**AI Integration Points**
- Available on every page via floating widget
- Keyboard shortcut (Ctrl/Cmd + K) from anywhere
- Right-click context menu "Ask AI about this"
- Maintains conversation context across pages
- WebSocket connection for real-time responses

**Enhanced Capabilities (v0.1)**
1. **Global Availability**: No longer limited to specific contexts
2. **Natural Language Actions**: Execute commands in plain English
3. **Context Intelligence**: Knows current page and suggests relevant actions
4. **Confirmation Workflow**: All data changes require explicit approval
5. **Quick Actions**: One-click access to common tasks
6. **Cross-Module Navigation**: "Show me..." commands work everywhere

**Orchestr8 AI Constraints**
- Cannot perform actions beyond user's permissions
- All AI actions are logged in audit trail
- Cannot delete or modify historical data
- Requires confirmation for data-modifying actions
- Rate limited to prevent abuse

---

### **7.11 📋 Audit Logs**

**🎯 Purpose**: Comprehensive audit trail for all activity operations, type changes, auto-incident decisions, and tag management

#### **7.11.1 🌐 Activity-Enhanced Audit Architecture**

**Activity Audit Categories**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        ACTIVITY AUDIT CATEGORIES                           │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ACTIVITY LIFECYCLE        TYPE CHANGES           AUTO-INCIDENT DECISIONS  │
│  ├─ Creation              ├─ Type Modified       ├─ Rule Triggered        │
│  ├─ Status Changes        ├─ Justification       ├─ Incident Created      │
│  ├─ Assignment           ├─ Impact Analysis     ├─ Supervisor Dismissal   │
│  └─ Resolution           └─ Re-routing          └─ Rule Bypassed         │
│                                                                             │
│  TAG OPERATIONS          INTEGRATION EVENTS      ARCHIVAL ACTIONS         │
│  ├─ Tag Added            ├─ Activity Created    ├─ Activities Archived   │
│  ├─ Tag Removed          ├─ Confidence Score    ├─ Retention Extended    │
│  ├─ Category Created     ├─ Source System       ├─ Restoration Request   │
│  └─ Bulk Tagging        └─ Data Mapping        └─ Purge Operations      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.11.2 📊 Activity-Specific Audit Events**

**Enhanced Audit Log Entries**

| **Audit Event** | **Details Captured** | **Activity Context** |
|-----------------|---------------------|----------------------|
| **ACTIVITY_CREATED** | Type, trigger, initial tags, confidence | Full creation context |
| **ACTIVITY_TYPE_CHANGED** | Old type → New type, reason, impact | Auto-incident implications |
| **AUTO_INCIDENT_CREATED** | Activity ID, rule triggered, incident created | Rule justification |
| **AUTO_INCIDENT_DISMISSED** | Supervisor ID, dismissal reason, activity outcome | Override tracking |
| **ACTIVITY_TAG_ADDED** | Tag name, category, added by, purpose | Tag permission validation |
| **ACTIVITY_TAG_REMOVED** | Tag name, removed by, justification | Audit tag changes |
| **ACTIVITY_STATUS_CHANGED** | Old → New status, changed by, timestamp | Workflow tracking |
| **ACTIVITY_ARCHIVED** | Archive reason, retention period, batch ID | Compliance tracking |

**Sample Activity Audit Trail**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ACTIVITY AUDIT TRAIL - ACT-2024-0234                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 14:23:15 | ACTIVITY_CREATED                                     │
│ • Type: alert | Trigger: integration | Source: Ambient.ai                  │
│ • Confidence: 89% | Location: Site A-B1                                    │
│ • Auto-tags: trigger:integration, location:building-a, confidence:89       │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 14:23:16 | AUTO_INCIDENT_EVALUATED                             │
│ • Rule: alert + confidence>80 + after-hours = CREATE INCIDENT             │
│ • Decision: CREATE | Incident: INC-2024-0445                              │
│ • Justification: Meets all criteria for auto-escalation                   │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 14:23:45 | ACTIVITY_TYPE_CHANGED                               │
│ • Changed by: Officer Wilson | Old: alert | New: security-breach           │
│ • Reason: "Visual confirmation of forced entry"                            │
│ • Impact: Incident priority elevated to HIGH                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 14:24:12 | ACTIVITY_TAG_ADDED                                  │
│ • Tag: priority:critical | Added by: Supervisor Chen                      │
│ • Category: priority | Permission: Supervisor+ required                    │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 14:45:00 | ACTIVITY_STATUS_CHANGED                             │
│ • Old: detecting | New: resolved | Changed by: Officer Wilson             │
│ • Resolution: "Subject apprehended, area secured"                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.11.3 🎛️ Auto-Incident Decision Logging**

**Detailed Auto-Incident Audit**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     AUTO-INCIDENT DECISION AUDIT LOG                       │
├─────────────────────────────────────────────────────────────────────────────┤
│ Time     │ Activity    │ Type      │ Decision │ Reason                     │
├──────────┼─────────────┼───────────┼──────────┼────────────────────────────┤
│ 14:23:16 │ ACT-0234   │ alert     │ CREATE   │ confidence>80 + after-hrs  │
│ 14:25:43 │ ACT-0235   │ medical   │ CREATE   │ medical always → incident  │
│ 14:27:19 │ ACT-0236   │ patrol    │ SKIP     │ patrol never → incident    │
│ 14:28:55 │ ACT-0237   │ property  │ SKIP     │ confidence:65 < 75 thresh  │
│ 14:30:12 │ ACT-0238   │ bol-event │ CREATE   │ bol always → incident      │
│ 14:31:45 │ ACT-0239   │ alert     │ DISMISS  │ Supervisor override        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Summary: 6 decisions, 3 incidents created, 1 dismissed, 2 skipped         │
│ Dismissal Rate: 16.7% (within acceptable range)                           │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.11.4 🏷️ Tag Operation Auditing**

**Tag Management Audit Trail**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         TAG OPERATION AUDIT LOG                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 08:00:00 | TAG_CATEGORY_CREATED                                 │
│ • Category: evidence-type | Created by: Admin Roberts                      │
│ • Values: photo, video, document, physical, digital                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 09:15:30 | ACTIVITY_TAG_ADDED                                  │
│ • Activity: ACT-0234 | Tag: evidence-type:photo                           │
│ • Added by: Officer Liu | Permission check: PASS (10 tag limit)           │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 10:45:00 | TAG_REMOVED                                         │
│ • Activity: ACT-0156 | Tag: priority:low                                  │
│ • Removed by: Supervisor Chen | Reason: "Escalated to high"               │
│ • Permission check: PASS (Supervisor can remove non-system tags)          │
├─────────────────────────────────────────────────────────────────────────────┤
│ 2024-01-15 11:00:00 | BULK_TAG_OPERATION                                 │
│ • Activities: 45 patrol activities | Tag added: shift:night               │
│ • Performed by: Admin Roberts | Justification: "Shift categorization"     │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.11.5 📊 Activity Audit Analytics**

**Activity Operation Metrics**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      ACTIVITY AUDIT ANALYTICS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│ Activity Operations (Last 30 Days):                                        │
│                                                                             │
│ TYPE CHANGES:                                                             │
│ • Total: 234 changes across 12,847 activities (1.8%)                     │
│ • Most common: alert → security-breach (45%)                             │
│ • By role: Officers 89%, Supervisors 11%                                 │
│ • Average time to change: 3.2 minutes after creation                     │
│                                                                             │
│ AUTO-INCIDENT DECISIONS:                                                  │
│ • Total evaluated: 3,456 activities                                      │
│ • Created incidents: 2,891 (83.6%)                                       │
│ • Skipped by rules: 456 (13.2%)                                         │
│ • Supervisor dismissals: 109 (3.2%)                                      │
│ • Rule effectiveness: 96.8% accuracy                                     │
│                                                                             │
│ TAG OPERATIONS:                                                           │
│ • Tags added: 45,678 (avg 3.6 per activity)                             │
│ • Tags removed: 2,345 (5.1% of additions)                               │
│ • Most used: location:* (100%), time:* (98%), trigger:* (100%)         │
│ • User-added: weather:*, priority:*, dept:*                             │
│                                                                             │
│ COMPLIANCE METRICS:                                                       │
│ • All activities have required audit trail: ✅ 100%                      │
│ • Type changes documented with reason: ✅ 100%                           │
│ • Auto-incident decisions logged: ✅ 100%                                │
│ • Tag permissions enforced: ✅ 100% (0 violations)                       │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Audit Logs**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | Audit logs automatically created for all activity operations | [Activity Audit Architecture](#7111-activity-enhanced-audit-architecture) |
| **Cardinality** | Many audit entries per activity, tracking all operations | [Activity-Specific Events](#7112-activity-specific-audit-events) |
| **Editable After Creation?** | No - Audit logs are immutable | Original immutability maintained |
| **Deletion/Archival Effects** | Cannot be deleted, permanent retention for activity audits | Original retention rules |
| **Mandatory Before Close?** | N/A - Automatic generation for all activity operations | Automatic |
| **Audit-Trail Requirement?** | Self-auditing system tracks all activity-related changes | [Auto-Incident Logging](#7113-auto-incident-decision-logging) |
| **Edge-Case Handling** | Captures failed operations, permission denials, system decisions | [Tag Operation Auditing](#7114-tag-operation-auditing) |

**✔️ Logic Cross-check**: Audit system comprehensively tracks all Activity operations including type changes, auto-incident decisions, and tag management with complete immutability.

---

### **7.12 🏢 Location Management**

**🎯 Purpose**: Location hierarchy management enhanced with activity-based metrics, routing rules, and type permissions

#### **7.12.1 🌍 Activity-Enhanced Location Structure**

**Location Hierarchy with Activity Context**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    LOCATION HIERARCHY WITH ACTIVITIES                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ACME Corp (12,847 activities/month)                                       │
│  └── North America (8,234 activities)                                       │
│      └── Site A - HQ (4,567 activities)                                    │
│          └── Building 1 (2,345 activities)                                 │
│              └── Floor 3 (567 activities)                                  │
│                  └── Zone 3A (123 activities)                              │
│                      • Patrol: 89                                          │
│                      • Alert: 23                                           │
│                      • Evidence: 11                                        │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Activity Metrics by Location**

| **Location Level** | **Activity Metrics** | **Routing Rules** |
|-------------------|---------------------|-------------------|
| **Organization** | Total activity volume, type distribution | Global activity policies |
| **Region** | Regional patterns, compliance metrics | Regional auto-incident rules |
| **Site** | Site-specific activity types, volumes | Site-based routing and tags |
| **Building** | Building activity density, hot spots | Building-specific thresholds |
| **Zone** | Detailed activity tracking, patterns | Zone-based alert sensitivity |

#### **7.12.2 🏗️ Activity-Based Location Configuration**

**Location Activity Settings**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LOCATION ACTIVITY CONFIGURATION                        │
├─────────────────────────────────────────────────────────────────────────────┤
│ Location: Site A → Building 1 → Floor 3                                    │
│                                                                             │
│ ACTIVITY ROUTING RULES:                                                    │
│ • Default activity assignment: Guards in Zone 3A                          │
│ • Auto-escalation: Activities unacknowledged for 5 minutes                │
│ • Priority boost: Medical and security-breach +1 level                    │
│                                                                             │
│ ACTIVITY TYPE PERMISSIONS:                                                 │
│ ✅ patrol - All guards can create                                         │
│ ✅ alert - Auto-created by integrations only                              │
│ ✅ medical - All staff can create (emergency)                             │
│ ⚠️ security-breach - Requires supervisor approval                         │
│ ✅ property-damage - All guards can create                                │
│ ✅ bol-event - Supervisors and above                                      │
│ ✅ evidence - All staff can create                                         │
│                                                                             │
│ AUTO-INCIDENT THRESHOLDS:                                                 │
│ • Alert confidence: 75% (5% lower than global)                            │
│ • After-hours definition: 18:00 - 06:00                                   │
│ • Response time SLA: 3 minutes (critical areas)                           │
│                                                                             │
│ ACTIVITY VOLUME LIMITS:                                                   │
│ • Expected daily: 150-200 activities                                      │
│ • Alert threshold: >300/day triggers investigation                        │
│ • Patrol minimum: 24 per shift required                                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.12.3 👥 Activity-Based Resource Allocation**

**Resource Planning by Activity Volume**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    ACTIVITY-BASED RESOURCE ALLOCATION                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ Site A Resource Analysis:                                                   │
│                                                                             │
│ ACTIVITY LOAD BY BUILDING:                                                 │
│ Building 1: 234 activities/day [████████░░] 80% capacity                  │
│ Building 2: 156 activities/day [██████░░░░] 60% capacity                  │
│ Building 3: 89 activities/day  [███░░░░░░░] 30% capacity                  │
│                                                                             │
│ GUARD ALLOCATION BY ACTIVITY DENSITY:                                      │
│ • Building 1: 8 guards (29 activities per guard)                          │
│ • Building 2: 5 guards (31 activities per guard)                          │
│ • Building 3: 3 guards (30 activities per guard) ✅ Optimal               │
│                                                                             │
│ 🤖 Coordinator Recommendation:                                            │
│ "Reallocate 1 guard from Building 3 to Building 1 during peak hours      │
│ (14:00-16:00) when activity volume increases 40%"                         │
│                                                                             │
│ ACTIVITY TYPE SPECIALIZATION:                                             │
│ • Medical response team: Cover all buildings (2 activities/day avg)       │
│ • Evidence specialists: Focus on Building 1 (45% of evidence activities)  │
│ • Patrol optimization: Reduce overlap in low-activity zones               │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.12.4 🔄 Cross-Site Activity Coordination**

**Multi-Location Activity Patterns**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    CROSS-SITE ACTIVITY CORRELATION                         │
├─────────────────────────────────────────────────────────────────────────────┤
│ ACTIVITY PATTERN ANALYSIS:                                                 │
│                                                                             │
│ Similar Patterns Detected:                                                 │
│ • Site A & B: Alert spikes during shift changes (correlation: 89%)        │
│ • All Sites: Reduced patrol activities during meal breaks                 │
│ • Site B & C: Increase in property-damage after weather events           │
│                                                                             │
│ CROSS-SITE ACTIVITY FLOWS:                                                │
│ Site A → Site B:                                                          │
│ • 12 bol-event activities triggered cross-site monitoring                 │
│ • 3 security-breach patterns suggested coordinated attempts              │
│                                                                             │
│ SHARED ACTIVITY INTELLIGENCE:                                             │
│ • Suspicious vehicle tracked across 3 sites (8 patrol activities)         │
│ • Evidence activities building multi-site case (CASE-2024-0089)          │
│ • Medical activity triggered mutual aid protocol                         │
│                                                                             │
│ OPTIMIZATION OPPORTUNITIES:                                               │
│ • Synchronize patrol schedules to prevent coverage gaps                   │
│ • Share alert thresholds for consistent auto-incident creation           │
│ • Coordinate evidence collection standards across sites                   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.12.5 🚨 Activity-Based Security Policies**

**Location-Specific Activity Rules**

| **Policy Level** | **Activity Rules** | **Override Capability** |
|-----------------|-------------------|------------------------|
| **Global** | Medical activities always create incidents | Cannot override |
| **Regional** | Evidence retention periods | Site-level extension only |
| **Site** | Activity response time SLAs | Building-level tightening |
| **Building** | Auto-incident confidence thresholds | Zone-level adjustment |
| **Zone** | Required patrol frequency | Shift-based flexibility |

**Security Zone Activity Configuration**
```
ZONE: Executive Floor (High Security)
┌─────────────────────────────────────────────────────────────────────────────┐
│ ENHANCED ACTIVITY POLICIES                                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│ ✅ Patrol required: Every 30 minutes (2x standard)                        │
│ ✅ Alert threshold: 60% confidence (20% more sensitive)                   │
│ 🔒 Security-breach: Immediate multi-site notification                     │
│ 🔒 Evidence activities: Require 2-person verification                     │
│ 🔒 BOL matches: Automatic lockdown protocol                               │
│                                                                             │
│ Special Activity Tags:                                                     │
│ • Auto-add: zone:executive, priority:high                                 │
│ • Restrict: Cannot remove priority tags                                   │
│                                                                             │
│ Activity History (30 days):                                               │
│ • 134 patrol activities (100% compliance)                                 │
│ • 12 alert activities (3 escalated)                                       │
│ • 0 security breaches ✅                                                  │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.12.6 📊 Location Activity Analytics**

**Activity-Based Performance Metrics**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                     LOCATION ACTIVITY ANALYTICS                            │
├─────────────────────────────────────────────────────────────────────────────┤
│ Site Comparison - Activity Metrics:                                        │
│                                                                             │
│ Metric              │ Site A  │ Site B  │ Site C  │ Target               │
├─────────────────────┼─────────┼─────────┼─────────┼────────────────────────┤
│ Activities/Day      │ 234     │ 189     │ 145     │ 150-250             │
│ Auto-Incidents      │ 12%     │ 15%     │ 8%      │ 10-15%              │
│ Response Time       │ 2.3 min │ 2.8 min │ 2.1 min │ <3 min              │
│ Evidence Quality    │ 94%     │ 89%     │ 91%     │ >90%                │
│ Patrol Compliance   │ 98%     │ 95%     │ 99%     │ >95%                │
│                                                                             │
│ Activity Type Distribution:                                                │
│         Site A    Site B    Site C                                        │
│ Patrol  ████ 58%  ████ 61%  █████ 65%                                   │
│ Alert   ██ 22%    ██ 19%    ██ 18%                                      │
│ Other   ██ 20%    ██ 20%    ██ 17%                                      │
│                                                                             │
│ 🏆 Best Practices:                                                        │
│ • Site C: Highest patrol compliance rate                                  │
│ • Site A: Best evidence documentation                                     │
│ • Site B: Most balanced activity distribution                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### **📋 V0 Logic Checklist - Location Management**

| **❓ Logic Question** | **✅ Answer** | **🔗 Source Section/Link** |
|-----------------------|---------------|----------------------------|
| **Can the entity be created without its parent?** | No - Hierarchy enforced (unchanged) | Original hierarchy rules |
| **Cardinality** | One


---

### **7.13 💬 In-App Messaging** *(Deprecated - See Section 7.16)*

**🎯 Note**: For MVP, messaging is handled through integrated platforms (Telegram, future Slack/Teams) as described in Section 5.16. This section describes potential future native messaging capabilities.

**Purpose**: Future native secure communication between users within the platform

#### **7.13.1 📱 Future Messaging Interface**

**Potential Native Messaging View**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              MESSAGES                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│ [➕ New Message]  [👥 Groups]  [📋 Case Channels]  [🔍 Search]             │
├─────────────────────────────────────────────────────────────────────────────┤
│ CONVERSATIONS                          │ ACTIVE CHAT                        │
│                                        │                                    │
│ 🟢 Johnson, Sarah                     │ 💬 Case Team: CASE-2024-0089      │
│    "Confirmed - heading to Site B"    │                                    │
│    2 min ago                          │ Wilson: Found matching vehicle     │
│                                        │         in lot C                   │
│ 👥 Shift Team - Day                   │         [Photo attached]           │
│    Garcia: "Medical incident resolved" │                                    │
│    15 min ago                         │ You: Great work. Can you get       │
│                                        │      the plate number?             │
│ 📋 CASE-2024-0089                     │                                    │
│    3 new messages                     │ Johnson: Already did - ABC123      │
│    Active case discussion             │          Same as the BOL           │
│                                        │                                    │
│ 🔴 Emergency Channel                  │ [Type a message...] [📎] [Send]    │
│    No new messages                    │                                    │
└────────────────────────────────────────┴────────────────────────────────────┘
```

#### **7.13.2 💬 Message Types**

**Supported Message Formats**

| **Type** | **Features** | **Use Cases** |
|----------|--------------|---------------|
| **Direct Messages** | 1-on-1 conversations | Quick coordination, private updates |
| **Group Messages** | Multi-user threads | Shift teams, location groups |
| **Case Channels** | Case-specific discussions | Investigation coordination |
| **Incident Threads** | Incident-linked chats | Real-time response coordination |
| **Broadcast Messages** | One-to-many announcements | Shift updates, alerts |

#### **7.13.3 📎 Message Features**

**Enhanced Messaging Capabilities**
- File attachments (images, documents)
- Activity/incident/case linking
- Read receipts and typing indicators
- Message search and history
- Notification preferences
- @mentions for user attention
- Priority/urgent message flags

#### **7.13.4 🔐 Message Security**

**Security & Permissions**
- Messages visible only to participants
- Location-based access restrictions
- Audit trail for all messages
- No message deletion (only archival)
- Encrypted message storage
- Role-based channel access

---

### **7.14 🎥 Ambient.ai Integration**

**🎯 Purpose**: Integrate with Ambient.ai for intelligent video analytics and real-time security alerts with visual context

#### **7.14.1 📹 GIF Preview Feature**

**Core Functionality**
- **Pre/Post Roll**: 5 seconds before alert + 5 seconds after alert
- **Playback Speed**: 2x speed for rapid review
- **Total Duration**: 10 seconds compressed to 5 seconds viewing time
- **Purpose**: Quick visual verification of what triggered the alert

**GIF Preview Display**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         AMBIENT ALERT PREVIEW                               │
├─────────────────────────────────────────────────────────────────────────────┤
│ Alert: Tailgating Detected - Main Entrance                                 │
│ Confidence: 89% | Time: 14:23:15 PST                                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                       │  │
│  │                     [GIF PREVIEW PLAYER]                             │  │
│  │                                                                       │  │
│  │                   ◄◄ ▐▐ ► ►► @ 2x speed                             │  │
│  │                                                                       │  │
│  │                 Timeline: [-5s]━━━━━●━━━━━[+5s]                     │  │
│  │                                                                       │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│ [Create Activity] [Dismiss] [View Full Video] [Correlate with Lenel]       │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.14.2 🔌 Integration Specifications**

**Webhook Configuration**
```yaml
Endpoint: /api/webhooks/ambient
Method: POST
Authentication: Bearer token
Payload Structure:
  {
    "alert_id": "AMB-2024-001234",
    "type": "tailgate_detected",
    "confidence": 89,
    "timestamp": "2024-01-15T14:23:15Z",
    "camera_id": "CAM-MAIN-01",
    "location": {
      "building": "Building A",
      "floor": "1",
      "zone": "Main Entrance"
    },
    "preview_url": "https://ambient.ai/api/previews/AMB-2024-001234",
    "full_video_url": "https://ambient.ai/video/AMB-2024-001234"
  }
```

**Activity Creation Rules**
| **Ambient Alert Type** | **Situ8 Activity Type** | **Auto-Incident** | **Confidence Threshold** |
|------------------------|-------------------------|-------------------|--------------------------|
| weapon_detected | security-breach | ALWAYS | Any |
| tailgate_detected | alert | IF confidence > 80% | 80% |
| person_of_interest | alert | IF after-hours | 75% |
| crowd_detected | alert | IF size > threshold | 70% |
| vehicle_alert | alert | Based on rules | 75% |
| behavior_anomaly | alert | IF confidence > 85% | 85% |

#### **7.14.3 🔗 Alert Processing Workflow**

```
Ambient Alert Received
        │
        ▼
Create Activity (type based on mapping)
        │
        ▼
Fetch GIF Preview (cache for 15 minutes)
        │
        ▼
Apply Auto-Incident Rules
        │
        ├─── Meets Threshold ──→ Create Incident
        │                        Link Activity
        │
        └─── Below Threshold ──→ Activity Only
                                 Available in Stream
```

#### **7.14.4 ⚙️ Configuration Settings**

**Admin Configurable Parameters**
- Alert type mappings to activity types
- Confidence thresholds per alert type
- Business hours definition for after-hours rules
- GIF preview retention period (default: 15 minutes)
- Maximum concurrent preview downloads
- Webhook retry attempts and timeout

**Integration Health Monitoring**
- Last successful webhook timestamp
- Failed webhook count (last 24 hours)
- Average response time
- GIF retrieval success rate

---

### **7.15 🚪 Lenel Access Control Integration**

**🎯 Purpose**: Correlate access control events with security activities to automatically identify individuals involved in incidents

#### **7.15.1 🔍 Badge Correlation Engine**

**Core Functionality**
- **Time Window**: ±30 seconds from security event
- **Correlation Logic**: Match badge reads with security alerts
- **PII Handling**: Store and display badge holder photos/info
- **Use Case**: Identify authorized person vs. unauthorized follower

**Correlation Display**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                      LENEL BADGE CORRELATION                                │
├─────────────────────────────────────────────────────────────────────────────┤
│ Security Event: Tailgate Alert - Main Entrance                             │
│ Time: 14:23:15 PST | Confidence: 89%                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Correlated Badge Activity (±30 seconds):                                   │
│                                                                             │
│ ┌─────────────────┬─────────────────┬─────────────────┬─────────────────┐ │
│ │ 14:23:08       │ ┌─────────────┐ │ Badge: E12345   │ ✅ Authorized    │ │
│ │ Access Granted │ │   [Photo]   │ │ Phil Jang       │ Main Entrance   │ │
│ │                │ │             │ │ Engineering     │                 │ │
│ │                │ └─────────────┘ │                 │                 │ │
│ └─────────────────┴─────────────────┴─────────────────┴─────────────────┘ │
│                                                                             │
│ ⚠️ Potential Unauthorized Entry: 1 person entered after badge scan         │
│                                                                             │
│ [Create Incident] [Add to Activity] [View Access History] [Notify]         │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.15.2 🔌 Integration Specifications**

**Event Stream Subscription**
```yaml
Connection Type: WebSocket/Event Stream
Endpoint: wss://lenel.company.com/events
Authentication: API Key + Certificate
Event Types:
  - access_granted
  - access_denied
  - door_forced
  - door_held_open
  - tailgate_detected
  - invalid_card
Event Structure:
  {
    "event_id": "LNL-2024-567890",
    "type": "access_granted",
    "timestamp": "2024-01-15T14:23:08Z",
    "door": {
      "id": "DOOR-MAIN-01",
      "name": "Main Entrance",
      "building": "Building A",
      "floor": "1"
    },
    "badge": {
      "number": "E12345",
      "holder": {
        "name": "Phil Jang",
        "photo_url": "/api/badges/E12345/photo",
        "department": "Engineering",
        "clearance_level": "standard"
      }
    }
  }
```

**Correlation Rules**
| **Lenel Event** | **Situ8 Activity Type** | **Auto-Incident** | **Correlation Action** |
|-----------------|-------------------------|-------------------|------------------------|
| door_forced | security-breach | ALWAYS | Pull last badge used |
| door_held_open | alert | After 30 seconds | Identify badge holder |
| tailgate_detected | alert | ALWAYS | Compare badge count vs. people |
| access_denied | alert | After 3 attempts | Track badge number |
| invalid_card | alert | Pattern detected | Log attempts |

#### **7.15.3 🔐 PII Data Management**

**Data Storage Requirements**
- Badge holder photos cached locally
- Personal information encrypted at rest
- Access logs retained per policy
- GDPR/privacy compliance built-in

**Privacy Controls**
- Role-based access to PII
- Audit trail for all PII access
- Configurable retention periods
- Right to be forgotten support

#### **7.15.4 🔄 Correlation Workflow**

```
Security Alert Triggered (Ambient/Other)
            │
            ▼
Query Lenel Events (±30 seconds)
            │
            ▼
Find Related Badge Activity
            │
            ├─── Match Found ──→ Display Badge Holder(s)
            │                     Assess Authorization
            │                     Create Enhanced Activity
            │
            └─── No Match ──→ Flag as Unauthorized
                              Escalate Priority
                              Create Incident
```

---

### **7.16 📱 Communication Platforms**

**🎯 Purpose**: Enable multi-channel communication with modular architecture, starting with Telegram for MVP

#### **7.16.1 📲 Telegram Integration (MVP)**

**Core Functionality**
- **Voice Memos**: Transcribe and create activities
- **Image Processing**: Attach photos to activities
- **Text Commands**: Quick activity creation
- **Bot Commands**: Status updates, queries

**Telegram Bot Interface**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SITU8 TELEGRAM BOT                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ Officer Johnson (Voice Memo - 0:15)                                        │
│ 🎤 "Patrol complete in Zone A. Found broken window in Building 2,         │
│     third floor. Appears to be vandalism. Taking photos now."              │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐   │
│ │ 🤖 Situ8 Bot:                                                        │   │
│ │ ✅ Activity created: Property Damage - Building 2                    │   │
│ │ Type: property-damage                                                │   │
│ │ Status: detecting                                                    │   │
│ │ Location: Zone A, Building 2, Floor 3                                │   │
│ │                                                                       │   │
│ │ Please attach photos when ready.                                     │   │
│ └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│ Officer Johnson (Photo)                                                     │
│ 📷 [Window damage photo attached]                                           │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐   │
│ │ 🤖 Situ8 Bot:                                                        │   │
│ │ ✅ Photo attached to activity                                        │   │
│ │ 🚨 Auto-incident created due to property damage                     │   │
│ │ Incident #: INC-2024-0890                                            │   │
│ └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.16.2 🔄 N8N Workflow Orchestration**

**Workflow Architecture**
```yaml
N8N Workflow: Telegram Message Processing
Triggers:
  - Telegram webhook (voice/text/image)
  
Nodes:
  1. Receive Message
     - Extract message type
     - Get user info
     
  2. Process Voice Memo
     - Send to OpenAI Whisper
     - Transcribe to text
     
  3. LLM Processing (GPT-4.0 mini)
     - Extract activity details
     - Determine activity type
     - Parse location info
     
  4. Create Activity
     - Call Situ8 API
     - Set appropriate fields
     
  5. Send Response
     - Confirm via Telegram
     - Include activity/incident ID
```

**Bot Commands**
| **Command** | **Function** | **Example** |
|-------------|--------------|-------------|
| /patrol | Start patrol activity | /patrol Zone A |
| /status | Get current status | /status |
| /incident | Quick incident report | /incident Medical emergency Room 205 |
| /photo | Attach photo to last activity | /photo [send image] |
| /help | Show available commands | /help |

#### **7.16.3 🔌 Modular Architecture**

**Platform Abstraction Layer**
```javascript
// Modular messaging interface
interface MessagingPlatform {
  sendMessage(recipient: string, message: string): Promise<void>;
  receiveMessage(handler: MessageHandler): void;
  sendFile(recipient: string, file: File): Promise<void>;
  transcribeVoice(audio: AudioFile): Promise<string>;
}

// Implementations
class TelegramPlatform implements MessagingPlatform { }
class SlackPlatform implements MessagingPlatform { }
class TeamsPlatform implements MessagingPlatform { }

// Easy platform switching
const messagingService = new MessagingService(
  process.env.MESSAGING_PLATFORM || 'telegram'
);
```

#### **7.16.4 🚀 Future Platform Support**

**Slack Integration (Post-MVP)**
- Slash commands for quick actions
- Voice clip support
- Thread-based incident discussions
- Rich message formatting

**Teams Integration (Post-MVP)**
- Corporate authentication
- Channel-based operations
- Adaptive cards for activities
- Meeting integration for incidents

---

### **7.17 🗺️ Map-Based Visualization**

**🎯 Purpose**: Provide real-time visual tracking of guard locations and incident positions on an interactive map

#### **7.17.1 📍 Guard Tracking**

**Real-Time Guard Positions**
```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SECURITY MAP VIEW                                  │
├─────────────────────────────────────────────────────────────────────────────┤
│ [🔍 Search] [⚙️ Filters] [📊 Stats] [🔄 Refresh] [⛶ Fullscreen]          │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐  │
│  │                                                                       │  │
│  │   🏢 Building A          🏢 Building B          🏢 Building C      │  │
│  │   ┌─────────┐           ┌─────────┐           ┌─────────┐         │  │
│  │   │    👮‍♂️   │           │         │           │ 🚨      │         │  │
│  │   │ Johnson │           │    👮‍♀️   │           │ INC-089 │         │  │
│  │   │ [On Patrol]         │ Garcia  │           │ Medical │         │  │
│  │   └─────────┘           │ [Available]         └─────────┘         │  │
│  │                         └─────────┘                                │  │
│  │                                                                     │  │
│  │   🚗 Parking Lot                     🌳 Courtyard                  │  │
│  │   ┌─────────────┐                   ┌─────────────┐              │  │
│  │   │      👮‍♂️     │                   │             │              │  │
│  │   │   Wilson    │                   │    👮‍♀️ 🏃    │              │  │
│  │   │ [Responding]│                   │   Chen →    │              │  │
│  │   └─────────────┘                   │ [In Transit]│              │  │
│  │                                     └─────────────┘              │  │
│  └─────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│ Guard Status:  ✅ Available: 2  |  🚶 Patrol: 1  |  🏃 Responding: 2      │
│ Active Incidents: 1 Medical | 0 Security | 0 Property                      │
└─────────────────────────────────────────────────────────────────────────────┘
```

#### **7.17.2 🚨 Incident Visualization**

**Incident Display Rules**
- Only incidents shown on map (not all activities)
- Color coding by severity/type
- Click for quick details
- Real-time status updates

**Incident Markers**
| **Type** | **Color** | **Icon** | **Priority** |
|----------|-----------|----------|--------------|
| Medical | Red | 🚨 | Highest |
| Security Breach | Orange | ⚠️ | High |
| Property Damage | Yellow | 🔧 | Medium |
| BOL Event | Purple | 👁️ | High |
| Alert | Blue | 🔔 | Variable |

#### **7.17.3 🎮 Map Controls**

**Interactive Features**
```
Map Control Panel:
┌─────────────────────────────────────┐
│ View Options:                       │
│ ☑ Guards      ☑ Incidents          │
│ ☐ Patrol Routes  ☐ Cameras         │
│                                     │
│ Filter by:                          │
│ [All Zones ▼] [All Types ▼]        │
│ [Last Hour ▼]                      │
│                                     │
│ Guard Commands:                     │
│ [Dispatch Selected] [Broadcast]     │
│ [View Details] [Message]            │
└─────────────────────────────────────┘
```

**Click Actions**
- **Guard**: View status, send message, view activity history
- **Incident**: View details, assign guard, update status
- **Building/Zone**: Filter view, see statistics
- **Empty Space**: Create manual activity at location

#### **7.17.4 📊 Location Data Requirements**

**Guard Location Updates**
- Update frequency: Every 30 seconds when active
- GPS/Indoor positioning support
- Last known position retention
- Privacy mode for breaks

**Incident Location Fields**
```javascript
interface IncidentLocation {
  coordinates?: {
    lat: number;
    lng: number;
  };
  building?: string;
  floor?: string;
  zone?: string;
  landmark?: string;
  accuracy?: number; // meters
}
```

#### **7.17.5 ⚙️ Configuration Options**

**Admin Settings**
- Default map center and zoom
- Indoor/outdoor map layers
- Guard tracking frequency
- Incident display duration
- Custom map markers
- Geofence definitions

**Performance Optimization**
- Cluster nearby incidents
- Limit simultaneous guard updates
- Cache map tiles locally
- Progressive detail loading

---

## **🆕 Summary of v0.1 Enhancements**

### **Major Features Added in v0.1**

1. **Enhanced Case Management (Section 5.3.8-5.3.10)**
   - AI-powered case insights with pattern analysis
   - Automated timeline aggregating all related activities
   - Smart incident suggestion engine
   - Risk assessment and similar case matching

2. **Full Reports & Analytics (Section 5.6)**
   - Replaced basic daily reports with comprehensive suite
   - Pre-built report library (6 report types)
   - Custom report builder with drag-and-drop
   - Report queue with background processing
   - Multi-format export (PDF, Excel, CSV)
   - Scheduled report distribution

3. **Global AI Assistant (Section 5.10.5)**
   - Floating widget available on all pages
   - Natural language command processing
   - Context-aware suggestions
   - Action confirmation framework
   - Quick actions menu
   - Keyboard shortcut (Ctrl/Cmd + K)

### **Integration Principles**
- All enhancements respect the activities → incidents → cases workflow
- Existing functionality remains unchanged
- New features integrate seamlessly with current RBAC model
- AI capabilities limited by user permissions
- Full audit trail for all new features

### **Migration Notes**
- No database schema changes required for basic functionality
- Optional performance indexes recommended for reports
- AI features use existing WebSocket infrastructure
- Backward compatible with v0.0 APIs

---

## **📚 9. Implementation Guide**