import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import {
  Home,
  Camera,
  BarChart3,
  ShoppingCart,
  User,
  Menu,
  X,
  Leaf,
  Settings,
  LogOut,
  Search,
  Award
} from 'lucide-react';

const Navigation = () => {
  const [user, setUser] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  };

  const navigation = [
    { name: 'Home', href: '/', icon: Home },
    { name: 'Disease Scanner', href: '/scanner', icon: Search },
    { name: 'Quality Grader', href: '/grader', icon: Award },
    { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
    { name: 'Marketplace', href: '/marketplace', icon: ShoppingCart },
  ];

  const isActive = (href) => {
    if (href === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(href);
  };

  return (
    <nav className="bg-background border-b border-border/50 sticky top-0 z-50 backdrop-blur-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-accent rounded-lg flex items-center justify-center">
                <Leaf className="h-5 w-5 text-accent-foreground" />
              </div>
              <span className="text-xl font-bold text-foreground">Agro<span className="text-accent">Grade</span></span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-1">
            {navigation.map((item) => (
              <Link
                key={item.name}
                to={item.href}
                className={`flex items-center space-x-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${isActive(item.href)
                    ? 'text-accent bg-accent/10 border border-accent/20'
                    : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                  }`}
              >
                <item.icon className="h-4 w-4" />
                <span>{item.name}</span>
              </Link>
            ))}
          </div>

          {/* User Menu */}
          <div className="hidden md:flex items-center space-x-3">
            {user ? (
              <>
                <Badge variant="outline" className="text-accent border-accent/30">
                  {user.farm_name || user.username}
                </Badge>
                <Button variant="outline" size="sm" onClick={handleLogout} className="border-border/50">
                  <LogOut className="h-4 w-4 mr-2" />
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost" size="sm">
                    Log In
                  </Button>
                </Link>
                <Link to="/login">
                  <Button size="sm" className="bg-accent hover:bg-accent/90 text-accent-foreground">
                    Get Started
                  </Button>
                </Link>
              </>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            >
              {isMobileMenuOpen ? (
                <X className="h-6 w-6" />
              ) : (
                <Menu className="h-6 w-6" />
              )}
            </Button>
          </div>
        </div>

        {/* Mobile Navigation */}
        {isMobileMenuOpen && (
          <div className="md:hidden border-t border-border/50 bg-card/50 backdrop-blur-sm">
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={`flex items-center space-x-3 px-3 py-2 rounded-lg text-base font-medium transition-all ${isActive(item.href)
                      ? 'text-accent bg-accent/10 border border-accent/20'
                      : 'text-muted-foreground hover:text-foreground hover:bg-secondary/50'
                    }`}
                  onClick={() => setIsMobileMenuOpen(false)}
                >
                  <item.icon className="h-5 w-5" />
                  <span>{item.name}</span>
                </Link>
              ))}

              {user ? (
                <>
                  <div className="border-t border-border/50 pt-4 mt-4">
                    <div className="px-3 py-2">
                      <p className="text-sm text-muted-foreground">Logged in as:</p>
                      <p className="text-sm font-medium text-foreground">{user.username}</p>
                      <p className="text-xs text-muted-foreground">{user.farm_name || 'Farmer'}</p>
                    </div>
                    <Button
                      variant="outline"
                      size="sm"
                      className="ml-3 mt-2"
                      onClick={handleLogout}
                    >
                      <LogOut className="h-4 w-4 mr-2" />
                      Logout
                    </Button>
                  </div>
                </>
              ) : (
                <div className="border-t border-border/50 pt-4 mt-4 space-y-2">
                  <Link to="/login" onClick={() => setIsMobileMenuOpen(false)}>
                    <Button variant="ghost" size="sm" className="ml-3 w-full">
                      Log In
                    </Button>
                  </Link>
                  <Link to="/login" onClick={() => setIsMobileMenuOpen(false)}>
                    <Button size="sm" className="ml-3 w-full bg-accent hover:bg-accent/90 text-accent-foreground">
                      Get Started
                    </Button>
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navigation;
