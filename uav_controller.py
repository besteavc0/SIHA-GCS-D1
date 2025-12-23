import time
from dronekit import connect, VehicleMode, LocationGlobalRelative
from pymavlink import mavutil

class UAVController:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.vehicle = None

    def connect_uav(self):
        print(f"Bağlanıyor: {self.connection_string}")
        self.vehicle = connect(self.connection_string, wait_ready=True)
        print("Bağlantı Başarılı!")

    def arm_and_takeoff(self, target_altitude):
        print("Sistem kontrolleri yapılıyor...")
        while not self.vehicle.is_armable:
            time.sleep(1)
        
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            time.sleep(1)

        print(f"{target_altitude} metreye kalkış başlıyor...")
        self.vehicle.simple_takeoff(target_altitude)

        while True:
            if self.vehicle.location.global_relative_frame.alt >= target_altitude * 0.95:
                print("Hedef irtifaya ulaşıldı.")
                break
            time.sleep(1)

    def get_telemetry(self):
        return {
            "mode": self.vehicle.mode.name,
            "altitude": self.vehicle.location.global_relative_frame.alt,
            "battery": self.vehicle.battery.level,
            "gps_status": self.vehicle.gps_0.fix_type,
            "heading": self.vehicle.heading
        }