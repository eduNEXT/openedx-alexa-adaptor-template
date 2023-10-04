# Eox-core

## What is `eox-core`?

Eox-core (A.K.A. Edunext Open extensions) is an openedx plugin, for the
edx-platform that adds multiple API endpoints in order to extend the
functionality of the edx-platform and avoid changing the base code directly.
These API endpoints includes bulk creation of pre-activated users (for example,
skip sending an activation email), enrollments and pre-enrollment operations.

## Why `eox-core`?

We need to extend the functionality of the edx-platform in order to integrate
it with the Alexa skill. This integration requires querying user data, and
their progress in the courses. The edx-platform does not provide an API for
this, so the `eox-core` plugin adds theses API endpoints.

## How to configure `eox-core`?

1. Create a Django OAuth Toolkit application at `<lms_domain>admin/oauth2_provider/application/add/`,
   copy the `client-id` and `client-secret`. Note the following when creating
   the application from the Django admin:

   - The **Client id** and **Client secret** are automatically generated, do
     not modify them.
   - The selected **User** should have administrator permissions.
   - Add to **Redirect uris** the URL of the LMS domain of the platform.
   - Select **Client type** as "Confidential"
   - Select **Authorization grant type** as "Client credentials"
   - Add a custom **Name** to identify the application.
   - Save the application.

   ![add-app](https://github.com/eduNEXT/openedx-alexa-adaptor-template/assets/64033729/b7f28637-d83c-4f46-918b-8ec8f0f0831c)
