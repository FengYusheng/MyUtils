## 1. My folder in jiaozi IT

`\\jiaozi\IT\Documents\Feng Yusheng`

My local VM : Fengyusheng/beyondsoft


## 2. The structure of each proxy template

### The main proxy template

Each template contains these scripts:

1. globals.bash
2. preload.bash
3. settings.sh
4. start-p4p.bash

These four scripts are in "Cardinal P4" folder. The "Cardinal folder" is inherited by
every individual specific proxy template.

### Individual specific proxy templates

Every individual specific proxy is inherited from the "Cardinal P4" template and
they have three python scripts:

1. clearup.py
2. get_latest_cl.py
3. getDepotSize.py

and three shell scrpits:

1. test.sh
2. test2.sh
3. trust-p4

## What the scripts do in each template?

### Two kinds of "start-p4p" bash scripts

#### 1. `Cardinal P4/start-p4p`
Guide the user through **starting a `p4p` process** and save the process id in a `start-p4p.pid` plain text file.

#### 2. `start-p4p` in "clean P4P"
Initialize the system environment by calling "globals.sh" and "settings.sh" in the same folder
 and then starting a `p4p` process (*Questions or my script should supply something*).

`globals.sh` in "clean P4P" initializes several variables. What do these variables do?

1. `proxy_ip`
2. `build_share_server`
3. `build_share_user`
4. `build_share_domain`
5. `build_share_name`
6. `build_share_password`
7. `base_dir`

`settings.sh` in "clean P4P" initializes some variables and proxy preload paths. (*Questions or my script should supply something*).

Variables in `settings.sh`:
1. `project_name`
2. `project_port`
3. `depotSourcePath`
4. `buildPath`
5. `root_dir`
6. `p4_remote_pass`
7. `p4_user`
8. `p4_remote`
9. `workspace`
10. `preload_paths`

`Preload.sh` in "clean P4P" logins the proxy and sync files from the specific depot path. (*Questions or my script should supply something*).

#### 3. `start-p4p` in "nuke p4"
This file is identical to the `start-p4p` in "clean P4P".

`globals.sh` in "nuke p4" is identical to the `globals.sh` in "clean P4P".

`settings.sh` in "nuke p4" is identical to the `settings.sh` in "nuke p4".

`status.sh` in "nuke p4" class `sync -N` to retrieve statistic information (*Questions or my script should supply something*).

`test2.sh` and `test.sh` seem useless.

`cleanup.py` in "nuke p4" delete the files which are either older than specific days or ... in a proxy cache(*Questions or my script should supply something*).

`getDepotSize.py` in "nuke p4" gets the depot size from the customer's server.

`get_latest_cl.py` in "nuke p4" gets the file names from a samba server, and write these
names into a file called "/raid5/ram_1111/bin/latest_cl". (*Questions or my script should supply something*)

`shared_scripts/get_latest_cl.py` in "nuke p4" seems like a command line interface.
This file get global variables by reading `globals.sh` and `settings.sh`, and then gets the file names
from a samba server, and write these names into a file.


`shared_scripts/parse_sync_output.py` in "nuke p4" displays the sync progress. (*Questions or my script should supply something*).

`shared_scripts/set_build_ok.py` in "nuke p4" sets the ".ini" files, it seems incomplete.

`shared_scripts/set_build_uncached.py` in "nuke p4" seems identical to `shared_scripts/set_build_ok.py`

`shared_scripts/UberSync.py` in "nuke p4", **the comment at the head of this file is important.**

## 3. TODOs
Generate bash scripts via Python shlex module.

## 4. Questions

1. Who are the users?
2. What does the tool do, connect to a proxy or create a proxy?
3. Make a directory, named "PROJECT_PORT"?
4. Some variables are used to connect to a p4 proxy. Some variables are used to connect
to a samba server. What are stored in the samba?
