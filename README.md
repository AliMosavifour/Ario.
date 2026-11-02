# Ario website

Static site for GitHub Pages. No build step.

## Publish
1. Create a repo (for example `ario-site`) and push everything in this folder to the `main` branch.
2. Repo Settings > Pages > Source: "Deploy from a branch", branch `main`, folder `/ (root)`.
3. The site opens at `https://<username>.github.io/ario-site/`.

## Site URL and link previews
`index.html` has `https://USERNAME.github.io/REPO/` in `canonical`, `og:url` and `og:image`.
The workflow replaces it with your real address on the first push (it uses your custom domain if a `CNAME` file exists),
so Telegram and WhatsApp show the preview image from `assets/og.jpg`.

## Live demo
`app/` is the real web build of Ario. It runs inside the phone frame on the site after the visitor taps the demo button.
Replace its contents when you ship a new version of the web assets.

## Release a new APK
Replace `ario.apk`, commit and push. The workflow in `.github/workflows/update-version.yml`
rewrites `version.json` (version, size, date, sha256) and the site shows it automatically.
The version comes from the APK's `versionName`; set it in your app's build.gradle.

## Edit
- Texts (fa/ar/en): the `T` object at the bottom of `index.html` and `privacy.html`.
- Support email on the privacy page: `CONTACT_EMAIL` at the top of the script in `privacy.html`.
