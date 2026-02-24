from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional
from app.modules.vision.scanner import PlotScanner
from app.modules.compliance.rule_engine import RuleEngine
from app.modules.estimation.calculator import CostEstimator

router = APIRouter()
scanner = PlotScanner()
rules = RuleEngine()
estimator = CostEstimator()


@router.post("/analyze")
async def analyze_plot(
    city: str = Form(...),
    file: UploadFile = File(...),
    manual_width: Optional[float] = Form(None),
    manual_length: Optional[float] = Form(None),
    manual_fsi: Optional[float] = Form(None),
    manual_floors: Optional[int] = Form(None),
):
    image_bytes = await file.read()
    scan_result = scanner.process_image(image_bytes)

    if manual_width is not None and manual_length is not None:
        scan_result["width_ft"] = manual_width
        scan_result["length_ft"] = manual_length
        scan_result["area_sqft"] = round(manual_width * manual_length, 2)
        scan_result["confidence"] = 1.0
        scan_result["status"] = "Manual Override"

    area = scan_result["area_sqft"]
    legal_result = rules.check_feasibility(city, area, manual_fsi)
    cost_result = estimator.calculate(area, city, manual_floors)

    return {
        "vision": scan_result,
        "legal": legal_result,
        "finance": cost_result,
    }
