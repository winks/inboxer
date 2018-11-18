# inboxer - send stuff via mail and automatically put it on the web

Clone and configure (please take a non-guessable email address or whitelist):
```
git clone https://github.com/winks/inboxer
cd inboxer
vi run_inboxer.sh
```

Add a cronjob:

```
*/5 *   * * *   /home/USER/code/inboxer/run_inboxer.sh
```
