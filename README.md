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

## Reviews and support (new)
`index.html` now has two more pages: **Reviews** (`#p-comments`) with star ratings and replies, and **Support** (`#p-support`)
with quick contact cards and a support-request form. Both are in fa/ar/en and follow the light/dark theme.

Out of the box they run in **demo mode**: everything is saved in the visitor's own browser, so only they can see it.
To share reviews between all visitors, connect a free Firebase Realtime Database (no server code needed):

1. Create a Firebase project, then Build > Realtime Database > Create database.
2. Rules tab: paste the contents of `firebase-rules.json` and publish. Visitors can only add reviews and requests;
   nobody can edit or delete them, and support requests cannot be read by the public.
3. Copy the database URL (like `https://xxxx-default-rtdb.firebaseio.com`) into `COMMUNITY.db` near the end of the script in `index.html`.
4. Push to GitHub. Done.

**Owner access.** Tap "Admin sign in" at the bottom of Reviews or Support and enter the database secret
(Project settings > Service accounts > Database secrets). It is typed only in that dialog and kept in your browser,
never in the code. Signed in, your replies show as "Ario team" with an official badge, you can delete reviews or replies,
and the Support page lists the requests people sent. Keep the secret private.

Contact cards on the Support page appear automatically when you fill in `SOCIAL` (telegram, instagram, email) in `index.html`.
