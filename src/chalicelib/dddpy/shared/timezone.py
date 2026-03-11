from datetime import datetime
import pytz

class Timezone:
    
    @staticmethod
    def get_datetime(timezone_name: str ="America/Los_Angeles") -> datetime:
        timezone=pytz.timezone(timezone_name)
        currrent_datetime=datetime.now(timezone)
        return currrent_datetime