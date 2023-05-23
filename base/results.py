import pickle
import matplotlib.pyplot as plt
from utils.qlearn_utils import make_plots

# fr = open('all_dists_logs', 'rb')
# dists_logs = pickle.load(fr)
# make_plots(dists_logs)


fr = open('./TRAINED_FILES/tot_avg_rewards', 'rb')
tot_avg_rewards = pickle.load(fr)
length = len(tot_avg_rewards)
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ax.plot(range(length), tot_avg_rewards, color='tab:blue')
plt.savefig("REWARDS.png")
