# Zero-cost AI Comedy Shorts Automation (Android-managed)

This starter project creates stylized, original text-and-cartoon comedy Shorts with Python/Pillow, system TTS (`espeak-ng`) and FFmpeg, then schedules them through the YouTube Data API.

**Important reality check:** This is not an unlimited AI-video generator. It uses a small original story library and procedural graphics. Add original story templates regularly. Free GitHub Actions minutes, API access, and Google's free tiers can change. Scheduled Actions can be delayed; this is not a guaranteed publishing SLA.

## What it does

- Runs twice daily at 12:30 and 19:30 India time (07:00 and 14:00 UTC).
- Generates a vertical 720x1280 MP4 with original cartoon graphics and synthesized English narration.
- Uploads privately and sets `publishAt` about 15 minutes ahead.
- Uses GitHub Actions, Python, FFmpeg, espeak-ng and YouTube Data API.

## Android-only setup

Use Chrome on Android with **Desktop site** enabled for GitHub and Google Cloud Console. You do not need to install Python on your phone.

### 1. Create a GitHub repository

1. Sign in at https://github.com
2. Create a new repository named `ai-comedy-shorts`.
3. Set it to **Private** initially.
4. Upload all files from this project ZIP, preserving the folder structure. GitHub's web interface supports uploading files; create `.github/workflows/` folders first if needed.
5. In the repository, open **Actions** and enable workflows.

GitHub scheduled workflows run from the default branch. Scheduled runs can be delayed, and public repositories with no activity for 60 days can have scheduled workflows disabled. Check current GitHub limits for your account and repository visibility.

### 2. Enable YouTube Data API

1. Open https://console.cloud.google.com/
2. Create a Google Cloud project.
3. Enable **YouTube Data API v3**.
4. Configure the OAuth consent screen. Add your Google account as a test user if the app is in Testing.
5. Create an OAuth Client ID. For a manual refresh-token flow, use an OAuth client type supported by Google's OAuth Playground flow; do not publish the client secret.
6. Open https://developers.google.com/oauthplayground/
7. Open settings (gear icon), enable **Use your own OAuth credentials**, and enter your OAuth Client ID and Client Secret.
8. In Step 1, enter this scope:
   `https://www.googleapis.com/auth/youtube.upload`
9. Authorize with the Google account that owns the channel.
10. Exchange the authorization code in Step 2 and copy the **refresh_token**.

Google may require consent-screen verification or additional project checks depending on the account and publishing use. If uploads are blocked or restricted to private, stop and resolve the API project restriction before relying on automation. Never try to bypass YouTube review or verification.

### 3. Add GitHub secrets

Repository → Settings → Secrets and variables → Actions → New repository secret.

Add exactly these three secrets:

- `YT_CLIENT_ID` — OAuth client ID
- `YT_CLIENT_SECRET` — OAuth client secret
- `YT_REFRESH_TOKEN` — refresh token from OAuth Playground

Never put these values in source code, README, screenshots, or commits. If exposed, revoke the OAuth grant and create new credentials.

### 4. Test safely

1. In `upload_short.py`, temporarily change `"privacyStatus": "private"` and remove `publishAt` to test a private upload, or leave the default scheduled-private configuration.
2. Open Actions → Create and schedule comedy Shorts → Run workflow.
3. Check the job logs.
4. Check YouTube Studio → Content → Scheduled.
5. Verify the video, narration, title and scheduled time manually before relying on the twice-daily schedule.

After a successful test, keep `privacyStatus` as `private` with a future `publishAt`; YouTube will publish it at that time if the API accepts the schedule. Do not set public immediately during early testing.

## Editing content

Edit `STORIES` in `generate_short.py`. Add original scripts, not copied movie scenes, memes, celebrity voices or other creators' clips. Each entry needs a unique title, four scene tuples `(speaker, dialogue, emoji)`, and an original description.

The current renderer uses simple cartoon graphics and system TTS. It does not create realistic AI people, lip-sync or cinematic animation. Emoji display depends on runner fonts; the character face itself is drawn with vector-like shapes.

## Important production notes

- The project currently has only five story templates. A random choice can repeat. Expand the library and add a persistent story-history file before enabling unattended daily publication.
- The workflow uses English narration and captions.
- It does not yet inspect analytics or generate ideas from current trends.
- It does not automatically determine whether a video is eligible for monetization.
- Review YouTube's altered/synthetic-content disclosure rules and mark content accurately when required.
- YouTube monetization requires original, valuable content. High-volume template repetition can be rejected as repetitive or inauthentic content.
- Scheduled publishing requires a valid future `publishAt` time and a successful upload. Upload/API restrictions may apply to your Cloud project.
- Keep backups of OAuth credentials securely. Do not share refresh tokens with anyone.

## Useful official documentation

- YouTube upload API: https://developers.google.com/youtube/v3/docs/videos/insert
- YouTube video resource / publishAt: https://developers.google.com/youtube/v3/docs/videos
- YouTube API quota: https://developers.google.com/youtube/v3/getting-started
- GitHub scheduled workflows: https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows#schedule
- Google OAuth Playground: https://developers.google.com/oauthplayground/
