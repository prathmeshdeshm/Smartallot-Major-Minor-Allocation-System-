from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Student(models.Model):
    """
    Represents a student in the system.
    Each student is linked to a Django User account.
    """
    DEPARTMENTS = [
        ('CSE', 'Computer Science and Engineering'),
        ('IT', 'Information Technology'),
        ('ECE', 'Electronics and Communication Engineering'),
        ('EEE', 'Electrical and Electronics Engineering'),
        ('MECH', 'Mechanical Engineering'),
        ('CIVIL', 'Civil Engineering'),
    ]
    
    ACADEMIC_STATUS_CHOICES = [
        ('REGULAR', 'Regular'),
        ('ARREAR', 'Arrear'),
        ('PROBATION', 'Probation'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    roll_no = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=50, choices=DEPARTMENTS)
    percentage = models.FloatField()
    email = models.EmailField()
    academic_status = models.CharField(
        max_length=30, 
        choices=ACADEMIC_STATUS_CHOICES, 
        default='REGULAR'
    )
    backlog_count = models.PositiveIntegerField(default=0)
    has_backlog = models.BooleanField(default=False)
    reassessment_applied = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.roll_no})"
    
    class Meta:
        ordering = ['-percentage', 'roll_no']


class MinorBranch(models.Model):
    """
    Represents a Minor program/branch that students can opt for.
    """
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    restricted_dept = models.CharField(max_length=50, blank=True, null=True)
    offering_dept = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Minor Branches"


class OpenElective(models.Model):
    """
    Represents an Open Elective subject.
    """
    name = models.CharField(max_length=100)
    capacity = models.IntegerField()
    offering_dept = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Open Electives"


class PreferenceWindow(models.Model):
    """
    Defines time windows when students can submit preferences.
    """
    name = models.CharField(max_length=100)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.start_at} to {self.end_at})"
    
    def is_open(self):
        now = timezone.now()
        return self.is_active and self.start_at <= now <= self.end_at


class EligibilityRule(models.Model):
    """
    Rules that determine student eligibility for a MinorBranch.
    Related name: 'rules' for reverse relation from MinorBranch.
    """
    RULE_TYPE_CHOICES = [
        ('MIN_PERCENTAGE', 'Minimum Percentage'),
        ('DEPARTMENT_BLOCK', 'Department Block'),
    ]
    
    branch = models.ForeignKey(
        MinorBranch, 
        on_delete=models.CASCADE,
        related_name='rules'  # MinorBranch.rules.all()
    )
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    value = models.JSONField()  # Stores rule-specific data
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.rule_type} for {self.branch.name}"


class OEEligibilityRule(models.Model):
    """
    Rules that determine student eligibility for an OpenElective.
    Related name: 'rules' for reverse relation from OpenElective.
    """
    RULE_TYPE_CHOICES = [
        ('MIN_PERCENTAGE', 'Minimum Percentage'),
        ('DEPARTMENT_BLOCK', 'Department Block'),
    ]
    
    oe_subject = models.ForeignKey(
        OpenElective,
        on_delete=models.CASCADE,
        related_name='rules'  # OpenElective.rules.all()
    )
    rule_type = models.CharField(max_length=20, choices=RULE_TYPE_CHOICES)
    value = models.JSONField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.rule_type} for {self.oe_subject.name}"


# ==================== PREFERENCES ====================

class MinorPreference(models.Model):
    """
    Student's preference for Minor 1.
    Related name: 'minor_preferences' for reverse relation from Student.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='minor_preferences'  # Student.minor_preferences.all()
    )
    minor_branch = models.ForeignKey(MinorBranch, on_delete=models.CASCADE)
    priority = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.minor_branch.name} (Priority {self.priority})"
    
    class Meta:
        ordering = ['student', 'priority']
        unique_together = ['student', 'minor_branch']


class DoubleMinorPreference(models.Model):
    """
    Student's preference for Minor 2 (double minor).
    Related name: 'double_minor_preferences' for reverse relation from Student.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='double_minor_preferences'  # Student.double_minor_preferences.all()
    )
    minor_branch = models.ForeignKey(MinorBranch, on_delete=models.CASCADE)
    priority = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.minor_branch.name} (Priority {self.priority})"
    
    class Meta:
        ordering = ['student', 'priority']
        unique_together = ['student', 'minor_branch']


class OEPreference(models.Model):
    """
    Student's preference for Open Electives.
    Related name: 'oe_preferences' for reverse relation from Student.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='oe_preferences'  # Student.oe_preferences.all()
    )
    oe_subject = models.ForeignKey(OpenElective, on_delete=models.CASCADE)
    priority = models.IntegerField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.student.name} - {self.oe_subject.name} (Priority {self.priority})"
    
    class Meta:
        ordering = ['student', 'priority']
        unique_together = ['student', 'oe_subject']


# ==================== ALLOCATIONS ====================

class MinorAllocation(models.Model):
    """
    Final allocation of Minor 1 to a student.
    Related name: 'minorallocation' (default lowercase model name) for reverse relation from Student.
    Note: Django's default related_name for MinorAllocation is 'minorallocation_set',
    but when checking if allocated, we use minorallocation__isnull (lowercase).
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
        # No explicit related_name, so Django uses default: 'minorallocation_set'
        # But in queries, we reference it as 'minorallocation' (lowercase model name without _set)
    )
    minor_branch = models.ForeignKey(MinorBranch, on_delete=models.CASCADE)
    explanation = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.name} -> {self.minor_branch.name}"
    
    class Meta:
        unique_together = ['student']  # One student can only have one Minor 1 allocation


class DoubleMinorAllocation(models.Model):
    """
    Final allocation of Minor 2 (double minor) to a student.
    Related name: 'doubleminorallocation' (default lowercase model name) for reverse relation from Student.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
        # Default related_name: 'doubleminorallocation_set'
        # In queries: 'doubleminorallocation' (lowercase)
    )
    minor_branch = models.ForeignKey(MinorBranch, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student.name} -> {self.minor_branch.name} (Minor 2)"
    
    class Meta:
        unique_together = ['student']


class OEAllocation(models.Model):
    """
    Final allocation of Open Elective to a student.
    Related name: 'oeallocation' (default lowercase model name) for reverse relation from Student.
    """
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE
        # Default related_name: 'oeallocation_set'
        # In queries: 'oeallocation' (lowercase)
    )
    oe_subject = models.ForeignKey(OpenElective, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.student.name} -> {self.oe_subject.name}"
    
    class Meta:
        unique_together = ['student']
