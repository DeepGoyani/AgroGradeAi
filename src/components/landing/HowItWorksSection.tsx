import { motion } from "framer-motion";
import { Camera, Cpu, Award, ShoppingCart, ArrowRight } from "lucide-react";

const steps = [
  {
    icon: Camera,
    title: "Capture",
    description: "Take a photo of your crop leaf or harvest pile using the app",
    color: "accent",
  },
  {
    icon: Cpu,
    title: "AI Analysis",
    description: "Our CNN models analyze for disease or grade quality in seconds",
    color: "primary",
  },
  {
    icon: Award,
    title: "Get Certified",
    description: "Receive Trust Tag with verified grade and sensor data fusion",
    color: "success",
  },
  {
    icon: ShoppingCart,
    title: "Sell Direct",
    description: "List on marketplace with verified badge, connect with buyers",
    color: "warning",
  },
];

const HowItWorksSection = () => {
  return (
    <section className="py-24 bg-card/50 relative overflow-hidden">
      {/* Background Pattern */}
      <div className="absolute inset-0 pattern-grid opacity-50" />

      <div className="container mx-auto px-4 relative z-10">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <span className="text-accent text-sm font-semibold tracking-wider uppercase">
            Simple Process
          </span>
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold mt-4 mb-6">
            How AgroGrade Works
          </h2>
          <p className="text-muted-foreground text-lg">
            Four simple steps from crop scanning to market success. 
            AI does the heavy lifting so you can focus on farming.
          </p>
        </motion.div>

        {/* Steps */}
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {steps.map((step, i) => (
            <motion.div
              key={step.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.15 }}
              className="relative"
            >
              {/* Connector Line */}
              {i < steps.length - 1 && (
                <div className="hidden lg:block absolute top-12 left-1/2 w-full h-0.5 bg-gradient-to-r from-border to-transparent" />
              )}

              <div className="text-center relative z-10">
                {/* Step Number */}
                <div className="absolute -top-3 left-1/2 -translate-x-1/2 w-8 h-8 rounded-full bg-secondary border-2 border-accent flex items-center justify-center text-sm font-bold text-accent">
                  {i + 1}
                </div>

                {/* Icon */}
                <div className={`w-24 h-24 mx-auto rounded-2xl bg-${step.color}/10 border border-${step.color}/30 flex items-center justify-center mb-6`}>
                  <step.icon className={`w-10 h-10 text-${step.color}`} />
                </div>

                {/* Content */}
                <h3 className="font-display text-xl font-semibold mb-3">
                  {step.title}
                </h3>
                <p className="text-muted-foreground text-sm">
                  {step.description}
                </p>
              </div>
            </motion.div>
          ))}
        </div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center mt-16"
        >
          <a
            href="/scanner"
            className="inline-flex items-center gap-2 px-8 py-4 rounded-xl bg-accent text-accent-foreground font-semibold hover:bg-accent/90 transition-colors group"
          >
            Start Scanning Now
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
          </a>
        </motion.div>
      </div>
    </section>
  );
};

export default HowItWorksSection;
