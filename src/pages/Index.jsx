import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Leaf, 
  Camera, 
  BarChart3, 
  ShoppingCart, 
  CheckCircle, 
  ArrowRight,
  Star,
  TrendingUp,
  Users,
  Award,
  Zap,
  Shield,
  Droplets,
  Sun,
  Wind,
  Sprout,
  AlertTriangle,
  Play,
  ChevronRight,
  Globe,
  Heart,
  Target,
  Lightbulb
} from 'lucide-react';

const Index = () => {
  const [currentTestimonial, setCurrentTestimonial] = useState(0);
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const testimonials = [
    {
      name: "Rajesh Patel",
      farm: "Green Valley Farms",
      quote: "AgroGrade AI helped me detect early blight in my tomato crop and saved 40% of my yield. The AI recommendations were spot on!",
      rating: 5,
      avatar: "👨‍🌾"
    },
    {
      name: "Priya Sharma",
      farm: "Sunshine Organics",
      quote: "The quality grading feature helped me get premium prices for my produce. Buyers trust the AI certification.",
      rating: 5,
      avatar: "👩‍🌾"
    },
    {
      name: "Amit Kumar",
      farm: "Modern Agriculture Co.",
      quote: "The marketplace integration is game-changing. I can sell directly to buyers and get better prices.",
      rating: 5,
      avatar: "👨‍🌾"
    }
  ];

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTestimonial((prev) => (prev + 1) % testimonials.length);
    }, 5000);
    return () => clearInterval(interval);
  }, [testimonials.length]);

  const features = [
    {
      icon: Camera,
      title: "AI Disease Detection",
      description: "Upload leaf images and get instant AI-powered disease detection with 95% accuracy",
      color: "text-green-600",
      bgColor: "bg-green-100",
      stats: "95% Accuracy"
    },
    {
      icon: BarChart3,
      title: "Smart Dashboard",
      description: "Track your farm's health, analysis history, and get actionable insights",
      color: "text-blue-600",
      bgColor: "bg-blue-100",
      stats: "Real-time Data"
    },
    {
      icon: ShoppingCart,
      title: "Digital Marketplace",
      description: "Connect directly with buyers, sell your produce, and get better prices",
      color: "text-purple-600",
      bgColor: "bg-purple-100",
      stats: "1000+ Buyers"
    },
    {
      icon: Award,
      title: "Quality Grading",
      description: "Automated quality assessment based on international standards",
      color: "text-yellow-600",
      bgColor: "bg-yellow-100",
      stats: "Grade A+ Certification"
    }
  ];

  const stats = [
    { number: "95%", label: "Accuracy Rate", icon: Target },
    { number: "50K+", label: "Analyses Done", icon: Camera },
    { number: "1000+", label: "Happy Farmers", icon: Users },
    { number: "24/7", label: "AI Support", icon: Zap }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-50 via-emerald-50 to-teal-50">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div 
          className="absolute w-96 h-96 bg-green-200 rounded-full opacity-20 blur-3xl"
          style={{ 
            top: `${10 + scrollY * 0.05}%`, 
            left: `${10 + scrollY * 0.02}%` 
          }}
        />
        <div 
          className="absolute w-96 h-96 bg-blue-200 rounded-full opacity-20 blur-3xl"
          style={{ 
            bottom: `${10 + scrollY * 0.03}%`, 
            right: `${10 + scrollY * 0.04}%` 
          }}
        />
        <div 
          className="absolute w-64 h-64 bg-yellow-200 rounded-full opacity-20 blur-2xl"
          style={{ 
            top: `${50 + scrollY * 0.02}%`, 
            left: `${50 + scrollY * 0.03}%` 
          }}
        />
      </div>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 relative z-10">
          <div className="text-center">
            {/* Floating Logo */}
            <div className="flex items-center justify-center mb-8 animate-bounce">
              <div className="flex items-center space-x-3 bg-white rounded-full p-4 shadow-2xl border border-green-200">
                <div className="relative">
                  <div className="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl flex items-center justify-center shadow-lg">
                    <div className="text-white font-bold text-2xl">🌾</div>
                  </div>
                  <div className="absolute -top-1 -right-1 w-4 h-4 bg-yellow-400 rounded-full flex items-center justify-center">
                    <span className="text-xs font-bold text-green-800">AI</span>
                  </div>
                </div>
                <div className="text-left">
                  <h1 className="text-4xl font-bold text-gray-900 bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                    AgroGrade
                  </h1>
                  <p className="text-sm text-gray-600 font-medium">AI-Powered Agriculture</p>
                </div>
              </div>
            </div>
            
            {/* Main Hero Content */}
            <div className="max-w-5xl mx-auto">
              <h1 className="text-5xl md:text-7xl font-bold text-gray-900 mb-6 leading-tight">
                Transform Your Farming with
                <span className="block bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent">
                  AI Technology
                </span>
              </h1>
              <p className="text-xl md:text-2xl text-gray-600 mb-8 max-w-3xl mx-auto leading-relaxed">
                Advanced disease detection, quality grading, and marketplace integration for modern agriculture.
                Get instant AI analysis of your crops and connect with buyers directly.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12">
                <Link to="/login">
                  <Button size="lg" className="bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white px-8 py-4 text-lg shadow-xl transform hover:scale-105 transition-all duration-200">
                    Get Started
                    <ArrowRight className="ml-2 h-5 w-5" />
                  </Button>
                </Link>
                <Link to="/ai-analysis">
                  <Button variant="outline" size="lg" className="border-2 border-green-600 text-green-600 hover:bg-green-50 px-8 py-4 text-lg">
                    <Play className="mr-2 h-5 w-5" />
                    Try AI Analysis
                  </Button>
                </Link>
              </div>

              {/* Trust Indicators */}
              <div className="flex flex-wrap justify-center gap-8 mb-12">
                {[
                  { icon: Shield, text: "Bank-level Security" },
                  { icon: Award, text: "Certified AI" },
                  { icon: Globe, text: "Global Standards" },
                  { icon: Heart, text: "Farmer First" }
                ].map((item, index) => (
                  <div key={index} className="flex items-center gap-2 text-gray-600">
                    <item.icon className="h-5 w-5 text-green-600" />
                    <span className="font-medium">{item.text}</span>
                  </div>
                ))}
              </div>
            </div>
            
            {/* Animated Stats */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-8 mt-16 max-w-4xl mx-auto">
              {stats.map((stat, index) => (
                <div 
                  key={index} 
                  className="text-center transform hover:scale-110 transition-all duration-300"
                  style={{ animationDelay: `${index * 100}ms` }}
                >
                  <div className="bg-white rounded-2xl p-6 shadow-lg border border-gray-100">
                    <stat.icon className="h-8 w-8 text-green-600 mx-auto mb-3" />
                    <div className="text-4xl font-bold text-gray-900 mb-2">{stat.number}</div>
                    <div className="text-gray-600 font-medium">{stat.label}</div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* Interactive Features Section */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-green-100 text-green-800 px-4 py-2">Features</Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Modern Agriculture
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Everything you need to manage your farm efficiently with AI-powered insights
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <Card 
                key={index} 
                className="group hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-2 border-0 bg-white/80 backdrop-blur-sm"
                style={{ animationDelay: `${index * 150}ms` }}
              >
                <CardHeader className="text-center">
                  <div className={`w-16 h-16 rounded-2xl ${feature.bgColor} flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300`}>
                    <feature.icon className={`h-8 w-8 ${feature.color}`} />
                  </div>
                  <CardTitle className="text-xl font-semibold">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent className="text-center">
                  <CardDescription className="text-gray-600 mb-4">
                    {feature.description}
                  </CardDescription>
                  <Badge className={`${feature.bgColor} ${feature.color}`}>
                    {feature.stats}
                  </Badge>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works - Interactive */}
      <section className="py-20 bg-gradient-to-r from-green-50 to-emerald-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-blue-100 text-blue-800 px-4 py-2">Process</Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              How AgroGrade AI Works
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Simple 3-step process to transform your farming experience
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {[
              {
                step: 1,
                icon: Camera,
                title: "Upload Leaf Image",
                description: "Take a photo of your crop leaf and upload it to our AI system",
                color: "bg-green-500"
              },
              {
                step: 2,
                icon: BarChart3,
                title: "Get AI Analysis",
                description: "Our AI analyzes the image for diseases and provides detailed results",
                color: "bg-blue-500"
              },
              {
                step: 3,
                icon: CheckCircle,
                title: "Take Action",
                description: "Get treatment recommendations and sell your produce in the marketplace",
                color: "bg-purple-500"
              }
            ].map((item, index) => (
              <div key={index} className="text-center group">
                <div className="relative mb-8">
                  <div className={`w-20 h-20 rounded-full ${item.color} flex items-center justify-center mx-auto mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg`}>
                    <item.icon className="h-10 w-10 text-white" />
                  </div>
                  <div className="absolute -top-2 -right-2 w-8 h-8 bg-white rounded-full flex items-center justify-center shadow-md border-2 border-gray-200">
                    <span className="text-sm font-bold text-gray-700">{item.step}</span>
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-3">{item.title}</h3>
                <p className="text-gray-600 leading-relaxed">{item.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Testimonials - Auto-rotating */}
      <section className="py-20 bg-white/50 backdrop-blur-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <Badge className="mb-4 bg-yellow-100 text-yellow-800 px-4 py-2">Testimonials</Badge>
            <h2 className="text-4xl font-bold text-gray-900 mb-4">
              What Farmers Are Saying
            </h2>
          </div>
          
          <div className="max-w-4xl mx-auto">
            <Card className="bg-gradient-to-br from-green-50 to-emerald-50 border-0 shadow-xl">
              <CardContent className="p-8">
                <div className="text-center">
                  <div className="text-6xl mb-6">{testimonials[currentTestimonial].avatar}</div>
                  <div className="flex justify-center mb-4">
                    {[...Array(testimonials[currentTestimonial].rating)].map((_, i) => (
                      <Star key={i} className="h-5 w-5 text-yellow-400 fill-current" />
                    ))}
                  </div>
                  <p className="text-xl text-gray-700 mb-6 italic leading-relaxed">
                    "{testimonials[currentTestimonial].quote}"
                  </p>
                  <div>
                    <p className="font-semibold text-lg text-gray-900">
                      {testimonials[currentTestimonial].name}
                    </p>
                    <p className="text-gray-600">{testimonials[currentTestimonial].farm}</p>
                  </div>
                </div>
                
                {/* Testimonial Dots */}
                <div className="flex justify-center mt-8 space-x-2">
                  {testimonials.map((_, index) => (
                    <button
                      key={index}
                      onClick={() => setCurrentTestimonial(index)}
                      className={`w-2 h-2 rounded-full transition-all duration-300 ${
                        index === currentTestimonial 
                          ? 'bg-green-600 w-8' 
                          : 'bg-gray-300 hover:bg-gray-400'
                      }`}
                    />
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* CTA Section - Enhanced */}
      <section className="py-20 bg-gradient-to-r from-green-600 to-emerald-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/10"></div>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
          <Badge className="mb-4 bg-white/20 text-white px-4 py-2">Get Started</Badge>
          <h2 className="text-4xl font-bold text-white mb-6">
            Ready to Transform Your Farming?
          </h2>
          <p className="text-xl text-green-100 mb-8 max-w-3xl mx-auto">
            Join thousands of farmers who are already using AI to improve their crop yield and quality.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/login">
              <Button size="lg" className="bg-white text-green-600 hover:bg-gray-100 px-8 py-4 text-lg shadow-2xl transform hover:scale-105 transition-all duration-200">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link to="/ai-analysis">
              <Button variant="outline" size="lg" className="border-white text-white hover:bg-white hover:text-green-600 px-8 py-4 text-lg">
                <Play className="mr-2 h-5 w-5" />
                Try Demo Analysis
              </Button>
            </Link>
          </div>
          
          {/* Additional Trust Elements */}
          <div className="mt-12 flex flex-wrap justify-center gap-8 text-white/80">
            <div className="flex items-center gap-2">
              <CheckCircle className="h-5 w-5" />
              <span>No Credit Card Required</span>
            </div>
            <div className="flex items-center gap-2">
              <Zap className="h-5 w-5" />
              <span>Instant Setup</span>
            </div>
            <div className="flex items-center gap-2">
              <Shield className="h-5 w-5" />
              <span>100% Secure</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer - Enhanced */}
      <footer className="bg-gray-900 text-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="relative">
                  <div className="w-10 h-10 bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl flex items-center justify-center shadow-lg">
                    <div className="text-white font-bold text-lg">🌾</div>
                  </div>
                  <div className="absolute -top-1 -right-1 w-3 h-3 bg-yellow-400 rounded-full flex items-center justify-center">
                    <span className="text-xs font-bold text-green-800">AI</span>
                  </div>
                </div>
                <div>
                  <h3 className="text-lg font-semibold">AgroGrade AI</h3>
                  <p className="text-gray-400">AI-Powered Agriculture</p>
                </div>
              </div>
              <p className="text-gray-400">
                Empowering farmers with artificial intelligence for better crop management and increased yields.
              </p>
              <div className="flex space-x-4 mt-4">
                {['f', 't', 'i'].map((social, index) => (
                  <div key={index} className="w-8 h-8 bg-gray-800 rounded-full flex items-center justify-center hover:bg-green-600 transition-colors cursor-pointer">
                    <span className="text-white text-sm">{social}</span>
                  </div>
                ))}
              </div>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Quick Links</h3>
              <ul className="space-y-2">
                {[
                  { name: 'Login', path: '/login' },
                  { name: 'AI Analysis', path: '/ai-analysis' },
                  { name: 'Dashboard', path: '/dashboard' },
                  { name: 'Marketplace', path: '/marketplace' }
                ].map((link) => (
                  <li key={link.name}>
                    <Link to={link.path} className="text-gray-400 hover:text-white transition-colors flex items-center gap-1">
                      {link.name}
                      <ChevronRight className="h-3 w-3" />
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Features</h3>
              <ul className="space-y-2">
                {[
                  'Disease Detection',
                  'Quality Grading',
                  'Smart Dashboard',
                  'Digital Marketplace'
                ].map((feature) => (
                  <li key={feature}>
                    <span className="text-gray-400 hover:text-white transition-colors cursor-pointer flex items-center gap-1">
                      <Lightbulb className="h-3 w-3" />
                      {feature}
                    </span>
                  </li>
                ))}
              </ul>
            </div>
            
            <div>
              <h3 className="text-lg font-semibold mb-4">Contact</h3>
              <ul className="space-y-2 text-gray-400">
                <li className="flex items-center gap-2">
                  <Globe className="h-4 w-4" />
                  support@agrograde.ai
                </li>
                <li className="flex items-center gap-2">
                  <Users className="h-4 w-4" />
                  +91 98765 43210
                </li>
                <li className="flex items-center gap-2">
                  <Sun className="h-4 w-4" />
                  24/7 Available
                </li>
              </ul>
            </div>
          </div>
          
          <div className="border-t border-gray-800 pt-8 mt-8">
            <div className="flex flex-col md:flex-row justify-between items-center">
              <p className="text-gray-400">
                © 2024 AgroGrade AI. All rights reserved.
              </p>
              <div className="flex space-x-6 mt-4 md:mt-0">
                <span className="text-gray-400 hover:text-white cursor-pointer">Privacy Policy</span>
                <span className="text-gray-400 hover:text-white cursor-pointer">Terms of Service</span>
                <span className="text-gray-400 hover:text-white cursor-pointer">Cookie Policy</span>
              </div>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
