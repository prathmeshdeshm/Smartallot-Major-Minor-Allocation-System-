from django.db import models
from django.conf import settings
from .models import (
    Student, MinorBranch, OpenElective,
    MinorPreference, DoubleMinorPreference, OEPreference,
    MinorAllocation, DoubleMinorAllocation, OEAllocation , OEEligibilityRule
)
from django.db.models import Min, Count

# ============================================================================
# Related Names Reference for Query Construction
# ============================================================================
# This module uses Django's reverse relation lookups extensively.
# The following related_name values are defined in models.py:
#
# Student foreign keys in preference models:
#   - MinorPreference.student → Student.minor_preferences
#   - DoubleMinorPreference.student → Student.double_minor_preferences
#   - OEPreference.student → Student.oe_preferences
#
# Student foreign keys in allocation models (using Django defaults):
#   - MinorAllocation.student → Student.minorallocation_set (accessed as 'minorallocation' in filters)
#   - DoubleMinorAllocation.student → Student.doubleminorallocation_set (accessed as 'doubleminorallocation')
#   - OEAllocation.student → Student.oeallocation_set (accessed as 'oeallocation')
#
# Branch/OE foreign keys in rule models:
#   - EligibilityRule.branch → MinorBranch.rules
#   - OEEligibilityRule.oe_subject → OpenElective.rules
# ============================================================================





def is_student_eligible(student, branch: MinorBranch) -> bool:
    """
    Check if a student is eligible for a given MinorBranch based on
    all active EligibilityRule rows attached to that branch.
    Returns True if all rules pass, False if any rule fails.
    """
    rules = branch.rules.filter(is_active=True)

    for rule in rules:
        rtype = rule.rule_type
        data = rule.value or {}

        # 1) Minimum percentage rule
        if rtype == "MIN_PERCENTAGE":
            min_pct = data.get("min_percentage")
            if min_pct is not None:
                try:
                    min_pct = float(min_pct)
                except (TypeError, ValueError):
                    # bad config → fail safe OR skip; here we skip to not block allocation
                    continue

                if student.percentage < min_pct:
                    return False

        # 2) Blocked departments rule
        elif rtype == "DEPARTMENT_BLOCK":
            blocked_depts = data.get("blocked_departments", [])
            # normalize to upper-case strings
            blocked_depts = [str(d).upper().strip() for d in blocked_depts if str(d).strip()]
            if (student.department or "").upper() in blocked_depts:
                return False

       

    # If no rule failed → eligible
    return True


def is_student_eligible_for_oe(student, oe_subject: OpenElective) -> bool:
    """
    Check if a student is eligible for a given OpenElective based on
    active OEEligibilityRule rows attached to that OE.
    """
    rules = oe_subject.rules.filter(is_active=True)

    for rule in rules:
        rtype = rule.rule_type
        data = rule.value or {}

        if rtype == "MIN_PERCENTAGE":
            min_pct = data.get("min_percentage")
            if min_pct is not None:
                try:
                    min_pct = float(min_pct)
                except (TypeError, ValueError):
                    continue

                if student.percentage < min_pct:
                    return False

        elif rtype == "DEPARTMENT_BLOCK":
            blocked_depts = data.get("blocked_departments", [])
            blocked_depts = [str(d).upper().strip() for d in blocked_depts if str(d).strip()]
            if (student.department or "").upper() in blocked_depts:
                return False

        # Future OE-specific rules go here
        # elif rtype == "ONLY_NON_PARENT_DEPT":
        #     ...

    return True
def run_minor1_allocation():
    # Clear previous allocations
    MinorAllocation.objects.all().delete()

    # Students with preferences (sorted by merit + earliest submission)
    students_with_prefs = Student.objects.filter(
        minor_preferences__isnull=False
    ).annotate(
        submission_time=Min('minor_preferences__submitted_at')
    ).order_by('-percentage', 'submission_time')

    # Allocation for students WITH preferences
    for student in students_with_prefs:
        preferences = MinorPreference.objects.filter(
            student=student
        ).order_by('priority')

        for pref in preferences:
            branch = pref.minor_branch

            if not is_student_eligible(student, branch):
                continue

            allocated_count = MinorAllocation.objects.filter(
                minor_branch=branch
            ).count()

            if allocated_count < branch.capacity:
                explanation = (
                    f"Allocated Minor '{branch.name}' using preference #{pref.priority}. "
                    f"Student percentage: {student.percentage}. "
                    f"Eligible as per configured eligibility rules. "
                    f"Seats filled before allocation: {allocated_count} / {branch.capacity}."
                )

                MinorAllocation.objects.create(
                    student=student,
                    minor_branch=branch,
                    explanation=explanation
                )
                break

    # Auto-allocation for students WITHOUT preferences
    students_without_prefs = Student.objects.filter(
        minorallocation__isnull=True
    ).order_by('-percentage', 'user__date_joined')

    for student in students_without_prefs:
        for branch in MinorBranch.objects.all():
            if not is_student_eligible(student, branch):
                continue

            allocated_count = MinorAllocation.objects.filter(
                minor_branch=branch
            ).count()

            if allocated_count < branch.capacity:
                explanation = (
                    f"Auto-allocated Minor '{branch.name}'. "
                    f"Student percentage: {student.percentage}. "
                    f"No preferences submitted. "
                    f"Seats filled before allocation: {allocated_count} / {branch.capacity}."
                )

                MinorAllocation.objects.create(
                    student=student,
                    minor_branch=branch,
                    explanation=explanation
                )
                break

    return "Minor 1 allocation completed successfully"



def run_minor2_allocation():
    DoubleMinorAllocation.objects.all().delete()

    # Use correct related_name for reverse relations
    students_with_prefs = Student.objects.filter(double_minor_preferences__isnull=False).annotate(
        submission_time=Min('double_minor_preferences__submitted_at')
    ).order_by('-percentage', 'submission_time')

    for student in students_with_prefs:
        # Get the student's Minor 1 allocation to exclude it from Minor 2
        minor1_allocation = MinorAllocation.objects.filter(student=student).first()
        minor1_branch_id = minor1_allocation.minor_branch_id if minor1_allocation else None
        
        preferences = DoubleMinorPreference.objects.filter(student=student).order_by('priority')
        for pref in preferences:
            branch = pref.minor_branch
            # Check if student is eligible and hasn't already been allocated this branch for Minor 1
            if is_student_eligible(student, branch) and branch.id != minor1_branch_id:
                allocated_count = DoubleMinorAllocation.objects.filter(minor_branch=branch).count()
                if allocated_count < branch.capacity:
                    DoubleMinorAllocation.objects.create(student=student, minor_branch=branch)
                    break
    
    # Auto-allocation phase for students without preferences
    students_without_prefs = Student.objects.filter(doubleminorallocation__isnull=True).order_by('-percentage', 'user__date_joined')
    for student in students_without_prefs:
        # Get the student's Minor 1 allocation to exclude it from Minor 2
        minor1_allocation = MinorAllocation.objects.filter(student=student).first()
        minor1_branch_id = minor1_allocation.minor_branch_id if minor1_allocation else None
        
        available_branches = MinorBranch.objects.all()
        for branch in available_branches:
            # Check if student is eligible and hasn't already been allocated this branch for Minor 1
            if is_student_eligible(student, branch) and branch.id != minor1_branch_id:
                allocated_count = DoubleMinorAllocation.objects.filter(minor_branch=branch).count()
                if allocated_count < branch.capacity:
                    DoubleMinorAllocation.objects.create(student=student, minor_branch=branch)
                    break
    
    return "Minor 2 allocation completed. Unassigned students were auto-allocated where possible."


def run_oe_allocation():
    OEAllocation.objects.all().delete()
    
    # Students who submitted OE preferences
    students_with_prefs = Student.objects.filter(
        oe_preferences__isnull=False
    ).annotate(
        submission_time=Min('oe_preferences__submitted_at')
    ).order_by('-percentage', 'submission_time')

    for student in students_with_prefs:
        preferences = OEPreference.objects.filter(student=student).order_by('priority')
        for pref in preferences:
            oe_subject = pref.oe_subject

            # ✅ Apply all OE eligibility logic here
            if not is_student_eligible_for_oe(student, oe_subject):
                continue

            allocated_count = OEAllocation.objects.filter(oe_subject=oe_subject).count()
            if allocated_count < oe_subject.capacity:
                OEAllocation.objects.create(student=student, oe_subject=oe_subject)
                break
                
    # Auto-allocation phase for students without OE preferences
    students_without_prefs = Student.objects.filter(
        oeallocation__isnull=True
    ).order_by('-percentage', 'user__date_joined')

    for student in students_without_prefs:
        available_oes = OpenElective.objects.all()
        for oe_subject in available_oes:
            if not is_student_eligible_for_oe(student, oe_subject):
                continue

            allocated_count = OEAllocation.objects.filter(oe_subject=oe_subject).count()
            if allocated_count < oe_subject.capacity:
                OEAllocation.objects.create(student=student, oe_subject=oe_subject)
                break
    
    return "Open Elective allocation completed with eligibility rules based on major and minors."
