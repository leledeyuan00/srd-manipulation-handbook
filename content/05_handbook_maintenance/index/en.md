# Handbook maintenance

Learn how to contribute to this handbook and prepare it for transfer to an authorized lab administrator.

## Edit a page

Open the page editor, load the latest Git revision, edit in one language, review the Markdown and commit. Use translation correction only for wording changes that do not alter the source meaning. Report translation problems through the issue tracker without including restricted information.

## Review before publishing

Confirm permission to publish and use the translation provider. Check technical instructions, numbers, units, error messages, warnings and all translated versions. Do not regard drafts as verified operating procedures.

## Transfer ownership

The source repository contains Markdown and the build scripts. The maintainer can build static output locally and serve it with an authorized web server. The online editor and CI configuration must be adapted to the internal Git service. Rotate credentials and test access restrictions before adding internal material.

> **TODO:** Complete a real deployment and migration rehearsal; document the actual lab service after approval.
