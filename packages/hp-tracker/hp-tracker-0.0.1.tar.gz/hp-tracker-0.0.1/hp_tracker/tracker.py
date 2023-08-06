import requests
from bs4 import BeautifulSoup

from hp_tracker.exceptions import TrackingNetworkError, TrackingStatusError


class HPTracker:
    """Main tracking class."""

    def __init__(self):
        self.allowed_classes = ["styles__date", "styles__status"]
        self.base_url = "https://posiljka.posta.hr/Tracking/Details"
        self.target_container = "div[class*='styles__row']"
        self.target_id = "hp-track-and-trace-component"

    def track(self, track_no):
        return self._get_response(track_no)

    def _get_response(self, track_no):
        param = {"Barcode": track_no}
        try:
            page = requests.get(self.base_url, params=param)
        except requests.exceptions.RequestException:
            raise TrackingNetworkError
        soup = BeautifulSoup(page.content, "html.parser")
        target = soup.find(id=self.target_id)
        if not target:
            raise TrackingStatusError(track_no)
        track_status = {}
        for list_element in soup.select(self.target_container):
            elements = [
                e
                for e in list(list_element.children)
                if any(x in str(e) for x in self.allowed_classes)
            ]
            if len(elements) < 2:
                continue
            track_status[elements[0].get_text()] = elements[1].get_text()

        return track_status
