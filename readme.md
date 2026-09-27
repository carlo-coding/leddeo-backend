# Leddeo · backend

> **Archived (2023).** Leddeo was a SaaS I built and ran in early 2023. The code stays here as a record; it is no longer maintained.

Leddeo turned a video into editable subtitles in any language, then burned them back into the video. This repository is the Django REST API behind it; the user app is [leddeo-frontend](https://github.com/carlo-coding/leddeo-frontend) and the admin panel is [leddeo-admin](https://github.com/carlo-coding/leddeo-admin).

## What it does

1. **Transcription with a local speech model.** The uploaded video's audio is extracted with moviepy and transcribed with [OpenAI Whisper](https://github.com/openai/whisper) running on the server (the `small` model), returning timed segments. No third-party transcription API.
2. **Offline machine translation.** Segments are translated with [Argos Translate](https://github.com/argosopentech/argos-translate). When there is no direct model for a language pair, the text goes through an intermediate language (two hops), and the needed language packages are downloaded on demand.
3. **Subtitle burn-in.** The edited subtitles are rendered onto the video with moviepy, ffmpeg and ImageMagick, with a choice of about 40 Google Fonts, colour, background and position. The video is compressed first (H.264, CRF 23) and the font size scales with the video resolution.
4. **Wait-time estimates from logged jobs.** Every transcription, translation and render is logged with its input size and how long it took. Simple linear models on those logs (`duration/functions/preditions.py`) estimate the wait before a job starts, and the front end shows it as a countdown.
5. **The product around it.** JWT and Google sign-in, email verification, Stripe checkout, customer portal and subscription webhooks, user history, FAQs and versioned terms acceptance.

## Stack

Python · Django 4 · Django REST Framework · Whisper · Argos Translate · moviepy · ffmpeg · ImageMagick · OpenCV · Stripe · PostgreSQL · Docker · Nginx

## Looking back

- Transcription and rendering run synchronously inside the HTTP request. A job queue with a worker would be the first thing to change.
- The wait-time models are refitted by hand and their coefficients are pasted into the code; the fitting step is not in this repository.

## Deployment, as it ran in 2023

A single Ubuntu server: the API in Docker (`Dockerfile`, `deploy.sh`, `run.sh`) behind Nginx with Certbot for TLS. `run.sh` installs the fonts into ImageMagick, runs the migrations and starts the server. Configuration comes from environment variables (see `.env.example`).
