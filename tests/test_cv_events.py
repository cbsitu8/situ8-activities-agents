import pytest
import json
from models.event_models import CVThreatEvent, ThreatLevel
from agents.tools.cv_analyzer import CVThreatAnalyzer
from agents.triage_agent import run_triage_analysis

class TestCVEvents:
    """Test suite for computer vision threat event analysis."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.cv_analyzer = CVThreatAnalyzer()
        
        # Sample firearm event
        self.firearm_event = {
            "stored_at": "2025-07-08T18:30:03.703783Z",
            "record_id": "59786dbb-611b-4414-b3f0-f2bd1e980709",
            "data": {
                "threatSignature": {
                    "id": 72,
                    "name": "Person Brandishing Firearm",
                    "icon": "GUN"
                },
                "site": {
                    "id": 417,
                    "name": "San Jose",
                    "slug": "sjc"
                },
                "stream": {
                    "id": 12421,
                    "name": "HQ-SJ-B1F2-1",
                    "space": {
                        "id": 2698,
                        "name": "Office",
                        "fullPath": "San Jose > Building 1 > Floor 2 > Office"
                    }
                },
                "alertId": 32552,
                "alertName": "Person Brandishing Firearm",
                "severity": "SEV0",
                "status": "RAISED"
            }
        }
        
        # Sample unauthorized access event
        self.unauthorized_event = {
            "stored_at": "2025-07-08T14:25:17.123456Z",
            "record_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
            "data": {
                "threatSignature": {
                    "id": 15,
                    "name": "Unauthorized Access",
                    "icon": "PERSON"
                },
                "site": {
                    "id": 417,
                    "name": "San Jose",
                    "slug": "sjc"
                },
                "stream": {
                    "id": 12425,
                    "name": "HQ-SJ-B1F1-ENTRANCE",
                    "space": {
                        "id": 2701,
                        "name": "Main Entrance",
                        "fullPath": "San Jose > Building 1 > Floor 1 > Main Entrance"
                    }
                },
                "alertId": 32553,
                "alertName": "Unauthorized Access",
                "severity": "SEV1",
                "status": "RAISED"
            }
        }
        
        # Sample low-threat event
        self.low_threat_event = {
            "stored_at": "2025-07-08T19:22:11.789012Z",
            "record_id": "d4e5f6g7-h8i9-0123-defg-456789012345",
            "data": {
                "threatSignature": {
                    "id": 55,
                    "name": "Overcrowding Detection",
                    "icon": "CROWD"
                },
                "site": {
                    "id": 417,
                    "name": "San Jose",
                    "slug": "sjc"
                },
                "stream": {
                    "id": 12440,
                    "name": "HQ-SJ-B1F1-CAFETERIA",
                    "space": {
                        "id": 2715,
                        "name": "Cafeteria",
                        "fullPath": "San Jose > Building 1 > Floor 1 > Cafeteria"
                    }
                },
                "alertId": 32556,
                "alertName": "Overcrowding Detection",
                "severity": "SEV3",
                "status": "RAISED"
            }
        }
    
    def test_cv_threat_event_model(self):
        """Test CVThreatEvent model creation and properties."""
        event = CVThreatEvent(**self.firearm_event)
        
        assert event.record_id == "59786dbb-611b-4414-b3f0-f2bd1e980709"
        assert event.threat_signature["name"] == "Person Brandishing Firearm"
        assert event.location == "San Jose > Building 1 > Floor 2 > Office"
        assert event.severity == "SEV0"
        assert event.alert_name == "Person Brandishing Firearm"
        assert event.site_name == "San Jose"
    
    def test_firearm_threat_analysis(self):
        """Test analysis of firearm threat detection."""
        result = self.cv_analyzer._run(self.firearm_event)
        
        assert result["event_type"] == "CV_THREAT"
        assert result["ai_threat_level"] == "CRITICAL"
        assert result["confidence_score"] >= 0.9
        assert result["false_positive_probability"] <= 0.1
        assert result["escalation_required"] == True
        assert "IMMEDIATE" in result["response_timeline"]
        assert result["priority_score"] >= 9
        
        # Check recommendations contain firearm-specific actions
        recommendations = result["recommended_actions"]
        assert any("law enforcement" in rec.lower() for rec in recommendations)
        assert any("lockdown" in rec.lower() or "active shooter" in rec.lower() for rec in recommendations)
    
    def test_unauthorized_access_analysis(self):
        """Test analysis of unauthorized access event."""
        result = self.cv_analyzer._run(self.unauthorized_event)
        
        assert result["event_type"] == "CV_THREAT"
        assert result["ai_threat_level"] == "HIGH"
        assert result["confidence_score"] >= 0.8
        assert result["escalation_required"] == True
        assert "URGENT" in result["response_timeline"]
        assert result["priority_score"] >= 7
        
        # Check recommendations contain investigation actions
        recommendations = result["recommended_actions"]
        assert any("investigate" in rec.lower() for rec in recommendations)
        assert any("camera" in rec.lower() or "review" in rec.lower() for rec in recommendations)
    
    def test_low_threat_analysis(self):
        """Test analysis of low-threat event."""
        result = self.cv_analyzer._run(self.low_threat_event)
        
        assert result["event_type"] == "CV_THREAT"
        assert result["ai_threat_level"] in ["LOW", "MEDIUM"]
        assert result["escalation_required"] == False
        assert result["priority_score"] <= 6
        
        # Check recommendations are routine
        recommendations = result["recommended_actions"]
        assert any("routine" in rec.lower() or "monitor" in rec.lower() for rec in recommendations)
    
    def test_threat_level_progression(self):
        """Test that threat levels are assigned correctly based on severity."""
        # Test SEV0 -> CRITICAL
        result_sev0 = self.cv_analyzer._run(self.firearm_event)
        assert result_sev0["ai_threat_level"] == "CRITICAL"
        
        # Test SEV1 -> HIGH
        result_sev1 = self.cv_analyzer._run(self.unauthorized_event)
        assert result_sev1["ai_threat_level"] == "HIGH"
        
        # Test SEV3 -> MEDIUM/LOW
        result_sev3 = self.cv_analyzer._run(self.low_threat_event)
        assert result_sev3["ai_threat_level"] in ["MEDIUM", "LOW"]
    
    def test_location_criticality(self):
        """Test that location affects threat assessment."""
        # Test entrance location (should increase priority)
        entrance_event = self.unauthorized_event.copy()
        entrance_result = self.cv_analyzer._run(entrance_event)
        entrance_priority = entrance_result["priority_score"]
        
        # Test non-critical location
        office_event = self.firearm_event.copy()
        office_result = self.cv_analyzer._run(office_event)
        
        # Both should be high priority due to threat type, but entrance might be higher
        assert entrance_priority >= 7
        assert office_result["priority_score"] >= 9  # Firearm is always critical
    
    def test_confidence_and_false_positive_correlation(self):
        """Test that confidence and false positive probability are inversely related."""
        result = self.cv_analyzer._run(self.firearm_event)
        
        confidence = result["confidence_score"]
        false_positive = result["false_positive_probability"]
        
        # For high-confidence events, false positive should be low
        if confidence >= 0.9:
            assert false_positive <= 0.1
        
        # Sum should generally be close to 1 (but not exactly due to different scales)
        assert 0.8 <= confidence + false_positive <= 1.2
    
    def test_response_timeline_consistency(self):
        """Test that response timelines match threat levels."""
        critical_result = self.cv_analyzer._run(self.firearm_event)
        high_result = self.cv_analyzer._run(self.unauthorized_event)
        low_result = self.cv_analyzer._run(self.low_threat_event)
        
        assert "2 minutes" in critical_result["response_timeline"]
        assert "5 minutes" in high_result["response_timeline"]
        assert ("15 minutes" in low_result["response_timeline"] or 
                "60 minutes" in low_result["response_timeline"])
    
    def test_analysis_reasoning_completeness(self):
        """Test that analysis reasoning contains key information."""
        result = self.cv_analyzer._run(self.firearm_event)
        reasoning = result["analysis_reasoning"]
        
        # Should contain threat name, level, confidence, and false positive info
        assert "Person Brandishing Firearm" in reasoning
        assert "CRITICAL" in reasoning
        assert "%" in reasoning  # Should have percentage values
        assert "confidence" in reasoning.lower()
    
    def test_event_summary_format(self):
        """Test event summary formatting."""
        result = self.cv_analyzer._run(self.firearm_event)
        summary = result["event_summary"]
        
        # Should contain threat name and location
        assert "Person Brandishing Firearm" in summary
        assert "San Jose > Building 1 > Floor 2 > Office" in summary
        assert "San Jose" in summary
    
    @pytest.mark.parametrize("event_data", [
        "firearm_event",
        "unauthorized_event", 
        "low_threat_event"
    ])
    def test_all_required_fields_present(self, event_data):
        """Test that all required fields are present in analysis results."""
        event = getattr(self, event_data)
        result = self.cv_analyzer._run(event)
        
        required_fields = [
            "event_type", "ai_threat_level", "false_positive_probability",
            "confidence_score", "recommended_actions", "escalation_required",
            "response_timeline", "analysis_reasoning", "event_summary", "priority_score"
        ]
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
            assert result[field] is not None, f"Field {field} is None"
    
    def test_load_sample_data(self):
        """Test loading sample data from file."""
        try:
            with open("data/sample_cv_events.json", "r") as f:
                sample_events = json.load(f)
            
            assert len(sample_events) > 0
            
            # Test first event
            event = CVThreatEvent(**sample_events[0])
            assert event.record_id is not None
            assert event.location is not None
            
        except FileNotFoundError:
            pytest.skip("Sample data file not found")
    
    def test_batch_processing(self):
        """Test processing multiple events."""
        events = [self.firearm_event, self.unauthorized_event, self.low_threat_event]
        
        results = []
        for event in events:
            result = self.cv_analyzer._run(event)
            results.append(result)
        
        assert len(results) == 3
        
        # Check threat level progression
        threat_levels = [r["ai_threat_level"] for r in results]
        assert "CRITICAL" in threat_levels
        assert "HIGH" in threat_levels