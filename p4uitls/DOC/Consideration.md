## 1. How shoud we handle the exception?
`p4.errors->list` : Returns an array containing the error messages
received during execution of the last command.

> https://www.perforce.com/perforce/r15.1/manuals/p4script/python.p4.html

## 2. Supply input of a command using `p4.input->string | dict | list`.

## 3. Prevent your client program from costing too long time of the server.
* `p4.maxlocktime->int`
* `p4.maxscanrows->int`

## 4. Handle the messages retrived from the server.
* `p4.maxresults->int`
* `p4.messages->list(read-only)`
* `p4.warnings->list(read-only)`
* `p4.errors-list(read-only)`

## 5. Display the progress.
* Implement a subclass of `P4.Progress`.
* `p4.track_output->list(read-only)`.

## 6 Create your local perforce server
`P4.init()`, just like `git init`?

What is DVCS?
