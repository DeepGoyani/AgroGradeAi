import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { ArrowRight, Scan, Award, TrendingUp, Play } from "lucide-react";
import { Link } from "react-router-dom";
import heroImage from "@/assets/hero-farm.jpg";

const stats = [
  { value: "50K+", label: "Farmers Empowered" },
  { value: "2M+", label: "Crops Analyzed" },
  { value: "₹500Cr", label: "Farmer Earnings" },
  { value: "98%", label: "Accuracy Rate" },
];

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center pt-20 overflow-hidden">
      {/* Background Image with Overlay */}
      <div className="absolute inset-0 z-0">
        <img
          src={heroImage}
          alt="Indian farm field"
          className="w-full h-full object-cover opacity-30"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-background via-background/90 to-background" />
        <div className="absolute inset-0 pattern-dots" />
      </div>

      {/* Animated Floating Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            className="absolute w-4 h-4 rounded-full bg-accent/20"
            initial={{ x: Math.random() * 100 + "%", y: "100%" }}
            animate={{
              y: "-20%",
              x: `${Math.random() * 100}%`,
            }}
            transition={{
              duration: 15 + Math.random() * 10,
              repeat: Infinity,
              ease: "linear",
              delay: i * 2,
            }}
          />
        ))}
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Left Content */}
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 border border-accent/30">
              <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
              <span className="text-accent text-sm font-medium">
                AI-Powered Agricultural Revolution
              </span>
            </div>

            <h1 className="font-display text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold leading-tight">
              From{" "}
              <span className="text-accent">Crop Health</span>
              <br />
              To{" "}
              <span className="text-warning">Market Wealth</span>
            </h1>

            <p className="text-lg md:text-xl text-muted-foreground leading-relaxed max-w-xl">
              Empowering Indian farmers with instant AI disease diagnosis, certified quality grading, 
              and direct market access. Bypass middlemen. Secure fair value.
            </p>

            <div className="flex flex-wrap gap-4">
              <Link to="/scanner">
                <Button variant="hero" size="xl" className="group">
                  <Scan className="w-5 h-5" />
                  Scan Your Crop
                  <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                </Button>
              </Link>
              <Button variant="heroOutline" size="xl" className="group">
                <Play className="w-5 h-5" />
                Watch Demo
              </Button>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 pt-8 border-t border-border/50">
              {stats.map((stat, i) => (
                <motion.div
                  key={stat.label}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 + i * 0.1 }}
                  className="text-center md:text-left"
                >
                  <div className="font-display text-2xl md:text-3xl font-bold text-accent">
                    {stat.value}
                  </div>
                  <div className="text-sm text-muted-foreground">{stat.label}</div>
                </motion.div>
              ))}
            </div>
          </motion.div>

          {/* Right Content - Feature Cards */}
          <motion.div
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="relative hidden lg:block"
          >
            <div className="relative">
              {/* Main Feature Card */}
              <motion.div
                className="glass-card p-6 rounded-2xl"
                whileHover={{ scale: 1.02 }}
                transition={{ type: "spring", stiffness: 300 }}
              >
                <div className="flex items-center gap-4 mb-4">
                  <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center">
                    <Scan className="w-6 h-6 text-accent" />
                  </div>
                  <div>
                    <h3 className="font-display text-lg font-semibold">Disease Detection</h3>
                    <p className="text-sm text-muted-foreground">AI-powered diagnosis in seconds</p>
                  </div>
                </div>
                <div className="aspect-video rounded-xl bg-secondary/50 flex items-center justify-center overflow-hidden">
                  <img
                    src={heroImage}
                    alt="Crop scanning"
                    className="w-full h-full object-cover opacity-60"
                  />
                  <div className="absolute inset-0 flex items-center justify-center">
                    <div className="w-32 h-32 border-4 border-accent/50 rounded-xl animate-pulse" />
                  </div>
                </div>
              </motion.div>

              {/* Floating Cards */}
              <motion.div
                className="absolute -right-8 top-1/4 glass-card p-4 rounded-xl"
                animate={{ y: [0, -10, 0] }}
                transition={{ duration: 4, repeat: Infinity }}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-success/20 flex items-center justify-center">
                    <Award className="w-5 h-5 text-success" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold">Grade A</div>
                    <div className="text-xs text-muted-foreground">Trust Score: 95</div>
                  </div>
                </div>
              </motion.div>

              <motion.div
                className="absolute -left-8 bottom-1/4 glass-card p-4 rounded-xl"
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 5, repeat: Infinity }}
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-lg bg-warning/20 flex items-center justify-center">
                    <TrendingUp className="w-5 h-5 text-warning" />
                  </div>
                  <div>
                    <div className="text-sm font-semibold">+40% Earnings</div>
                    <div className="text-xs text-muted-foreground">Direct Market Access</div>
                  </div>
                </div>
              </motion.div>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
