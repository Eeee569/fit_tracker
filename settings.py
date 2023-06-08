from dataclasses import dataclass
@dataclass
class Settings:
    proj_root: str = "/home/will/Documents/fitproj/fit_tracker"
    scale_address: str = "D0:3E:7D:0F:48:52"
    metrics_uuid: str = "0000181b-0000-1000-8000-00805f9b34fb"
    db_path: str = ""
    weight_interval: int = 10
    impedance_interval: int = 50
    device: str = "SCALE LISTENER"
    time_interval: int = 60
    email: str = "donotreply@loseit.com"
    email_check_interval: int = 24 # hours