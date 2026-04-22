import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent } from '@/components/ui/card';
import {
  Leaf,
  ArrowRight,
  Play,
  Camera,
  Scan,
  Award,
  ShoppingCart,
  Wifi,
  TrendingUp,
  Users,
  Shield,
  Download,
  MapPin,
  Phone,
  Mail,
  ChevronRight
} from 'lucide-react';

const Index = () => {
  const stats = [
    { value: '50K+', label: 'Farmers Empowered' },
    { value: '2M+', label: 'Crops Analyzed' },
    { value: '₹500Cr', label: 'Farmer Earnings' },
    { value: '98%', label: 'Accuracy Rate' }
  ];

  const features = [
    {
      icon: <Scan className="h-5 w-5" />,
      title: 'AI Disease Scanner',
      description: 'Capture a leaf photo and get instant AI diagnosis with treatment recommendations. Supports 38+ disease types across 15 Indian crops.',
      image: 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=400&h=250&fit=crop',
      link: '/disease-scanner'
    },
    {
      icon: <Award className="h-5 w-5" />,
      title: 'Quality Grading',
      description: 'AI-powered quality assessment assigns Grade A/B/C to your harvest. Creates verified Trust Tags for marketplace listings.',
      image: 'https://images.unsplash.com/photo-1542838132-92c53300491e?w=400&h=250&fit=crop',
      link: '/quality-grader'
    },
    {
      icon: <Shield className="h-5 w-5" />,
      title: 'Trust Tags',
      description: 'Blockchain-backed verification combining visual grading with IoT sensor data. Build buyer confidence with transparent quality scores.',
      link: '/dashboard'
    }
  ];

  const moreFeatures = [
    {
      icon: <Wifi className="h-5 w-5" />,
      title: 'IoT Sensors',
      description: 'Real-time soil moisture and NPK monitoring. Receive predictive alerts for drought and nutrient deficiencies before they cause damage.',
      link: '/dashboard'
    },
    {
      icon: <TrendingUp className="h-5 w-5" />,
      title: 'Direct Market Access',
      description: 'List your verified produce directly to wholesalers and retailers. Eliminate middlemen and secure 40% higher earnings.',
      link: '/marketplace'
    },
    {
      icon: <Users className="h-5 w-5" />,
      title: 'Farmer Community',
      description: 'Connect with fellow farmers, share insights, and learn best practices. Access expert agronomist support when needed.',
      link: '/dashboard'
    }
  ];

  const steps = [
    { icon: <Camera className="h-6 w-6" />, title: 'Capture', number: 1 },
    { icon: <Scan className="h-6 w-6" />, title: 'AI Analysis', number: 2 },
    { icon: <Award className="h-6 w-6" />, title: 'Get Certified', number: 3 },
    { icon: <ShoppingCart className="h-6 w-6" />, title: 'Sell Direct', number: 4 }
  ];

  return (
    <div className="min-h-screen bg-[#1a2e1a]">
      {/* Hero Section */}
      <section className="relative pt-8 pb-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid lg:grid-cols-2 gap-12 items-center">
            {/* Left Content */}
            <div>
              {/* Badge */}
              <Badge className="bg-[#2d4a2d] text-[#7cb342] border-[#3d5a3d] mb-6 px-4 py-1.5">
                <span className="w-2 h-2 bg-[#7cb342] rounded-full mr-2 inline-block"></span>
                AI-Powered Agricultural Revolution
              </Badge>

              {/* Headline */}
              <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold text-white mb-6 leading-tight">
                From <span className="text-[#7cb342]">Crop Health</span>
                <br />
                To <span className="text-[#7cb342]">Market Wealth</span>
              </h1>

              {/* Description */}
              <p className="text-gray-400 text-lg mb-8 max-w-xl">
                Empowering Indian farmers with instant AI disease diagnosis, certified quality grading, and direct market access. Bypass middlemen. Secure fair value.
              </p>

              {/* CTA Buttons */}
              <div className="flex flex-wrap gap-4 mb-12">
                <Link to="/disease-scanner">
                  <Button className="bg-[#4a7c23] hover:bg-[#5a8c33] text-white px-6 py-6 text-base">
                    <Scan className="mr-2 h-5 w-5" />
                    Scan Your Crop
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Button variant="outline" className="border-[#3d5a3d] bg-[#2d4a2d] text-white hover:bg-[#3d5a3d] px-6 py-6 text-base">
                  <Play className="mr-2 h-4 w-4" />
                  Watch Demo
                </Button>
              </div>

              {/* Stats */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-6">
                {stats.map((stat, index) => (
                  <div key={index}>
                    <div className="text-2xl sm:text-3xl font-bold text-[#7cb342]">{stat.value}</div>
                    <div className="text-sm text-gray-500">{stat.label}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Right Content - Disease Detection Card */}
            <div className="relative">
              <Card className="bg-[#2d4a2d]/80 border-[#3d5a3d] overflow-hidden">
                <CardContent className="p-0">
                  {/* Header */}
                  <div className="p-4 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-lg bg-[#4a7c23] flex items-center justify-center">
                      <Scan className="h-5 w-5 text-white" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-white">Disease Detection</h3>
                      <p className="text-sm text-gray-400">AI-powered diagnosis in seconds</p>
                    </div>
                  </div>

                  {/* Farm Image */}
                  <div className="relative">
                    <img
                      src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=600&h=300&fit=crop"
                      alt="Farm field"
                      className="w-full h-48 object-cover"
                    />

                    {/* Grade Badge */}
                    <div className="absolute top-4 right-4 bg-[#2d4a2d]/90 backdrop-blur-sm rounded-lg px-3 py-2 flex items-center gap-2">
                      <div className="w-8 h-8 rounded bg-[#4a7c23] flex items-center justify-center">
                        <Award className="h-4 w-4 text-white" />
                      </div>
                      <div>
                        <div className="text-white font-semibold text-sm">Grade A</div>
                        <div className="text-gray-400 text-xs">Trust Score: 95</div>
                      </div>
                    </div>

                    {/* Earnings Badge */}
                    <div className="absolute bottom-4 left-4 bg-[#2d4a2d]/90 backdrop-blur-sm rounded-lg px-4 py-2 flex items-center gap-2">
                      <TrendingUp className="h-4 w-4 text-[#7cb342]" />
                      <div>
                        <div className="text-white font-semibold text-sm">+40% Earnings</div>
                        <div className="text-gray-400 text-xs">Direct Market Access</div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" className="py-20 px-4 sm:px-6 lg:px-8 bg-[#1a2e1a] scroll-mt-20">
        <div className="max-w-7xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <Badge className="bg-transparent border-[#4a7c23] text-[#7cb342] mb-4">
              POWERFUL FEATURES
            </Badge>
            <h2
              onClick={() => document.getElementById('feature-cards')?.scrollIntoView({ behavior: 'smooth' })}
              className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4 cursor-pointer hover:text-[#7cb342] transition-colors"
            >
              Everything You Need To Thrive
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              A complete ecosystem bridging crop health monitoring to market wealth creation. AI, IoT, and blockchain working together for farmer prosperity.
            </p>
          </div>

          {/* Feature Cards */}
          <div id="feature-cards" className="grid md:grid-cols-3 gap-6 scroll-mt-20">
            {features.map((feature, index) => (
              <Card key={index} className={`bg-[#1a2e1a] border-[#2d4a2d] overflow-hidden hover:border-[#4a7c23] transition-colors ${index === 2 ? 'flex flex-col justify-between' : ''}`}>
                <CardContent className="p-0">
                  {feature.image && (
                    <img
                      src={feature.image}
                      alt={feature.title}
                      className="w-full h-48 object-cover"
                    />
                  )}
                  <div className={`p-6 ${!feature.image ? 'pt-8' : ''}`}>
                    <div className="flex items-center gap-3 mb-4">
                      <div className="w-10 h-10 rounded-lg bg-[#2d4a2d] border border-[#4a7c23] flex items-center justify-center text-[#7cb342]">
                        {feature.icon}
                      </div>
                      {!feature.image && <h3 className="font-semibold text-white text-lg">{feature.title}</h3>}
                    </div>
                    {feature.image && <h3 className="font-semibold text-white text-lg mb-2">{feature.title}</h3>}
                    <p className="text-gray-400 text-sm mb-4">{feature.description}</p>
                    <Link to={feature.link} className="text-[#7cb342] text-sm hover:underline inline-flex items-center">
                      Learn more <ChevronRight className="h-4 w-4 ml-1" />
                    </Link>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>

          {/* More Features */}
          <div className="grid md:grid-cols-3 gap-6 mt-8">
            {moreFeatures.map((feature, index) => (
              <Card key={index} className="bg-[#1a2e1a] border-[#2d4a2d] hover:border-[#4a7c23] transition-colors">
                <CardContent className="p-6">
                  <div className="w-10 h-10 rounded-lg bg-[#2d4a2d] border border-[#4a7c23] flex items-center justify-center text-[#7cb342] mb-4">
                    {feature.icon}
                  </div>
                  <h3 className="font-semibold text-white text-lg mb-2">{feature.title}</h3>
                  <p className="text-gray-400 text-sm mb-4">{feature.description}</p>
                  <Link to={feature.link} className="text-[#7cb342] text-sm hover:underline inline-flex items-center">
                    Learn more <ChevronRight className="h-4 w-4 ml-1" />
                  </Link>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-[#1f3620]">
        <div className="max-w-7xl mx-auto">
          {/* Section Header */}
          <div className="text-center mb-16">
            <Badge className="bg-transparent border-[#4a7c23] text-[#7cb342] mb-4">
              SIMPLE PROCESS
            </Badge>
            <h2 className="text-3xl sm:text-4xl lg:text-5xl font-bold text-white mb-4">
              How AgroGrade Works
            </h2>
            <p className="text-gray-400 max-w-2xl mx-auto">
              Four simple steps from crop scanning to market success. AI does the heavy lifting so you can focus on farming.
            </p>
          </div>

          {/* Steps */}
          <div className="grid sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {steps.map((step, index) => (
              <div key={index} className="text-center">
                <div className="relative inline-block mb-6">
                  {/* Step Number */}
                  <div className="absolute -top-2 -right-2 w-6 h-6 rounded-full bg-[#7cb342] text-black text-xs font-bold flex items-center justify-center">
                    {step.number}
                  </div>
                  {/* Icon Container */}
                  <div className="w-20 h-20 rounded-2xl bg-[#2d4a2d] border-2 border-[#4a7c23] flex items-center justify-center text-[#7cb342]">
                    {step.icon}
                  </div>
                </div>
                <h3 className="text-white font-semibold text-lg">{step.title}</h3>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4 sm:px-6 lg:px-8 bg-[#1a2e1a]">
        <div className="max-w-4xl mx-auto">
          <Card className="bg-gradient-to-br from-[#2d4a2d] to-[#1a2e1a] border-[#3d5a3d] overflow-hidden relative">
            {/* Decorative elements */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-[#4a7c23]/20 rounded-full blur-3xl"></div>
            <div className="absolute bottom-0 left-0 w-32 h-32 bg-[#7cb342]/10 rounded-full blur-3xl"></div>

            <CardContent className="p-10 text-center relative z-10">
              <Badge className="bg-[#4a7c23]/30 border-[#7cb342] text-[#7cb342] mb-6">
                <Leaf className="h-3 w-3 mr-1" />
                Available Now
              </Badge>

              <h2 className="text-3xl sm:text-4xl font-bold text-white mb-4">
                Start Your Journey to{' '}
                <span className="text-[#7cb342]">Agricultural Prosperity</span>
              </h2>

              <p className="text-gray-400 mb-8 max-w-xl mx-auto">
                Join 50,000+ farmers already using AgroGrade to diagnose diseases, certify quality, and access direct markets. Available in Gujarati, Hindi, and English.
              </p>

              <div className="flex flex-wrap justify-center gap-4 mb-8">
                <Link to="/auth">
                  <Button className="bg-[#4a7c23] hover:bg-[#5a8c33] text-white px-8 py-6 text-base">
                    <Download className="mr-2 h-4 w-4" />
                    Download App
                    <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Button variant="outline" className="border-[#3d5a3d] bg-[#2d4a2d] text-white hover:bg-[#3d5a3d] px-8 py-6 text-base">
                  Schedule Demo
                </Button>
              </div>

              {/* Trust Badges */}
              <div className="flex flex-wrap justify-center gap-6 text-sm text-gray-500">
                <span className="flex items-center gap-1">✓ ISO 27001 Certified</span>
                <span className="flex items-center gap-1">✓ NABARD Partner</span>
                <span className="flex items-center gap-1">✓ ICAR Validated</span>
                <span className="flex items-center gap-1">✓ Made in India</span>
              </div>
            </CardContent>
          </Card>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-[#1a2e1a] border-t border-[#2d4a2d] py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-4 gap-10">
            {/* Brand */}
            <div>
              <div className="flex items-center gap-2 mb-4">
                <div className="w-10 h-10 rounded-lg bg-[#2d4a2d] flex items-center justify-center">
                  <Leaf className="h-5 w-5 text-[#7cb342]" />
                </div>
                <span className="text-xl font-bold text-white">
                  Agro<span className="text-[#7cb342]">Grade</span>
                </span>
              </div>
              <p className="text-sm text-gray-500 mb-4">
                Empowering Indian farmers with AI-powered disease diagnosis and quality grading. From Crop Health to Market Wealth.
              </p>
              <div className="flex gap-3">
                {['f', 't', 'i', 'in'].map((social, index) => (
                  <div key={index} className="w-9 h-9 rounded-full border border-[#3d5a3d] flex items-center justify-center text-gray-500 hover:border-[#7cb342] hover:text-[#7cb342] transition-colors cursor-pointer">
                    <span className="text-sm">{social}</span>
                  </div>
                ))}
              </div>
            </div>

            {/* Features */}
            <div>
              <h3 className="font-semibold text-[#7cb342] mb-4">Features</h3>
              <ul className="space-y-3 text-sm text-gray-500">
                <li><Link to="/disease-scanner" className="hover:text-white transition-colors">Disease Scanner</Link></li>
                <li><Link to="/quality-grader" className="hover:text-white transition-colors">Quality Grader</Link></li>
                <li><Link to="/dashboard" className="hover:text-white transition-colors">Trust Tags</Link></li>
                <li><Link to="/dashboard" className="hover:text-white transition-colors">IoT Sensors</Link></li>
                <li><Link to="/marketplace" className="hover:text-white transition-colors">Marketplace</Link></li>
              </ul>
            </div>

            {/* Resources */}
            <div>
              <h3 className="font-semibold text-[#7cb342] mb-4">Resources</h3>
              <ul className="space-y-3 text-sm text-gray-500">
                <li><a href="#" className="hover:text-white transition-colors">Documentation</a></li>
                <li><a href="#" className="hover:text-white transition-colors">API Reference</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Farmer Guide</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Buyer Guide</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Support Center</a></li>
              </ul>
            </div>

            {/* Contact */}
            <div>
              <h3 className="font-semibold text-[#7cb342] mb-4">Contact Us</h3>
              <ul className="space-y-3 text-sm text-gray-500">
                <li className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-[#7cb342]" />
                  Gujarat, India
                </li>
                <li className="flex items-center gap-2">
                  <Phone className="h-4 w-4 text-[#7cb342]" />
                  +91 98765 43210
                </li>
                <li className="flex items-center gap-2">
                  <Mail className="h-4 w-4 text-[#7cb342]" />
                  hello@agrograde.in
                </li>
              </ul>
            </div>
          </div>

          {/* Bottom */}
          <div className="border-t border-[#2d4a2d] mt-12 pt-8 flex flex-col md:flex-row justify-between items-center">
            <p className="text-sm text-gray-600">© 2025 AgroGrade. All rights reserved.</p>
            <div className="flex gap-6 mt-4 md:mt-0 text-sm text-gray-600">
              <a href="#" className="hover:text-white transition-colors">Privacy Policy</a>
              <a href="#" className="hover:text-white transition-colors">Terms of Service</a>
              <a href="#" className="hover:text-white transition-colors">Cookie Policy</a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
