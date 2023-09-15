# What is ASK CLI?

ASK CLI *(Alexa Skills Kit Command Line Interface)* is a command line tool provided by Amazon for developers working on creating and managing voice skills for Alexa-compatible devices, such as Amazon Echo devices. The ASK CLI simplifies various tasks related to Alexa skill development, making it easy to create and maintain these voice applications. All the steps to perform its installation are listed below. More information about this process can be found at the [following link](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html).


# Prerequisites for installing ASK CLI

Before installing the ASK CLI it is essential to have:

1. An [Amazon Developer account](https://developer.amazon.com/).

Also, you must install on your computer:

1. Node.js and `npm`. Install Node.js from version 14 or higher.
2. Git.


# Install and Initialize the ASK CLI

Using `npm` install the ASK CLI.

- If you are using **Windows** you must install the windows-build-tools package, to do this run PowerShell as administrator and run `npm install -g -production windows-build-tools`. Then run the command `npm install -g ask-cli`.

- If you are using **Linux/macOS** just run the command `sudo npm install -g ask-cli`.

You are now ready to configure the ASK CLI.


# How to configure ASK CLI?

To use the ASK CLI for the first time you need to configure it with your Amazon Developer account.

Run the `ask configure` command in your computer, and perform the following steps:

1. Create a new profile, and assign it a name.
Login to the Amazon Developer account from the browser window, and confirm from the console `(Y)`.
3. You do not need to associate the AWS profile with the ASK CLI, as it will be an [Alexa-hosted Skill](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/build-a-skill-end-to-end-using-an-alexa-hosted-skill.html), so type `(n)` from the console.

These steps will allow to execute any command using the ASK CLI.


# ASK CLI Commands

Among the most useful commands in the ASK CLI are:

- `ask new`: Allows you to create a Skill from scratch.
- `ask init --hosted-skill-id <hosted-skill-id>`: Allows to clone a Skill hosted in the current directory. The Skill ID can be obtained from the Amazon Development console in the Skills listing.
- `ask dialog`: Allows you to test the Skill from the console with an Alexa simulator.

To see a detailed description of all ASK CLI commands go to the [following link](https://developer.amazon.com/en-US/docs/alexa/smapi/ask-cli-command-reference.html).


# How to configure `eox-core`?

1. Create a Django OAuth Toolkit application at `<lms_domain>admin/oauth2_provider/application/add/`, copy the `client-id` and `client-secret`. Note the following when creating the application from the Django admin:

    - The **Client id** and **Client secret** are automatically generated, do not modify them.
    - The selected **User** should have administrator permissions.
    - Add to **Redirect uris** the URL of the LMS domain of the platform.
    - Select **Client type** as "Confidential"
    - Select **Authorization grant type** as "Client credentials"

    ![add-app](https://github.com/eduNEXT/openedx-alexa-adaptor-template/assets/64033729/b7f28637-d83c-4f46-918b-8ec8f0f0831c)
