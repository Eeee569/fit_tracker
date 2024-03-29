from dataclasses import dataclass
@dataclass
class Settings:
    proj_root: str = "/home/will/Documents/fitproj/fit_tracker"
    scale_address: str = "D0:3E:7D:0F:48:52"
    metrics_uuid: str = "0000181b-0000-1000-8000-00805f9b34fb"
    db_path: str = "mongodb://10.2.242.189:6565/fitdb"
    weight_interval: int = 10
    impedance_interval: int = 50
    first_db_value_fill: tuple[int,int] = (444, 205)
    device: str = "SCALE LISTENER"
    time_interval: int = 60
    email: str = "donotreply@loseit.com"
    email_check_interval: int = 24 # hours
    # fitbit_interval: int = '1min'
    # fitbit_user: str = "willwolfe1@gmail.com"
    # fitbit_pass: str = "Eeeee569"
