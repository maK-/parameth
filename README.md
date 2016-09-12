# parameth
This tool can be used to brute discover GET and POST parameters

Often when you are busting a directory for common files, 
you can identify scripts (for example test.php) that look like they need
to be passed an unknown parameter. This hopefully can help find them.

![example scan](http://makthepla.net/parameth/parameth.png)

The **-o** flag allows you to specify an offset (helps with dynamic pages)
so for example, if you were getting alternating response sizes of 4444 and
4448, set the offset to 5 and it will only show the stuff outside the norm


***NOTE:***
I will develop this further to account for dynamic pages etc., 
but at least it's a start
