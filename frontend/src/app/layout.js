import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { Web3Provider } from "../context/Web3Context";
import Navbar from "../components/Navbar";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: "TrustResQ | Verifiable Disaster Reporting",
  description: "Blockchain-verified, AI-summarized disaster intelligence.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased bg-zinc-50 dark:bg-black text-zinc-900 dark:text-zinc-50`}
      >
        <Web3Provider>
          <Navbar />
          <div className="pt-6">
            {children}
          </div>
        </Web3Provider>
      </body>
    </html>
  );
}
