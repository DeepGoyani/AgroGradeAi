import { motion } from "framer-motion";
import { Scan, Award, Shield, Wifi, TrendingUp, Users, ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";
import healthyLeaf from "@/assets/healthy-leaf.jpg";
import freshProduce from "@/assets/fresh-produce.jpg";

const features = [
  {
    icon: Scan,
    title: "AI Disease Scanner",
    description: "Capture a leaf photo and get instant AI diagnosis with treatment recommendations. Supports 38+ disease types across 15 Indian crops.",
    link: "/scanner",
    color: "accent",
    image: healthyLeaf,
  },
  {
    icon: Award,
    title: "Quality Grading",
    description: "AI-powered quality assessment assigns Grade A/B/C to your harvest. Creates verified Trust Tags for marketplace listings.",
    link: "/grader",
    color: "success",
    image: freshProduce,
  },
  {
    icon: Shield,
    title: "Trust Tags",
    description: "Blockchain-backed verification combining visual grading with IoT sensor data. Build buyer confidence with transparent quality scores.",
    link: "/dashboard",
    color: "warning",
  },
  {
    icon: Wifi,
    title: "IoT Sensors",
    description: "Real-time soil moisture and NPK monitoring. Receive predictive alerts for drought and nutrient deficiencies before they cause damage.",
    link: "/dashboard",
    color: "moisture",
  },
  {
    icon: TrendingUp,
    title: "Direct Market Access",
    description: "List your verified produce directly to wholesalers and retailers. Eliminate middlemen and secure 40% higher earnings.",
    link: "/marketplace",
    color: "accent",
  },
  {
    icon: Users,
    title: "Farmer Community",
    description: "Connect with fellow farmers, share insights, and learn best practices. Access expert agronomist support when needed.",
    link: "/",
    color: "primary",
  },
];

const FeaturesSection = () => {
  return (
    <section className="py-24 relative">
      <div className="container mx-auto px-4">
        {/* Section Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="text-center max-w-3xl mx-auto mb-16"
        >
          <span className="text-accent text-sm font-semibold tracking-wider uppercase">
            Powerful Features
          </span>
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold mt-4 mb-6">
            Everything You Need To Thrive
          </h2>
          <p className="text-muted-foreground text-lg">
            A complete ecosystem bridging crop health monitoring to market wealth creation. 
            AI, IoT, and blockchain working together for farmer prosperity.
          </p>
        </motion.div>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.1 }}
            >
              <Link to={feature.link}>
                <div className="group glass-card p-6 rounded-2xl h-full hover:border-accent/50 transition-all duration-300 hover:shadow-lg">
                  {feature.image && (
                    <div className="aspect-video rounded-xl overflow-hidden mb-4">
                      <img
                        src={feature.image}
                        alt={feature.title}
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                      />
                    </div>
                  )}
                  
                  <div className="flex items-start gap-4">
                    <div className={`w-12 h-12 rounded-xl bg-${feature.color}/20 flex items-center justify-center shrink-0`}>
                      <feature.icon className={`w-6 h-6 text-${feature.color}`} />
                    </div>
                    <div className="flex-1">
                      <h3 className="font-display text-xl font-semibold mb-2 group-hover:text-accent transition-colors">
                        {feature.title}
                      </h3>
                      <p className="text-muted-foreground text-sm leading-relaxed mb-4">
                        {feature.description}
                      </p>
                      <div className="flex items-center text-accent text-sm font-medium group-hover:gap-2 transition-all">
                        Learn more
                        <ChevronRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
                      </div>
                    </div>
                  </div>
                </div>
              </Link>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
