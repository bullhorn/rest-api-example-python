bullhorn-api-example-python
===========================
This a sample Python application that demonstrates a very simple usage of the Bullhorn REST API from a Web application.

The biggest initial hurdle for developers is typically getting OAuth authentication working properly, so much
of this sample is dedicated to that.

You will need an OAuth partner key and secret to run the sample app successfully.

This sample uses a small Python Web framework, [web.py](http://webpy.org/) to spin up a Web application
in order to demonstrate the full OAuth redirect, authenticate, redirect flow.

There are four source files:
 1. api.py - Utility functions for logging in to the REST API and making calls to it
 2. oauth.py - Utility functions for making OAuth authentication calls
 3. web_utils.py - A few general Web utility functions
 4. api_example.py - The main sample app code.  Spins up and configures the Web app, and
    implements request handlers for OAuth and sample API calls.
