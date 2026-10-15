# RBWH services, cleaned from the "Service Mapping" sheet of the RBWH Service Map and Stakeholder Register (V.02, Sept 2025).
# Archived / out-of-scope rows dropped, duplicates merged, spelling fixed, Allied Health split by profession.
# Only service names live here (no staff names). Change a row here, then re-run fwbuild.py.
SCC = "Surgical & Critical Care"
WCMH = "Women's, Cancer & Mental Health"
IME = "Internal Medicine & Emergency"

# service line -> BAU stream. Anything not listed = Other.
LINE_STREAM = {
    "Surgical & Perioperative Services": SCC,
    "Critical Care & Clinical Support Services": SCC,
    "Internal Medicine & Emergency Services": IME,
    "Cancer Care Services": WCMH,
    "Mental Health": WCMH,
    "Women's & Newborn Services": WCMH,
}

_S = {
    "Aboriginal & Torres Strait Islander Health": [
        "Aboriginal & Torres Strait Islander Health"],
    "Administration Services": [
        "Administration Services", "Admissions Office", "Central Messenger Services", "Switchboard", "Trust Office",
        "Ward Administration", "Patient Experience & Volunteers"],
    "Allied Health": [
        "Physiotherapy", "Occupational Therapy", "Speech Pathology", "Social Work", "Social Work - Sexual Assault Service",
        "Social Work - Child Protection Liaison", "Nutrition & Dietetics", "Psychology & Neuropsychology", "Podiatry",
        "Audiology", "Orthotics & Prosthetics", "Pulmonary Rehabilitation", "Indigenous Hospital Liaison Service",
        "Allied Health Workforce (Metro North)", "Allied Health - Other"],
    "Cancer Care Services": [
        "Ambulatory Cancer Care (ODTU)", "Blood Management & Transfusion", "Breast Screen Northside", "CAR-T Cell Therapy",
        "Haematology / BMT", "Medical Oncology", "Metro North Cancer Care - TPCH", "North Lakes / Bribie Cancer Care",
        "Queensland Haemophilia Centre", "Radiation Oncology", "Research / Cancer Clinical Trials", "Ward 6AS Oncology",
        "You Can Centre"],
    "Critical Care & Clinical Support Services": [
        "Intensive Care Unit (ICU)", "Tracheostomy Service", "Donate Life", "Central Specialised Outpatient Services",
        "Confirmation Centre", "Genetic Health Queensland", "Hyperbaric Medicine", "Tess Cramond Pain & Research Centre",
        "Medical Imaging", "Herston Imaging Research Facility", "Nuclear Medicine & PET", "Pharmacy",
        "Skin Integrity Service", "Brisbane City Watchhouse"],
    "Finance": [
        "Health Information Services (Medical Records)"],
    "Internal Medicine & Emergency Services": [
        "Emergency & Trauma Centre", "Cardiology", "Clinical Immunology & Allergy", "Clinical Pharmacology", "Dermatology",
        "Endocrinology & Diabetes", "Gastroenterology & Hepatology", "Gender Services", "Infectious Diseases",
        "Internal Medicine & Aged Care", "Kidney Health", "Neurology", "Palliative & Supportive Care", "Rheumatology",
        "Sexual Health & HIV Service", "Thoracic Medicine & Sleep", "Vascular Access Surveillance & Education (VASE)"],
    "Medical Services": [
        "CMORE (Medical Education)", "Chaplaincy"],
    "Mental Health": [
        "Psychiatric Emergency Centre", "Consultation Liaison Psychiatry (CLPS)", "MH Inpatient Ward - G Floor",
        "MH Inpatient Ward - I Floor", "MH Adolescent Inpatient Ward - F Floor", "MH Inpatient Ward (Vulnerable People, Eating Disorders, Older)",
        "Mental Health HITH", "Hospital Alcohol & Drug Service (HADS)", "Queensland Eating Disorder Service (QuEDS)",
        "ECT", "Community Care Unit / Somerset Villas", "Complex Care Coordinator", "Dual Diagnosis Coordinator",
        "Multicultural Mental Health Coordinator", "Advanced A&TSI Mental Health Worker", "Mental Health Nurse Navigators",
        "Mental Health Allied Health"],
    "Nursing & Midwifery": [
        "Clinical Equipment & Loans", "Community Interface Services", "Discharge Transit Centre",
        "Nursing & Midwifery After Hours", "Patient Transport Unit", "Relief Pool"],
    "Other": [
        "Pathology", "Metro North Stroke", "Seniors Legal & Support Service", "Spiritual Support & Multi Faith"],
    "RBWH Operations": [
        "Access & Patient Flow", "Safety & Quality", "Infection Management & Prevention"],
    "Surgical & Perioperative Services": [
        "Acute Pain Management Service", "Anaesthetics", "Pre-Anaesthetic Clinic", "Operating Theatres (Level 4 / Level 5)",
        "PACU", "Minor Procedure Unit", "SDCU & 23 Hour Unit", "Day of Surgery Admission (DOSA)", "Perioperative Bookings & Admin",
        "ORMIS", "Clinical Consumables Group", "Perioperative Asset Management", "Sterile Processing Centre", "Burns",
        "Skin Bank", "Breast Health", "ENT / Head & Neck Surgery", "General Surgery", "Stomal Therapy", "Pre-Admission Clinic",
        "Neurosurgery", "Ophthalmology & Eye Casualty", "Oral & Maxillofacial Surgery", "Orthopaedics",
        "Plastics & Reconstructive Surgery", "Trauma Service", "Urology", "Vascular Surgery"],
    "Women's & Newborn Services": [
        "Birth Suite", "Birth Centre, Ngarrama & MGP", "Maternity Ward 6BN", "Maternity Outpatients", "Antenatal Classes",
        "Community Midwifery (Home Visiting)", "Diabetes in Pregnancy", "Lactation Service", "Perinatal Mental Health",
        "Pregnancy Assessment Service (PAS)", "Obstetric Review Centre (ORC)", "Obstetric Medicine (Complex Care)",
        "Maternal Fetal Medicine (EPAU)", "Centre for Advanced Prenatal Care (CAPC)", "Gynaecology",
        "Gynaecology Outpatients", "Gynaecological Oncology", "Ward 6AN Gynaecology", "Queensland Trophoblastic Centre",
        "Intensive Care Nursery", "Special Care Nursery", "Grantley Stable Neonatal Unit", "Neonatology", "Milk Bank",
        "Neonatal Retrieval Service", "Healthy Hearing", "Deadly Ears"],
}
SERVICES = [(line, s) for line, items in _S.items() for s in items]
