import type { Metadata } from "next";
import { Manrope } from "next/font/google";
import { connection } from "next/server";
import "./globals.css";

const manrope = Manrope({
  variable: "--font-manrope",
  subsets: ["latin"],
  weight: ["400", "500", "700", "800"],
});

export const metadata: Metadata = {
  title: "Zenflow",
  description: "Generate agent skills for your AI assistant.",
};

export default async function RootLayout({ children }: LayoutProps<"/">) {
  // Forces dynamic rendering so proxy.ts's per-request CSP nonce can reach
  // the inline scripts Next injects — see content-security-policy.md.
  await connection();

  return (
    <html lang="en" className={`${manrope.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
