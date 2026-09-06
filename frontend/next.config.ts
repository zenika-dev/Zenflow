import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "standalone",
  // Next's file tracer resolves @swc/helpers dynamically inside require-hook.js,
  // so it misses the esm/* files that end up needed at runtime — force-include
  // the whole package. See node_modules/next/dist/docs/.../output.md.
  outputFileTracingIncludes: {
    "/*": ["./node_modules/@swc/helpers/**/*"],
  },
  // Security headers (including a per-request CSP nonce) are set in proxy.ts —
  // a nonce can't be generated from next.config's static headers().
};

export default nextConfig;
