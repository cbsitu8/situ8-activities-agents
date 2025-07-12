import pytest
import json
from models.event_models import AccessControlEvent, ThreatLevel
from agents.tools.access_analyzer import AccessControlAnalyzer

class TestAccessControlEvents:
    """Test suite for access control event analysis."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.access_analyzer = AccessControlAnalyzer()
        
        # Sample forced entry event (critical)
        self.forced_entry_event = {
            "serial_number": "AC001236",
            "device_id": "DR-B1-SECURE",
            "controller_id": "CTRL-B1-02",
            "segment_id": "SEG-02",
            "timestamp_processed": "2025-07-09T11:30:15Z",
            "alarm_name": "Forced Entry Detected",
            "timestamp": "2025-07-09T11:30:12Z",
            "alarm_id": "AL-45680",
            "source": "door_contact_sensor",
            "Subdevice_id": "SUB-003"
        }
        
        # Sample door held open event (high)
        self.door_held_open_event = {
            "serial_number": "AC001234",
            "device_id": "DR-B1-101",
            "controller_id": "CTRL-B1-01",
            "segment_id": "SEG-01",
            "timestamp_processed": "2025-07-09T14:23:45Z",
            "alarm_name": "Door Held Open",
            "timestamp": "2025-07-09T14:23:30Z",
            "alarm_id": "AL-45678",
            "source": "door_contact_sensor",
            "Subdevice_id": "SUB-001"
        }
        
        # Sample duress event (critical)
        self.duress_event = {
            "serial_number": "AC001239",
            "device_id": "DR-B3-VAULT",
            "controller_id": "CTRL-B3-01",
            "segment_id": "SEG-04",
            "timestamp_processed": "2025-07-09T08:12:18Z",
            "alarm_name": "Duress Code Entered",
            "timestamp": "2025-07-09T08:12:15Z",
            "alarm_id": "AL-45683",
            "source": "keypad",
            "Subdevice_id": "SUB-006"
        }
        
        # Sample invalid card event (high)
        self.invalid_card_event = {
            "serial_number": "AC001235",
            "device_id": "DR-B1-ENTRANCE",
            "controller_id": "CTRL-B1-01",
            "segment_id": "SEG-01",
            "timestamp_processed": "2025-07-09T09:15:22Z",
            "alarm_name": "Invalid Card Presented",
            "timestamp": "2025-07-09T09:15:18Z",
            "alarm_id": "AL-45679",
            "source": "card_reader",
            "Subdevice_id": "SUB-002"
        }
        
        # Sample communication lost event (medium)
        self.comm_lost_event = {
            "serial_number": "AC001237",
            "device_id": "DR-B2-201",
            "controller_id": "CTRL-B2-01",
            "segment_id": "SEG-03",
            "timestamp_processed": "2025-07-09T16:45:33Z",
            "alarm_name": "Communication Lost",
            "timestamp": "2025-07-09T16:45:30Z",
            "alarm_id": "AL-45681",
            "source": "controller_network",
            "Subdevice_id": "SUB-004"
        }
        
        # Sample battery low event (low)
        self.battery_low_event = {
            "serial_number": "AC001240",
            "device_id": "DR-B1-102",
            "controller_id": "CTRL-B1-01",
            "segment_id": "SEG-01",
            "timestamp_processed": "2025-07-09T17:55:29Z",
            "alarm_name": "Battery Low Warning",
            "timestamp": "2025-07-09T17:55:25Z",
            "alarm_id": "AL-45684",
            "source": "battery_monitor",
            "Subdevice_id": "SUB-007"
        }
    
    def test_access_control_event_model(self):
        """Test AccessControlEvent model creation."""
        event = AccessControlEvent(**self.forced_entry_event)
        
        assert event.alarm_name == "Forced Entry Detected"
        assert event.device_id == "DR-B1-SECURE"
        assert event.source == "door_contact_sensor"
        assert event.alarm_id == "AL-45680"
    
    def test_forced_entry_analysis(self):
        """Test analysis of forced entry event."""
        result = self.access_analyzer._run(self.forced_entry_event)
        
        assert result["event_type"] == "ACCESS_CONTROL"
        assert result["ai_threat_level"] == "CRITICAL"
        assert result["confidence_score"] >= 0.85
        assert result["false_positive_probability"] <= 0.1
        assert result["escalation_required"] == True
        assert "IMMEDIATE" in result["response_timeline"]
        assert result["priority_score"] >= 9
        
        # Check recommendations contain security response
        recommendations = result["recommended_actions"]
        assert any("security" in rec.lower() for rec in recommendations)
        assert any("immediate" in rec.lower() for rec in recommendations)
    
    def test_duress_analysis(self):
        """Test analysis of duress event."""
        result = self.access_analyzer._run(self.duress_event)
        
        assert result["event_type"] == "ACCESS_CONTROL"
        assert result["ai_threat_level"] == "CRITICAL"
        assert result["escalation_required"] == True
        assert "IMMEDIATE" in result["response_timeline"]
        assert result["priority_score"] >= 9
        
        # Check recommendations contain critical response
        recommendations = result["recommended_actions"]
        assert any("immediate" in rec.lower() for rec in recommendations)
    
    def test_door_held_open_analysis(self):
        """Test analysis of door held open event."""
        result = self.access_analyzer._run(self.door_held_open_event)
        
        assert result["event_type"] == "ACCESS_CONTROL"
        assert result["ai_threat_level"] == "HIGH"
        assert result["escalation_required"] == True
        assert "URGENT" in result["response_timeline"]
        assert result["priority_score"] >= 7
        
        # Check recommendations contain investigation actions
        recommendations = result["recommended_actions"]
        assert any("investigate" in rec.lower() or "check" in rec.lower() for rec in recommendations)
    
    def test_invalid_card_analysis(self):
        """Test analysis of invalid card event."""
        result = self.access_analyzer._run(self.invalid_card_event)
        
        assert result["event_type"] == "ACCESS_CONTROL"
        assert result["ai_threat_level"] == "HIGH"
        assert result["escalation_required"] == True
        
        # Check recommendations contain credential verification
        recommendations = result["recommended_actions"]
        assert any("card" in rec.lower() or "credential" in rec.lower() for rec in recommendations)
    
    def test_communication_lost_analysis(self):
        """Test analysis of communication lost event."""
        result = self.access_analyzer._run(self.comm_lost_event)
        
        assert result["event_type"] == "ACCESS_CONTROL"
        assert result["ai_threat_level"] == "MEDIUM"
        assert result["escalation_required"] == False
        assert "PROMPT" in result["response_timeline"]
        assert result["priority_score"] <= 6
        
        # Check recommendations contain technical actions
        recommendations = result["recommended_actions"]
        assert any("network" in rec.lower() or "communication" in rec.lower() or "connectivity" in rec.lower() for rec in recommendations)
    
    def test_battery_low_analysis(self):
        """Test analysis of battery low event."""
        result = self.access_analyzer._run(self.battery_low_event)
        
        assert result["event_type"] == "ACCESS_CONTROL"
        assert result["ai_threat_level"] in ["LOW", "MEDIUM"]
        assert result["escalation_required"] == False
        assert result["priority_score"] <= 5
        
        # Check recommendations contain maintenance actions
        recommendations = result["recommended_actions"]
        assert any("battery" in rec.lower() or "maintenance" in rec.lower() for rec in recommendations)
    
    def test_threat_level_classification(self):
        """Test correct threat level classification across different event types."""
        # Critical events
        critical_events = [self.forced_entry_event, self.duress_event]
        for event in critical_events:
            result = self.access_analyzer._run(event)
            assert result["ai_threat_level"] == "CRITICAL"
        
        # High events
        high_events = [self.door_held_open_event, self.invalid_card_event]
        for event in high_events:
            result = self.access_analyzer._run(event)
            assert result["ai_threat_level"] == "HIGH"
        
        # Medium/Low events
        maintenance_events = [self.comm_lost_event, self.battery_low_event]
        for event in maintenance_events:
            result = self.access_analyzer._run(event)
            assert result["ai_threat_level"] in ["MEDIUM", "LOW"]
    
    def test_source_based_assessment(self):
        """Test that source type affects threat assessment."""
        # Door sensor events should be physical security focused
        door_result = self.access_analyzer._run(self.door_held_open_event)
        assert "door" in door_result["analysis_reasoning"].lower()
        
        # Card reader events should be credential focused
        card_result = self.access_analyzer._run(self.invalid_card_event)
        assert "credential" in card_result["analysis_reasoning"].lower()
        
        # Network events should be technical focused
        network_result = self.access_analyzer._run(self.comm_lost_event)
        assert "sensor" in network_result["analysis_reasoning"].lower()
    
    def test_response_timeline_mapping(self):
        """Test response timeline mapping to threat levels."""
        # Critical -> 2 minutes
        critical_result = self.access_analyzer._run(self.forced_entry_event)
        assert "2 minutes" in critical_result["response_timeline"]
        
        # High -> 5 minutes
        high_result = self.access_analyzer._run(self.door_held_open_event)
        assert "5 minutes" in high_result["response_timeline"]
        
        # Medium -> 15 minutes
        medium_result = self.access_analyzer._run(self.comm_lost_event)
        assert "15 minutes" in medium_result["response_timeline"]
    
    def test_false_positive_rates(self):
        """Test false positive rates are reasonable for different event types."""
        # Security events should have low false positive rates
        security_result = self.access_analyzer._run(self.forced_entry_event)
        assert security_result["false_positive_probability"] <= 0.1
        
        # Technical events should have higher false positive rates
        technical_result = self.access_analyzer._run(self.comm_lost_event)
        assert technical_result["false_positive_probability"] >= 0.15
    
    def test_priority_score_calculation(self):
        """Test priority score calculation logic."""
        # Critical events should have priority 9-10
        critical_result = self.access_analyzer._run(self.forced_entry_event)
        assert 9 <= critical_result["priority_score"] <= 10
        
        # High events should have priority 7-8
        high_result = self.access_analyzer._run(self.door_held_open_event)
        assert 7 <= high_result["priority_score"] <= 8
        
        # Medium events should have priority 4-6
        medium_result = self.access_analyzer._run(self.comm_lost_event)
        assert 4 <= medium_result["priority_score"] <= 6
        
        # Low events should have priority 1-4
        low_result = self.access_analyzer._run(self.battery_low_event)
        assert 1 <= low_result["priority_score"] <= 4
    
    def test_device_criticality_assessment(self):
        """Test that device type affects assessment."""
        # Vault door should be high criticality
        vault_result = self.access_analyzer._run(self.duress_event)
        assert vault_result["priority_score"] >= 9
        
        # Regular door should be standard assessment
        regular_result = self.access_analyzer._run(self.door_held_open_event)
        assert regular_result["priority_score"] >= 7
    
    def test_alarm_specific_recommendations(self):
        """Test that specific alarm types generate appropriate recommendations."""
        # Forced entry should mention physical security
        forced_result = self.access_analyzer._run(self.forced_entry_event)
        recommendations = " ".join(forced_result["recommended_actions"]).lower()
        assert "physical security" in recommendations or "security response" in recommendations
        
        # Card reader should mention credentials
        card_result = self.access_analyzer._run(self.invalid_card_event)
        recommendations = " ".join(card_result["recommended_actions"]).lower()
        assert "credential" in recommendations or "access rights" in recommendations
        
        # Battery low should mention maintenance
        battery_result = self.access_analyzer._run(self.battery_low_event)
        recommendations = " ".join(battery_result["recommended_actions"]).lower()
        assert "battery" in recommendations or "maintenance" in recommendations
    
    def test_event_summary_format(self):
        """Test event summary formatting."""
        result = self.access_analyzer._run(self.forced_entry_event)
        summary = result["event_summary"]
        
        # Should contain alarm name and device ID
        assert "Forced Entry Detected" in summary
        assert "DR-B1-SECURE" in summary
        assert "door_contact_sensor" in summary
    
    @pytest.mark.parametrize("event_data", [
        "forced_entry_event",
        "door_held_open_event",
        "duress_event",
        "invalid_card_event",
        "comm_lost_event",
        "battery_low_event"
    ])
    def test_all_required_fields_present(self, event_data):
        """Test that all required fields are present in analysis results."""
        event = getattr(self, event_data)
        result = self.access_analyzer._run(event)
        
        required_fields = [
            "event_type", "ai_threat_level", "false_positive_probability",
            "confidence_score", "recommended_actions", "escalation_required",
            "response_timeline", "analysis_reasoning", "event_summary", "priority_score"
        ]
        
        for field in required_fields:
            assert field in result, f"Missing field: {field}"
            assert result[field] is not None, f"Field {field} is None"
    
    def test_confidence_score_ranges(self):
        """Test that confidence scores are within valid ranges."""
        events = [
            self.forced_entry_event, self.door_held_open_event,
            self.duress_event, self.invalid_card_event,
            self.comm_lost_event, self.battery_low_event
        ]
        
        for event in events:
            result = self.access_analyzer._run(event)
            confidence = result["confidence_score"]
            false_positive = result["false_positive_probability"]
            
            # Confidence should be between 0 and 1
            assert 0 <= confidence <= 1
            
            # False positive should be between 0 and 1
            assert 0 <= false_positive <= 1
    
    def test_load_sample_data(self):
        """Test loading sample data from file."""
        try:
            with open("data/sample_access_events.json", "r") as f:
                sample_events = json.load(f)
            
            assert len(sample_events) > 0
            
            # Test first event
            event = AccessControlEvent(**sample_events[0])
            assert event.alarm_name is not None
            assert event.device_id is not None
            
        except FileNotFoundError:
            pytest.skip("Sample data file not found")
    
    def test_escalation_logic(self):
        """Test escalation logic for different threat levels."""
        # Critical and high should escalate
        critical_result = self.access_analyzer._run(self.forced_entry_event)
        high_result = self.access_analyzer._run(self.door_held_open_event)
        
        assert critical_result["escalation_required"] == True
        assert high_result["escalation_required"] == True
        
        # Medium and low should not escalate
        medium_result = self.access_analyzer._run(self.comm_lost_event)
        low_result = self.access_analyzer._run(self.battery_low_event)
        
        assert medium_result["escalation_required"] == False
        assert low_result["escalation_required"] == False