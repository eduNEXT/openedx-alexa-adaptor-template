# Table of Contents

- [Purpose](#purpose)
- [Usage](#usage)
- [The Sample Skill](#the-sample-skill)
- [Getting Help](#getting-help)
- [Contributing](#contributing)
- [License](#license)

## Purpose

This repository contains a sample Alexa skill that allows users to connect to
Open edX. With this skill, users can access course information, check grades,
and perform other Open edX-related tasks using voice commands with their
Alexa-enabled devices.

## Usage

To use this Alexa skill, you can use the Alexa simulator in the Amazon
Developer Console or an Alexa-enabled device. The skill is currently available
in English and Spanish.

The current version of the skill supports the following interactions:

- **Launch the skill**: "Alexa, open educational assistant."

  > _Alexa Response_: "Welcome \<first_name\>, this is the Open edX assistant,
  > I can provide you information about student metrics and important aspects
  > of a course."

  e.g:

  > "_Alexa Response_: Welcome **John**, this is the Open edX assistant, I can
  > provide you information about student metrics and important aspects of a
  > course."

- **Get course progress**: "Alexa, give me my progress in the course of
  \<course-name\>."

  > _Alexa Response_: "The progress for the student with
  > username \<username\> in the course of \<coursename\> is \<percentage\>.

  e.g:

  > "_Alexa Response_: The progress for the student with username **johndoe**
  > in the course of **Introduction to Linux** is **50%**."

### Develop

We created a `Makefile` to help you to prepare your environment and init with
the development of the skill. Before to use the commands, ensure that you have
the following requirements:

- Python 3.8, we recommend to use a virtual environment to avoid conflicts with other python projects.
- ASK CLI, follow the steps in the [ASK CLI documentation](./docs/1-ask-cli.md)

After to ensure that you have the requirements, you can use the following
commands:

- `make configure`: Configure the ASK CLI.
- `make build`: Create a new skill based in the sample skill.
- `make bootstrap`: Execute the above `configure` and `build`` commands.

### Deploy

Make deploy is very easy. As the skill is alexa-hosted, you can deploy the skill using only git commands. Follow the steps below:

1. Make your changes.
2. Commit your changes.
3. Push your changes to the repository. Ensure that you push to the `master` branch.

After to push your changes, the skill will be deployed automatically, only you need to wait a few seconds to see the changes in the skill in the Alexa Developer Console.

## The Sample Skill

### Purpose

The sample skill included in this repository is a basic demonstration of how to
integrate Alexa with Open edX. It showcases how to handle user requests,
authenticate with Open edX, and retrieve course data. Developers can use this
as a starting point to build more advanced interactions for Open edX.

### Requirements

Before setting up and running this sample skill, ensure you have the following
prerequisites:

1. An [Amazon Developer account](https://developer.amazon.com/) for creating
   and configuring the skill.
2. Access to an Open edX platform with admin privileges.
3. ASK CLI installed and configured. Follow the steps in the
   [ASK CLI documentation](./docs/1-ask-cli.md)
4. `eox-core` installed and configured. Follow the steps in the
   [Eox-core documentation](./docs/2-eox-core.md)

### Permissions

This skill requires some permissions in the alexa account to work properly.
Follow the steps below to configure the permissions:

1. Open the Alexa app.
2. Go to "More" → "Settings" → "Skills & Games" → "Your Skills".
3. Select "Open edX Assistant".
4. Select "Settings".
5. Select "Manage account permissions".
6. Enable **Email Address** permission.
7. Save the changes.

### Testing in the Amazon Developers Console

To test the sample Alexa skill, follow these steps:

1. Login to the [Amazon Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Select the Skill you want to test.
3. Select the "Test" tab.
4. Select "Development" from the "Skill testing is enabled in:" dropdown.
5. As the Skill uses voice profiles, to test interactions you need to do it by
   voice. If you are known profile, you can interact with the skill without
   problems. If you are not a known profile, the skill show you a message
   indicating that you are not a known profile and the interaction will finish.

## Getting Help

If you encounter any issues or have questions about using this Alexa skill,
feel free to create an issue in this repository. Our community and maintainers
will be happy to assist you.

## License

The code in this repository is licensed under the AGPL-3.0 unless otherwise
noted.

Please see LICENSE.txt for details.

## Contributing

We welcome contributions to improve this Alexa skill and make it more robust.
If you'd like to contribute, please follow these guidelines:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and commit them with clear, concise commit messages.
4. Push your changes to your fork.
5. Create a pull request to merge your changes into the main repository.

Please ensure that your code follows best practices.

Thank you for your interest in contributing to this project!

### Translations

This sample skill is initially available in English and Spanish. If you want
update your translation, please follow the steps below:

## Reporting Security Issues

Please do not report a potential security issue in public. Please email <security@edunext.co>.
