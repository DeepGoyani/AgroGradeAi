import { Link } from "react-router-dom";
import { Leaf, Mail, Phone, MapPin, Facebook, Twitter, Instagram, Linkedin } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-card border-t border-border/50 mt-20">
      <div className="container mx-auto px-4 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-12">
          {/* Brand */}
          <div className="space-y-4">
            <Link to="/" className="flex items-center gap-2">
              <div className="w-10 h-10 rounded-xl bg-accent flex items-center justify-center">
                <Leaf className="w-6 h-6 text-accent-foreground" />
              </div>
              <span className="font-display text-xl font-bold text-foreground">
                Agro<span className="text-accent">Grade</span>
              </span>
            </Link>
            <p className="text-muted-foreground text-sm leading-relaxed">
              Empowering Indian farmers with AI-powered disease diagnosis and quality grading. 
              From Crop Health to Market Wealth.
            </p>
            <div className="flex gap-3">
              {[Facebook, Twitter, Instagram, Linkedin].map((Icon, i) => (
                <a
                  key={i}
                  href="#"
                  className="w-10 h-10 rounded-lg bg-secondary flex items-center justify-center text-muted-foreground hover:text-accent hover:bg-accent/10 transition-colors"
                >
                  <Icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="font-display text-lg font-semibold mb-4">Features</h4>
            <ul className="space-y-3">
              {["Disease Scanner", "Quality Grader", "Trust Tags", "IoT Sensors", "Marketplace"].map((item) => (
                <li key={item}>
                  <a href="#" className="text-muted-foreground hover:text-accent transition-colors text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h4 className="font-display text-lg font-semibold mb-4">Resources</h4>
            <ul className="space-y-3">
              {["Documentation", "API Reference", "Farmer Guide", "Buyer Guide", "Support Center"].map((item) => (
                <li key={item}>
                  <a href="#" className="text-muted-foreground hover:text-accent transition-colors text-sm">
                    {item}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact */}
          <div>
            <h4 className="font-display text-lg font-semibold mb-4">Contact Us</h4>
            <ul className="space-y-3">
              <li className="flex items-center gap-3 text-muted-foreground text-sm">
                <MapPin className="w-4 h-4 text-accent" />
                Gujarat, India
              </li>
              <li className="flex items-center gap-3 text-muted-foreground text-sm">
                <Phone className="w-4 h-4 text-accent" />
                +91 98765 43210
              </li>
              <li className="flex items-center gap-3 text-muted-foreground text-sm">
                <Mail className="w-4 h-4 text-accent" />
                hello@agrograde.in
              </li>
            </ul>
          </div>
        </div>

        <div className="border-t border-border/50 mt-12 pt-8 flex flex-col md:flex-row justify-between items-center gap-4">
          <p className="text-muted-foreground text-sm">
            © 2025 AgroGrade. All rights reserved.
          </p>
          <div className="flex gap-6">
            {["Privacy Policy", "Terms of Service", "Cookie Policy"].map((item) => (
              <a key={item} href="#" className="text-muted-foreground hover:text-accent transition-colors text-sm">
                {item}
              </a>
            ))}
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
