import "./globals.css";
import { Inter } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";
import { Toaster } from "@/components/ui/toaster";
import { cn } from "@/lib/utils";

const inter = Inter({ subsets: ["latin"] });

export const metadata = {
  title: "SpectraAI - Advanced AI Assistant",
  description: "AI Assistant with Memory, Emotions, and Personality - 2025 Edition",
  keywords: ["AI", "Assistant", "OpenHermes", "Memory", "Emotions", "Personality"],
  authors: [{ name: "Vesryin" }],
  viewport: "width=device-width, initial-scale=1",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <ClerkProvider>
      <html lang="en" suppressHydrationWarning>
        <body className={cn(inter.className, "min-h-screen bg-background antialiased")}>
          <div className="relative flex min-h-screen flex-col">
            <div className="flex-1">{children}</div>
          </div>
          <Toaster />
        </body>
      </html>
    </ClerkProvider>
  );
}
