import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import {
  Search,
  ShoppingCart,
  Star,
  MapPin,
  Heart,
  Phone,
  MessageCircle,
  Shield,
  ChevronDown,
  Leaf,
  Scale,
  Package,
  Wifi,
  BookOpen,
  FileText,
  HelpCircle,
  Mail,
  MapPinned
} from 'lucide-react';
import { Link } from 'react-router-dom';

const Marketplace = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [sortBy, setSortBy] = useState('newest');

  useEffect(() => {
    // No login required - load products directly
    loadProducts();
  }, []);

  const loadProducts = async () => {
    try {
      const response = await fetch('https://agrogradeai-1.onrender.com/api/marketplace/products');
      if (response.ok) {
        const data = await response.json();
        setProducts(data.products || getMockProducts());
      } else {
        setProducts(getMockProducts());
      }
    } catch (error) {
      console.log('Using mock products');
      setProducts(getMockProducts());
    } finally {
      setLoading(false);
    }
  };

  const getMockProducts = () => [
    {
      id: 1,
      name: 'Green Chillies',
      seller: 'Anita Devi',
      category: 'vegetables',
      grade: 'A',
      price: 60,
      unit: 'kg',
      quantity: 150,
      location: 'Vadodara, Gujarat',
      rating: 4.7,
      reviews: 89,
      image: 'https://images.unsplash.com/photo-1583119022894-919a68a3d0e3?w=400&h=300&fit=crop',
      trustScore: 91,
      verified: true
    },
    {
      id: 2,
      name: 'Red Onions',
      seller: 'Mahesh Kumar',
      category: 'vegetables',
      grade: 'B',
      price: 28,
      unit: 'kg',
      quantity: 1000,
      location: 'Bhavnagar, Gujarat',
      rating: 4.3,
      reviews: 45,
      image: 'https://images.unsplash.com/photo-1518977956812-cd3dbadaaf31?w=400&h=300&fit=crop',
      trustScore: 78,
      verified: true
    },
    {
      id: 3,
      name: 'Fresh Cabbage',
      seller: 'Priya Patel',
      category: 'vegetables',
      grade: 'A',
      price: 25,
      unit: 'kg',
      quantity: 400,
      location: 'Gandhinagar, Gujarat',
      rating: 4.6,
      reviews: 112,
      image: 'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?w=400&h=300&fit=crop',
      trustScore: 89,
      verified: true
    },
    {
      id: 4,
      name: 'Organic Tomatoes',
      seller: 'Ramesh Sharma',
      category: 'vegetables',
      grade: 'A',
      price: 45,
      unit: 'kg',
      quantity: 500,
      location: 'Ahmedabad, Gujarat',
      rating: 4.8,
      reviews: 156,
      image: 'https://images.unsplash.com/photo-1546470427-227c7e36b0d8?w=400&h=300&fit=crop',
      trustScore: 94,
      verified: true
    },
    {
      id: 5,
      name: 'Fresh Potatoes',
      seller: 'Sunita Ben',
      category: 'vegetables',
      grade: 'B',
      price: 22,
      unit: 'kg',
      quantity: 2000,
      location: 'Rajkot, Gujarat',
      rating: 4.2,
      reviews: 78,
      image: 'https://images.unsplash.com/photo-1518977676601-b53f82ber601?w=400&h=300&fit=crop',
      trustScore: 72,
      verified: false
    },
    {
      id: 6,
      name: 'Premium Cotton',
      seller: 'Kishan Patel',
      category: 'cotton',
      grade: 'A',
      price: 85,
      unit: 'kg',
      quantity: 300,
      location: 'Surat, Gujarat',
      rating: 4.9,
      reviews: 203,
      image: 'https://images.unsplash.com/photo-1616431101491-554c8c8eb9ab?w=400&h=300&fit=crop',
      trustScore: 96,
      verified: true
    },
    {
      id: 7,
      name: 'Organic Cotton',
      seller: 'Bharat Farmers',
      category: 'cotton',
      grade: 'A',
      price: 92,
      unit: 'kg',
      quantity: 500,
      location: 'Bharuch, Gujarat',
      rating: 4.7,
      reviews: 134,
      image: 'https://images.unsplash.com/photo-1605000797499-95a51c5269ae?w=400&h=300&fit=crop',
      trustScore: 88,
      verified: true
    },
    {
      id: 8,
      name: 'Basmati Rice',
      seller: 'Golden Harvest',
      category: 'grains',
      grade: 'A',
      price: 120,
      unit: 'kg',
      quantity: 1500,
      location: 'Mehsana, Gujarat',
      rating: 4.8,
      reviews: 289,
      image: 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop',
      trustScore: 95,
      verified: true
    },
    {
      id: 9,
      name: 'Fresh Wheat',
      seller: 'Kisan Union',
      category: 'grains',
      grade: 'B',
      price: 35,
      unit: 'kg',
      quantity: 3000,
      location: 'Patan, Gujarat',
      rating: 4.4,
      reviews: 167,
      image: 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=300&fit=crop',
      trustScore: 82,
      verified: true
    },
    {
      id: 10,
      name: 'Fresh Mangoes',
      seller: 'Fruit Valley',
      category: 'fruits',
      grade: 'A',
      price: 150,
      unit: 'kg',
      quantity: 200,
      location: 'Junagadh, Gujarat',
      rating: 4.9,
      reviews: 312,
      image: 'https://images.unsplash.com/photo-1553279768-865429fa0078?w=400&h=300&fit=crop',
      trustScore: 97,
      verified: true
    },
    {
      id: 11,
      name: 'Organic Bananas',
      seller: 'Green Farms',
      category: 'fruits',
      grade: 'A',
      price: 45,
      unit: 'dozen',
      quantity: 500,
      location: 'Navsari, Gujarat',
      rating: 4.6,
      reviews: 198,
      image: 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=300&fit=crop',
      trustScore: 91,
      verified: true
    }
  ];

  const getGradeColor = (grade) => {
    switch (grade) {
      case 'A': return 'bg-accent text-accent-foreground';
      case 'B': return 'bg-yellow-500 text-black';
      case 'C': return 'bg-orange-500 text-white';
      default: return 'bg-muted text-muted-foreground';
    }
  };

  const getTrustScoreColor = (score) => {
    if (score >= 85) return 'bg-accent';
    if (score >= 70) return 'bg-yellow-500';
    return 'bg-orange-500';
  };

  const filteredProducts = products
    .filter(product => {
      const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.seller.toLowerCase().includes(searchTerm.toLowerCase());
      const matchesCategory = selectedCategory === 'all' || product.category === selectedCategory;
      return matchesSearch && matchesCategory;
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'price-low':
          return a.price - b.price;
        case 'price-high':
          return b.price - a.price;
        case 'rating':
          return b.rating - a.rating;
        case 'trust':
          return b.trustScore - a.trustScore;
        default:
          return b.id - a.id; // newest first
      }
    });

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-accent mx-auto mb-4"></div>
          <p className="text-muted-foreground">Loading marketplace...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Category Tabs */}
      <div className="border-b border-border/50 bg-card/20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex gap-2 overflow-x-auto py-4 scrollbar-hide">
            {[
              { id: 'all', label: 'All Products', icon: '🛒' },
              { id: 'vegetables', label: 'Vegetables', icon: '🥬' },
              { id: 'cotton', label: 'Cotton', icon: '🌿' },
              { id: 'grains', label: 'Grains', icon: '🌾' },
              { id: 'fruits', label: 'Fruits', icon: '🍎' },
            ].map((cat) => (
              <button
                key={cat.id}
                onClick={() => setSelectedCategory(cat.id)}
                className={`px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-all ${selectedCategory === cat.id
                  ? 'bg-accent text-accent-foreground'
                  : 'bg-secondary/50 text-muted-foreground hover:bg-secondary hover:text-foreground'
                  }`}
              >
                <span className="mr-2">{cat.icon}</span>
                {cat.label}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Search & Filters */}
      <div className="border-b border-border/50 bg-card/30 backdrop-blur-sm sticky top-16 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col md:flex-row gap-4 items-center">
            <div className="relative flex-1 w-full">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                placeholder="Search products, farmers..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 bg-secondary/50 border-border/50"
              />
            </div>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger className="w-full md:w-[180px] bg-secondary/50 border-border/50">
                <SelectValue placeholder="Category" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">All Categories</SelectItem>
                <SelectItem value="vegetables">Vegetables</SelectItem>
                <SelectItem value="cotton">Cotton</SelectItem>
                <SelectItem value="grains">Grains</SelectItem>
                <SelectItem value="fruits">Fruits</SelectItem>
              </SelectContent>
            </Select>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger className="w-full md:w-[150px] bg-secondary/50 border-border/50">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="newest">Newest</SelectItem>
                <SelectItem value="price-low">Price: Low</SelectItem>
                <SelectItem value="price-high">Price: High</SelectItem>
                <SelectItem value="rating">Top Rated</SelectItem>
                <SelectItem value="trust">Trust Score</SelectItem>
              </SelectContent>
            </Select>
            <Badge variant="outline" className="hidden md:flex border-accent/50 text-accent">
              {filteredProducts.length} Products
            </Badge>
          </div>
        </div>
      </div>

      {/* Products Grid */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.map((product) => (
            <Card key={product.id} className="glass-card overflow-hidden group hover:border-accent/50 transition-all duration-300">
              {/* Image Container */}
              <div className="relative h-48 overflow-hidden">
                <img
                  src={product.image}
                  alt={product.name}
                  className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
                  onError={(e) => {
                    e.target.src = 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=400&h=300&fit=crop';
                  }}
                />

                {/* Grade Badge */}
                <div className={`absolute top-3 left-3 w-10 h-10 rounded-full ${getGradeColor(product.grade)} flex items-center justify-center font-bold text-lg shadow-lg`}>
                  {product.grade}
                </div>

                {/* Favorite Button */}
                <button className="absolute top-3 right-3 w-10 h-10 rounded-full bg-card/50 backdrop-blur-sm flex items-center justify-center hover:bg-card transition-colors border border-border/50">
                  <Heart className="h-5 w-5 text-muted-foreground hover:text-red-500" />
                </button>

                {/* Verified Badge */}
                {product.verified && (
                  <div className="absolute bottom-3 left-3">
                    <Badge className="bg-card/80 backdrop-blur-sm text-accent border border-accent/30">
                      <Shield className="h-3 w-3 mr-1" />
                      Verified
                    </Badge>
                  </div>
                )}
              </div>

              <CardContent className="p-4 space-y-3">
                {/* Product Name & Price */}
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="text-lg font-semibold text-foreground">{product.name}</h3>
                    <p className="text-sm text-muted-foreground">{product.seller}</p>
                  </div>
                  <div className="text-right">
                    <span className="text-xl font-bold text-accent">₹{product.price}</span>
                    <span className="text-sm text-muted-foreground ml-1">per {product.unit}</span>
                  </div>
                </div>

                {/* Location & Rating */}
                <div className="flex items-center justify-between text-sm">
                  <div className="flex items-center text-muted-foreground">
                    <MapPin className="h-4 w-4 mr-1" />
                    {product.location}
                  </div>
                  <div className="flex items-center">
                    <Star className="h-4 w-4 text-yellow-500 fill-yellow-500 mr-1" />
                    <span className="text-foreground">{product.rating}</span>
                    <span className="text-muted-foreground ml-1">({product.reviews})</span>
                  </div>
                </div>

                {/* Trust Score */}
                <div className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <div className="flex items-center text-muted-foreground">
                      <Shield className="h-4 w-4 mr-1 text-accent" />
                      Trust Score
                    </div>
                    <span className="text-foreground font-medium">{product.trustScore}</span>
                  </div>
                  <div className="w-full h-2 bg-secondary rounded-full overflow-hidden">
                    <div
                      className={`h-full ${getTrustScoreColor(product.trustScore)} rounded-full transition-all duration-500`}
                      style={{ width: `${product.trustScore}%` }}
                    />
                  </div>
                </div>

                {/* Available Quantity */}
                <div className="flex items-center text-sm text-muted-foreground">
                  <Package className="h-4 w-4 mr-1" />
                  {product.quantity} {product.unit} available
                </div>

                {/* Action Buttons */}
                <div className="flex items-center gap-2 pt-2">
                  <Button className="flex-1 bg-accent hover:bg-accent/90 text-accent-foreground">
                    <ShoppingCart className="h-4 w-4 mr-2" />
                    Buy Now
                  </Button>
                  <Button variant="outline" size="icon" className="border-border/50 hover:border-accent/50">
                    <Phone className="h-4 w-4" />
                  </Button>
                  <Button variant="outline" size="icon" className="border-border/50 hover:border-accent/50">
                    <MessageCircle className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Load More Button */}
        <div className="flex justify-center mt-12">
          <Button variant="outline" className="border-accent/50 text-accent hover:bg-accent/10 px-8">
            Load More Listings
            <ChevronDown className="h-4 w-4 ml-2" />
          </Button>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-card/50 border-t border-border/50 mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            {/* Brand */}
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                  <Leaf className="h-5 w-5 text-accent-foreground" />
                </div>
                <span className="text-xl font-bold text-foreground">Agro<span className="text-accent">Grade</span></span>
              </div>
              <p className="text-sm text-muted-foreground mb-4">
                Empowering Indian farmers with AI-powered disease diagnosis and quality grading. From Crop Health to Market Wealth.
              </p>
              <div className="flex space-x-3">
                {['f', 't', 'i', 'in'].map((social, index) => (
                  <div key={index} className="w-8 h-8 rounded-full bg-secondary flex items-center justify-center hover:bg-accent/20 transition-colors cursor-pointer">
                    <span className="text-muted-foreground text-sm">{social}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Features */}
            <div>
              <h3 className="font-semibold text-accent mb-4">Features</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="hover:text-foreground cursor-pointer transition-colors">Disease Scanner</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">Quality Grader</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">Trust Tags</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">IoT Sensors</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">Marketplace</li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h3 className="font-semibold text-accent mb-4">Resources</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="hover:text-foreground cursor-pointer transition-colors">Documentation</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">API Reference</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">Farmer Guide</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">Buyer Guide</li>
                <li className="hover:text-foreground cursor-pointer transition-colors">Support Center</li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h3 className="font-semibold text-accent mb-4">Contact Us</h3>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-center">
                  <MapPinned className="h-4 w-4 mr-2 text-accent" />
                  Gujarat, India
                </li>
                <li className="flex items-center">
                  <Phone className="h-4 w-4 mr-2 text-accent" />
                  +91 98765 43210
                </li>
                <li className="flex items-center">
                  <Mail className="h-4 w-4 mr-2 text-accent" />
                  hello@agrograde.in
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom Bar */}
          <div className="border-t border-border/50 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-muted-foreground">
              © 2025 AgroGrade. All rights reserved.
            </p>
            <div className="flex space-x-6 mt-4 md:mt-0 text-sm text-muted-foreground">
              <span className="hover:text-foreground cursor-pointer transition-colors">Privacy Policy</span>
              <span className="hover:text-foreground cursor-pointer transition-colors">Terms of Service</span>
              <span className="hover:text-foreground cursor-pointer transition-colors">Cookie Policy</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Marketplace;
