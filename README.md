# Coinbase DCA Script

This is a basic Python script with the Coinbase API to purchase $SOL and $ETH tokens.
You can add to a cron job with `crontab -e` and then adding something along the lines
of `10 0 * * * /path/to/script/main.py >> ~/cron.log 2>&1`
