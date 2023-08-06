# HP Tracker

Tracking lib for python regarding [posta.hr](https://posta.hr) parcels.

## Usage

```python
>>> from hp_tracker import HPTracker
>>> track = HPTracker()
>>> track.track("LG616677175XX")
'{"23.12.2020 02:10:00": "Event information"}'
```

## Exceptions

`TrackingNetworkError` - Exception raised for errors with network connection or target server.
`TrackingStatusError` - Exception raised for errors with tracking number.


## Installing HP Tracker

HP Tracker is available on PyPI:

```console
$ python -m pip install hp_tracker
```