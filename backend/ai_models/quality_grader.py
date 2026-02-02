"""
AgroGrade AI - Dynamic Quality Grading Engine
CROP-SPECIFIC OpenCV analysis (color/size/defects)
Returns REAL metrics with pixel-level defect detection
"""

import os
import io
import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import cv2
import numpy as np
from PIL import Image

# Try to import skimage for advanced morphology
try:
    from skimage.measure import label, regionprops
    SKIMAGE_AVAILABLE = True
except ImportError:
    SKIMAGE_AVAILABLE = False
    print("⚠️ scikit-image not available - using OpenCV fallback for region analysis")


# =============================================================================
# CONFIGURATION
# =============================================================================
AI_MODELS_DIR = Path(__file__).parent
GRADING_RULES_DIR = AI_MODELS_DIR / "grading_rules"

# Market prices (2024 Gujarat APMC rates - ₹/kg or ₹/quintal for cotton)
MARKET_PRICES = {
    "tomato": {"A": 48, "B": 35, "C": 22},
    "cotton": {"A": 7500, "B": 6300, "C": 5100},  # ₹/quintal
    "wheat": {"A": 28, "B": 24, "C": 20},
    "rice": {"A": 42, "B": 35, "C": 28},
    "okra": {"A": 55, "B": 40, "C": 28},
    "potato": {"A": 25, "B": 18, "C": 12},
    "chilli": {"A": 85, "B": 65, "C": 45},
    "onion": {"A": 32, "B": 24, "C": 16},
    "groundnut": {"A": 72, "B": 58, "C": 45},
    "sugarcane": {"A": 350, "B": 310, "C": 280}  # ₹/quintal
}


# =============================================================================
# QUALITY GRADING ENGINE
# =============================================================================
class QualityGrader:
    """
    Crop-specific quality grading using real OpenCV analysis.
    
    Features:
    - Color uniformity analysis (HSV/LAB)
    - Defect detection with pixel coordinates
    - Size consistency measurement
    - Crop-specific grading rules
    - Market value estimation
    """
    
    def __init__(self):
        self.grading_rules = self._load_grading_rules()
    
    def _load_grading_rules(self) -> Dict:
        """Load all crop-specific grading rules"""
        rules = {}
        if GRADING_RULES_DIR.exists():
            for rule_file in GRADING_RULES_DIR.glob("*_rules.json"):
                crop = rule_file.stem.replace("_rules", "")
                try:
                    with open(rule_file, 'r') as f:
                        rules[crop] = json.load(f)
                except Exception as e:
                    print(f"⚠️ Failed to load {rule_file}: {e}")
        return rules
    
    def grade_produce(
        self, 
        image_bytes: bytes, 
        crop_type: str, 
        grading_rules: Optional[Dict] = None
    ) -> Dict:
        """
        CROP-SPECIFIC grading using REAL OpenCV analysis.
        
        Args:
            image_bytes: Raw image bytes
            crop_type: Detected crop type
            grading_rules: Optional crop-specific rules (or uses loaded rules)
            
        Returns:
            {crop, grade, score, metrics, defect_map, market_value, trust_tag}
        """
        start_time = time.time()
        
        # Convert bytes to OpenCV image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            return self._error_response(crop_type, "Failed to decode image")
        
        # Get grading rules
        rules = grading_rules or self.grading_rules.get(crop_type, {})
        if not rules:
            rules = self._get_default_rules(crop_type)
        
        # Crop-specific analysis
        graders = {
            "tomato": self._grade_tomato,
            "cotton": self._grade_cotton,
            "wheat": self._grade_wheat,
            "rice": self._grade_rice,
            "okra": self._grade_okra,
            "potato": self._grade_potato,
            "chilli": self._grade_chilli,
            "onion": self._grade_onion,
        }
        
        grader_func = graders.get(crop_type, self._grade_generic)
        result = grader_func(img, rules)
        
        # Assign grade based on thresholds
        score = result["overall_score"]
        thresholds = rules.get("grade_thresholds", {"A": 85, "B": 65, "C": 45})
        
        if score >= thresholds.get("A", 85):
            grade = "A"
        elif score >= thresholds.get("B", 65):
            grade = "B"
        else:
            grade = "C"
        
        # Estimate market value
        market_value = self._estimate_market_value(crop_type, grade)
        
        # Generate trust tag
        trust_tag = self._generate_trust_tag(crop_type, grade, score, result["metrics"])
        
        inference_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "crop": crop_type,
            "grade": grade,
            "score": round(score, 2),
            "metrics": result["metrics"],
            "defect_map": result.get("defect_map", []),
            "defect_count": len(result.get("defect_map", [])),
            "market_value_per_kg": market_value,
            "trust_tag": trust_tag,
            "analysis_method": result.get("method", "opencv_analysis"),
            "inference_time_ms": inference_time_ms
        }
    
    # =========================================================================
    # TOMATO GRADING
    # =========================================================================
    def _grade_tomato(self, img: np.ndarray, rules: Dict) -> Dict:
        """
        REAL tomato grading:
        - Red color uniformity (deep red = ripe)
        - Defect detection (bruises, cracks, blemishes)
        - Size consistency
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        total_pixels = img.shape[0] * img.shape[1]
        
        # 1. Red color analysis (tomato-specific red ranges)
        # Red wraps around 0 in HSV
        lower_red1 = np.array([0, 70, 50])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 70, 50])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)
        
        red_pixels = cv2.countNonZero(red_mask)
        red_coverage = (red_pixels / total_pixels) * 100
        
        # Ideal red hue range for ripe tomato
        h_channel = hsv[:, :, 0]
        red_region_hue = h_channel[red_mask > 0] if np.any(red_mask > 0) else [0]
        hue_uniformity = 100 - (np.std(red_region_hue) * 2) if len(red_region_hue) > 0 else 50
        
        # 2. Defect detection (bruises = dark spots, cracks = edges)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Detect dark spots (bruises, rot)
        _, dark_mask = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
        
        # Detect cracks using Canny edges
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 30, 100)
        
        # Combine defect masks
        defect_mask = cv2.bitwise_or(dark_mask, edges)
        defect_pixels = cv2.countNonZero(defect_mask)
        defect_ratio = (defect_pixels / total_pixels) * 100
        
        # Find defect locations
        defect_locations = self._find_defect_locations(defect_mask, min_area=50)
        
        # 3. Size analysis  
        size_score = self._analyze_size_consistency(img, "tomato")
        
        # 4. Green shoulder detection (unripe indicator)
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_ratio = (cv2.countNonZero(green_mask) / total_pixels) * 100
        
        # Calculate scores
        min_red = rules.get("min_red_hue", 0.92) * 100
        color_score = min(red_coverage / min_red * 100, 100) if min_red > 0 else red_coverage
        
        max_defect = rules.get("max_defect_area_percent", 5)
        defect_penalty = min(defect_ratio / max_defect * 40, 40) if max_defect > 0 else 0
        
        green_penalty = min(green_ratio * 2, 20)  # Penalize unripe areas
        
        overall_score = max(0, 
            (color_score * 0.45) + 
            (hue_uniformity * 0.15) + 
            (size_score * 0.20) - 
            defect_penalty - 
            green_penalty
        )
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "red_coverage_percent": round(red_coverage, 2),
                "hue_uniformity": round(max(0, hue_uniformity), 2),
                "defect_ratio_percent": round(defect_ratio, 2),
                "green_shoulder_percent": round(green_ratio, 2),
                "size_consistency_score": round(size_score, 2),
                "defect_count": len(defect_locations)
            },
            "defect_map": defect_locations,
            "method": "tomato_hsv_analysis"
        }
    
    # =========================================================================
    # COTTON GRADING
    # =========================================================================
    def _grade_cotton(self, img: np.ndarray, rules: Dict) -> Dict:
        """
        REAL cotton grading:
        - Whiteness (LAB L* channel)
        - Yellowing detection
        - Boll opening percentage
        - Foreign matter detection
        """
        # Convert to LAB for accurate whiteness measurement
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        a_channel = lab[:, :, 1]
        b_channel = lab[:, :, 2]
        
        total_pixels = img.shape[0] * img.shape[1]
        
        # 1. Whiteness score (L* channel, 0-100)
        whiteness = np.mean(l_channel) / 2.55  # Normalize to 0-100
        whiteness_std = np.std(l_channel) / 2.55
        whiteness_uniformity = 100 - whiteness_std
        
        # 2. Yellowing detection (positive b* values indicate yellow)
        yellow_pixels = np.sum(b_channel > 140)
        yellowing_percent = (yellow_pixels / total_pixels) * 100
        
        # 3. Boll opening analysis (white exposed cotton)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, white_mask = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
        
        # Clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        white_mask = cv2.morphologyEx(white_mask, cv2.MORPH_OPEN, kernel)
        
        white_pixels = cv2.countNonZero(white_mask)
        boll_opening = (white_pixels / total_pixels) * 100
        
        # 4. Foreign matter / staining detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Non-white colored areas
        lower_colored = np.array([10, 50, 50])
        upper_colored = np.array([170, 255, 200])
        colored_mask = cv2.inRange(hsv, lower_colored, upper_colored)
        foreign_matter = (cv2.countNonZero(colored_mask) / total_pixels) * 100
        
        # Find stain locations
        defect_locations = self._find_defect_locations(colored_mask, min_area=100)
        
        # Calculate scores using rules
        min_whiteness = rules.get("min_whiteness", 0.85) * 100
        max_yellowing = rules.get("max_yellowing_percent", 15)
        min_boll = rules.get("boll_opening_min", 0.7) * 100
        
        whiteness_score = min(whiteness / min_whiteness * 100, 100) if min_whiteness > 0 else whiteness
        yellowing_penalty = min(yellowing_percent / max_yellowing * 20, 20) if max_yellowing > 0 else 0
        boll_score = min(boll_opening / min_boll * 100, 100) if min_boll > 0 else boll_opening
        foreign_penalty = min(foreign_matter * 2, 25)
        
        overall_score = max(0,
            (whiteness_score * 0.40) +
            (whiteness_uniformity * 0.15) +
            (boll_score * 0.30) -
            yellowing_penalty -
            foreign_penalty
        )
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "whiteness_score": round(whiteness, 2),
                "whiteness_uniformity": round(whiteness_uniformity, 2),
                "yellowing_percent": round(yellowing_percent, 2),
                "boll_opening_percent": round(boll_opening, 2),
                "foreign_matter_percent": round(foreign_matter, 2),
                "stain_count": len(defect_locations)
            },
            "defect_map": defect_locations,
            "method": "cotton_lab_analysis"
        }
    
    # =========================================================================
    # WHEAT GRADING
    # =========================================================================
    def _grade_wheat(self, img: np.ndarray, rules: Dict) -> Dict:
        """
        REAL wheat grading:
        - Golden hue analysis
        - Grain density estimation
        - Chaff/foreign matter detection
        - Moisture indicator (color)
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        total_pixels = img.shape[0] * img.shape[1]
        
        # 1. Golden hue analysis (wheat should be golden-yellow)
        lower_golden = np.array([15, 50, 100])
        upper_golden = np.array([35, 255, 255])
        golden_mask = cv2.inRange(hsv, lower_golden, upper_golden)
        golden_pixels = cv2.countNonZero(golden_mask)
        golden_coverage = (golden_pixels / total_pixels) * 100
        
        # Analyze hue uniformity in golden regions
        h_channel = hsv[:, :, 0]
        golden_hues = h_channel[golden_mask > 0] if np.any(golden_mask > 0) else [25]
        hue_uniformity = 100 - (np.std(golden_hues) * 3) if len(golden_hues) > 0 else 50
        
        # 2. Grain density (texture analysis)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Use Laplacian variance for texture density
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        texture_variance = laplacian.var()
        grain_density = min(texture_variance / 1000 * 100, 100)  # Normalize
        
        # 3. Chaff detection (light/beige areas)
        lower_chaff = np.array([20, 20, 150])
        upper_chaff = np.array([40, 80, 255])
        chaff_mask = cv2.inRange(hsv, lower_chaff, upper_chaff)
        chaff_percent = (cv2.countNonZero(chaff_mask) / total_pixels) * 100
        
        # 4. Dark/damaged grain detection
        _, dark_mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)
        dark_percent = (cv2.countNonZero(dark_mask) / total_pixels) * 100
        
        defect_locations = self._find_defect_locations(dark_mask, min_area=30)
        
        # Calculate scores
        min_golden = rules.get("min_golden_hue", 0.75) * 100
        max_chaff = rules.get("max_chaff_percent", 8)
        min_density = rules.get("grain_density_min", 0.6) * 100
        
        golden_score = min(golden_coverage / min_golden * 100, 100) if min_golden > 0 else golden_coverage
        chaff_penalty = min(chaff_percent / max_chaff * 15, 15) if max_chaff > 0 else 0
        density_score = min(grain_density / min_density * 100, 100) if min_density > 0 else grain_density
        damage_penalty = min(dark_percent * 3, 20)
        
        overall_score = max(0,
            (golden_score * 0.35) +
            (hue_uniformity * 0.15) +
            (density_score * 0.30) -
            chaff_penalty -
            damage_penalty
        )
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "golden_coverage_percent": round(golden_coverage, 2),
                "hue_uniformity": round(max(0, hue_uniformity), 2),
                "grain_density_score": round(grain_density, 2),
                "chaff_percent": round(chaff_percent, 2),
                "damaged_grain_percent": round(dark_percent, 2),
                "damage_count": len(defect_locations)
            },
            "defect_map": defect_locations,
            "method": "wheat_hsv_texture_analysis"
        }
    
    # =========================================================================
    # RICE GRADING
    # =========================================================================
    def _grade_rice(self, img: np.ndarray, rules: Dict) -> Dict:
        """
        REAL rice grading:
        - Whiteness/translucency
        - Broken grain detection
        - Chalkiness analysis
        - Foreign matter
        """
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        total_pixels = img.shape[0] * img.shape[1]
        
        # 1. Whiteness analysis
        l_channel = lab[:, :, 0]
        whiteness = np.mean(l_channel) / 2.55
        
        # 2. Chalkiness detection (opaque white regions)
        _, chalky_mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
        chalkiness = (cv2.countNonZero(chalky_mask) / total_pixels) * 100
        
        # 3. Broken grain estimation (small contours)
        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            areas = [cv2.contourArea(c) for c in contours if cv2.contourArea(c) > 10]
            if len(areas) > 0:
                median_area = np.median(areas)
                small_grains = [a for a in areas if a < median_area * 0.4]
                broken_percent = (len(small_grains) / len(areas)) * 100
            else:
                broken_percent = 0
        else:
            broken_percent = 0
        
        # 4. Discoloration detection
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_yellow = np.array([15, 50, 100])
        upper_yellow = np.array([35, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        discoloration = (cv2.countNonZero(yellow_mask) / total_pixels) * 100
        
        # Calculate scores
        min_whiteness = rules.get("min_whiteness", 0.88) * 100
        max_broken = rules.get("max_broken_percent", 5)
        max_chalk = rules.get("chalkiness_max_percent", 8)
        
        whiteness_score = min(whiteness / min_whiteness * 100, 100)
        broken_penalty = min(broken_percent / max_broken * 20, 20) if max_broken > 0 else 0
        chalk_penalty = min(chalkiness / max_chalk * 15, 15) if max_chalk > 0 else 0
        discolor_penalty = min(discoloration * 2, 15)
        
        overall_score = max(0,
            (whiteness_score * 0.50) +
            50 -  # Base score
            broken_penalty -
            chalk_penalty -
            discolor_penalty
        )
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "whiteness_score": round(whiteness, 2),
                "chalkiness_percent": round(chalkiness, 2),
                "broken_grain_percent": round(broken_percent, 2),
                "discoloration_percent": round(discoloration, 2),
                "grain_count_estimate": len(contours)
            },
            "method": "rice_whiteness_analysis"
        }
    
    # =========================================================================
    # OKRA GRADING
    # =========================================================================
    def _grade_okra(self, img: np.ndarray, rules: Dict) -> Dict:
        """Okra grading: color, size, fibrous detection"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        total_pixels = img.shape[0] * img.shape[1]
        
        # Green color analysis
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_coverage = (cv2.countNonZero(green_mask) / total_pixels) * 100
        
        # Yellowing (overripe)
        lower_yellow = np.array([20, 50, 100])
        upper_yellow = np.array([35, 255, 255])
        yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        yellowing = (cv2.countNonZero(yellow_mask) / total_pixels) * 100
        
        # Size consistency
        size_score = self._analyze_size_consistency(img, "okra")
        
        # Calculate scores
        color_score = min(green_coverage * 1.2, 100)
        yellow_penalty = min(yellowing * 2, 25)
        
        overall_score = max(0, (color_score * 0.5) + (size_score * 0.3) - yellow_penalty)
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "green_coverage_percent": round(green_coverage, 2),
                "yellowing_percent": round(yellowing, 2),
                "size_consistency": round(size_score, 2)
            },
            "method": "okra_color_analysis"
        }
    
    # =========================================================================
    # POTATO GRADING
    # =========================================================================
    def _grade_potato(self, img: np.ndarray, rules: Dict) -> Dict:
        """Potato grading: skin quality, blemishes, sprouting"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        total_pixels = img.shape[0] * img.shape[1]
        
        # Skin smoothness (low edge density = smoother)
        edges = cv2.Canny(gray, 30, 100)
        edge_density = (cv2.countNonZero(edges) / total_pixels) * 100
        smoothness = max(0, 100 - edge_density * 3)
        
        # Blemish detection (dark spots)
        _, dark_mask = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
        blemish_percent = (cv2.countNonZero(dark_mask) / total_pixels) * 100
        
        # Green spots (solanine - toxic)
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 200])
        green_mask = cv2.inRange(hsv, lower_green, upper_green)
        green_percent = (cv2.countNonZero(green_mask) / total_pixels) * 100
        
        defect_locations = self._find_defect_locations(
            cv2.bitwise_or(dark_mask, green_mask), min_area=80
        )
        
        # Calculate scores
        smoothness_score = smoothness * 0.4
        blemish_penalty = min(blemish_percent / 8 * 25, 25)
        green_penalty = min(green_percent * 5, 30)  # Heavy penalty for green
        
        overall_score = max(0, 70 + smoothness_score - blemish_penalty - green_penalty)
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "skin_smoothness": round(smoothness, 2),
                "blemish_percent": round(blemish_percent, 2),
                "green_spots_percent": round(green_percent, 2),
                "defect_count": len(defect_locations)
            },
            "defect_map": defect_locations,
            "method": "potato_surface_analysis"
        }
    
    # =========================================================================
    # CHILLI GRADING
    # =========================================================================
    def _grade_chilli(self, img: np.ndarray, rules: Dict) -> Dict:
        """Chilli grading: color intensity, blemishes"""
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        total_pixels = img.shape[0] * img.shape[1]
        
        # Red color intensity
        lower_red1 = np.array([0, 100, 100])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([160, 100, 100])
        upper_red2 = np.array([180, 255, 255])
        
        red_mask = cv2.bitwise_or(
            cv2.inRange(hsv, lower_red1, upper_red1),
            cv2.inRange(hsv, lower_red2, upper_red2)
        )
        red_coverage = (cv2.countNonZero(red_mask) / total_pixels) * 100
        
        # Saturation analysis (vibrant = higher quality)
        s_channel = hsv[:, :, 1]
        saturation = np.mean(s_channel) / 2.55
        
        # Size consistency
        size_score = self._analyze_size_consistency(img, "chilli")
        
        color_score = min(red_coverage * 1.1, 100)
        sat_bonus = saturation * 0.3
        
        overall_score = max(0, (color_score * 0.5) + sat_bonus + (size_score * 0.2))
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "red_coverage_percent": round(red_coverage, 2),
                "color_saturation": round(saturation, 2),
                "size_consistency": round(size_score, 2)
            },
            "method": "chilli_color_analysis"
        }
    
    # =========================================================================
    # ONION GRADING
    # =========================================================================
    def _grade_onion(self, img: np.ndarray, rules: Dict) -> Dict:
        """Onion grading: skin integrity, sprouting, firmness indicators"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        total_pixels = img.shape[0] * img.shape[1]
        
        # Skin color uniformity (reddish-brown to golden)
        lower_onion = np.array([5, 50, 50])
        upper_onion = np.array([25, 255, 255])
        color_mask = cv2.inRange(hsv, lower_onion, upper_onion)
        color_coverage = (cv2.countNonZero(color_mask) / total_pixels) * 100
        
        # Sprouting detection (green shoots)
        lower_green = np.array([35, 50, 50])
        upper_green = np.array([85, 255, 255])
        sprout_mask = cv2.inRange(hsv, lower_green, upper_green)
        sprouting = (cv2.countNonZero(sprout_mask) / total_pixels) * 100
        
        # Surface damage
        edges = cv2.Canny(gray, 50, 150)
        damage_ratio = (cv2.countNonZero(edges) / total_pixels) * 100
        
        color_score = min(color_coverage * 1.2, 100)
        sprout_penalty = min(sprouting * 4, 30)
        damage_penalty = min(damage_ratio * 1.5, 20)
        
        overall_score = max(0, (color_score * 0.6) - sprout_penalty - damage_penalty + 30)
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "skin_color_coverage": round(color_coverage, 2),
                "sprouting_percent": round(sprouting, 2),
                "surface_damage_indicator": round(damage_ratio, 2)
            },
            "method": "onion_surface_analysis"
        }
    
    # =========================================================================
    # GENERIC GRADING (FALLBACK)
    # =========================================================================
    def _grade_generic(self, img: np.ndarray, rules: Dict) -> Dict:
        """Generic grading for unknown crops"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Color uniformity
        h_std = np.std(hsv[:, :, 0])
        color_uniformity = max(0, 100 - h_std * 2)
        
        # Defect detection
        edges = cv2.Canny(gray, 50, 150)
        defect_ratio = cv2.countNonZero(edges) / (img.shape[0] * img.shape[1]) * 100
        
        overall_score = max(0, color_uniformity - defect_ratio)
        
        return {
            "overall_score": overall_score,
            "metrics": {
                "color_uniformity": round(color_uniformity, 2),
                "defect_indicator": round(defect_ratio, 2)
            },
            "method": "generic_analysis"
        }
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    def _find_defect_locations(
        self, 
        mask: np.ndarray, 
        min_area: int = 50
    ) -> List[Dict]:
        """Find bounding boxes of defect regions"""
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        defects = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > min_area:
                x, y, w, h = cv2.boundingRect(cnt)
                defects.append({
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "area_px": int(area)
                })
        
        return defects[:20]  # Limit to 20 defects
    
    def _analyze_size_consistency(self, img: np.ndarray, crop: str) -> float:
        """Analyze size uniformity of produce items"""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) < 2:
            return 75.0  # Single item or not enough for comparison
        
        areas = [cv2.contourArea(cnt) for cnt in contours if cv2.contourArea(cnt) > 100]
        
        if len(areas) < 2:
            return 70.0
        
        mean_area = np.mean(areas)
        std_area = np.std(areas)
        cv_area = (std_area / mean_area) * 100 if mean_area > 0 else 100
        
        # Lower coefficient of variation = more uniform = higher score
        size_score = max(0, 100 - cv_area * 1.5)
        return size_score
    
    def _estimate_market_value(self, crop: str, grade: str) -> float:
        """Estimate ₹/kg based on crop and grade"""
        prices = MARKET_PRICES.get(crop, {"A": 30, "B": 22, "C": 15})
        price = prices.get(grade, prices.get("C", 15))
        
        # Convert quintal to kg for cotton/sugarcane
        if crop in ["cotton", "sugarcane"]:
            price = price / 100
        
        return round(price, 2)
    
    def _generate_trust_tag(
        self, 
        crop: str, 
        grade: str, 
        score: float, 
        metrics: Dict
    ) -> Dict:
        """Generate AgroGrade Trust Tag for marketplace"""
        return {
            "grade": grade,
            "score": round(score, 1),
            "verified": True,
            "verification_method": "ai_opencv_analysis",
            "crop_type": crop,
            "key_metrics": {
                k: v for k, v in list(metrics.items())[:3]  # Top 3 metrics
            },
            "tag_id": f"AG-{crop[:3].upper()}-{grade}-{int(time.time()) % 100000}"
        }
    
    def _get_default_rules(self, crop: str) -> Dict:
        """Get default grading rules for a crop"""
        defaults = {
            "tomato": {"min_red_hue": 0.92, "max_defect_area_percent": 5, "grade_thresholds": {"A": 85, "B": 65, "C": 45}},
            "cotton": {"min_whiteness": 0.85, "max_yellowing_percent": 15, "boll_opening_min": 0.7, "grade_thresholds": {"A": 85, "B": 65, "C": 45}},
            "wheat": {"min_golden_hue": 0.75, "max_chaff_percent": 8, "grain_density_min": 0.6, "grade_thresholds": {"A": 90, "B": 70, "C": 50}},
            "rice": {"min_whiteness": 0.88, "max_broken_percent": 5, "chalkiness_max_percent": 8, "grade_thresholds": {"A": 88, "B": 68, "C": 48}},
        }
        return defaults.get(crop, {"grade_thresholds": {"A": 80, "B": 60, "C": 40}})
    
    def _error_response(self, crop: str, error: str) -> Dict:
        """Return error response"""
        return {
            "crop": crop,
            "grade": "N/A",
            "score": 0,
            "metrics": {},
            "error": error
        }


# =============================================================================
# SINGLETON & CONVENIENCE FUNCTIONS
# =============================================================================
_grader_instance: Optional[QualityGrader] = None

def get_quality_grader() -> QualityGrader:
    """Get singleton QualityGrader instance"""
    global _grader_instance
    if _grader_instance is None:
        _grader_instance = QualityGrader()
    return _grader_instance


def grade_produce(
    image_bytes: bytes, 
    crop_type: str, 
    grading_rules: Optional[Dict] = None
) -> Dict:
    """
    Convenience function for quality grading.
    
    Usage:
        from ai_models.quality_grader import grade_produce
        result = grade_produce(image_bytes, "tomato")
    """
    grader = get_quality_grader()
    return grader.grade_produce(image_bytes, crop_type, grading_rules)
