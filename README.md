### Description
This is a pet project to count number of nodes for OpenShift Kubernetes cluster by given number of PODS/CNFs

### Installation / Setup  
**Python 3.8+ and installed venv module are needed**
```
python3 -m venv .venv 
source .venv/bin/activate
pip install -r requirements.txt
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


### Input data format
```cvs
name,mem,cpu,count,affinity
apache,100,3,3,3
nginx,100,3,3,3
```
`name` - name of pod group (must be unique)

`mem` - required memory per instance (MB)

`cpu` - required cpu per instance (Milli-Core) 

`count` - number of instances

`affinity` - affinity rules (pods in same group can not be launched on same server)

### Resuts and Demo

```python
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

```
Detailed view
```python
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


```

### TODO 
Probably make a web version
