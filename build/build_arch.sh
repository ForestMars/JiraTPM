# build.sh - Build script for compiling LoanInfo source code.

# CQRS read model
gcc -c -fPIC -I/usr/include/python3.8 -o jira_read_model .o lib/c/jira_read_model.c
gcc -shared -fPIC -I/usr/include/python3.8 -o lib/ext/jira_read_model.so jira_read_model.o

# CQRS wrute model
gcc -c -fPIC -I/usr/include/python3.8 -o jira_write_model .o lib/c/jira_write_model.c
gcc -shared -fPIC -I/usr/include/python3.8 -o lib/ext/jira_write_model.so jira_write_model.o
