import csv
import random
from typing import List, Optional
from models.event_models import CVThreatEvent, AccessControlEvent
import os

class DataLoader:
    """Load and manage mock data from CSV files."""
    
    def __init__(self, cv_csv_path: str, access_csv_path: str):
        self.cv_csv_path = cv_csv_path
        self.access_csv_path = access_csv_path
        self.cv_events: List[CVThreatEvent] = []
        self.access_events: List[AccessControlEvent] = []
        self._load_data()
    
    def _load_data(self):
        """Load data from CSV files."""
        try:
            self._load_cv_events()
            self._load_access_events()
            print(f"Loaded {len(self.cv_events)} CV events and {len(self.access_events)} access control events")
        except Exception as e:
            print(f"Error loading data: {e}")
            # Create fallback data if CSV files can't be loaded
            self._create_fallback_data()
    
    def _load_cv_events(self):
        """Load computer vision events from CSV."""
        if not os.path.exists(self.cv_csv_path):
            print(f"CV CSV file not found: {self.cv_csv_path}")
            return
            
        with open(self.cv_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    event = CVThreatEvent(
                        alert_event_id=row['alert_event_id'],
                        severity=row['severity'],
                        site_name=row['site_name'],
                        detection_name=row['detection_name'],
                        creation_time=row['creation_time'],
                        camera_name=row['camera_name'],
                        readers_name=row.get('readers_name') or None
                    )
                    self.cv_events.append(event)
                except Exception as e:
                    print(f"Error parsing CV event row: {row}, error: {e}")
    
    def _load_access_events(self):
        """Load access control events from CSV."""
        if not os.path.exists(self.access_csv_path):
            print(f"Access CSV file not found: {self.access_csv_path}")
            return
            
        with open(self.access_csv_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    event = AccessControlEvent(
                        serial_number=row['serial_number'],
                        device_id=row['device_id'],
                        controller_id=row['controller_id'],
                        segment_id=row['segment_id'],
                        alarm_name=row['alarm_name'],
                        timestamp=row['timestamp'],
                        alarm_id=row['alarm_id'],
                        badge_id=row.get('badge_id') or None
                    )
                    self.access_events.append(event)
                except Exception as e:
                    print(f"Error parsing access event row: {row}, error: {e}")
    
    def _create_fallback_data(self):
        """Create fallback data if CSV files are not available."""
        print("Creating fallback data...")
        
        # Fallback CV events
        cv_fallback = [
            {
                "alert_event_id": "8472951063",
                "severity": "High",
                "site_name": "Building A",
                "detection_name": "Person Brandishing Firearm",
                "creation_time": "1717920318",
                "camera_name": "CAM-North-01",
                "readers_name": None
            },
            {
                "alert_event_id": "2847195620",
                "severity": "Medium",
                "site_name": "Building B",
                "detection_name": "Door Propped Open",
                "creation_time": "1717920892",
                "camera_name": "CAM-East-02",
                "readers_name": "READER-MainEntrance"
            },
            {
                "alert_event_id": "9381745628",
                "severity": "High",
                "site_name": "Building C",
                "detection_name": "Smoke or Fire",
                "creation_time": "1717921445",
                "camera_name": "CAM-South-03",
                "readers_name": None
            }
        ]
        
        for data in cv_fallback:
            event = CVThreatEvent(**data)
            self.cv_events.append(event)
        
        # Fallback access events
        access_fallback = [
            {
                "serial_number": "K7M3Q8N5",
                "device_id": "READER-MainEntrance",
                "controller_id": "H9K2L7",
                "segment_id": "P4X8M3",
                "alarm_name": "Granted Access",
                "timestamp": "1717920145",
                "alarm_id": "94738205",
                "badge_id": "12847369"
            },
            {
                "serial_number": "B5R8T2W4",
                "device_id": "READER-BackDoor",
                "controller_id": "F3J6N9",
                "segment_id": "R7Y4K1",
                "alarm_name": "Door Forced Open",
                "timestamp": "1717920521",
                "alarm_id": "67294851",
                "badge_id": "58392047"
            },
            {
                "serial_number": "A9L4C6X1",
                "device_id": "READER-SideEntrance",
                "controller_id": "M8Q5P2",
                "segment_id": "L3W9H6",
                "alarm_name": "Invalid Badge Read",
                "timestamp": "1717920897",
                "alarm_id": "83759241",
                "badge_id": "74628591"
            }
        ]
        
        for data in access_fallback:
            event = AccessControlEvent(**data)
            self.access_events.append(event)
    
    def get_random_cv_event(self) -> Optional[CVThreatEvent]:
        """Get a random computer vision event."""
        if not self.cv_events:
            return None
        return random.choice(self.cv_events)
    
    def get_random_access_event(self) -> Optional[AccessControlEvent]:
        """Get a random access control event."""
        if not self.access_events:
            return None
        return random.choice(self.access_events)
    
    def get_cv_events_count(self) -> int:
        """Get the number of loaded CV events."""
        return len(self.cv_events)
    
    def get_access_events_count(self) -> int:
        """Get the number of loaded access control events."""
        return len(self.access_events)
    
    def get_stats(self) -> dict:
        """Get data loader statistics."""
        return {
            "cv_events_loaded": len(self.cv_events),
            "access_events_loaded": len(self.access_events),
            "cv_csv_path": self.cv_csv_path,
            "access_csv_path": self.access_csv_path,
            "cv_csv_exists": os.path.exists(self.cv_csv_path),
            "access_csv_exists": os.path.exists(self.access_csv_path)
        }