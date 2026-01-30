import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { Button } from "@/components/ui/button";
import { Camera, Upload, Leaf, AlertTriangle, CheckCircle, RefreshCw, Droplets, Bug, Zap } from "lucide-react";
import diseasedLeaf from "@/assets/diseased-leaf.jpg";
import healthyLeaf from "@/assets/healthy-leaf.jpg";

// Mock disease data for demo
const mockDiseases = [
  {
    name: "Early Blight",
    confidence: 94.7,
    severity: "Moderate",
    crop: "Tomato",
    description: "Fungal infection caused by Alternaria solani. Brown spots with concentric rings on leaves.",
    remedies: [
      { type: "Organic", name: "Neem Oil Spray", instructions: "Mix 5ml neem oil in 1L water. Spray every 7 days." },
      { type: "Organic", name: "Copper Fungicide", instructions: "Apply Bordeaux mixture (1%) on affected areas." },
      { type: "Prevention", name: "Crop Rotation", instructions: "Rotate with non-solanaceous crops for 2-3 years." },
    ],
  },
  {
    name: "Healthy",
    confidence: 98.2,
    severity: "None",
    crop: "General",
    description: "No disease detected. Your crop appears to be healthy with good leaf coloration and structure.",
    remedies: [
      { type: "Prevention", name: "Regular Monitoring", instructions: "Continue weekly inspections of your crops." },
      { type: "Nutrition", name: "Balanced Fertilizer", instructions: "Apply NPK fertilizer as per soil test recommendations." },
    ],
  },
];

const DiseaseScanner = () => {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [isScanning, setIsScanning] = useState(false);
  const [scanResult, setScanResult] = useState<typeof mockDiseases[0] | null>(null);
  const [dragActive, setDragActive] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  }, []);

  const handleFile = (file: File) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      setUploadedImage(e.target?.result as string);
      setScanResult(null);
    };
    reader.readAsDataURL(file);
  };

  const handleScan = () => {
    setIsScanning(true);
    // Simulate AI processing
    setTimeout(() => {
      // Randomly pick healthy or diseased for demo
      const result = Math.random() > 0.5 ? mockDiseases[0] : mockDiseases[1];
      setScanResult(result);
      setIsScanning(false);
    }, 2500);
  };

  const handleReset = () => {
    setUploadedImage(null);
    setScanResult(null);
    setIsScanning(false);
  };

  const useSampleImage = (type: "diseased" | "healthy") => {
    setUploadedImage(type === "diseased" ? diseasedLeaf : healthyLeaf);
    setScanResult(null);
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
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/10 border border-accent/30 mb-4">
              <Bug className="w-4 h-4 text-accent" />
              <span className="text-accent text-sm font-medium">AI-Powered Diagnosis</span>
            </div>
            <h1 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
              Disease Scanner
            </h1>
            <p className="text-muted-foreground text-lg">
              Upload a photo of your crop leaf and get instant AI diagnosis with treatment recommendations.
            </p>
          </motion.div>

          <div className="grid lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
            {/* Upload Area */}
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.2 }}
              className="glass-card rounded-2xl p-6"
            >
              <h2 className="font-display text-xl font-semibold mb-4 flex items-center gap-2">
                <Camera className="w-5 h-5 text-accent" />
                Upload Leaf Image
              </h2>

              {!uploadedImage ? (
                <>
                  <div
                    className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
                      dragActive
                        ? "border-accent bg-accent/10"
                        : "border-border hover:border-accent/50"
                    }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                  >
                    <input
                      type="file"
                      accept="image/*"
                      onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])}
                      className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                    />
                    <Upload className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
                    <p className="text-foreground font-medium mb-2">
                      Drag & drop your leaf image here
                    </p>
                    <p className="text-sm text-muted-foreground">
                      or click to browse • PNG, JPG up to 10MB
                    </p>
                  </div>

                  {/* Sample Images */}
                  <div className="mt-6">
                    <p className="text-sm text-muted-foreground mb-3">Or try with sample images:</p>
                    <div className="flex gap-3">
                      <button
                        onClick={() => useSampleImage("diseased")}
                        className="flex-1 group relative rounded-xl overflow-hidden aspect-video"
                      >
                        <img
                          src={diseasedLeaf}
                          alt="Diseased leaf sample"
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent flex items-end p-3">
                          <span className="text-sm font-medium text-destructive">Diseased</span>
                        </div>
                      </button>
                      <button
                        onClick={() => useSampleImage("healthy")}
                        className="flex-1 group relative rounded-xl overflow-hidden aspect-video"
                      >
                        <img
                          src={healthyLeaf}
                          alt="Healthy leaf sample"
                          className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent flex items-end p-3">
                          <span className="text-sm font-medium text-success">Healthy</span>
                        </div>
                      </button>
                    </div>
                  </div>
                </>
              ) : (
                <div className="space-y-4">
                  <div className="relative rounded-xl overflow-hidden aspect-video">
                    <img
                      src={uploadedImage}
                      alt="Uploaded leaf"
                      className="w-full h-full object-cover"
                    />
                    {isScanning && (
                      <div className="absolute inset-0 bg-background/50 flex items-center justify-center">
                        <div className="text-center">
                          <div className="w-20 h-20 mx-auto border-4 border-accent/30 border-t-accent rounded-full animate-spin mb-4" />
                          <p className="text-accent font-medium">Analyzing with AI...</p>
                        </div>
                        {/* Scan Line Effect */}
                        <div className="absolute left-0 right-0 h-1 bg-accent/50 animate-scan" />
                      </div>
                    )}
                  </div>

                  <div className="flex gap-3">
                    <Button
                      variant="scan"
                      className="flex-1"
                      onClick={handleScan}
                      disabled={isScanning}
                    >
                      {isScanning ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin" />
                          Scanning...
                        </>
                      ) : (
                        <>
                          <Zap className="w-4 h-4" />
                          Scan Now
                        </>
                      )}
                    </Button>
                    <Button variant="outline" onClick={handleReset}>
                      <RefreshCw className="w-4 h-4" />
                      Reset
                    </Button>
                  </div>
                </div>
              )}
            </motion.div>

            {/* Results Area */}
            <motion.div
              initial={{ opacity: 0, x: 30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.3 }}
              className="glass-card rounded-2xl p-6"
            >
              <h2 className="font-display text-xl font-semibold mb-4 flex items-center gap-2">
                <Leaf className="w-5 h-5 text-accent" />
                Diagnosis Result
              </h2>

              <AnimatePresence mode="wait">
                {!scanResult ? (
                  <motion.div
                    key="empty"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="h-[400px] flex items-center justify-center text-center"
                  >
                    <div>
                      <div className="w-20 h-20 mx-auto rounded-full bg-secondary flex items-center justify-center mb-4">
                        <Camera className="w-10 h-10 text-muted-foreground" />
                      </div>
                      <p className="text-muted-foreground">
                        Upload an image and click "Scan Now" to get AI diagnosis
                      </p>
                    </div>
                  </motion.div>
                ) : (
                  <motion.div
                    key="result"
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    className="space-y-6"
                  >
                    {/* Disease Info */}
                    <div
                      className={`p-4 rounded-xl border ${
                        scanResult.name === "Healthy"
                          ? "border-success/30 bg-success/10"
                          : "border-destructive/30 bg-destructive/10"
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <div
                          className={`w-12 h-12 rounded-xl flex items-center justify-center ${
                            scanResult.name === "Healthy" ? "bg-success/20" : "bg-destructive/20"
                          }`}
                        >
                          {scanResult.name === "Healthy" ? (
                            <CheckCircle className="w-6 h-6 text-success" />
                          ) : (
                            <AlertTriangle className="w-6 h-6 text-destructive" />
                          )}
                        </div>
                        <div className="flex-1">
                          <h3 className="font-display text-xl font-semibold">{scanResult.name}</h3>
                          <p className="text-sm text-muted-foreground">
                            Crop: {scanResult.crop} • Severity: {scanResult.severity}
                          </p>
                        </div>
                        <div className="text-right">
                          <div className="text-2xl font-bold text-accent">{scanResult.confidence}%</div>
                          <div className="text-xs text-muted-foreground">Confidence</div>
                        </div>
                      </div>
                      <p className="mt-3 text-sm text-muted-foreground">{scanResult.description}</p>
                    </div>

                    {/* Remedies */}
                    <div>
                      <h4 className="font-semibold mb-3 flex items-center gap-2">
                        <Droplets className="w-4 h-4 text-accent" />
                        Recommended Treatment
                      </h4>
                      <div className="space-y-3">
                        {scanResult.remedies.map((remedy, i) => (
                          <div
                            key={i}
                            className="p-3 rounded-lg bg-secondary/50 border border-border/50"
                          >
                            <div className="flex items-center gap-2 mb-1">
                              <span
                                className={`text-xs font-medium px-2 py-0.5 rounded-full ${
                                  remedy.type === "Organic"
                                    ? "bg-success/20 text-success"
                                    : remedy.type === "Prevention"
                                    ? "bg-accent/20 text-accent"
                                    : "bg-warning/20 text-warning"
                                }`}
                              >
                                {remedy.type}
                              </span>
                              <span className="font-medium text-sm">{remedy.name}</span>
                            </div>
                            <p className="text-sm text-muted-foreground">{remedy.instructions}</p>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-3 pt-4 border-t border-border/50">
                      <Button variant="trust" className="flex-1">
                        Save Report
                      </Button>
                      <Button variant="outline">Share</Button>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          </div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default DiseaseScanner;
