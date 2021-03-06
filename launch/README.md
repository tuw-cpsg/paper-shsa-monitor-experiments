# Demo Commands

The commands below demonstrate [shsa-prolog] for the [SASO 2019](https://saso2019.cs.umu.se/) paper:
*"Fault Detection exploiting Implicit Redundancy with Uncertainties in Space and Time"*

Prerequisites:

* Build [custom docker image] for demos with [SHSA] and [Daisy].
* Clone this repository (`/path/to/paper-shsa-monitor-experiments`).


## Network

Notebook has to be time-synchronized with [Daisy]
(because the demo uses transforms and timestamps are essential for the SHSA monitor).
Used router to connect to the hosts on the rover
(however, NTP could be established with IP forwarding too).


## Application

Start application, [Daisy] starts moving around (turning when it comes near an obstacle):
```bash
$ docker run --rm -it --network=host \
    -v /home/<username>/.ssh/:/root/.ssh/ \
    -v /path/to/paper-shsa-monitor-experiments/:/catkin_ws/src/demo/ \
    paper:shsa-prolog roslaunch demo demo.launch notebook:=<your hostname>
```

Enable motors (if necessary):
```bash
$ docker run --rm -it --network=host \
    -v /path/to/paper-shsa-monitor-experiments/:/catkin_ws/src/demo/ \
    paper:shsa-prolog roslaunch demo enablemotors.launch
```


## SHSA

Start monitoring:
```bash
$ docker run --rm -it --network=host \
    -v /path/to/paper-shsa-monitor-experiments/:/catkin_ws/src/demo/ \
    paper:shsa-prolog roslaunch demo monitor.launch
```


## Log

```bash
$ docker run --rm -it --network=host \
    -v /path/to/paper-shsa-monitor-experiments/:/catkin_ws/src/demo/ \
    paper:shsa-prolog roslaunch demo log.launch
```


## Visualization

Uses [docker GUI image] in addition.

### Runtime information

Run `visualization.launch` and rviz:
```bash
$ x11docker --hostnet ros:gui rviz
```
To reuse configs (`visualization.rviz`) for rviz use additional option
`--homedir /path/to/paper-shsa-monitor-experiments` of `x11docker`.

Other:
```bash
$ x11docker --hostnet --homedir /path/to/paper-shsa-monitor-experiments ros:gui rviz -d ~/config/visualization.rviz
$ x11docker --hostnet ros:gui rqt_plot /emergency_stop/dmin/data /dmin_monitor/value_0/data /dmin_monitor/value_1/data
$ x11docker --hostnet ros:gui rqt_graph
$ x11docker --hostnet ros:gui rosrun rqt_tf_tree rqt_tf_tree
```

### Plot logged data

```bash
$ x11docker --homedir /path/to/paper-shsa-monitor-experiments \
    paper:shsa-prolog ~/plot/plt_monitor.py ~/log/topics_<timestamp>.bag
```

Plot specific signals with:
```bash
$ x11docker --homedir /path/to/paper-shsa-monitor-experiments/ \
    paper:shsa-prolog -- bag_plot -b ~/log/topics_<timestamp>.bag -k /dmin_monitor/debug/outputs/0/bot /dmin_monitor/debug/outputs/1/bot /dmin_monitor/debug/outputs/2/bot
```


[custom docker image]: ../docker/README.md
[docker GUI image]: https://github.com/dratasich/docker/ros-gui
[Daisy]: https://tuw-cpsg.github.io/tutorials/daisy/
[SHSA]: https://github.com/dratasich/shsa_ros
[shsa-prolog]: https://github.com/dratasich/shsa-prolog
