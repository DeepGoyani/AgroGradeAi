import { motion } from "framer-motion";
import { Star, Quote } from "lucide-react";

const testimonials = [
  {
    name: "Ramesh Patel",
    role: "Cotton Farmer, Gujarat",
    content: "AgroGrade saved my entire cotton crop this season. The disease scanner detected early blight before I could see symptoms. The organic remedy worked within days!",
    rating: 5,
    avatar: "RP",
  },
  {
    name: "Sunita Sharma",
    role: "Vegetable Grower, Maharashtra",
    content: "My earnings increased by 45% after getting Trust Tags. Buyers now pay premium prices because they can verify my produce quality. No more haggling with middlemen.",
    rating: 5,
    avatar: "SS",
  },
  {
    name: "Vikram Singh",
    role: "Wholesale Buyer, Delhi",
    content: "As a buyer, Trust Tags give me confidence to purchase remotely. I know exactly what grade I'm getting. The sensor data showing soil health is a game-changer.",
    rating: 5,
    avatar: "VS",
  },
];

const TestimonialsSection = () => {
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
            Success Stories
          </span>
          <h2 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold mt-4 mb-6">
            Trusted By Farmers & Buyers
          </h2>
          <p className="text-muted-foreground text-lg">
            Real stories from the farming community using AgroGrade 
            to transform their agricultural business.
          </p>
        </motion.div>

        {/* Testimonials Grid */}
        <div className="grid md:grid-cols-3 gap-8">
          {testimonials.map((testimonial, i) => (
            <motion.div
              key={testimonial.name}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: i * 0.15 }}
              className="glass-card p-8 rounded-2xl relative"
            >
              {/* Quote Icon */}
              <div className="absolute top-6 right-6 w-10 h-10 rounded-full bg-accent/10 flex items-center justify-center">
                <Quote className="w-5 h-5 text-accent" />
              </div>

              {/* Rating */}
              <div className="flex gap-1 mb-4">
                {[...Array(testimonial.rating)].map((_, j) => (
                  <Star key={j} className="w-5 h-5 fill-warning text-warning" />
                ))}
              </div>

              {/* Content */}
              <p className="text-foreground leading-relaxed mb-6">
                "{testimonial.content}"
              </p>

              {/* Author */}
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-accent to-primary flex items-center justify-center text-primary-foreground font-semibold">
                  {testimonial.avatar}
                </div>
                <div>
                  <div className="font-semibold">{testimonial.name}</div>
                  <div className="text-sm text-muted-foreground">{testimonial.role}</div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TestimonialsSection;
