from typing import Dict, Any

from phone_tracker.neo4j_service import Neo4jConnection


# from neo4j_service import Neo4jConnection

class DeviceRepository:
    def __init__(self, connection: Neo4jConnection):
        self.db = connection

    def create_interaction_with_interaction(self, data: Dict[str, Any]):

        self._validate_interaction_data(data)

        query = """
        
        MERGE (d1:Device {id: $device1.id})
        SET d1 += $device1_props

            
        MERGE (d2:Device { id: $device2.id})
        SET d2 += $device2_props
            
       
        MERGE (d1)-[r:CONNECTED {
            method: $interaction.method,
            signal_strength: $interaction.signal_strength_dbm,
            distance: $interaction.distance_meters,
            timestamp: datetime($interaction.timestamp)
        }]->(d2)
        RETURN d1, d2, r
        """
        params = {
            "device1": {
                "id": data["devices"][0]["id"]
            },
            "device2": {
                "id": data["devices"][1]["id"]
            },
            "device1_props": {
                "name": data["devices"][0]["name"],
                "brand": data["devices"][0]["brand"],
                "model": data["devices"][0]["model"],
                "os": data["devices"][0]["os"],
                "latitude": data["devices"][0]["location"]["latitude"],
                "longitude": data["devices"][0]["location"]["longitude"]
            },
            "device2_props": {
                "name": data["devices"][1]["name"],
                "brand": data["devices"][1]["brand"],
                "model": data["devices"][1]["model"],
                "os": data["devices"][1]["os"],
                "latitude": data["devices"][1]["location"]["latitude"],
                "longitude": data["devices"][1]["location"]["longitude"]
            },
            "interaction": data["interaction"]
        }

        try:
            result = self.db.execute_write(query, params)
            return result
        except Exception as e:
            print(f"Error executing query: {str(e)}")
            raise




    def _validate_interaction_data(self, data: Dict[str, Any]):
        if data["devices"][0]["id"] == data["devices"][1]["id"]:
            raise ValueError("Cannot connect device to itself")
            
        if not data["interaction"]["method"] in ["Bluetooth", "WiFi", "NFC"]:
            raise ValueError("Invalid connection method")
            
        if data["interaction"]["signal_strength_dbm"] > 0:
            raise ValueError("Signal strength must be negative")
    



    def get_bluetooth_connections(self):
        query = """
        MATCH path = (d1:Device)-[r:CONNECTED*]-(d2:Device)
        WHERE
            ALL(rel IN r WHERE rel.method = 'Bluetooth')
            AND d1 <> d2
        RETURN {
            start_device: d1.name,
            end_device: d2.name,
            path_length: length(path),
            devices: [node IN nodes(path) | node.name],
            total_distance: reduce(s = 0, rel IN r | s + rel.distance_meters)
        } as bluetooth_path
        ORDER BY length(path)
        """
        return self.db.execute_read(query)

    def get_strong_signal_connections(self,min_strength: int = -60):
        query = """
        MATCH (d1:Device)-[r:CONNECTED]->(d2:Device)
        WHERE r.signal_strength_dbm < $min_strength
        WITH d1, d2, r
        ORDER BY r.signal_strength_dbm
         RETURN {
        source: d1.name,
        target: d2.name,
        strength: r.signal_strength_dbm,
            distance: r.distance_meters,
            method: r.method
        } as connection
        """
        return self.db.execute_read(query, {"min_strength": min_strength})


    def count_device_connections(self, device_id: str):
        query = """
        MATCH (d:Device {id: $device_id})-[r]->()
        RETURN COUNT(r)
        """
        return self.db.execute_read(query, {"device_id": device_id})

    def check_direct_connection(self, device1_id: str, device2_id: str):
        query = """
        MATCH (d1:Device {id: $device1_id})-[r]->(d2:Device {id: $device2_id})
        RETURN EXISTS(r)
        """
        return self.db.execute_read(query, {"device1_id": device1_id, "device2_id": device2_id})

    def get_latest_interaction(self, device_id: str):
        query = """
        MATCH (d:Device {id: $device_id})-[r]->()
        RETURN r ORDER BY r.timestamp DESC LIMIT 1
        """
        return self.db.execute_read(query, {"device_id": device_id})

    #
    #