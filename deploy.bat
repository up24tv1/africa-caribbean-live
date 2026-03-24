@echo off
echo === Africa x Caribbean Live — Deploy Script ===
echo.

REM Step 1: Login to Vercel (opens browser)
echo [1/3] Logging into Vercel...
call npx vercel login
if errorlevel 1 (
    echo ERROR: Vercel login failed.
    pause
    exit /b 1
)

REM Step 2: Deploy to Vercel
echo.
echo [2/3] Deploying to Vercel (production)...
call npx vercel --yes --prod
if errorlevel 1 (
    echo ERROR: Deployment failed.
    pause
    exit /b 1
)

echo.
echo [3/3] Done! Your site is live.
echo.
echo NEXT STEPS:
echo   1. Run: python -X utf8 scripts/create_stripe_links.py
echo      (after adding STRIPE_SECRET_KEY to worldcup-x-agent/.env)
echo   2. Update PaySection.tsx with the Stripe links
echo   3. Set NEXT_PUBLIC_DISCORD_INVITE_URL in Vercel env vars
echo   4. Redeploy: npx vercel --prod
echo.
pause
