"""
Rapido-Style Dispatch & Fallback State Machine with Dual OTP Lifecycle.
"""
from typing import List, Dict, Any, Optional
from geopy.distance import geodesic
import datetime
from seed_data import WORKERS, DEBARRED_CUSTOMERS, WORKER_REJECTIONS_LOG
from pricing import calculate_transparent_fare

# In-memory storage for prototype bookings and rejection tracking
BOOKINGS_DB: Dict[int, Dict[str, Any]] = {
    1088: {
        "booking_id": 1088,
        "customer_name": "Aarav Mehta",
        "customer_phone": "+91 98765 43210",
        "service_type": "driver",
        "sub_service": "Emergency & Outstation Highway Driver",
        "booking_date": "2026-10-20",
        "booking_time": "02:00 PM - 05:00 PM",
        "status": "COMPLETED",
        "start_otp": "3819",
        "end_otp": "9021",
        "start_otp_verified": True,
        "end_otp_verified": True,
        "assigned_worker": {
            "id": 104,
            "name": "Vikram Singh",
            "phone": "+91 98911 34567",
            "skill": "driver",
            "coop_name": "Delhi Transport Guild Cooperative",
            "rating": 4.9,
            "photo": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=120"
        },
        "pricing": {
            "cooperative_wage_payout": 580.0,
            "total_payable": 629.3,
            "statutory_tax": 29.0
        },
        "proof_of_work": {
            "image_url": "https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=600",
            "work_notes": "Executive transit completed safely from Connaught Place to Airport T3. Keys handed over.",
            "odometer_reading": "24,842 km",
            "timestamp": "2026-10-20T17:14:00Z",
            "verified": True
        },
        "telemetry": {
            "distance_km": 18.4,
            "avg_speed_kmh": 44.0,
            "route": "Connaught Place -> Dhaula Kuan -> NH-48 -> IGI T3"
        },
        "timeline": [
            "Job initialized for DRIVER",
            "Dispatched to Vikram Singh",
            "Customer verified START_OTP",
            "Proof of work attached & verified",
            "Dual-OTP verified and payout released"
        ]
    },
    1072: {
        "booking_id": 1072,
        "customer_name": "Aarav Mehta",
        "customer_phone": "+91 98765 43210",
        "service_type": "electrician",
        "sub_service": "Modular MCB & DB Dressing",
        "booking_date": "2026-10-18",
        "booking_time": "10:00 AM - 12:30 PM",
        "status": "COMPLETED",
        "start_otp": "8812",
        "end_otp": "4509",
        "start_otp_verified": True,
        "end_otp_verified": True,
        "assigned_worker": {
            "id": 101,
            "name": "Rajesh Kumar",
            "phone": "+91 98765 43210",
            "skill": "electrician",
            "coop_name": "Delhi Central Labour Cooperative",
            "rating": 4.9,
            "photo": "https://images.unsplash.com/photo-1540569014015-19a7be504e3a?w=120"
        },
        "pricing": {
            "cooperative_wage_payout": 420.0,
            "total_payable": 455.7
        },
        "proof_of_work": {
            "image_url": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?w=600",
            "work_notes": "Replaced tripping MCB with 32A breaker, full load tested.",
            "odometer_reading": None,
            "timestamp": "2026-10-18T12:28:00Z",
            "verified": True
        },
        "timeline": [
            "Job initialized for ELECTRICIAN",
            "Dispatched to Rajesh Kumar",
            "START_OTP verified",
            "Photo proof validated and completed"
        ]
    }
}
BOOKING_REJECTIONS: Dict[int, List[int]] = {} # booking_id -> list of worker_ids who rejected
BOOKING_COUNTER = 1100

def find_nearest_workers(
    customer_coords: tuple[float, float],
    service_type: str,
    exclude_worker_ids: Optional[List[int]] = None,
    max_radius_km: float = 25.0
) -> List[Dict[str, Any]]:
    """
    Finds and ranks all available workers matching service_type within max_radius_km,
    excluding workers who have already declined or are under disciplinary suspension/fired.
    """
    exclude = set(exclude_worker_ids or [])
    matches = []

    for w in WORKERS:
        if w["id"] in exclude or not w["is_available"]:
            continue
        if w.get("disciplinary_status") in ["FIRED", "SUSPENDED"]:
            continue
        if not w.get("is_verified", True):
            continue
        if w["skill"].lower() != service_type.lower():
            continue

        worker_coords = (w["lat"], w["lng"])
        dist_km = round(geodesic(customer_coords, worker_coords).km, 2)
        
        if dist_km <= max_radius_km:
            match_data = dict(w)
            match_data["distance_km"] = dist_km
            matches.append(match_data)

    # Sort by closest distance first, then highest rating
    matches.sort(key=lambda x: (x["distance_km"], -x["rating"]))
    return matches

def create_booking(
    customer_name: str,
    customer_coords: tuple[float, float],
    service_type: str,
    plan: str,
    is_emergency: bool = False,
    is_ngo: bool = False,
    booking_date: Optional[str] = None,
    booking_time: Optional[str] = None
) -> Dict[str, Any]:
    """
    Initializes a new booking, checks customer debarment status, finds the primary nearest worker,
    calculates transparent fare, and broadcasts the job alert.
    """
    # 1. Check Customer Debarment Status
    clean_cust = (customer_name or "").strip()
    clean_svc = (service_type or "").strip().lower()
    for deb_name, deb_info in DEBARRED_CUSTOMERS.items():
        if deb_info.get("status") == "DEBARRED" and deb_name.lower() == clean_cust.lower():
            debarred_services = [s.lower() for s in deb_info.get("services", ["all"])]
            if "all" in debarred_services or clean_svc in debarred_services:
                rep_workers = ", ".join(deb_info.get("reporting_worker_names", ["Certified Technicians"]))
                svc_desc = "all cooperative services" if "all" in debarred_services else f"'{service_type}' service"
                return {
                    "success": False,
                    "status": "CUSTOMER_DEBARRED",
                    "debarred_services": deb_info.get("services", ["ALL"]),
                    "message": (
                        f"Citizen '{customer_name}' is DEBARRED from booking {svc_desc} by the Ministry of Cooperation. "
                        f"Reason: {deb_info.get('reason', 'Multiple escalated incident complaints')} ({rep_workers})."
                    )
                }

    global BOOKING_COUNTER
    BOOKING_COUNTER += 1
    booking_id = BOOKING_COUNTER

    # Find candidates
    candidates = find_nearest_workers(customer_coords, service_type)
    if not candidates:
        return {
            "success": False,
            "message": f"No available cooperative workers found for {service_type} within 25km radius."
        }

    primary_worker = candidates[0]
    worker_coords = (primary_worker["lat"], primary_worker["lng"])

    # Calculate itemized pricing
    pricing = calculate_transparent_fare(
        service_type=service_type,
        plan=plan,
        customer_coords=customer_coords,
        worker_coords=worker_coords,
        is_emergency=is_emergency,
        is_ngo=is_ngo
    )

    schedule_desc = f"{booking_date} at {booking_time}" if (booking_date and booking_time) else (booking_time or "Immediate Dispatch")

    booking_record = {
        "booking_id": booking_id,
        "customer_name": customer_name,
        "customer_lat": customer_coords[0],
        "customer_lng": customer_coords[1],
        "service_type": service_type,
        "plan": plan,
        "is_emergency": is_emergency,
        "is_ngo": is_ngo,
        "booking_date": booking_date or "Today",
        "booking_time": booking_time or "Immediate (<30 mins)",
        "status": "BROADCASTING", # BROADCASTING -> ACCEPTED -> IN_PROGRESS -> COMPLETED / CANCELLED
        "assigned_worker": primary_worker,
        "pricing": pricing,
        "start_otp": pricing["start_otp"],
        "end_otp": pricing["end_otp"],
        "start_otp_verified": False,
        "end_otp_verified": False,
        "proof_of_work_url": None,
        "timeline": [
            f"Job request initialized for {service_type.capitalize()} ({plan.capitalize()} Plan) • Slot: {schedule_desc}",
            f"Broadcast dispatched to nearest cooperative worker: {primary_worker['name']} ({primary_worker['distance_km']} km away)"
        ]
    }

    BOOKINGS_DB[booking_id] = booking_record
    BOOKING_REJECTIONS[booking_id] = []

    return {"success": True, "booking": booking_record}

def worker_respond_to_job(booking_id: int, worker_id: int, accept: bool) -> Dict[str, Any]:
    """
    Handles worker accept or reject (Rapido-style fallback engine).
    If a worker rejects (either initially or after accepting), it tracks the rejection count,
    logs the event for the Ministry of Cooperation, and triggers immediate fallback to the next candidate.
    """
    booking = BOOKINGS_DB.get(booking_id)
    if not booking:
        return {"success": False, "message": "Booking not found"}

    if accept:
        booking["status"] = "ACCEPTED"
        assigned = booking.get("assigned_worker")
        w_name = assigned["name"] if assigned else "Technician"
        booking["timeline"].append(f"Worker {w_name} accepted the job. En route to customer.")
        return {
            "success": True,
            "status": "ACCEPTED",
            "message": f"Job accepted by {w_name}.",
            "booking": booking,
            "worker": assigned,
            "start_otp": booking.get("start_otp"),
            "end_otp": booking.get("end_otp")
        }
    else:
        # Worker rejected -> Track rejection for Ministry disciplinary audit
        declined_worker = booking.get("assigned_worker") or {"id": worker_id, "name": "Cooperative Technician"}
        for w in WORKERS:
            if w["id"] == worker_id or w["id"] == declined_worker.get("id"):
                w["rejection_count"] = w.get("rejection_count", 0) + 1
                curr_count = w["rejection_count"]
                
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                rejection_entry = {
                    "id": len(WORKER_REJECTIONS_LOG) + 801,
                    "worker_id": w["id"],
                    "worker_name": w["name"],
                    "booking_id": booking_id,
                    "service_type": booking.get("service_type", "general"),
                    "timestamp": now_str,
                    "reason": "Declined automated cooperative dispatch",
                    "total_worker_rejections": curr_count,
                    "severity": "CRITICAL" if curr_count >= 3 else ("WARNING" if curr_count == 2 else "NORMAL")
                }
                WORKER_REJECTIONS_LOG.append(rejection_entry)

                if curr_count >= 3:
                    w["disciplinary_status"] = "UNDER_REVIEW"
                    w.setdefault("disciplinary_history", []).append({
                        "action": "FLAGGED_FOR_MINISTRY_REVIEW",
                        "reason": f"Accumulated {curr_count} rejections. Ministry termination/show-cause protocol activated.",
                        "timestamp": now_str
                    })
                    booking["timeline"].append(
                        f"⚠️ Worker {w['name']} reached {curr_count} dispatches declined. Worker flagged to Ministry Cockpit for disciplinary review."
                    )
                break

        # Activate Fallback Reassignment Engine
        BOOKING_REJECTIONS.setdefault(booking_id, []).append(worker_id)
        booking["timeline"].append(f"Worker {booking['assigned_worker']['name']} declined/cancelled the job.")
        
        customer_coords = (booking["customer_lat"], booking["customer_lng"])
        remaining_candidates = find_nearest_workers(
            customer_coords=customer_coords,
            service_type=booking["service_type"],
            exclude_worker_ids=BOOKING_REJECTIONS[booking_id]
        )


        if remaining_candidates:
            fallback_worker = remaining_candidates[0]
            booking["assigned_worker"] = fallback_worker
            booking["status"] = "BROADCASTING"
            
            # Recalculate distance & transit for the new worker
            worker_coords = (fallback_worker["lat"], fallback_worker["lng"])
            updated_pricing = calculate_transparent_fare(
                service_type=booking["service_type"],
                plan=booking["plan"],
                customer_coords=customer_coords,
                worker_coords=worker_coords,
                is_emergency=booking["is_emergency"],
                is_ngo=booking["is_ngo"]
            )
            # Retain original OTPs
            updated_pricing["start_otp"] = booking["start_otp"]
            updated_pricing["end_otp"] = booking["end_otp"]
            booking["pricing"] = updated_pricing
            
            booking["timeline"].append(
                f"🚨 FALLBACK TRIGGERED: Reassigned to next nearest worker {fallback_worker['name']} ({fallback_worker['distance_km']} km away)"
            )
            return {
                "success": True,
                "status": "FALLBACK_REASSIGNED",
                "message": f"Reassigned to next closest worker: {fallback_worker['name']}",
                "booking": booking
            }
        else:
            booking["status"] = "NO_WORKERS_AVAILABLE"
            booking["timeline"].append("No other cooperative workers available within radius.")
            return {
                "success": False,
                "status": "NO_WORKERS_AVAILABLE",
                "message": "All nearby workers are currently busy.",
                "booking": booking
            }

def verify_start_otp(booking_id: int, entered_otp: str) -> Dict[str, Any]:
    """
    Worker enters START_OTP provided by the customer upon arrival.
    Unlocks work commencement.
    Ensures service request has been ACCEPTED by worker first.
    """
    booking = BOOKINGS_DB.get(booking_id)
    if not booking:
        return {"success": False, "message": "Booking not found"}

    # Enforce worker acceptance before allowing OTP fill/verification
    if booking.get("status") not in ["ACCEPTED", "IN_PROGRESS"]:
        return {
            "success": False,
            "message": "Cannot verify OTP: Service request must be ACCEPTED by worker first before OTP can be entered."
        }

    if booking["start_otp"] == entered_otp.strip():
        booking["start_otp_verified"] = True
        booking["status"] = "IN_PROGRESS"
        booking["timeline"].append("Customer verified START_OTP. Service execution in progress.")
        return {"success": True, "status": "IN_PROGRESS", "message": "START_OTP verified! Work commenced."}
    else:
        return {"success": False, "message": "Invalid START_OTP. Please ask customer to show their screen."}

def complete_job_with_proof(
    booking_id: int,
    entered_otp: str,
    proof_image: Optional[str] = None,
    work_notes: Optional[str] = None,
    odometer_reading: Optional[str] = None
) -> Dict[str, Any]:
    """
    Worker uploads completion proof-of-work and enters customer's END_OTP.
    Enforces mandatory Proof of Work before allowing service completion.
    Finalizes the service, logs direct payout, and registers in Ministry records.
    """
    booking = BOOKINGS_DB.get(booking_id)
    if not booking:
        return {"success": False, "message": "Booking not found"}

    # Mandatory Proof of Work validation
    if not proof_image or not proof_image.strip():
        return {
            "success": False,
            "message": "Mandatory Criteria Violation: Service cannot be completed without verified Proof of Work! Please attach completion photo."
        }

    if booking["end_otp"] == entered_otp.strip():
        booking["end_otp_verified"] = True
        booking["proof_of_work_url"] = proof_image
        booking["proof_of_work"] = {
            "image_url": proof_image,
            "work_notes": work_notes or "Cooperative standard quality service completed with photo verification.",
            "odometer_reading": odometer_reading,
            "timestamp": datetime.datetime.now().isoformat(),
            "verified": True
        }
        booking["status"] = "COMPLETED"
        payout = booking["pricing"].get("cooperative_wage_payout", 0.0)
        booking["timeline"].append("Job successfully completed. Proof of work uploaded and END_OTP validated.")
        booking["timeline"].append(f"₹{payout} disbursed directly to worker's cooperative account.")
        
        # Credit worker's cooperative account and completed jobs count
        assigned_worker = booking.get("assigned_worker")
        if assigned_worker:
            for w in WORKERS:
                if w["id"] == assigned_worker["id"]:
                    w["total_earned"] = round(w.get("total_earned", 0.0) + payout, 2)
                    w["completed_jobs"] = w.get("completed_jobs", 0) + 1
                    break
                    
        return {
            "success": True,
            "status": "COMPLETED",
            "message": "Service successfully completed! Direct wage disbursed with verified Proof of Work.",
            "booking": booking
        }
    else:
        return {"success": False, "message": "Invalid END_OTP. Please ask customer for completion OTP."}

def get_customer_service_history(customer_name: str) -> List[Dict[str, Any]]:
    """Retrieve full service history for a specific citizen."""
    results = []
    c_lower = customer_name.strip().lower()
    for b in BOOKINGS_DB.values():
        if b.get("customer_name", "").strip().lower() == c_lower:
            results.append(b)
    # Sort newest first
    results.sort(key=lambda x: x.get("booking_id", 0), reverse=True)
    return results

def get_worker_service_history(worker_id: int) -> List[Dict[str, Any]]:
    """Retrieve all jobs undertaken or completed by a specific cooperative worker."""
    results = []
    for b in BOOKINGS_DB.values():
        assigned = b.get("assigned_worker")
        if assigned and assigned.get("id") == worker_id:
            results.append(b)
    results.sort(key=lambda x: x.get("booking_id", 0), reverse=True)
    return results

