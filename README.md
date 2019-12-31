# tinysyslogd
tiny syslogd server written in python

## configuring rsyslog to send to this

create a file such as /etc/rsyslog.d/10-music-server.conf with:

    if $programname == 'music' then {
        @127.0.0.1:514
        ~
    }

Then restart rsyslog:

    service rsyslog restart

Then run the tinysyslogd to receive these messages:

    ./tinysyslogd.py

