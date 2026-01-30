import { useState } from "react";
import { motion } from "framer-motion";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { Button } from "@/components/ui/button";
import {
  Search,
  Filter,
  MapPin,
  Star,
  Shield,
  Award,
  Phone,
  MessageCircle,
  Heart,
  ShoppingCart,
  ChevronDown,
  Check,
  Package,
} from "lucide-react";
import freshProduce from "@/assets/fresh-produce.jpg";

// Mock marketplace listings
const listings = [
  {
    id: 1,
    title: "Premium Tomatoes",
    farmer: "Ramesh Patel",
    location: "Ahmedabad, Gujarat",
    price: 45,
    unit: "kg",
    quantity: "500 kg available",
    grade: "A",
    trustScore: 94,
    image: freshProduce,
    verified: true,
    rating: 4.8,
    reviews: 128,
  },
  {
    id: 2,
    title: "Organic Cotton",
    farmer: "Sunita Sharma",
    location: "Rajkot, Gujarat",
    price: 120,
    unit: "kg",
    quantity: "2000 kg available",
    grade: "A",
    trustScore: 96,
    image: freshProduce,
    verified: true,
    rating: 4.9,
    reviews: 256,
  },
  {
    id: 3,
    title: "Fresh Eggplants",
    farmer: "Vikram Singh",
    location: "Surat, Gujarat",
    price: 35,
    unit: "kg",
    quantity: "300 kg available",
    grade: "B",
    trustScore: 82,
    image: freshProduce,
    verified: true,
    rating: 4.5,
    reviews: 67,
  },
  {
    id: 4,
    title: "Green Chillies",
    farmer: "Anita Devi",
    location: "Vadodara, Gujarat",
    price: 60,
    unit: "kg",
    quantity: "150 kg available",
    grade: "A",
    trustScore: 91,
    image: freshProduce,
    verified: true,
    rating: 4.7,
    reviews: 89,
  },
  {
    id: 5,
    title: "Red Onions",
    farmer: "Mahesh Kumar",
    location: "Bhavnagar, Gujarat",
    price: 28,
    unit: "kg",
    quantity: "1000 kg available",
    grade: "B",
    trustScore: 78,
    image: freshProduce,
    verified: false,
    rating: 4.3,
    reviews: 45,
  },
  {
    id: 6,
    title: "Fresh Cabbage",
    farmer: "Priya Patel",
    location: "Gandhinagar, Gujarat",
    price: 25,
    unit: "kg",
    quantity: "400 kg available",
    grade: "A",
    trustScore: 89,
    image: freshProduce,
    verified: true,
    rating: 4.6,
    reviews: 112,
  },
];

const categories = ["All", "Vegetables", "Fruits", "Grains", "Cotton", "Spices"];

const Marketplace = () => {
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [favorites, setFavorites] = useState<number[]>([]);

  const toggleFavorite = (id: number) => {
    setFavorites((prev) =>
      prev.includes(id) ? prev.filter((f) => f !== id) : [...prev, id]
    );
  };

  const getGradeClass = (grade: string) => {
    switch (grade) {
      case "A":
        return "grade-a";
      case "B":
        return "grade-b";
      case "C":
        return "grade-c";
      default:
        return "";
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4">
          {/* Page Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="text-center max-w-3xl mx-auto mb-12"
          >
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-success/10 border border-success/30 mb-4">
              <ShoppingCart className="w-4 h-4 text-success" />
              <span className="text-success text-sm font-medium">Direct Farm-to-Buyer</span>
            </div>
            <h1 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
              Marketplace
            </h1>
            <p className="text-muted-foreground text-lg">
              Browse AI-verified Grade A produce directly from farmers. Trust Tags ensure quality.
            </p>
          </motion.div>

          {/* Search and Filters */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="glass-card p-4 rounded-2xl mb-8"
          >
            <div className="flex flex-col md:flex-row gap-4">
              {/* Search */}
              <div className="flex-1 relative">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
                <input
                  type="text"
                  placeholder="Search for produce, farmers, or locations..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-12 pr-4 py-3 rounded-xl bg-secondary border border-border focus:border-accent focus:outline-none transition-colors"
                />
              </div>

              {/* Category Filter */}
              <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0">
                {categories.map((category) => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition-all ${
                      selectedCategory === category
                        ? "bg-accent text-accent-foreground"
                        : "bg-secondary hover:bg-secondary/80 text-muted-foreground"
                    }`}
                  >
                    {category}
                  </button>
                ))}
              </div>

              {/* Filter Button */}
              <Button variant="outline" className="shrink-0">
                <Filter className="w-4 h-4" />
                Filters
                <ChevronDown className="w-4 h-4" />
              </Button>
            </div>
          </motion.div>

          {/* Listings Grid */}
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {listings.map((listing, i) => (
              <motion.div
                key={listing.id}
                initial={{ opacity: 0, y: 30 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
                className="glass-card rounded-2xl overflow-hidden group"
              >
                {/* Image */}
                <div className="relative aspect-[4/3]">
                  <img
                    src={listing.image}
                    alt={listing.title}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-background/80 via-transparent to-transparent" />
                  
                  {/* Grade Badge */}
                  <div className={`absolute top-4 left-4 w-12 h-12 rounded-xl ${getGradeClass(listing.grade)} flex items-center justify-center shadow-lg`}>
                    <span className="text-xl font-bold">{listing.grade}</span>
                  </div>

                  {/* Favorite Button */}
                  <button
                    onClick={() => toggleFavorite(listing.id)}
                    className="absolute top-4 right-4 w-10 h-10 rounded-full bg-background/80 backdrop-blur-sm flex items-center justify-center hover:bg-background transition-colors"
                  >
                    <Heart
                      className={`w-5 h-5 ${
                        favorites.includes(listing.id)
                          ? "fill-destructive text-destructive"
                          : "text-muted-foreground"
                      }`}
                    />
                  </button>

                  {/* Verified Badge */}
                  {listing.verified && (
                    <div className="absolute bottom-4 left-4 flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-accent/90 backdrop-blur-sm text-accent-foreground text-sm font-medium">
                      <Shield className="w-4 h-4" />
                      Verified
                    </div>
                  )}
                </div>

                {/* Content */}
                <div className="p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="font-display text-xl font-semibold">{listing.title}</h3>
                      <p className="text-sm text-muted-foreground">{listing.farmer}</p>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold text-accent">₹{listing.price}</div>
                      <div className="text-xs text-muted-foreground">per {listing.unit}</div>
                    </div>
                  </div>

                  <div className="flex items-center gap-4 mb-4 text-sm text-muted-foreground">
                    <span className="flex items-center gap-1">
                      <MapPin className="w-4 h-4" />
                      {listing.location}
                    </span>
                    <span className="flex items-center gap-1">
                      <Star className="w-4 h-4 fill-warning text-warning" />
                      {listing.rating} ({listing.reviews})
                    </span>
                  </div>

                  {/* Trust Score */}
                  <div className="flex items-center justify-between p-3 rounded-lg bg-secondary/50 mb-4">
                    <div className="flex items-center gap-2">
                      <Award className="w-4 h-4 text-success" />
                      <span className="text-sm">Trust Score</span>
                    </div>
                    <div className="flex items-center gap-2">
                      <div className="w-20 h-2 bg-secondary rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-accent to-success rounded-full"
                          style={{ width: `${listing.trustScore}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold">{listing.trustScore}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 text-sm text-muted-foreground mb-4">
                    <Package className="w-4 h-4" />
                    {listing.quantity}
                  </div>

                  {/* Actions */}
                  <div className="flex gap-2">
                    <Button variant="trust" className="flex-1">
                      <ShoppingCart className="w-4 h-4" />
                      Buy Now
                    </Button>
                    <Button variant="outline" size="icon">
                      <Phone className="w-4 h-4" />
                    </Button>
                    <Button variant="outline" size="icon">
                      <MessageCircle className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Load More */}
          <div className="text-center mt-12">
            <Button variant="outline" size="lg">
              Load More Listings
              <ChevronDown className="w-4 h-4" />
            </Button>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Marketplace;
