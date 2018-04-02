import sys
sys.path.append('/home/kevin/Documents/github/e-coli-beach-predictions/python_src')

import read_data as rd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.cluster.hierarchy import linkage, fcluster

df = rd.read_data(verbose=True, read_drek=False, read_holiday=False,
                  read_weather_station=False, read_water_sensor=False,
                  read_daily_forecast=False, read_hourly_forecast=False,
                  group_beaches=True)
df = df.pivot(index='Full_date',
              columns='Client.ID',
              values='Escherichia.coli')
df.sort_index()

df.columns = [c.replace('North', 'N.').replace('South', 'S.')
              for c in df.columns]

lag_corr = df.apply(lambda col: col.autocorr(lag=1))

corr = df.corr()

l = linkage(corr)
labels = fcluster(l, .2)
inds = np.zeros(corr.shape[0], dtype=int)

inds = []
for label in range(max(labels)):
    inds.extend(np.where(labels == label)[0].tolist())

inds = np.array(inds)

corrv = corr.values[inds].T[inds]

f = plt.figure(figsize=(9,9))

gs = gridspec.GridSpec(10, 10)

ax_lag_bot = plt.subplot(gs[1:, -1])
ax_lag_bot.imshow(lag_corr.values[inds][:, None], vmin=0, vmax=1)
ax_lag_bot.set_ylabel('auto-correlation (lag 1)')
ax_lag_bot.set_axis_off()

ax = plt.subplot(gs[1:, :-1])

ax.set_title('same-day interbeach correlations (left), lag 1 auto-correlations (right)')
ax.imshow(corrv, vmin=0, vmax=1)
ax.set_xticks(np.arange(corr.shape[0]))
plt.xticks(rotation=70)
ax.set_xticklabels(corr.columns[inds])
ax.set_yticks(np.arange(corr.shape[0]))
ax.set_yticklabels(corr.columns[inds])
ax.set_xlim([-.5, corr.shape[0]-1.5])
ax.set_ylim([-.5, corr.shape[0]-1.5])
for d in ["left", "top", "bottom", "right"]:
    ax.spines[d].set_visible(False)
f.align_labels()
plt.savefig('corr.png', transparent=True)
plt.show()
