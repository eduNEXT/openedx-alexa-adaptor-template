# Open edX Alexa Adaptor Template

## Table of Contents

- [Purpose](#purpose)
- [The Sample Skill](#the-sample-skill)

  - [Description](#description)
  - [Features](#features)
  - [Usage](#usage)

- [Creating the Skill](#creating-the-skill)

  - [Prerequisites](#prerequisites)
  - [Development](#development)
  - [Deployment](#deployment)

- [Configuring the Skill](#configuring-the-skill)

  - [Adding Environment Variables](#adding-environment-variables)
  - [Configuring Permissions](#configuring-permissions)

- [Testing the Skill](#testing-the-skill)

  - [Testing In Amazon Developer Console](#testing-in-amazon-developer-console)

- [Working with the Skill](#working-with-the-skill)

  - [Create a Custom Email Authentication Backend](#create-a-custom-email-authentication-backend)
  - [Update Translations](#update-translations)

- [Getting Help](#getting-help)
- [License](#license)
- [Contributing](#contributing)
- [Reporting Security Issues](#reporting-security-issues)

## Purpose

This repository contains a sample Alexa skill that allows users to connect to
Open edX. With this skill, users can access course information, check grades,
and perform other Open edX-related tasks using voice commands with their
Alexa-enabled devices.

## The Sample Skill

### Description

The sample skill included in this repository is a basic demonstration of how to
integrate Alexa with Open edX. It showcases how to handle user requests,
authenticate with Open edX, and retrieve course data. Developers can use this
as a starting point to build more advanced interactions for Open edX.

### Features

The sample skill includes the following features:

- **Voice profile support**: The skill can identify users by their voice and
  retrieve their course information. If the user is not recognized, the skill
  will return a message indicating that the user is not recognized and the
  interaction will finish.
- **Internationalization support**: The skill is available in English and
  Spanish. Developers can add support for other languages by adding the
  appropriate translations.
- **Custom Email Authentication**: The skill uses a custom authentication
  mechanism to authenticate users with Open edX. By default, the skill uses the
  email address of the Alexa account to authenticate with Open edX. The developers
  can create a custom authentication mechanism to authenticate users with Open edX.

### Usage

To use this Alexa skill, you can use the Alexa simulator in the Amazon
Developer Console or an Alexa-enabled device. The skill is available in English
and Spanish. The current version of the skill supports the following
interactions:

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

## Creating the Skill

### Prerequisites

Before setting up and running this sample skill, ensure you have the following
prerequisites:

1. An [Amazon Developer account](https://developer.amazon.com/) for creating
   and configuring the skill.
2. Installed [Node.js and npm](https://nodejs.org/en), [Python 3.8](https://www.python.org/downloads/),
   and [git](https://git-scm.com/).
3. Access to an Open edX platform with admin privileges.
4. ASK CLI installed and configured in your computer. Follow the steps in the
   [ASK CLI documentation](./docs/1-ask-cli.md)
5. `eox-core` installed and configured in your Open edX platform. Follow the
   steps in the [eox-core documentation](./docs/2-eox-core.md)

### Development

We created a `Makefile` to help you to prepare and initialize your environment
for Alexa's skill development. Before using the commands, ensure that you have
the following requirements:

- Python 3.8, we recommend to use a virtual environment to avoid conflicts with
  other python projects.
- ASK CLI, follow the steps in the [ASK CLI documentation](./docs/1-ask-cli.md)

After to ensure that you have the requirements, you only need to execute the
following command:

```bash
make bootstrap
```

This command allows you initialize and configure the development environment.
Under the hood, the command executes the following commands:

- `make configure`: Configure the ASK CLI with your Amazon Developer account.
- `make setup`: Create a new skill based in the sample skill. This command
  creates a new skill based in the our sample-skill in the Alexa Developer
  Console, and a new git repository in the `skills/` folder.

### Deployment

As the skill is [alexa-hosted](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/build-a-skill-end-to-end-using-an-alexa-hosted-skill.html),
you can deploy the skill using only git commands. So, deployment is very straightforward!. Follow the steps below:

1. Go to the created skill in the `skills/<skill-name>/` folder, where
   `<skill-name>` is the name of your skill. e.g: `skills/openedx-skill/`.
2. Make your changes.
3. Commit your changes.
4. Push your changes to the repository. Ensure that you push to the `master` branch.

After to push your changes, the skill will be deployed automatically, only you
need to wait a few minutes to see the changes in the skill in the Alexa
Developer Console.

## Configuring the Skill

### Adding Environment Variables

This skill requires some environment variables to work properly. Follow the
steps below to configure the environment variables:

1. Go to the created skill in the `skills/<skill-name>/` folder, where
   `<skill-name>` is the name of your skill. e.g: `skills/openedx-skill/`.
2. Create a `.env` file in the `lambda/alexa/` folder. e.g: `skills/openedx-skill/lambda/alexa/.env`.
3. Add the following environment variables to the `.env` file:

   ```bash
    SKILL_PROFILE_EMAIL_BACKEND=<your-email-backend> # e.g: auth.backends.custom.CustomEmailBackend
    LMS_DOMAIN=<your-lms-domain> # e.g: https://lms.example.com
    EOX_CORE_CLIENT_ID=<your-eox-core-client-id>
    EOX_CORE_CLIENT_SECRET=<your-eox-core-client-secret>
    EOX_CORE_GRANT_TYPE=client_credentials
    REQUEST_MAX_TIMEOUT=<your-request-max-timeout> # e.g: 5
   ```

   **NOTE**: The `EOX_CORE_CLIENT_ID`, `EOX_CORE_CLIENT_SECRET`, and
   `EOX_CORE_GRANT_TYPE` environment variables are provided by the [`eox-core`
   configuration](./docs/2-eox-core.md) explained in the prerequisites section.

4. Save the changes.
5. Commit and push the changes to the repository.

### Configuring Permissions

This skill requires some permissions in the Alexa account to work properly.
Follow the steps below to configure the permissions:

1. Open the Alexa app (Android or iOS). **IMPORTANT**: The account must be the
   same account that you use to create the skill in the Alexa Developer
   Console.
2. Go to "More" → "Skills & Games" → "Your Skills".
3. Select the skill you want to configure. e.g: "Open edX Assistant".
4. Select "Settings".
5. Select "Manage account permissions".
6. Enable "Email Address" permission.
7. Save the changes.

Additionally, if you want to use the skill you need to enable the "Voice
Profile" permission. Follow the steps below to enable (if you don't have
enabled) the "Voice Profile" permission:

1. Open the Alexa app (Android or iOS). **IMPORTANT**: The account must be the
   same account that you use to create the skill in the Alexa Developer
   Console.
2. Go to "More" → "Settings" → "Your Profile & Family".
3. Select your profile.
4. Select "Voice ID".
5. If you don't have set up your Voice ID, perform the setup.
6. Go to "Voice ID settings".
7. Enable "Personalize Skills" permission.

### Enabling Spanish Support

By default, the skill only recognizes in English. If you want to activate
Spanish, you need to follow the steps below:

1. Go to the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Select the skill you want to configure.
3. Select the "Build" tab.
4. Select "Language Settings".
5. Select "+ Add New Language".
6. Select "Spanish (ES)".
7. Select "Save Changes".

## Testing the Skill

### Testing in Amazon Developer Console

To test the sample Alexa skill, follow these steps:

1. Go to the [Amazon Developer Console](https://developer.amazon.com/alexa/console/ask).
2. Select the Skill you want to test.
3. Select the "Test" tab.
4. Select "Development" from the "Skill testing is enabled in:" dropdown.
5. As the Skill uses voice profiles, to test interactions you need to do it by
   voice. If you are known profile, you can interact with the skill without
   any issues. If you are not a known profile, the skill show you a message
   indicating that you are not a known profile and the interaction will finish.

Also, you can test the skill using the Alexa app, be sure you are using the
same account you use to create the skill in the Alexa Developer.

## Working with the Skill

### Create a Custom Email Authentication Backend

You can create a custom email authentication backend to authenticate users with
Open edX. To create a custom email authentication backend, follow the steps:

1. Create a new file in the `auth` directory with the name of the backend, e.g. `custom.py`
2. Create a class that inherits from `BaseEmailAuthenticationBackend`, e.g.
   `CustomEmailAuthentication(BaseEmailAuthenticationBackend)`
3. Implement the `get_email` method to retrieve the email of the user
   associated with the Open edX account. This method should return the email as
   a `str` or `None` (if the email can't be obtained). The method should NOT
   raise any exceptions.
4. Create optionally `EMAIL_ERROR_MESSAGE` attribute to the class to customize
   the error. If not, the default error message will be used.
5. Add to the `.env` file the following environment variable:

   ```bash
    SKILL_PROFILE_EMAIL_BACKEND=<path-to-the-backend> # e.g: auth.backends.custom.CustomEmailAuthentication
   ```

   If not added, it will take the default `AlexaEmailAuthentication` class

### Update Translations

The skill is available in English and Spanish. If you want to update the
translations, you can use our `make` commands to help you. Follow the steps:

1. Go to the created skill in the `skills/<skill-name>/` folder, where
   `<skill-name>` is the name of your skill. e.g: `skills/openedx-skill/`.
2. In the `lambda/` folder, there is an Makefile with the following commands:

   - `extract-translations`: Extract the text marked for translation in
     the `lambda/` folder. This update the `.po` files. (After you execute this
     command, you need to update the translations in the `.po` files)
   - `compile-translations`: Compile the translations in the `lambda/`
     folder. This update the `.mo` files.

## Getting Help

If you encounter any issues or have questions about using this Alexa skill,
feel free to create an issue in this repository. Our community and maintainers
will be happy to assist you.

## License

The code in this repository is licensed under the AGPL-3.0 unless otherwise
noted.

Please see [LICENSE.txt](./LICENSE.txt) for details.

## Contributing

Contributions are very welcome.

This project is currently accepting all types of contributions, bug fixes,
security fixes, maintenance work, or new features. However, please make sure to
have a discussion about your new feature idea with the maintainers prior to
beginning development to maximize the chances of your change being accepted.
You can start a conversation by creating a new issue on this repo summarizing
your idea.

## Reporting Security Issues

Please do not report a potential security issue in public. Please email <security@edunext.co>.
