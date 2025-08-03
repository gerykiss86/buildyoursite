/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // Enable experimental features if needed
  experimental: {
    // serverActions: true,
  },
  // Environment variables that should be available on the client
  env: {
    NEXT_PUBLIC_APP_NAME: 'BuildYourSite',
  },
}

module.exports = nextConfig