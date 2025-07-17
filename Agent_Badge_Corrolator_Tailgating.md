┌─────────────────────────────────────────────────────────────────────────────┐  
│                    TAILGATING ALERT CREWAI WORKFLOW                         │  
└─────────────────────────────────────────────────────────────────────────────┘

                        External Tailgate Alert Received  
                              (from Ambient AI)  
                                      │  
                                      ▼  
                      ┌───────────────────────────────┐  
                      │    Incident Coordinator      │  
                      │         Agent                │  
                      │  • Parses alert details      │  
                      │  • Extracts timestamp        │  
                      │  • Extracts door location    │  
                      └───────────┬─────────────────┘  
                                  │  
                                  │ Alert Data:  
                                  │ \- Time: 10:32:17  
                                  │ \- Door: Main-01  
                                  │ \- Type: Tailgate  
                                  │  
                                  ▼  
                      ┌───────────────────────────────┐  
                      │     Badge Log Query          │  
                      │         Agent                │  
                      │                              │  
                      │  Queries stored badge logs   │  
                      │  Time window: ±30 seconds    │  
                      │  Location: Main-01           │  
                      └───────────┬─────────────────┘  
                                  │  
                                  │  
                                  ▼  
                      ┌───────────────────────────────┐  
                      │      Query Result:           │  
                      │  • Badge ID: 12345           │  
                      │  • Name: Phil Smith          │  
                      │  • Time: 10:32:15            │  
                      │  • Door: Main-01             │  
                      │  • Access: Granted           │  
                      └───────────┬─────────────────┘  
                                  │  
                                  ▼  
                      ┌───────────────────────────────┐  
                      │     Report Generator         │  
                      │         Agent                │  
                      │                              │  
                      │  Creates incident summary    │  
                      │  with badge correlation      │  
                      └───────────┬─────────────────┘  
                                  │  
                                  ▼  
                      ┌───────────────────────────────┐  
                      │      INCIDENT REPORT         │  
                      ├───────────────────────────────┤  
                      │ Alert Type: Tailgate         │  
                      │ Time: 10:32:17               │  
                      │ Location: Main-01 Door       │  
                      │                              │  
                      │ Badge Activity Found:        │  
                      │ • Phil Smith (ID: 12345\)     │  
                      │ • Badged in at 10:32:15      │  
                      │ • 2 seconds before alert     │  
                      │                              │  
                      │ Conclusion: Unauthorized     │  
                      │ person followed Phil Smith   │  
                      │ through Main-01              │  
                      │                              │  
                      │ Response: Dispatch officer   │  
                      └───────────┬─────────────────┘  
                                  │  
                                  ▼  
                      ┌───────────────────────────────┐  
                      │    Notification Agent        │  
                      │                              │  
                      │ • Sends alert to SOC         │  
                      │ • Creates incident ticket    │  
                      └─────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

MINIMAL VIABLE CREW \- 4 AGENTS:

1\. INCIDENT COORDINATOR AGENT  
   \- Receives and parses the tailgate alert  
   \- Extracts key data (time, location)  
   \- Initiates the workflow

2\. BADGE LOG QUERY AGENT  
   \- Single purpose: Query badge database  
   \- Input: Timestamp \+ Door location  
   \- Output: Who badged in during time window

3\. REPORT GENERATOR AGENT  
   \- Takes alert data \+ badge query result  
   \- Creates clear, actionable summary  
   \- States the correlation clearly

4\. NOTIFICATION AGENT  
   \- Delivers the report to security team  
   \- Creates trackable incident

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE VALUE DELIVERED:

Input: "Tailgate alert at Main-01 door at 10:32:17"

Output: "Phil Smith badged in at 10:32:15. Someone followed him through."

This simple correlation is exactly what saves the security officer time \-   
no manual log lookups needed\!  
