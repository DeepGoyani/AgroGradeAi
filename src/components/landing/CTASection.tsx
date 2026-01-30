import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Smartphone, Download } from "lucide-react";

const CTASection = () => {
  return (
    <section className="py-24 relative overflow-hidden">
      {/* Background */}
      <div className="absolute inset-0 bg-gradient-to-br from-accent/20 via-background to-primary/20" />
      <div className="absolute inset-0 pattern-dots" />

      <div className="container mx-auto px-4 relative z-10">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="glass-card rounded-3xl p-8 md:p-12 lg:p-16 text-center max-w-4xl mx-auto glow-accent"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 border border-accent/30 mb-6">
            <Smartphone className="w-4 h-4 text-accent" />
            <span className="text-accent text-sm font-medium">
              Available Now
            </span>
          </div>

          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold mb-6">
            Start Your Journey to{" "}
            <span className="text-accent">Agricultural Prosperity</span>
          </h2>

          <p className="text-muted-foreground text-lg max-w-2xl mx-auto mb-8">
            Join 50,000+ farmers already using AgroGrade to diagnose diseases, 
            certify quality, and access direct markets. Available in Gujarati, Hindi, and English.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Button variant="hero" size="xl" className="group">
              <Download className="w-5 h-5" />
              Download App
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Button>
            <Button variant="heroOutline" size="xl">
              Schedule Demo
            </Button>
          </div>

          {/* Trust Badges */}
          <div className="flex flex-wrap justify-center gap-8 mt-12 pt-8 border-t border-border/50">
            {["ISO 27001 Certified", "NABARD Partner", "ICAR Validated", "Made in India"].map((badge) => (
              <div key={badge} className="text-sm text-muted-foreground">
                ✓ {badge}
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default CTASection;
