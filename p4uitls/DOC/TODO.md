## Get the p4 environment variables.
P4CHARSET, P4CLIENT, P4CONFIG, P4HOST, P4IGNORE,
`p4.config_file->string(read-only)`, P4PASSWD, `p4.server_case_insensitive`,
P4TICKETS,

`p4.server_level->int(read-only)`
This variable will be assign a number to indicate the server number after the
first command is run.

>http://answers.perforce.com/articles/KB/3194?startURL=%2Farticles%2FKB_Article%2FPerforce-Server-Levels

`p4.server_unicode->boolean`: Detect whether or not the server is in Unicode mode.

`p4.ticket_file->string`: Contains the location of your P4TICKETS file.

`P4.identify()`: Return the version of P4PYTHON that you are using.

`p4.env(var)`

## Make a multi-thread version .
`p4.disable_tmp_cleanup -> string`: call this method prior to connecting to
server, this method make your connection thead-safe.

> https://www.perforce.com/perforce/r15.1/manuals/p4script/python.p4.html

## Implement a subclass of `P4.OutputHandler`

## Get the information of the <spectype>
* Get information: `p4.fecth_<spectype>()->P4.Spec`.
* Display the information: `p4.format_<spectype>(dict)->string`
