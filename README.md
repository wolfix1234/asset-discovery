# watchtower
welcome to my watchtower :) this is a crawler for bug bounty for finding some asset

## setup the watch
1. inside the database folder run `docker compose up -d`
2. modify the config/.env file
3. install requirements
```bash
pip3 install -r requirements.txt
```
if you get error for not having virtualenv you can install them one by one with
```bash
apt install python3-xyz
```
4. configure zsh alias variables

## zshrc configurations
add following lines to your `~/.zshrc` file:
```bash
export WATCH="/opt/watch_narutow"
alias watch_sync_programs="$WATCH/programs/watch_sync_programs.py"
alias watch_sync_chaos="$WATCH/chaos/watch_sync_chaos.py"
alias watch_subfinder="$WATCH/enum/watch_subfinder.py"
alias watch_crtsh="$WATCH/enum/watch_crtsh.py"
alias watch_abuseipdb="$WATCH/enum/watch_abuseipdb.py"
alias watch_chaos="$WATCH/enum/watch_chaos.py"
alias watch_wayback="$WATCH/enum/watch_wayback.py"
alias watch_gau="$WATCH/enum/watch_gau.py"
alias watch_enum_all="$WATCH/enum/watch_enum_all.py"
alias watch_ns="$WATCH/ns/watch_ns.py"
alias watch_ns_static_brute="$WATCH/ns/watch_ns_static_brute.py"
alias watch_ns_dynamic_brute="$WATCH/ns/watch_ns_dynamic_brute.py"
alias watch_ns_all="$WATCH/ns/watch_ns_all.py"
alias watch_http="$WATCH/http/watch_http.py"
alias watch_http_all="$WATCH/http/watch_http_all.py"
alias watch_nuclei="$WATCH/nuclei/watch_nuclei.py"
alias watch_nuclei_all="$WATCH/nuclei/watch_nuclei_all.py"
```
5. you need to add your resolvers in ~/.resolvers

6. do the following commands for start:
```bash
watch_sync_programs
watch_sync_chaos
watch_enum_all
watch_ns_all
watch_http_all
watch_nuclei_all
```
7. run with this command:
```bash
python3 app.py
```
8. put watch.sh in cronjob
