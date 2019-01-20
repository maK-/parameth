# parameth
This tool can be used to brute discover GET and POST parameters

Often when you are busting a directory for common files, 
you can identify scripts (for example test.php) that look like they need
to be passed an unknown parameter. This hopefully can help find them.

![example scan](https://pbs.twimg.com/media/CsHJsjsXEAAOgxK.jpg)

The ***-off*** flag allows you to specify an offset (helps with dynamic pages)
so for example, if you were getting alternating response sizes of 4444 and
4448, set the offset to 5 and it will only show the stuff outside the norm

# Installation

```shell
virtualenv venv
. ./venv/bin/activate
pip install -u -r requirements.txt
```


# Usage

```
usage: parameth.py [-h] [-v] [-u URL] [-p PARAMS] [-H HEADER] [-a AGENT]
                   [-t THREADS] [-off VARIANCE] [-diff DIFFERENCE] [-o OUT]
                   [-P PROXY] [-x IGNORE] [-s SIZEIGNORE] [-d DATA]
                   [-i IGMETH] [-c COOKIE] [-T TIMEOUT]

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Version Information
  -u URL, --url URL     Target URL
  -p PARAMS, --params PARAMS
                        Provide a list of parameters to scan for
  -H HEADER, --header HEADER
                        Add headers in format a:b c:d
  -a AGENT, --agent AGENT
                        Specify a user agent
  -t THREADS, --threads THREADS
                        Specify the number of threads.
  -off VARIANCE, --variance VARIANCE
                        The offset in difference to ignore (if dynamic pages)
  -diff DIFFERENCE, --difference DIFFERENCE
                        Percentage difference in response (recommended 95)
  -o OUT, --out OUT     Specify output file
  -P PROXY, --proxy PROXY
                        Specify a proxy in the form http|s://[IP]:[PORT]
  -x IGNORE, --ignore IGNORE
                        Specify a status to ignore eg. 404,302...
  -s SIZEIGNORE, --sizeignore SIZEIGNORE
                        Ignore responses of specified size
  -d DATA, --data DATA  Provide default post data (also taken from provided
                        url after ?)
  -i IGMETH, --igmeth IGMETH
                        Ignore GET or POST method. Specify g or p
  -c COOKIE, --cookie COOKIE
                        Specify Cookies
  -T TIMEOUT, --timeout TIMEOUT
                        Specify a timeout in seconds to wait between each
                        request
```

# Adding new params from source:

The following regexes might be useful to parse `$_GET` or `$_POST` parameters from source:

> $> grep -rioP '\$_POST\[\s*["\']\s*\w+\s*["\']\s*\]' PHPSOURCE  | grep -oP '\$_POST\[\s*["\']\s*\w+\s*["\']\s*\]' | sed -e "s/\$_POST\[\s*[\"']//g"  -e "s/\s*['\"]\s*\]//g" | sort -u > /tmp/outfile.txt 

> $> grep -rioP '\$_GET\[\s*["\']\s*\w+\s*["\']\s*\]' PHPSOURCE  | grep -oP '\$_GET\[\s*["\']\s*\w+\s*["\']\s*\]' | sed -e "s/\$_GET\[\s*[\"']//g"  -e "s/\s*['\"]\s*\]//g" | sort -u > /tmp/outfile.txt
