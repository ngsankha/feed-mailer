# Feed Mailer

This script was made to scratch a personal itch - how to keep up with
multiple blog source that I would like to read. Feed mailer sends a
daily digest of new links from RSS/Atom feeds from the blogs you choose
directly to your inbox. No junk, all in plain text.

## Usage

1. Copy the `config.sample.yaml` to you `config.yaml` and add your feeds
  and your Gmail username and password.
2. Run `feed_email.py` and it should send you an email with all links
   aggregated from the RSS feeds you listed.
3. Add `feed_email.py` to your crontab. My crontab runs the script every
   midnight!
4. Happy reading!

## License

MIT

