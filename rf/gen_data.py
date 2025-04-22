# make_close_tracks.py  – run this once
import pandas as pd, numpy as np
from pathlib import Path

rng = np.random.default_rng(7)

dt, N = 30, 40
T0    = pd.Timestamp("2025-04-22 12:00:00")

# central rendez‑vous off Cape Lookout, NC
LAT_C, LON_C = 34.35, -76.52

TEMPL = {
    111111111: dict(lat0=LAT_C+0.00, lon0=LON_C-0.02, heading= 75, speed=12, wifi=5, bt=3, radar=1),
    222222222: dict(lat0=LAT_C-0.01, lon0=LON_C+0.00, heading=255, speed=10, wifi=2, bt=6, radar=0),
    333333333: dict(lat0=LAT_C+0.02, lon0=LON_C+0.02, heading=165, speed=11, wifi=4, bt=4, radar=1),
}

def step(lat, lon, hdg_deg, spd_kn, secs):
    d_m   = spd_kn * 0.514444 * secs
    dlat  = d_m / 111_320
    dlon  = d_m / (111_320 * np.cos(np.deg2rad(lat)))
    th    = np.deg2rad(hdg_deg)
    return lat + dlat*np.cos(th), lon + dlon*np.sin(th)

rows=[]
for vid,cfg in TEMPL.items():
    lat, lon = cfg['lat0'], cfg['lon0']
    for k in range(N):
        ts = T0 + pd.Timedelta(seconds=k*dt)
        hdg = cfg['heading'] + rng.normal(0,2)
        lat, lon = step(lat, lon, hdg, cfg['speed'], dt)
        lat += rng.normal(0, 2e-4); lon += rng.normal(0, 2e-4)  # gps jitter
        claimed = vid
        if vid==222222222 and k in (10,25): claimed = 444444444  # spoof
        if vid==333333333 and k==15:        claimed = ""         # dark
        rows.append(dict(timestamp=ts, lat=round(lat,5), lon=round(lon,5),
                         wifi_ct=int(cfg['wifi']+rng.integers(-1,2)),
                         bt_ct=int(cfg['bt']+rng.integers(-1,2)),
                         radar_on=cfg['radar'], vhf_ch16=rng.integers(0,2),
                         mean_rssi=round(-60+rng.normal(0,3),1),
                         true_vessel_id=vid, claimed_id=claimed))

df = pd.DataFrame(rows).sort_values("timestamp").reset_index(drop=True)
df["gt_alert"] = df.apply(
    lambda r: "dark" if r.claimed_id=="" or pd.isna(r.claimed_id)
              else ("normal" if int(r.true_vessel_id)==int(r.claimed_id) else "spoof"), axis=1)

out = Path("stream_demo_close.csv")
df.to_csv(out, index=False)
print(f"Wrote {out}, centred at {LAT_C:.2f},{LON_C:.2f}")