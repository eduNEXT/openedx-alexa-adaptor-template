# ASK CLI

## What is ASK CLI?

ASK CLI _(Alexa Skills Kit Command Line Interface)_ is a command line tool
provided by Amazon for developers working on creating and managing voice skills
for Alexa-compatible devices, such as Amazon Echo devices. The ASK CLI
simplifies various tasks related to Alexa skill development, making it easy to
create and maintain these voice applications. All the steps to perform its
installation are listed below. More information about this process can be found
at the [following link](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html).

## Prerequisites for installing ASK CLI

Before installing the ASK CLI it is essential to have an
[Amazon Developer account](https://developer.amazon.com/).
Also, you must install on your computer [Node.js](https://nodejs.org/en),
npm and [git](https://git-scm.com/).

## Install and Initialize the ASK CLI

Using `npm` install the ASK CLI. You should use a Unix OS, such as Linux or
MacOS, if you are using Windows, we recommend using the Windows Subsystem for
Linux (WSL). To install the ASK CLI, run the following command:

```bash
sudo npm install -g ask-cli
```

Check that the ASK CLI was installed correctly by running the following command:

```bash
ask --version
```
