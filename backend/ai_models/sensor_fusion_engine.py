"""
AgroGrade AI - Dynamic Sensor Fusion Engine
Combines visual grading + REAL IoT sensor data to calculate Trust Score
Validates sensor data against crop-specific agronomic thresholds
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


# =============================================================================
# CROP-SPECIFIC AGRONOMIC THRESHOLDS
# =============================================================================

# Optimal moisture ranges (% soil moisture)
MOISTURE_RANGES = {
    "cotton": (55, 75),
    "wheat": (60, 80),
    "rice": (80, 95),  # Paddy requires high moisture
    "tomato": (65, 85),
    "okra": (60, 75),
    "potato": (65, 80),
    "chilli": (60, 75),
    "onion": (55, 70),
    "groundnut": (50, 65),
    "sugarcane": (70, 85)
}

# Ideal NPK requirements (kg/ha basis)
IDEAL_NPK = {
    "cotton": {"n": 120, "p": 60, "k": 60},
    "wheat": {"n": 150, "p": 60, "k": 40},
    "rice": {"n": 100, "p": 50, "k": 40},
    "tomato": {"n": 150, "p": 80, "k": 120},
    "okra": {"n": 100, "p": 50, "k": 50},
    "potato": {"n": 150, "p": 100, "k": 150},
    "chilli": {"n": 120, "p": 60, "k": 80},
    "onion": {"n": 100, "p": 80, "k": 60},
    "groundnut": {"n": 25, "p": 75, "k": 40},  # Legume - fixes own N
    "sugarcane": {"n": 250, "p": 100, "k": 125}
}

# Optimal pH ranges
PH_RANGES = {
    "cotton": (6.0, 7.5),
    "wheat": (6.0, 7.0),
    "rice": (5.5, 6.5),
    "tomato": (6.0, 6.8),
    "okra": (6.5, 7.0),
    "potato": (5.0, 6.0),  # Prefers acidic
    "chilli": (6.0, 7.0),
    "onion": (6.0, 7.0),
    "groundnut": (5.5, 6.5),
    "sugarcane": (6.0, 7.5)
}

# Optimal temperature ranges (°C)
TEMP_RANGES = {
    "cotton": (25, 35),
    "wheat": (15, 25),
    "rice": (25, 35),
    "tomato": (20, 30),
    "okra": (25, 35),
    "potato": (15, 25),
    "chilli": (25, 35),
    "onion": (15, 25),
    "groundnut": (25, 35),
    "sugarcane": (25, 38)
}


# =============================================================================
# SENSOR FUSION ENGINE
# =============================================================================
class SensorFusionEngine:
    """
    Combines visual AI grading with IoT sensor data to calculate Trust Score.
    
    Features:
    - Crop-specific agronomic threshold validation
    - Dynamic insight generation based on actual readings
    - Penalty/bonus calculation for abnormal conditions
    - Market readiness assessment
    """
    
    def __init__(self):
        self.last_fusion_time = None
    
    def calculate_trust_score(
        self,
        visual_grade: Dict,
        sensor_data: Optional[Dict] = None
    ) -> Dict:
        """
        REAL sensor fusion to calculate Trust Score.
        
        Args:
            visual_grade: Result from quality_grader.grade_produce()
            sensor_data: Optional IoT sensor readings {moisture, npk, ph, temperature, humidity}
            
        Returns:
            {trust_score, components, insights, market_ready, recommended_actions, ...}
        """
        start_time = time.time()
        
        crop = visual_grade.get("crop", "unknown")
        visual_score = visual_grade.get("score", 50)
        grade = visual_grade.get("grade", "C")
        
        # Initialize scores
        sensor_health = 70.0
        moisture_score = 70.0
        npk_score = 70.0
        ph_score = 70.0
        temp_score = 70.0
        insights: List[Dict] = []
        sensor_readings = {}
        
        # Process sensor data if available
        if sensor_data:
            # Validate and score moisture
            moisture = sensor_data.get("moisture", sensor_data.get("soil_moisture", 60))
            moisture_score = self._score_moisture(moisture, crop)
            sensor_readings["moisture"] = moisture
            
            # Validate and score NPK
            npk = sensor_data.get("npk", {})
            if npk:
                npk_score = self._score_npk(npk, crop)
                sensor_readings["npk"] = npk
            
            # Validate pH if available
            ph = sensor_data.get("ph", sensor_data.get("soil_ph"))
            if ph is not None:
                ph_score = self._score_ph(ph, crop)
                sensor_readings["ph"] = ph
            
            # Validate temperature if available
            temp = sensor_data.get("temperature", sensor_data.get("temp"))
            if temp is not None:
                temp_score = self._score_temperature(temp, crop)
                sensor_readings["temperature"] = temp
            
            # Calculate overall sensor health
            sensor_health = self._calculate_sensor_health(
                moisture_score, npk_score, ph_score, temp_score
            )
            
            # Generate dynamic insights
            insights = self._generate_sensor_insights(
                sensor_readings, crop, 
                moisture_score, npk_score, ph_score, temp_score
            )
        else:
            insights.append({
                "type": "info",
                "message": "📡 No sensor data available. Trust score based on visual analysis only.",
                "impact": "neutral"
            })
        
        # Calculate final Trust Score with crop-aware weighting
        visual_weight, sensor_weight = self._get_weights(crop, grade)
        
        trust_score = (visual_score * visual_weight) + (sensor_health * sensor_weight)
        
        # Apply penalties for critical issues
        trust_score, penalty_insights = self._apply_critical_penalties(
            trust_score, sensor_readings, crop
        )
        insights.extend(penalty_insights)
        
        # Apply bonuses for excellent conditions
        trust_score, bonus_insights = self._apply_bonuses(
            trust_score, sensor_readings, visual_score, crop
        )
        insights.extend(bonus_insights)
        
        # Clamp score
        trust_score = max(0, min(100, trust_score))
        
        # Market readiness assessment
        market_ready = trust_score >= 75
        market_tier = self._determine_market_tier(trust_score)
        
        # Generate recommended actions
        actions = self._generate_actions(trust_score, insights, crop, grade)
        
        self.last_fusion_time = time.time()
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return {
            "trust_score": round(trust_score, 1),
            "grade": grade,
            "components": {
                "visual_grade_score": round(visual_score, 1),
                "sensor_health_score": round(sensor_health, 1),
                "moisture_score": round(moisture_score, 1),
                "npk_score": round(npk_score, 1),
                "ph_score": round(ph_score, 1),
                "temperature_score": round(temp_score, 1),
                "weights": {
                    "visual": round(visual_weight, 2),
                    "sensor": round(sensor_weight, 2)
                }
            },
            "sensor_readings": sensor_readings,
            "insights": insights,
            "market_ready": market_ready,
            "market_tier": market_tier,
            "recommended_actions": actions,
            "timestamp": datetime.now().isoformat(),
            "processing_time_ms": processing_time_ms
        }
    
    # =========================================================================
    # SCORING FUNCTIONS
    # =========================================================================
    def _score_moisture(self, moisture: float, crop: str) -> float:
        """Score moisture against crop-specific optimal ranges"""
        low, high = MOISTURE_RANGES.get(crop, (50, 70))
        
        if moisture < low:
            # Drought stress - linear penalty
            if moisture < low * 0.5:
                return max(0, 20)  # Severe drought
            penalty = ((low - moisture) / low) * 60
            return max(0, 100 - penalty)
        elif moisture > high:
            # Waterlogging risk - steeper penalty
            if moisture > 95:
                return max(0, 25)  # Severe waterlogging
            penalty = ((moisture - high) / (100 - high)) * 50
            return max(0, 100 - penalty)
        else:
            # Optimal range - full score
            return 100.0
    
    def _score_npk(self, npk: Dict, crop: str) -> float:
        """Score NPK balance against crop requirements"""
        ideal = IDEAL_NPK.get(crop, {"n": 120, "p": 60, "k": 60})
        
        # Get actual values (handle various input formats)
        n_actual = npk.get("n", npk.get("nitrogen", 0))
        p_actual = npk.get("p", npk.get("phosphorus", 0))
        k_actual = npk.get("k", npk.get("potassium", 0))
        
        # Calculate deviation from ideal (as percentage)
        n_dev = abs(n_actual - ideal["n"]) / ideal["n"] if ideal["n"] > 0 else 0
        p_dev = abs(p_actual - ideal["p"]) / ideal["p"] if ideal["p"] > 0 else 0
        k_dev = abs(k_actual - ideal["k"]) / ideal["k"] if ideal["k"] > 0 else 0
        
        # Weighted average deviation (N is most critical)
        avg_dev = (n_dev * 0.4) + (p_dev * 0.3) + (k_dev * 0.3)
        
        # Convert to score (lower deviation = higher score)
        score = max(0, 100 - (avg_dev * 120))
        return score
    
    def _score_ph(self, ph: float, crop: str) -> float:
        """Score soil pH against crop-specific requirements"""
        low, high = PH_RANGES.get(crop, (6.0, 7.0))
        
        if ph < low:
            # Too acidic
            penalty = ((low - ph) / low) * 80
            return max(0, 100 - penalty)
        elif ph > high:
            # Too alkaline
            penalty = ((ph - high) / (14 - high)) * 80
            return max(0, 100 - penalty)
        else:
            return 100.0
    
    def _score_temperature(self, temp: float, crop: str) -> float:
        """Score temperature against crop requirements"""
        low, high = TEMP_RANGES.get(crop, (20, 35))
        
        if temp < low:
            # Cold stress
            if temp < 5:
                return 10  # Frost damage risk
            penalty = ((low - temp) / low) * 60
            return max(0, 100 - penalty)
        elif temp > high:
            # Heat stress
            if temp > 45:
                return 15  # Extreme heat
            penalty = ((temp - high) / (50 - high)) * 60
            return max(0, 100 - penalty)
        else:
            return 100.0
    
    def _calculate_sensor_health(
        self,
        moisture_score: float,
        npk_score: float,
        ph_score: float,
        temp_score: float
    ) -> float:
        """Calculate overall sensor health with weighted average"""
        # Weights based on impact on crop quality
        weights = {
            "moisture": 0.35,
            "npk": 0.30,
            "ph": 0.20,
            "temp": 0.15
        }
        
        health = (
            moisture_score * weights["moisture"] +
            npk_score * weights["npk"] +
            ph_score * weights["ph"] +
            temp_score * weights["temp"]
        )
        
        return health
    
    def _get_weights(self, crop: str, grade: str) -> tuple:
        """Get visual/sensor weights based on crop type and grade"""
        # Harvest-stage crops: visual weight higher (quality is visible)
        # Growing-stage crops: sensor weight higher (conditions matter more)
        
        harvest_crops = ["tomato", "cotton", "chilli", "okra", "onion"]
        
        if crop in harvest_crops:
            visual_weight = 0.65
        else:
            visual_weight = 0.55
        
        # Adjust based on grade (poor grades need more sensor context)
        if grade == "C":
            visual_weight -= 0.05  # Give more weight to sensor data
        elif grade == "A":
            visual_weight += 0.05  # Trust visual analysis more
        
        sensor_weight = 1.0 - visual_weight
        
        return visual_weight, sensor_weight
    
    # =========================================================================
    # INSIGHT GENERATION
    # =========================================================================
    def _generate_sensor_insights(
        self,
        readings: Dict,
        crop: str,
        moisture_score: float,
        npk_score: float,
        ph_score: float,
        temp_score: float
    ) -> List[Dict]:
        """Generate DYNAMIC, actionable insights based on REAL sensor values"""
        insights = []
        
        # Moisture insights
        moisture = readings.get("moisture")
        if moisture is not None:
            low, high = MOISTURE_RANGES.get(crop, (50, 70))
            
            if moisture_score < 40:
                insights.append({
                    "type": "alert",
                    "message": f"💧 LOW MOISTURE: {moisture}% (optimal: {low}-{high}% for {crop}). Irrigate within 12 hours.",
                    "impact": "negative",
                    "severity": "high"
                })
            elif moisture_score < 60:
                insights.append({
                    "type": "warning",
                    "message": f"💧 MOISTURE STRESS: {moisture}% (optimal: {low}-{high}%). Plan irrigation soon.",
                    "impact": "negative",
                    "severity": "medium"
                })
            elif moisture > high + 10:
                insights.append({
                    "type": "alert",
                    "message": f"💧 EXCESS MOISTURE: {moisture}% (optimal: {low}-{high}%). Risk of root rot - improve drainage.",
                    "impact": "negative",
                    "severity": "high"
                })
            else:
                insights.append({
                    "type": "success",
                    "message": f"💧 Moisture optimal at {moisture}%",
                    "impact": "positive",
                    "severity": "low"
                })
        
        # NPK insights
        npk = readings.get("npk", {})
        if npk and npk_score < 60:
            ideal = IDEAL_NPK.get(crop, {"n": 120, "p": 60, "k": 60})
            
            n_actual = npk.get("n", npk.get("nitrogen", 0))
            p_actual = npk.get("p", npk.get("phosphorus", 0))
            k_actual = npk.get("k", npk.get("potassium", 0))
            
            issues = []
            if n_actual < ideal["n"] * 0.6:
                issues.append("Nitrogen deficient")
            elif n_actual > ideal["n"] * 1.4:
                issues.append("Nitrogen excess")
                
            if p_actual < ideal["p"] * 0.6:
                issues.append("Phosphorus deficient")
            elif p_actual > ideal["p"] * 1.4:
                issues.append("Phosphorus excess")
                
            if k_actual < ideal["k"] * 0.6:
                issues.append("Potassium deficient")
            elif k_actual > ideal["k"] * 1.4:
                issues.append("Potassium excess")
            
            if issues:
                insights.append({
                    "type": "warning",
                    "message": f"🧪 NPK IMBALANCE: {', '.join(issues)}. Apply balanced fertilizer based on soil test.",
                    "impact": "negative",
                    "severity": "medium",
                    "current_npk": {"N": n_actual, "P": p_actual, "K": k_actual},
                    "ideal_npk": ideal
                })
        elif npk and npk_score >= 80:
            insights.append({
                "type": "success",
                "message": "🧪 NPK levels well-balanced for optimal growth",
                "impact": "positive",
                "severity": "low"
            })
        
        # pH insights
        ph = readings.get("ph")
        if ph is not None and ph_score < 70:
            low, high = PH_RANGES.get(crop, (6.0, 7.0))
            
            if ph < low:
                insights.append({
                    "type": "warning",
                    "message": f"🔬 SOIL TOO ACIDIC: pH {ph} (optimal: {low}-{high} for {crop}). Apply agricultural lime.",
                    "impact": "negative",
                    "severity": "medium"
                })
            else:
                insights.append({
                    "type": "warning",
                    "message": f"🔬 SOIL TOO ALKALINE: pH {ph} (optimal: {low}-{high}). Apply sulfur or gypsum.",
                    "impact": "negative",
                    "severity": "medium"
                })
        
        # Temperature insights
        temp = readings.get("temperature")
        if temp is not None:
            low, high = TEMP_RANGES.get(crop, (20, 35))
            
            if temp_score < 50:
                if temp < low:
                    insights.append({
                        "type": "alert",
                        "message": f"🌡️ COLD STRESS: {temp}°C (optimal: {low}-{high}°C). Protect crops from frost.",
                        "impact": "negative",
                        "severity": "high"
                    })
                else:
                    insights.append({
                        "type": "alert",
                        "message": f"🌡️ HEAT STRESS: {temp}°C (optimal: {low}-{high}°C). Apply shade net or increase irrigation.",
                        "impact": "negative",
                        "severity": "high"
                    })
        
        return insights
    
    def _apply_critical_penalties(
        self,
        trust_score: float,
        readings: Dict,
        crop: str
    ) -> tuple:
        """Apply penalties for critical conditions"""
        insights = []
        moisture = readings.get("moisture")
        
        if moisture is not None:
            if moisture < 25:
                trust_score *= 0.80  # Severe drought - 20% penalty
                insights.append({
                    "type": "critical",
                    "message": f"⚠️ SEVERE DROUGHT: Soil moisture {moisture}%. Immediate irrigation required!",
                    "impact": "very_negative",
                    "penalty_applied": "20%"
                })
            elif moisture > 92:
                trust_score *= 0.85  # Severe waterlogging - 15% penalty
                insights.append({
                    "type": "critical",
                    "message": f"⚠️ WATERLOGGING RISK: Soil moisture {moisture}%. Arrange drainage immediately.",
                    "impact": "very_negative",
                    "penalty_applied": "15%"
                })
        
        # Temperature critical conditions
        temp = readings.get("temperature")
        if temp is not None:
            if temp < 5:
                trust_score *= 0.75  # Frost damage risk
                insights.append({
                    "type": "critical",
                    "message": f"🥶 FROST ALERT: Temperature {temp}°C. Cover crops immediately!",
                    "impact": "very_negative",
                    "penalty_applied": "25%"
                })
            elif temp > 45:
                trust_score *= 0.80  # Extreme heat
                insights.append({
                    "type": "critical",
                    "message": f"🔥 EXTREME HEAT: Temperature {temp}°C. Increase irrigation frequency.",
                    "impact": "very_negative",
                    "penalty_applied": "20%"
                })
        
        return trust_score, insights
    
    def _apply_bonuses(
        self,
        trust_score: float,
        readings: Dict,
        visual_score: float,
        crop: str
    ) -> tuple:
        """Apply bonuses for excellent conditions"""
        insights = []
        
        # All-round excellent conditions bonus
        if visual_score >= 85 and readings:
            moisture = readings.get("moisture")
            if moisture:
                low, high = MOISTURE_RANGES.get(crop, (50, 70))
                mid = (low + high) / 2
                
                # Perfect moisture (within 5% of middle of optimal range)
                if abs(moisture - mid) < 5:
                    trust_score *= 1.05  # 5% bonus
                    insights.append({
                        "type": "bonus",
                        "message": f"⭐ EXCELLENT CONDITIONS: Visual quality + optimal moisture. Premium grade!",
                        "impact": "very_positive",
                        "bonus_applied": "5%"
                    })
        
        return trust_score, insights
    
    def _determine_market_tier(self, trust_score: float) -> str:
        """Determine market tier based on trust score"""
        if trust_score >= 90:
            return "premium"
        elif trust_score >= 80:
            return "export_quality"
        elif trust_score >= 70:
            return "grade_a_domestic"
        elif trust_score >= 55:
            return "grade_b_local"
        else:
            return "processing_only"
    
    def _generate_actions(
        self,
        trust_score: float,
        insights: List[Dict],
        crop: str,
        grade: str
    ) -> List[str]:
        """Generate context-aware recommended actions"""
        actions = []
        
        has_critical = any(i.get("type") == "critical" for i in insights)
        has_alerts = any(i.get("type") == "alert" for i in insights)
        
        if trust_score < 55:
            actions.append("❌ NOT MARKET READY: Address critical issues before listing")
            if has_critical:
                actions.append("→ Resolve CRITICAL alerts immediately (see insights above)")
            actions.append(f"→ Re-scan after 48-72 hours of remediation")
            actions.append("→ Consider for processing/local sale only")
            
        elif trust_score < 70:
            actions.append("⚠️ CONDITIONAL LISTING: Accept local buyers with inspection")
            if has_alerts:
                actions.append("→ Address sensor alerts to improve score")
            actions.append("→ Price 15-20% below Grade A market rate")
            actions.append("→ Target local mandis within 25km")
            
        elif trust_score < 80:
            actions.append("✅ MARKET READY: List at standard market rate")
            actions.append("→ Target buyers within 50km radius")
            if grade == "A":
                actions.append("→ Highlight visual Grade A in listing")
                
        else:
            actions.append("🌟 PREMIUM QUALITY: List at premium price (+10-15%)")
            actions.append("→ Target export buyers and urban supermarkets")
            if crop == "tomato":
                actions.append("→ Highlight 'Same-day harvest' for freshness premium")
            elif crop == "cotton":
                actions.append("→ Highlight 'Superior lint quality' for textile buyers")
            actions.append("→ Consider direct B2B sales for better margins")
        
        return actions


# =============================================================================
# SINGLETON & CONVENIENCE FUNCTIONS
# =============================================================================
_engine_instance: Optional[SensorFusionEngine] = None

def get_sensor_fusion_engine() -> SensorFusionEngine:
    """Get singleton SensorFusionEngine instance"""
    global _engine_instance
    if _engine_instance is None:
        _engine_instance = SensorFusionEngine()
    return _engine_instance


def calculate_trust_score(
    visual_grade: Dict,
    sensor_data: Optional[Dict] = None
) -> Dict:
    """
    Convenience function for trust score calculation.
    
    Usage:
        from ai_models.sensor_fusion_engine import calculate_trust_score
        
        visual_result = grade_produce(image_bytes, "tomato")
        sensor_data = {"moisture": 65, "npk": {"n": 120, "p": 60, "k": 80}}
        trust_result = calculate_trust_score(visual_result, sensor_data)
    """
    engine = get_sensor_fusion_engine()
    return engine.calculate_trust_score(visual_grade, sensor_data)


def fuse_all_data(
    image_bytes: bytes,
    crop_type: str,
    sensor_data: Optional[Dict] = None
) -> Dict:
    """
    Complete AI pipeline: Crop Detection → Disease Diagnosis → Quality Grading → Sensor Fusion
    
    Returns comprehensive analysis result.
    """
    from ai_models.crop_detector import detect_crop, get_valid_diseases_for_crop
    from ai_models.disease_detector import diagnose_disease
    from ai_models.quality_grader import grade_produce
    
    # Step 1: Detect crop (or use provided)
    if crop_type == "auto" or not crop_type:
        crop_result = detect_crop(image_bytes)
        crop_type = crop_result["crop"]
        valid_diseases = crop_result["valid_diseases"]
    else:
        valid_diseases = get_valid_diseases_for_crop(crop_type)
        crop_result = {"crop": crop_type, "confidence": 1.0}
    
    # Step 2: Diagnose disease
    disease_result = diagnose_disease(image_bytes, crop_type, valid_diseases)
    
    # Step 3: Grade quality
    quality_result = grade_produce(image_bytes, crop_type)
    
    # Step 4: Calculate trust score with sensor fusion
    trust_result = calculate_trust_score(quality_result, sensor_data)
    
    # Combine all results
    return {
        "crop_detection": crop_result,
        "disease_diagnosis": disease_result,
        "quality_grading": quality_result,
        "trust_score": trust_result,
        "summary": {
            "crop": crop_type,
            "grade": quality_result.get("grade"),
            "disease": disease_result.get("disease"),
            "severity": disease_result.get("severity_percent"),
            "trust_score": trust_result.get("trust_score"),
            "market_ready": trust_result.get("market_ready")
        }
    }
