# Thesis Robotics — Multi-World Q-Learning for Swarm Formation Control

A simulation framework, written in Python with `pygame`, for studying how a
swarm of differential-drive robots can learn to keep a formation while
travelling toward a goal. The headline contribution is a *multi-verse* (parallel
worlds) variant of Q-learning: several independent simulations run in parallel
and periodically exchange the best Q-tables when a single world is the leader
on both the *formation-disruption* and *trajectory-disruption* metrics.

The project was developed as part of a master's thesis. It includes both a
classical, distance-based formation controller (used as a baseline / reference
behaviour) and a learning controller trained from scratch with tabular
Q-learning.

---

## Repository layout

```
thesis_robotics/
├── base/                  # Active codebase
│   ├── main.py            # Entry point (training / demo / baseline)
│   ├── q_learn.py         # QLearn(Simulation): the Q-learning loop
│   ├── simulation.py      # Simulation: classical/baseline simulator
│   ├── formation.py       # Formation + Trajectory definitions
│   ├── state.py           # State representation seen by the agents
│   ├── sensor.py          # Ultrasonic ray-cast sensor
│   ├── graphics.py        # pygame rendering
│   ├── equilateral.py     # Helper to compute the third vertex of a triangle
│   ├── results.py         # Plot stored reward curves
│   ├── simple.job         # Slurm batch script (headless training)
│   ├── dependencies       # Plain-text list of Python deps
│   ├── robots/
│   │   ├── robot.py           # Base Robot (kinematics, sensors, paths)
│   │   ├── distance_robot.py  # Potential-field distance controller (baseline)
│   │   ├── learn_robot.py     # Q-learning agent
│   │   └── swarm.py           # Swarm + LearnSwarm aggregators
│   ├── utils/
│   │   ├── constants.py        # Action / direction / spacing constants
│   │   ├── dimensions.py       # Map, robot, sensor sizes
│   │   ├── counter.py          # Default-zero dict used as Q-table
│   │   ├── utils.py            # Geometry / heading / colour helpers
│   │   ├── qlearn_utils.py     # Pickle save/load, plotting, spacing helpers
│   │   └── simulation_utils.py # Distance logs, pygame quit handling
│   ├── sprites/                # Map, robot and area images (.png/.kra)
│   └── TRAINED_FILES/          # Pickled Q-tables and reward/distance logs
├── v3_backup/             # Older snapshot of main.py / learn_robot.py + logs
├── .vscode/
└── .gitignore
```

The active code lives under `base/`. `v3_backup/` keeps a previous iteration
of the same files for reference and is excluded by `.gitignore`.

---

## Requirements

Python 3.8+ and the libraries listed in `base/dependencies`:

- `pygame`
- `numpy`
- `scipy`
- `scikit-learn`
- `matplotlib`

Install with:

```bash
pip install pygame numpy scipy scikit-learn matplotlib
```

The simulator opens a pygame window by default. On a server / cluster, run
with `--headless` to use the SDL dummy video driver.

---

## Running

All commands are run from inside `base/`:

```bash
cd base
```

### Demo a trained controller

Loads the pickled Q-tables in `TRAINED_FILES/trained_controller` and replays
each learned world (or a random one if `ALL = False` in `main.py`):

```bash
python3 main.py --demo
```

### Baseline (no learning)

Set `Q_LEARN = False` in `main.py` and run any version. The baseline uses the
distance / potential-field controller from `robots/distance_robot.py`:

```bash
python3 main.py -v 0
```

### Train

`main.py` exposes four behaviour modes via `-v/--version` (mapped to the
`PROGRESS` variable):

| `-v` | mode                                                |
| :--: | --------------------------------------------------- |
| `-1` | Demo (same as `--demo`)                             |
| `0`  | Single-world training, optionally pooled            |
| `1`  | Parallel worlds, no info exchange                   |
| `2`  | Parallel worlds **with** best-world info exchange   |

The default (no flag) is `-v 2`, the multi-verse variant studied in the
thesis. To resume from the last checkpoint in `TRAINED_FILES/`:

```bash
python3 main.py -v 2 --resume
```

To run on a headless machine (no display):

```bash
python3 main.py -v 2 --headless
```

A Slurm batch script (`simple.job`) is provided for cluster runs:

```bash
sbatch simple.job
```

### Plot training curves

After (or during) training, regenerate `REWARDS.png` from the pickled reward
log:

```bash
python3 results.py
```

---

## How it works

### The world

The map (`sprites/MAP.png`) is `800 × 300` px and contains black obstacles
that the robots' ultrasonic ray-cast sensors detect by reading pixel colours
(`sensor.py`). Three robots are spawned in a tight triangle on the left edge
and must reach a goal point on the right while keeping their relative
distances close to `ideal_dist = 50` px.

### Robots

- **`Robot`** (`robots/robot.py`) — differential-drive kinematics, an
  `Ultrasonic` sensor with `n_rays = 9` over a 180° fan, and a basic
  obstacle-avoidance controller that biases left/right wheel speeds based on
  ray distances.
- **`DistanceRobot`** — overrides the controller with an artificial-potential
  field (`_ro_ij`, `_p_ij_tilda` in `utils/utils.py`) that pulls each robot
  toward the desired inter-robot distance. Used as the non-learning baseline.
- **`LearnRobot`** — Q-learning agent. Holds its own `Counter`-backed
  Q-table (`utils/counter.py`), an action history, and a small set of
  discrete actions: hard heading change to one of 8 compass directions plus
  `ACCELERATE` / `DECELERATE` / `STRAIGHT`.

### State

For each robot (`state.py`):

```
[ self.heading,
  towards_goal (bool),
  spacing(other₁) ∈ {IN_RANGE, TOO_FAR, TOO_CLOSE},
  relative_direction(other₁),
  other₁.heading,
  spacing(other₂),
  relative_direction(other₂),
  other₂.heading ]
```

The continuous heading is bucketed into 8 directions
(`get_direction_from_heading`) and inter-robot distances are bucketed into
3 spacing classes around `ideal_dist` (±15 px tolerance).

### Reward

Implemented in `LearnRobot.compute_reward`:

- `+30000 / dist_to_endpoint` — pull toward the goal.
- `+100` per neighbour that is `IN_RANGE`.
- `-10` per neighbour that is `TOO_FAR` or `TOO_CLOSE`.
- `-1` per step (penalises slow solutions).

### Q-learning loop

`q_learn.py` runs the standard tabular update

```
Q(s,a) ← Q(s,a) + α · ( r + γ · maxₐ' Q(s',a') − Q(s,a) )
```

at a fixed timer step (`0.05 s / training_speed`) inside the pygame loop.
Default hyper-parameters in `main.py`:

- `α = 0.7` (learning rate)
- `γ = 0.9` (discount)
- `ρ = 0.2` (ε-greedy exploration probability)
- `train_iterations = 1000`
- `training_speed = 10` (simulation frames per real frame)
- `sim_duration = 1500` ticks per episode

A "STRAIGHT_START" warm-up forces every agent to drive straight for the first
`train_iterations / 8` ticks so that the early Q-table is bootstrapped from
sensible trajectories instead of random spinning.

### Multi-verse with info exchange (PROGRESS = 2)

Each iteration spins up `learning_worlds` independent `QLearn` simulations
in parallel via `multiprocessing.Pool`. After every iteration each world
returns:

- `formation_disr` — accumulated triangle-area deviation (formation quality).
- `traj_disr` — variance of trapezoidal areas under each robot's path
  (trajectory quality, computed in `Trajectory.compute_total_traj_disruption`).
- the updated Q-tables, total rewards and distance logs.

If the same world is ranked first on both `formation_disr` and `traj_disr`,
its Q-tables are broadcast to every other world before the next iteration —
otherwise each world keeps its own tables. The exchange counter and the
iteration index of every exchange are persisted to
`TRAINED_FILES/info_exch[_counter]`.

Checkpoints are written every 10 iterations to `TRAINED_FILES/`:

| File                 | Contents                                       |
| -------------------- | ---------------------------------------------- |
| `trained_controller` | List of Q-tables, one per learning world       |
| `tot_avg_rewards`    | Mean rewards per iteration across worlds       |
| `tot_min_rewards`    | Min rewards per iteration                      |
| `tot_max_rewards`    | Max rewards per iteration                      |
| `all_dists_logs`     | Per-pair inter-robot distance averages         |
| `info_exch`          | Iterations on which an exchange happened       |
| `info_exch_counter`  | Total number of exchanges                      |
| `iter_counter`       | Cumulative iteration counter                   |

`--resume` reloads all of the above and continues training.

### Class hierarchy at runtime

```
main.py
└── QLearn(Simulation)              q_learn.py
    ├── LearnSwarm(Swarm)           robots/swarm.py
    │   └── LearnRobot(Robot) ×3    robots/learn_robot.py
    │       └── State               state.py
    ├── Formation                   formation.py
    │   └── Trajectory  ×3
    └── Graphics (pygame)           graphics.py
```

---

## Tunable parameters

The most useful knobs live near the top of `base/main.py`:

```python
Q_LEARN              = False        # baseline vs Q-learn
training_speed       = 10
exploration_rho      = 0.2          # ε
lr_alpha             = 0.7          # α
discount_rate_gamma  = 0.9          # γ
train_iterations     = 1000
RANDOM_START         = False
STRAIGHT_START       = True
learning_worlds      = 3            # parallel worlds (Pool size)
formation_discount   = 0.9
trajectory_discount  = 0.7
```

Map / sensor / robot sizes live in `base/utils/dimensions.py` and the action
& direction vocabularies in `base/utils/constants.py`.

---

## Known quirks

- Some files include an **OS-specific Python `match` statement** that has been
  commented out and replaced with `if/elif` chains, for compatibility with
  Python ≤ 3.9. Re-enable the `match` versions if you are on 3.10+.
- `utils/qlearn_utils.py` redefines `GLOBAL_DIRECTIONS` and `LOCAL_DIRECTIONS`
  with values that differ from `utils/constants.py`. The constants from
  `constants.py` are the ones actually used by the agents — the duplicates at
  the bottom of `qlearn_utils.py` are dead code.
- `main.py` contains two `if __name__ == "__main__" and PROGRESS == 0` blocks
  back-to-back; only the first one ever runs.
- The Slurm script in `simple.job` requests the `red`/`brown` partition and a
  64-core node — adapt to your cluster before submitting.
- `v3_backup/` is an older snapshot kept for reference; it is excluded by
  `.gitignore` and is **not** the code that is executed.

---

## Reproducing the figures

`base/REWARDS.png` and `base/lol.png` in the repository were produced by
running `results.py` against the checkpoints under `base/TRAINED_FILES/`.
After a training run, regenerate them with:

```bash
cd base
python3 results.py
```
