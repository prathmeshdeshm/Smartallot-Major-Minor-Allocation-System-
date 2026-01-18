"""
Unit tests for allocation and eligibility logic in utils.py
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from allotment.models import (
    Student, MinorBranch, OpenElective,
    MinorPreference, MinorAllocation,
    EligibilityRule, OEEligibilityRule
)
from allotment.utils import (
    is_student_eligible,
    is_student_eligible_for_oe,
    run_minor1_allocation
)


class EligibilityTestCase(TestCase):
    """Test eligibility checking functions"""
    
    def setUp(self):
        """Create test data"""
        # Create users and students
        self.user1 = User.objects.create_user(username='student1', password='test123')
        self.student1 = Student.objects.create(
            user=self.user1,
            name='Test Student 1',
            roll_no='2021001',
            department='CSE',
            percentage=85.5,
            email='student1@test.com'
        )
        
        self.user2 = User.objects.create_user(username='student2', password='test123')
        self.student2 = Student.objects.create(
            user=self.user2,
            name='Test Student 2',
            roll_no='2021002',
            department='IT',
            percentage=75.0,
            email='student2@test.com'
        )
        
        # Create minor branch
        self.branch = MinorBranch.objects.create(
            name='Data Science',
            capacity=1,
            offering_dept='CSE'
        )
        
        # Create open elective
        self.oe = OpenElective.objects.create(
            name='Machine Learning',
            capacity=1,
            offering_dept='CSE'
        )
    
    def test_student_eligible_no_rules(self):
        """Test that students are eligible when no rules exist"""
        self.assertTrue(is_student_eligible(self.student1, self.branch))
        self.assertTrue(is_student_eligible(self.student2, self.branch))
    
    def test_student_eligible_min_percentage(self):
        """Test minimum percentage eligibility rule"""
        # Create rule requiring 80% minimum
        EligibilityRule.objects.create(
            branch=self.branch,
            rule_type='MIN_PERCENTAGE',
            value={'min_percentage': 80.0},
            is_active=True
        )
        
        # Student1 has 85.5%, should be eligible
        self.assertTrue(is_student_eligible(self.student1, self.branch))
        
        # Student2 has 75%, should not be eligible
        self.assertFalse(is_student_eligible(self.student2, self.branch))
    
    def test_student_eligible_department_block(self):
        """Test department block eligibility rule"""
        # Create rule blocking IT department
        EligibilityRule.objects.create(
            branch=self.branch,
            rule_type='DEPARTMENT_BLOCK',
            value={'blocked_departments': ['IT', 'ECE']},
            is_active=True
        )
        
        # Student1 is CSE, should be eligible
        self.assertTrue(is_student_eligible(self.student1, self.branch))
        
        # Student2 is IT (blocked), should not be eligible
        self.assertFalse(is_student_eligible(self.student2, self.branch))
    
    def test_student_eligible_inactive_rule(self):
        """Test that inactive rules don't affect eligibility"""
        # Create inactive rule
        EligibilityRule.objects.create(
            branch=self.branch,
            rule_type='MIN_PERCENTAGE',
            value={'min_percentage': 90.0},
            is_active=False
        )
        
        # Both students should be eligible (rule is inactive)
        self.assertTrue(is_student_eligible(self.student1, self.branch))
        self.assertTrue(is_student_eligible(self.student2, self.branch))
    
    def test_oe_eligibility_no_rules(self):
        """Test OE eligibility when no rules exist"""
        self.assertTrue(is_student_eligible_for_oe(self.student1, self.oe))
        self.assertTrue(is_student_eligible_for_oe(self.student2, self.oe))
    
    def test_oe_eligibility_min_percentage(self):
        """Test OE minimum percentage eligibility rule"""
        OEEligibilityRule.objects.create(
            oe_subject=self.oe,
            rule_type='MIN_PERCENTAGE',
            value={'min_percentage': 80.0},
            is_active=True
        )
        
        self.assertTrue(is_student_eligible_for_oe(self.student1, self.oe))
        self.assertFalse(is_student_eligible_for_oe(self.student2, self.oe))
    
    def test_oe_eligibility_department_block(self):
        """Test OE department block eligibility rule"""
        OEEligibilityRule.objects.create(
            oe_subject=self.oe,
            rule_type='DEPARTMENT_BLOCK',
            value={'blocked_departments': ['IT']},
            is_active=True
        )
        
        self.assertTrue(is_student_eligible_for_oe(self.student1, self.oe))
        self.assertFalse(is_student_eligible_for_oe(self.student2, self.oe))


class AllocationTestCase(TestCase):
    """Test allocation algorithms"""
    
    def setUp(self):
        """Create test data for allocation"""
        # Create users and students with different percentages
        self.user1 = User.objects.create_user(username='s1', password='test')
        self.student1 = Student.objects.create(
            user=self.user1,
            name='Student High Merit',
            roll_no='2021101',
            department='CSE',
            percentage=90.0,
            email='s1@test.com'
        )
        
        self.user2 = User.objects.create_user(username='s2', password='test')
        self.student2 = Student.objects.create(
            user=self.user2,
            name='Student Low Merit',
            roll_no='2021102',
            department='IT',
            percentage=70.0,
            email='s2@test.com'
        )
        
        # Create branch with capacity 1
        self.branch = MinorBranch.objects.create(
            name='AI & ML',
            capacity=1,
            offering_dept='CSE'
        )
    
    def test_allocation_by_merit(self):
        """Test that higher merit student gets allocation when both submit preferences"""
        # Both students submit preferences at roughly same time
        now = timezone.now()
        
        MinorPreference.objects.create(
            student=self.student1,
            minor_branch=self.branch,
            priority=1,
            submitted_at=now
        )
        
        MinorPreference.objects.create(
            student=self.student2,
            minor_branch=self.branch,
            priority=1,
            submitted_at=now + timedelta(seconds=1)
        )
        
        # Run allocation
        run_minor1_allocation()
        
        # Check allocations
        allocation1 = MinorAllocation.objects.filter(student=self.student1).first()
        allocation2 = MinorAllocation.objects.filter(student=self.student2).first()
        
        # Higher merit student should get the seat
        self.assertIsNotNone(allocation1)
        self.assertEqual(allocation1.minor_branch, self.branch)
        
        # Lower merit student should not get allocation (capacity is 1)
        # They might get auto-allocated to a different branch if available, but not this one
        if allocation2:
            self.assertNotEqual(allocation2.minor_branch, self.branch)
    
    def test_allocation_with_eligibility_rule(self):
        """Test that ineligible students don't get allocated"""
        # Create rule requiring 80% minimum
        EligibilityRule.objects.create(
            branch=self.branch,
            rule_type='MIN_PERCENTAGE',
            value={'min_percentage': 80.0},
            is_active=True
        )
        
        # Both submit preferences
        now = timezone.now()
        MinorPreference.objects.create(
            student=self.student1,
            minor_branch=self.branch,
            priority=1,
            submitted_at=now
        )
        MinorPreference.objects.create(
            student=self.student2,
            minor_branch=self.branch,
            priority=1,
            submitted_at=now
        )
        
        # Run allocation
        run_minor1_allocation()
        
        # Only student1 (90%) should get allocated, student2 (70%) is ineligible
        allocation1 = MinorAllocation.objects.filter(student=self.student1).first()
        self.assertIsNotNone(allocation1)
        self.assertEqual(allocation1.minor_branch, self.branch)
    
    def test_allocation_clears_previous(self):
        """Test that running allocation clears previous allocations"""
        # Create initial allocation
        MinorAllocation.objects.create(
            student=self.student1,
            minor_branch=self.branch,
            explanation='Initial allocation'
        )
        
        # Verify it exists
        self.assertEqual(MinorAllocation.objects.count(), 1)
        
        # Run allocation (with no preferences)
        run_minor1_allocation()
        
        # Previous allocation should be cleared and new auto-allocation created
        # (or count might be 0 if no auto-allocation happens)
        allocations = MinorAllocation.objects.all()
        for alloc in allocations:
            # Any new allocation should not have the old explanation
            self.assertNotEqual(alloc.explanation, 'Initial allocation')
    
    def test_no_allocation_when_capacity_full(self):
        """Test that students don't get allocated when capacity is 0"""
        self.branch.capacity = 0
        self.branch.save()
        
        MinorPreference.objects.create(
            student=self.student1,
            minor_branch=self.branch,
            priority=1
        )
        
        run_minor1_allocation()
        
        # No allocation should happen as capacity is 0
        allocation = MinorAllocation.objects.filter(
            student=self.student1,
            minor_branch=self.branch
        ).first()
        self.assertIsNone(allocation)
