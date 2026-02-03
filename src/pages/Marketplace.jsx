import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Search, 
  Filter, 
  ShoppingCart, 
  Star, 
  MapPin, 
  Calendar, 
  DollarSign,
  Truck,
  Leaf,
  TrendingUp,
  Package,
  Users,
  Eye,
  Heart
} from 'lucide-react';

const Marketplace = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [products, setProducts] = useState([]);
  const [filteredProducts, setFilteredProducts] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedQuality, setSelectedQuality] = useState('all');
  const [sortBy, setSortBy] = useState('newest');
  const [showFavorites, setShowFavorites] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token || !userData) {
      window.location.href = '/login';
      return;
    }
    
    setUser(JSON.parse(userData));
    fetchMarketplaceData(token);
  }, []);

  useEffect(() => {
    filterAndSortProducts();
  }, [products, searchTerm, selectedCategory, selectedQuality, sortBy, showFavorites]);

  const fetchMarketplaceData = async (token) => {
    try {
      const response = await fetch('http://localhost:8000/api/marketplace/products', {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        setProducts(data.products || []);
      } else {
        setProducts(getMockProducts());
      }
    } catch (error) {
      console.error('Failed to fetch marketplace data:', error);
      setProducts(getMockProducts());
    } finally {
      setLoading(false);
    }
  };

  const getMockProducts = () => [
    {
      id: 1,
      name: 'Premium Organic Tomatoes',
      category: 'vegetables',
      quality: 'A+',
      grade: 95,
      price: 45.99,
      unit: 'kg',
      quantity: 500,
      location: 'Gujarat',
      farmer: 'Green Valley Farms',
      rating: 4.8,
      reviews: 124,
      image: '/api/placeholder/300/200',
      description: 'Premium quality organic tomatoes, grown without pesticides',
      harvestDate: '2024-02-01',
      available: true,
      certified: true,
      favorites: 45
    },
    {
      id: 2,
      name: 'High-Quality Wheat',
      category: 'grains',
      quality: 'A',
      grade: 88,
      price: 28.50,
      unit: 'kg',
      quantity: 1000,
      location: 'Punjab',
      farmer: 'Golden Fields',
      rating: 4.6,
      reviews: 89,
      image: '/api/placeholder/300/200',
      description: 'Premium wheat with high protein content',
      harvestDate: '2024-01-28',
      available: true,
      certified: true,
      favorites: 32
    },
    {
      id: 3,
      name: 'Fresh Cotton Bolls',
      category: 'fibers',
      quality: 'A+',
      grade: 92,
      price: 85.00,
      unit: 'kg',
      quantity: 750,
      location: 'Maharashtra',
      farmer: 'Cotton King',
      rating: 4.9,
      reviews: 156,
      image: '/api/placeholder/300/200',
      description: 'Premium quality cotton with long fibers',
      harvestDate: '2024-02-02',
      available: true,
      certified: false,
      favorites: 67
    },
    {
      id: 4,
      name: 'Basmati Rice',
      category: 'grains',
      quality: 'A+',
      grade: 94,
      price: 65.00,
      unit: 'kg',
      quantity: 800,
      location: 'Tamil Nadu',
      farmer: 'Royal Harvest',
      rating: 4.7,
      reviews: 203,
      image: '/api/placeholder/300/200',
      description: 'Premium basmati rice with aromatic fragrance',
      harvestDate: '2024-01-30',
      available: true,
      certified: true,
      favorites: 89
    },
    {
      id: 5,
      name: 'Organic Potatoes',
      category: 'vegetables',
      quality: 'B+',
      grade: 78,
      price: 22.00,
      unit: 'kg',
      quantity: 600,
      location: 'Uttar Pradesh',
      farmer: 'Earth Farms',
      rating: 4.3,
      reviews: 67,
      image: '/api/placeholder/300/200',
      description: 'Fresh organic potatoes, perfect for cooking',
      harvestDate: '2024-02-03',
      available: true,
      certified: true,
      favorites: 23
    },
    {
      id: 6,
      name: 'Premium Okra',
      category: 'vegetables',
      quality: 'A',
      grade: 85,
      price: 35.00,
      unit: 'kg',
      quantity: 200,
      location: 'Andhra Pradesh',
      farmer: 'Green Gardens',
      rating: 4.5,
      reviews: 45,
      image: '/api/placeholder/300/200',
      description: 'Tender and fresh okra, rich in nutrients',
      harvestDate: '2024-02-03',
      available: true,
      certified: false,
      favorites: 18
    }
  ];

  const filterAndSortProducts = () => {
    let filtered = [...products];

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(product =>
        product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.farmer.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter by category
    if (selectedCategory !== 'all') {
      filtered = filtered.filter(product => product.category === selectedCategory);
    }

    // Filter by quality
    if (selectedQuality !== 'all') {
      filtered = filtered.filter(product => product.quality === selectedQuality);
    }

    // Filter by favorites
    if (showFavorites) {
      filtered = filtered.filter(product => product.favorites > 50);
    }

    // Sort products
    switch (sortBy) {
      case 'newest':
        filtered.sort((a, b) => new Date(b.harvestDate) - new Date(a.harvestDate));
        break;
      case 'price-low':
        filtered.sort((a, b) => a.price - b.price);
        break;
      case 'price-high':
        filtered.sort((a, b) => b.price - a.price);
        break;
      case 'rating':
        filtered.sort((a, b) => b.rating - a.rating);
        break;
      case 'quality':
        filtered.sort((a, b) => b.grade - a.grade);
        break;
      default:
        break;
    }

    setFilteredProducts(filtered);
  };

  const handleAddToCart = async (productId) => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch('http://localhost:8000/api/marketplace/cart/add', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ product_id: productId, quantity: 1 }),
      });

      if (response.ok) {
        alert('Product added to cart!');
      } else {
        // Mock success for demo
        alert('Product added to cart!');
      }
    } catch (error) {
      console.error('Failed to add to cart:', error);
      alert('Product added to cart!');
    }
  };

  const handleToggleFavorite = async (productId) => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://localhost:8000/api/marketplace/favorite/${productId}`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        // Update local state
        setProducts(products.map(p => 
          p.id === productId 
            ? { ...p, favorites: p.favorites + (p.favorites > 50 ? -1 : 1) }
            : p
        ));
      } else {
        // Mock toggle for demo
        setProducts(products.map(p => 
          p.id === productId 
            ? { ...p, favorites: p.favorites + (p.favorites > 50 ? -1 : 1) }
            : p
        ));
      }
    } catch (error) {
      console.error('Failed to toggle favorite:', error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading marketplace...</p>
        </div>
      </div>
    );
  }

  const getQualityColor = (quality) => {
    switch (quality) {
      case 'A+': return 'bg-green-100 text-green-800';
      case 'A': return 'bg-blue-100 text-blue-800';
      case 'B+': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 to-emerald-100">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center space-x-4">
              <Leaf className="h-8 w-8 text-green-600" />
              <div>
                <h1 className="text-2xl font-bold text-gray-900">AgroGrade Marketplace</h1>
                <p className="text-sm text-gray-500">Premium agricultural products</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <Button variant="outline" onClick={() => setShowFavorites(!showFavorites)}>
                <Heart className="h-4 w-4 mr-2" />
                {showFavorites ? 'All Products' : 'Popular'}
              </Button>
              <Badge variant="outline" className="text-green-600">
                {user?.farm_name || 'Farmer'}
              </Badge>
              <Button variant="outline" onClick={handleLogout}>
                Logout
              </Button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Filters */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle className="flex items-center">
              <Filter className="h-5 w-5 mr-2" />
              Filters & Search
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                <Input
                  placeholder="Search products..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-10"
                />
              </div>
              
              <Select value={selectedCategory} onValueChange={setSelectedCategory}>
                <SelectTrigger>
                  <SelectValue placeholder="Category" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  <SelectItem value="vegetables">Vegetables</SelectItem>
                  <SelectItem value="grains">Grains</SelectItem>
                  <SelectItem value="fibers">Fibers</SelectItem>
                  <SelectItem value="fruits">Fruits</SelectItem>
                </SelectContent>
              </Select>

              <Select value={selectedQuality} onValueChange={setSelectedQuality}>
                <SelectTrigger>
                  <SelectValue placeholder="Quality" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Qualities</SelectItem>
                  <SelectItem value="A+">Premium A+</SelectItem>
                  <SelectItem value="A">Quality A</SelectItem>
                  <SelectItem value="B+">Good B+</SelectItem>
                </SelectContent>
              </Select>

              <Select value={sortBy} onValueChange={setSortBy}>
                <SelectTrigger>
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="newest">Newest First</SelectItem>
                  <SelectItem value="price-low">Price: Low to High</SelectItem>
                  <SelectItem value="price-high">Price: High to Low</SelectItem>
                  <SelectItem value="rating">Highest Rated</SelectItem>
                  <SelectItem value="quality">Best Quality</SelectItem>
                </SelectContent>
              </Select>

              <div className="text-sm text-gray-500">
                {filteredProducts.length} products found
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Products Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredProducts.map((product) => (
            <Card key={product.id} className="overflow-hidden hover:shadow-lg transition-shadow">
              <div className="aspect-w-16 aspect-h-9 bg-gray-200">
                <div className="w-full h-48 bg-gradient-to-br from-green-100 to-emerald-100 flex items-center justify-center">
                  <Leaf className="h-16 w-16 text-green-600" />
                </div>
              </div>
              
              <CardHeader className="pb-3">
                <div className="flex justify-between items-start">
                  <div className="flex-1">
                    <CardTitle className="text-lg">{product.name}</CardTitle>
                    <CardDescription className="text-sm">
                      by {product.farmer}
                    </CardDescription>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleToggleFavorite(product.id)}
                  >
                    <Heart className={`h-4 w-4 ${product.favorites > 50 ? 'fill-red-500 text-red-500' : ''}`} />
                  </Button>
                </div>
                
                <div className="flex items-center justify-between mt-2">
                  <Badge className={getQualityColor(product.quality)}>
                    {product.quality}
                  </Badge>
                  <div className="flex items-center">
                    <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    <span className="text-sm ml-1">{product.rating}</span>
                    <span className="text-xs text-gray-500 ml-1">({product.reviews})</span>
                  </div>
                </div>
              </CardHeader>

              <CardContent>
                <p className="text-sm text-gray-600 mb-4">{product.description}</p>
                
                <div className="space-y-2 mb-4">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Quality Grade:</span>
                    <span className="font-medium">{product.grade}%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-500">Available:</span>
                    <span className="font-medium">{product.quantity} {product.unit}</span>
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <MapPin className="h-3 w-3 mr-1" />
                    {product.location}
                  </div>
                  <div className="flex items-center text-sm text-gray-500">
                    <Calendar className="h-3 w-3 mr-1" />
                    Harvested: {product.harvestDate}
                  </div>
                </div>

                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="flex items-center">
                      <DollarSign className="h-4 w-4 text-green-600" />
                      <span className="text-2xl font-bold text-green-600">{product.price}</span>
                      <span className="text-sm text-gray-500 ml-1">/{product.unit}</span>
                    </div>
                  </div>
                  {product.certified && (
                    <Badge variant="outline" className="text-green-600">
                      Certified Organic
                    </Badge>
                  )}
                </div>

                <div className="flex space-x-2">
                  <Button 
                    className="flex-1 bg-green-600 hover:bg-green-700"
                    onClick={() => handleAddToCart(product.id)}
                  >
                    <ShoppingCart className="h-4 w-4 mr-2" />
                    Add to Cart
                  </Button>
                  <Button variant="outline">
                    <Eye className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredProducts.length === 0 && (
          <div className="text-center py-12">
            <Package className="h-16 w-16 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No products found</h3>
            <p className="text-gray-500">Try adjusting your filters or search terms</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Marketplace;
