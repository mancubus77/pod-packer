## Description
This is a pet project to count number of nodes for OpenShift Kubernetes cluster by given number of PODS/CNFs.

## Installation / Setup  
**Python 3.8+ and installed venv module are needed**
### install 
```shell
python3 -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
```
or for impatient
```shell
make install
make run
```

Script reads CSV file, which can be given via arguments
```
❯ python main.py -h
usage: main.py [-h] -i FILE [-d] [--csv]                                                                                                                                 ─╯

Read CSV form given path.

optional arguments:
  -h, --help            show this help message and exit
  -i FILE, --input FILE
                        input file
  -d, --detail          Detailed view of pods breakdown
  --csv                 csv output, needs to be used with -d/--detail
```

To update servers HW specifications modify `main.py`
```python
# Minimum workers to start calculation
MIN_WORKERS = 3 
# CPUs on server (cores)
COMPUTE_CPU = 104
# Memory on server (MB)
COMPUTE_MEM = 384000
# Allowed maximum resource allocation (for redudancy)
ALLOCATION_PERCENT = 70
```


## Input data format (CSV)
```
app,mem,cpu,count,affinity
apache,100,3,6,3
nginx,100,3,6,3
```
`name` - name of pod group (must be unique)

`mem` - required memory per instance (MB)

`cpu` - required cpu per instance (Milli-Core) 

`count` - number of instances

`affinity` - affinity rules (pods in same group can not be launched on same server)

`platform` - (optional) used when apps have same names, but belong to different groups/platforms. For example app1:nginx and app2:nginx are not the same

## Results and Demo

```shell
> python main.py -i data_sample/example.csv
 [Tue, 21 Dec 2021 23:46:13] INFO [main.py.<module>:31] Starting allocation, there are 2 pods to be allocated
 [Tue, 21 Dec 2021 23:46:13] INFO [node.py.__init__:29] Creating new node compute-0
 [Tue, 21 Dec 2021 23:46:13] INFO [node.py.__init__:29] Creating new node compute-1
 [Tue, 21 Dec 2021 23:46:13] INFO [node.py.__init__:29] Creating new node compute-2
+-----------+------+----------+-------------+----------+-------------+
|   Node    | Pods | CPU Used | CPU Used, % | MEM Used | MEM Used, % |
+-----------+------+----------+-------------+----------+-------------+
| compute-0 |  2   |  0.006   |    0.006    |   200    |    0.052    |
+-----------+------+----------+-------------+----------+-------------+
| compute-1 |  2   |  0.006   |    0.006    |   200    |    0.052    |
+-----------+------+----------+-------------+----------+-------------+
| compute-2 |  2   |  0.006   |    0.006    |   200    |    0.052    |
+-----------+------+----------+-------------+----------+-------------+
SUMMARY
+-------+------+-------+-------+
| nodes | pods |  cpu  |  mem  |
+-------+------+-------+-------+
|   3   |  12  | 0.036 | 1,200 |
+-------+------+-------+-------+

```
Detailed view
```shell
❯ python main.py -i data_sample/example.csv -d
 [Wed, 22 Dec 2021 16:59:43] INFO [main.py.<module>:65] Starting allocation, there are 2 apps to be allocated                                                            ─╯
 [Wed, 22 Dec 2021 16:59:43] INFO [node.py.__init__:29] Creating new node compute-0
 [Wed, 22 Dec 2021 16:59:43] INFO [node.py.__init__:29] Creating new node compute-1
 [Wed, 22 Dec 2021 16:59:43] INFO [node.py.__init__:29] Creating new node compute-2
+-----------+--------+-----+-------+----------+--------------+
|   node    |  app   | mem |  cpu  | affinity | max_per_node |
+-----------+--------+-----+-------+----------+--------------+
| compute-0 | apache | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-0 | apache | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-0 | nginx  | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-0 | nginx  | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-1 | apache | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-1 | apache | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-1 | nginx  | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-1 | nginx  | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-2 | apache | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-2 | apache | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-2 | nginx  | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
| compute-2 | nginx  | 100 | 0.003 |    3     |      2       |
+-----------+--------+-----+-------+----------+--------------+
+-----------+---+-------+-------+-----+-------+
| compute-0 | 4 | 0.012 | 0.012 | 400 | 0.104 |
+-----------+---+-------+-------+-----+-------+
| compute-1 | 4 | 0.012 | 0.012 | 400 | 0.104 |
+-----------+---+-------+-------+-----+-------+
| compute-2 | 4 | 0.012 | 0.012 | 400 | 0.104 |
+-----------+---+-------+-------+-----+-------+
SUMMARY
+-------+------+-------+-------+
| nodes | pods |  cpu  |  mem  |
+-------+------+-------+-------+
|   3   |  12  | 0.036 | 1,200 |
+-------+------+-------+-------+



```

### Failure domain
After allocation the application shutdown nodes on by one and ensure that pods can be evicted. Anit-Affinity violation is ignored.
In example below, if `compute-0` fails, pod `AUSF` won't be able to find a new node with sufficient resources. Test is failed (the app doesn't take in consideration min availability and pod disruption budget) 
```shell
[Sat, 12 Feb 2022 16:52:46] WARNING [node_list.py.is_node_schedulable:70] Node compute-2 is full: CPU: True MEM: False 216130 : 384000.0
[Sat, 12 Feb 2022 16:52:46] ERROR [main.py.run_allocations:49] FAILED: Can not evict AUSF from failed node compute-1
Reconsider ALLOCATION_PERCENT values, it's 100% now
Allocated nodes: 4
NODE BREAKDOWN
+-----------+-----------+---------+--------+---------+--------+
|   node    | pod count |   cpu   | cpu,%  | mem, GB | mem,%  |
+-----------+-----------+---------+--------+---------+--------+
| compute-0 |    90     | 103.953 | 99.955 | 215,767 | 56.189 |
+-----------+-----------+---------+--------+---------+--------+
| compute-1 |    85     | 103.977 | 99.978 | 215,216 | 56.046 |
+-----------+-----------+---------+--------+---------+--------+
| compute-2 |    92     | 103.99  | 99.99  | 210,212 | 54.743 |
+-----------+-----------+---------+--------+---------+--------+
| compute-3 |    14     |  8.135  | 7.822  | 18,596  | 4.843  |
+-----------+-----------+---------+--------+---------+--------+
```

### TODO 
Probably make a web version
