import { Hero } from '@/components/Hero';
import { Features } from '@/components/Features';
import { PricingComparison } from '@/components/PricingComparison';

export default function Home() {
  return (
    <main className="min-h-screen">
      <Hero />
      <Features />
      <PricingComparison />
      <footer className="py-8 px-8 bg-gray-900 text-center text-gray-400">
        <p>© 2026 ClipTheNews. All rights reserved.</p>
      </footer>
    </main>
  );
}
