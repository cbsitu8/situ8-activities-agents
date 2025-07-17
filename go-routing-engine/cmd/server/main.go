package main

import (
	"database/sql"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

type Server struct {
	db *sql.DB
}

func main() {
	// Database connection
	postgresURL := os.Getenv("POSTGRES_URL")
	if postgresURL == "" {
		postgresURL = "postgresql://postgres:password@localhost:5432/security_ops?sslmode=disable"
	}

	db, err := sql.Open("postgres", postgresURL)
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close()

	// Test database connection
	if err := db.Ping(); err != nil {
		log.Fatal("Failed to ping database:", err)
	}

	server := &Server{db: db}

	// Setup Gin router
	r := gin.Default()

	// CORS middleware
	r.Use(func(c *gin.Context) {
		c.Header("Access-Control-Allow-Origin", "*")
		c.Header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
		c.Header("Access-Control-Allow-Headers", "Content-Type, Authorization")

		if c.Request.Method == "OPTIONS" {
			c.AbortWithStatus(204)
			return
		}

		c.Next()
	})

	// API routes
	api := r.Group("/api/v1")
	{
		// Health check
		api.GET("/health", server.healthCheck)
		
		// Event processing
		api.POST("/events/process", server.processEvent)
		api.POST("/events/batch", server.processBatchEvents)
		
		// Testing endpoints
		api.POST("/test/load-csv", server.loadCSV)
		api.GET("/test/mock-event", server.generateMockEvent)
		
		// Rule management
		api.POST("/rules/refresh", server.refreshRules)
		api.GET("/rules/cache/stats", server.getCacheStats)
	}

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}

	log.Printf("Starting Go Routing Engine on port %s", port)
	log.Fatal(http.ListenAndServe(":"+port, r))
}

func (s *Server) healthCheck(c *gin.Context) {
	// Test database connection
	if err := s.db.Ping(); err != nil {
		c.JSON(http.StatusServiceUnavailable, gin.H{
			"status":    "unhealthy",
			"error":     "database connection failed",
			"timestamp": time.Now().UTC().Format(time.RFC3339),
		})
		return
	}

	c.JSON(http.StatusOK, gin.H{
		"status":    "healthy",
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"service":   "go-routing-engine",
		"version":   "1.0.0",
	})
}

func (s *Server) processEvent(c *gin.Context) {
	var event map[string]interface{}
	if err := c.ShouldBindJSON(&event); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	// Basic event processing (placeholder)
	result := gin.H{
		"event_id":       "evt_" + time.Now().Format("20060102150405"),
		"priority":       "MEDIUM",
		"matched_sop":    "Default SOP",
		"confidence":     0.75,
		"assigned_agents": []string{"DocumentationAgent"},
		"response_time":  "25ms",
	}

	c.JSON(http.StatusOK, result)
}

func (s *Server) processBatchEvents(c *gin.Context) {
	var events []map[string]interface{}
	if err := c.ShouldBindJSON(&events); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid JSON"})
		return
	}

	results := make([]gin.H, len(events))
	for i := range events {
		results[i] = gin.H{
			"event_id":       "evt_" + time.Now().Format("20060102150405") + "_" + string(rune(i)),
			"priority":       "MEDIUM",
			"matched_sop":    "Default SOP",
			"confidence":     0.75,
			"assigned_agents": []string{"DocumentationAgent"},
			"response_time":  "15ms",
		}
	}

	c.JSON(http.StatusOK, gin.H{
		"processed": len(events),
		"results":   results,
	})
}

func (s *Server) loadCSV(c *gin.Context) {
	// Placeholder for CSV loading
	c.JSON(http.StatusOK, gin.H{
		"message": "CSV loading not yet implemented",
		"status":  "pending",
	})
}

func (s *Server) generateMockEvent(c *gin.Context) {
	mockEvent := gin.H{
		"id":        "mock_" + time.Now().Format("20060102150405"),
		"source":    "computer_vision",
		"type":      "Person Falling Down",
		"location":  "Building A - Lobby",
		"timestamp": time.Now().UTC().Format(time.RFC3339),
		"severity":  "High",
		"raw_data": gin.H{
			"camera_name": "CAM-001",
			"confidence":  95,
		},
	}

	c.JSON(http.StatusOK, mockEvent)
}

func (s *Server) refreshRules(c *gin.Context) {
	// Placeholder for rule refreshing
	c.JSON(http.StatusOK, gin.H{
		"message":      "Rules refreshed",
		"rules_loaded": 0,
		"timestamp":    time.Now().UTC().Format(time.RFC3339),
	})
}

func (s *Server) getCacheStats(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"cache_size":     0,
		"hit_rate":       0.0,
		"total_requests": 0,
		"uptime":         time.Since(time.Now()).String(),
	})
}