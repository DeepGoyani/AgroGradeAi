import { useState, useCallback } from "react";
import { motion, AnimatePresence } from "framer-motion";
import Header from "@/components/layout/Header";
import Footer from "@/components/layout/Footer";
import { Button } from "@/components/ui/button";
import { Upload, Award, Star, CheckCircle, Package, RefreshCw, Shield, Palette, Ruler, Sparkles } from "lucide-react";
import freshProduce from "@/assets/fresh-produce.jpg";

// Mock grading results
const mockGrades = [
  {
    grade: "A",
    score: 92,
    label: "Premium Quality",
    color: "success",
    details: {
      colorUniformity: 95,
      sizeDistribution: 88,
      surfaceQuality: 93,
      freshness: 92,
    },
    trustScore: 94,
    priceMultiplier: 1.4,
  },
  {
    grade: "B",
    score: 75,
    label: "Standard Quality",
    color: "warning",
    details: {
      colorUniformity: 78,
      sizeDistribution: 72,
      surfaceQuality: 76,
      freshness: 74,
    },
    trustScore: 78,
    priceMultiplier: 1.15,
  },
  {
    grade: "C",
    score: 58,
    label: "Economy Quality",
    color: "destructive",
    details: {
      colorUniformity: 55,
      sizeDistribution: 60,
      surfaceQuality: 58,
      freshness: 59,
    },
    trustScore: 62,
    priceMultiplier: 0.9,
  },
];

const QualityGrader = () => {
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [isGrading, setIsGrading] = useState(false);
  const [gradeResult, setGradeResult] = useState<typeof mockGrades[0] | null>(null);
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
      setGradeResult(null);
    };
    reader.readAsDataURL(file);
  };

  const handleGrade = () => {
    setIsGrading(true);
    setTimeout(() => {
      // Weighted random for demo (higher chance of Grade A)
      const rand = Math.random();
      const result = rand > 0.6 ? mockGrades[0] : rand > 0.3 ? mockGrades[1] : mockGrades[2];
      setGradeResult(result);
      setIsGrading(false);
    }, 3000);
  };

  const handleReset = () => {
    setUploadedImage(null);
    setGradeResult(null);
    setIsGrading(false);
  };

  const useSampleImage = () => {
    setUploadedImage(freshProduce);
    setGradeResult(null);
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
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-warning/10 border border-warning/30 mb-4">
              <Award className="w-4 h-4 text-warning" />
              <span className="text-warning text-sm font-medium">AI Quality Certification</span>
            </div>
            <h1 className="font-display text-3xl md:text-4xl lg:text-5xl font-bold mb-4">
              Quality Grader
            </h1>
            <p className="text-muted-foreground text-lg">
              Upload a photo of your harvest and receive AI-verified quality certification with Trust Tag.
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
                <Package className="w-5 h-5 text-accent" />
                Upload Harvest Image
              </h2>

              {!uploadedImage ? (
                <>
                  <div
                    className={`relative border-2 border-dashed rounded-xl p-12 text-center transition-all ${
                      dragActive
                        ? "border-warning bg-warning/10"
                        : "border-border hover:border-warning/50"
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
                      Drag & drop your harvest pile image
                    </p>
                    <p className="text-sm text-muted-foreground">
                      or click to browse • PNG, JPG up to 10MB
                    </p>
                  </div>

                  <div className="mt-6">
                    <p className="text-sm text-muted-foreground mb-3">Or try with sample:</p>
                    <button
                      onClick={useSampleImage}
                      className="w-full group relative rounded-xl overflow-hidden aspect-video"
                    >
                      <img
                        src={freshProduce}
                        alt="Fresh produce sample"
                        className="w-full h-full object-cover group-hover:scale-105 transition-transform"
                      />
                      <div className="absolute inset-0 bg-gradient-to-t from-background/80 to-transparent flex items-end p-4">
                        <span className="text-sm font-medium">Fresh Vegetables</span>
                      </div>
                    </button>
                  </div>
                </>
              ) : (
                <div className="space-y-4">
                  <div className="relative rounded-xl overflow-hidden aspect-video">
                    <img
                      src={uploadedImage}
                      alt="Uploaded harvest"
                      className="w-full h-full object-cover"
                    />
                    {isGrading && (
                      <div className="absolute inset-0 bg-background/50 flex items-center justify-center">
                        <div className="text-center">
                          <div className="w-20 h-20 mx-auto border-4 border-warning/30 border-t-warning rounded-full animate-spin mb-4" />
                          <p className="text-warning font-medium">Analyzing Quality...</p>
                        </div>
                      </div>
                    )}
                  </div>

                  <div className="flex gap-3">
                    <Button
                      variant="gold"
                      className="flex-1"
                      onClick={handleGrade}
                      disabled={isGrading}
                    >
                      {isGrading ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin" />
                          Grading...
                        </>
                      ) : (
                        <>
                          <Award className="w-4 h-4" />
                          Grade Quality
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
                <Star className="w-5 h-5 text-warning" />
                Grading Result
              </h2>

              <AnimatePresence mode="wait">
                {!gradeResult ? (
                  <motion.div
                    key="empty"
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    exit={{ opacity: 0 }}
                    className="h-[400px] flex items-center justify-center text-center"
                  >
                    <div>
                      <div className="w-20 h-20 mx-auto rounded-full bg-secondary flex items-center justify-center mb-4">
                        <Award className="w-10 h-10 text-muted-foreground" />
                      </div>
                      <p className="text-muted-foreground">
                        Upload a harvest image and click "Grade Quality" to get AI certification
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
                    {/* Grade Badge */}
                    <div className="text-center py-6">
                      <motion.div
                        initial={{ scale: 0 }}
                        animate={{ scale: 1 }}
                        transition={{ type: "spring", stiffness: 200, delay: 0.2 }}
                        className={`w-32 h-32 mx-auto rounded-full ${getGradeClass(gradeResult.grade)} flex items-center justify-center shadow-lg`}
                      >
                        <div>
                          <div className="text-5xl font-bold">
                            {gradeResult.grade}
                          </div>
                          <div className="text-sm opacity-80">Grade</div>
                        </div>
                      </motion.div>
                      <h3 className="font-display text-2xl font-semibold mt-4">
                        {gradeResult.label}
                      </h3>
                      <p className="text-muted-foreground">
                        Overall Score: {gradeResult.score}/100
                      </p>
                    </div>

                    {/* Quality Breakdown */}
                    <div className="space-y-3">
                      <h4 className="font-semibold flex items-center gap-2">
                        <Sparkles className="w-4 h-4 text-accent" />
                        Quality Breakdown
                      </h4>
                      {[
                        { icon: Palette, label: "Color Uniformity", value: gradeResult.details.colorUniformity },
                        { icon: Ruler, label: "Size Distribution", value: gradeResult.details.sizeDistribution },
                        { icon: CheckCircle, label: "Surface Quality", value: gradeResult.details.surfaceQuality },
                        { icon: Star, label: "Freshness Index", value: gradeResult.details.freshness },
                      ].map((item) => (
                        <div key={item.label} className="flex items-center gap-3">
                          <item.icon className="w-4 h-4 text-muted-foreground" />
                          <span className="text-sm flex-1">{item.label}</span>
                          <div className="w-24 h-2 bg-secondary rounded-full overflow-hidden">
                            <motion.div
                              initial={{ width: 0 }}
                              animate={{ width: `${item.value}%` }}
                              transition={{ delay: 0.5, duration: 0.8 }}
                              className="h-full bg-accent rounded-full"
                            />
                          </div>
                          <span className="text-sm font-medium w-10 text-right">{item.value}%</span>
                        </div>
                      ))}
                    </div>

                    {/* Trust Tag Preview */}
                    <div className="p-4 rounded-xl bg-gradient-to-br from-accent/10 to-success/10 border border-accent/30">
                      <div className="flex items-center gap-3">
                        <div className="w-12 h-12 rounded-xl bg-accent/20 flex items-center justify-center">
                          <Shield className="w-6 h-6 text-accent" />
                        </div>
                        <div className="flex-1">
                          <div className="font-semibold">Trust Tag Generated</div>
                          <div className="text-sm text-muted-foreground">
                            Trust Score: {gradeResult.trustScore} • {gradeResult.priceMultiplier}x Price Multiplier
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex gap-3 pt-4 border-t border-border/50">
                      <Button variant="trust" className="flex-1">
                        <Shield className="w-4 h-4" />
                        Get Trust Tag
                      </Button>
                      <Button variant="outline">List to Market</Button>
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

export default QualityGrader;
